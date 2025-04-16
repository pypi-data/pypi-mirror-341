"""ModelIterator implementation for finding multiple distinct models.

This module provides tools for systematically finding multiple semantically
distinct models for a logical example. It works by adding constraints that
require each new model to differ from previously found models in at least
one component (sentence letter valuations, semantic function interpretations,
or model structure components).
"""

import z3
import itertools
import time
import traceback
import logging
import sys

from model_checker.builder.example import BuildExample
from model_checker.builder.progress import Spinner
from model_checker.builder.graph_utils import ModelGraph

# Configure logging
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[ITERATION] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Set to WARNING level to suppress debug messages
    logger.setLevel(logging.WARNING)

# Check if NetworkX is available for isomorphism checking
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    HAS_NETWORKX = False

class ModelIterator:
    """Handles systematic discovery of multiple distinct models for a logical example.
    
    This class manages the process of finding semantically distinct models by:
    1. Building on an initial model from a BuildExample instance
    2. Creating new model structures with extended constraints
    3. Iteratively solving for new models up to the specified limit
    
    Attributes:
        build_example: The BuildExample instance with the initial model
        max_iterations: Maximum number of models to find (from settings)
        found_models: List of Z3 models found so far
        model_structures: List of model structures found so far
        current_iteration: Current iteration count
        settings: Validated iteration settings
    """
    
    def __init__(self, build_example):
        """Initialize with a BuildExample that already has a valid model.
        
        Args:
            build_example: BuildExample instance with a valid model
            
        Raises:
            ValueError: If the build_example has no valid model
            TypeError: If build_example is not a BuildExample instance
        """
        # Type validation
        if not isinstance(build_example, BuildExample):
            raise TypeError(
                f"Expected BuildExample instance, got {type(build_example).__name__}"
            )
            
        # Model validation
        if not hasattr(build_example, 'model_structure') or build_example.model_structure is None:
            raise ValueError("BuildExample has no model_structure")
            
        if not hasattr(build_example.model_structure, 'z3_model_status') or \
           not build_example.model_structure.z3_model_status:
            raise ValueError("BuildExample does not have a valid model")
            
        if not hasattr(build_example.model_structure, 'z3_model') or \
           build_example.model_structure.z3_model is None:
            raise ValueError("BuildExample has no Z3 model")
            
        # Initialize properties
        self.build_example = build_example
        self.settings = self._get_iteration_settings()
        
        # Debug settings to file
        with open("/tmp/model_settings.log", "w") as f:
            f.write(f"Settings: {self.settings}\n")
            f.write(f"Original settings: {getattr(build_example, 'settings', {})}\n")
            
        self.max_iterations = self.settings.get('iterate', 1)
        self.current_iteration = 1  # First model is already found
        
        # Store the initial model and model structure
        self.found_models = [build_example.model_structure.z3_model]
        self.model_structures = [build_example.model_structure]
        
        # Create a persistent solver that will accumulate constraints
        self.solver = self._create_persistent_solver()
        
        # Initialize graph representation for the model
        self.model_graphs = []
        if HAS_NETWORKX:
            try:
                initial_graph = ModelGraph(
                    self.build_example.model_structure,
                    self.found_models[0]
                )
                self.model_graphs.append(initial_graph)
                # Store the graph with the model structure for reference
                self.build_example.model_structure.model_graph = initial_graph
            except Exception as e:
                print(f"Warning: Could not create graph for initial model: {str(e)}")
    
    def _create_persistent_solver(self):
        """Create a persistent solver with the initial model's constraints."""
        original_solver = self.build_example.model_structure.solver
        persistent_solver = z3.Solver()
        for assertion in original_solver.assertions():
            persistent_solver.add(assertion)
        return persistent_solver
        
    def _display_model_differences(self, model_structure, output=sys.stdout):
        """Display differences between the current model and previous ones.
        
        Delegates to theory-specific formatting when available.
        
        Args:
            model_structure: The model structure with differences
            output: Output stream to write to
        """
        if not hasattr(model_structure, 'model_differences') or not model_structure.model_differences:
            # If no model_differences are found but we have a previous_structure reference,
            # try to calculate differences on the fly
            if hasattr(model_structure, 'previous_structure') and model_structure.previous_structure is not None:
                model_structure.model_differences = self._calculate_differences(
                    model_structure, model_structure.previous_structure)
            else:
                return
            
        # Try theory-specific difference formatting
        if hasattr(model_structure, 'format_model_differences'):
            try:
                model_structure.format_model_differences(model_structure.model_differences, output)
                return
            except Exception as e:
                logger.warning(f"Error in theory-specific difference formatting: {e}")
        
        # Try legacy method for backward compatibility
        if hasattr(model_structure, 'print_model_differences'):
            try:
                model_structure.print_model_differences(output)
                return
            except Exception as e:
                logger.warning(f"Error in legacy difference formatting: {e}")
        
        # Fall back to generic difference display
        self._display_basic_differences(model_structure, output)
    
    def _display_basic_differences(self, model_structure, output=sys.stdout):
        """Fall back method to display model differences in a generic way."""
        differences = model_structure.model_differences
        if not differences:
            return
            
        print("\n=== MODEL DIFFERENCES ===\n", file=output)
        
        # Print sentence letter differences with more detail
        if 'sentence_letters' in differences and differences['sentence_letters']:
            print("Sentence Letter Changes:", file=output)
            for letter, change in differences['sentence_letters'].items():
                # Try to get a user-friendly letter name
                letter_name = letter
                if hasattr(model_structure, '_get_friendly_letter_name'):
                    try:
                        letter_name = model_structure._get_friendly_letter_name(str(letter))
                    except:
                        pass
                        
                # Print basic change
                if isinstance(change, dict) and 'old' in change and 'new' in change:
                    # Format for detailed difference info
                    old_val, new_val = None, None
                    
                    # Handle tuple format (verifiers, falsifiers)
                    if isinstance(change['old'], tuple) and isinstance(change['new'], tuple):
                        old_verifiers, old_falsifiers = change['old']
                        new_verifiers, new_falsifiers = change['new']
                        
                        print(f"  {letter_name}:", file=output)
                        print(f"    Verifiers: changed from {old_verifiers} to {new_verifiers}", file=output)
                        print(f"    Falsifiers: changed from {old_falsifiers} to {new_falsifiers}", file=output)
                    else:
                        # Handle simple value changes
                        print(f"  {letter_name}: {change['old']} -> {change['new']}", file=output)
                else:
                    # Fallback for simpler change format
                    print(f"  {letter_name}: changed from previous model", file=output)
        
        # Print world and state changes if available
        if 'worlds' in differences:
            print("\nWorld Changes:", file=output)
            worlds = differences['worlds']
            if 'added' in worlds and worlds['added']:
                from model_checker.utils import bitvec_to_substates
                for world in worlds['added']:
                    try:
                        state_repr = bitvec_to_substates(world, model_structure.semantics.N)
                        print(f"  + {state_repr} (world)", file=output)
                    except:
                        print(f"  + {world} (world)", file=output)
                        
            if 'removed' in worlds and worlds['removed']:
                from model_checker.utils import bitvec_to_substates
                for world in worlds['removed']:
                    try:
                        state_repr = bitvec_to_substates(world, model_structure.semantics.N)
                        print(f"  - {state_repr} (world)", file=output)
                    except:
                        print(f"  - {world} (world)", file=output)
        
        # Print possible state changes if available
        if 'possible_states' in differences:
            print("\nPossible State Changes:", file=output)
            states = differences['possible_states']
            if 'added' in states and states['added']:
                from model_checker.utils import bitvec_to_substates
                for state in states['added']:
                    try:
                        state_repr = bitvec_to_substates(state, model_structure.semantics.N)
                        print(f"  + {state_repr}", file=output)
                    except:
                        print(f"  + {state}", file=output)
                        
            if 'removed' in states and states['removed']:
                from model_checker.utils import bitvec_to_substates
                for state in states['removed']:
                    try:
                        state_repr = bitvec_to_substates(state, model_structure.semantics.N)
                        print(f"  - {state_repr}", file=output)
                    except:
                        print(f"  - {state}", file=output)
        
        # Print semantic function differences with more detail
        if 'semantic_functions' in differences and differences['semantic_functions']:
            print("\nSemantic Function Changes:", file=output)
            for func, changes in differences['semantic_functions'].items():
                if isinstance(changes, dict) and changes:
                    # Print function name
                    print(f"  {func}:", file=output)
                    # Show sample changes (limit to 5 to avoid overwhelming output)
                    sample_count = 0
                    for input_vals, change in changes.items():
                        if sample_count < 5:  # Limit to 5 examples
                            if isinstance(change, dict) and 'old' in change and 'new' in change:
                                print(f"    Input {input_vals}: {change['old']} -> {change['new']}", file=output)
                            else:
                                print(f"    Input {input_vals}: changed", file=output)
                            sample_count += 1
                    
                    # Show count if there are more changes
                    total_changes = len(changes)
                    if total_changes > 5:
                        print(f"    ... and {total_changes - 5} more changes", file=output)
                else:
                    # Fallback for simpler change format
                    print(f"  {func}: {len(changes) if isinstance(changes, dict) else 'unknown'} input(s) changed", file=output)
        
        # Print model structure differences
        if 'model_structure' in differences and differences['model_structure']:
            print("\nModel Structure Changes:", file=output)
            for component, change in differences['model_structure'].items():
                if isinstance(change, dict) and 'old' in change and 'new' in change:
                    print(f"  {component}: {change['old']} -> {change['new']}", file=output)
                else:
                    print(f"  {component}: changed", file=output)
                    
        # Print part-whole relationship changes if available
        if 'parthood' in differences and differences.get('parthood'):
            print("\nPart-Whole Relationship Changes:", file=output)
            for pair, change in differences['parthood'].items():
                if isinstance(change, dict) and 'old' in change and 'new' in change:
                    status = "now part of" if change['new'] else "no longer part of"
                    print(f"  {pair}: {status}", file=output)
    
    def iterate(self):
        """Find multiple distinct models up to max_iterations.
        
        Each new model will:
        1. Differ from ALL previous models through extended constraints
        2. Be non-isomorphic to all previous models
        3. Be a completely new model structure built from scratch
        4. Have its differences from the previous model tracked for presentation
        
        Returns:
            list: All found model structures (including the initial one)
        """
        # Proceed only if first model was successful
        if not self.build_example.model_structure.z3_model_status:
            raise RuntimeError("Cannot iterate when no initial model was found")
        
        # Set up timeout for the entire process
        max_time = self.settings.get('max_time', 1.0)
        iteration_timeout = max(max_time * 10, 30.0)
        start_time = time.time()
        
        # Track distinct models found (separate from iteration count)
        self.distinct_models_found = 1  # Starting with initial model
        
        # Track all models checked (including isomorphic ones)
        self.checked_model_count = 1
        
        # Track attempts to escape isomorphic models
        self.escape_attempts = 0
        escape_attempts = self.settings.get('escape_attempts', 3)
        
        # Start iteration from second model
        while self.current_iteration < self.max_iterations:
            try:
                # Check timeout
                current_time = time.time()
                if current_time - start_time > iteration_timeout:
                    print(f"Iteration process exceeded timeout of {iteration_timeout} seconds")
                    break
                
                # Create extended constraints requiring difference from all previous models
                try:
                    extended_constraints = self._create_extended_constraints()
                except RuntimeError as e:
                    print(f"Could not create extended constraints: {str(e)}")
                    break
                
                # Solve with extended constraints
                result = self.solver.check()
                if result != z3.sat:
                    print("No more models satisfy the extended constraints")
                    break
                
                # Get the new model
                new_model = self.solver.model()
                self.checked_model_count += 1
                
                # Build a completely new model structure with the extended constraints
                new_structure = self._build_new_model_structure(new_model)
                
                if not new_structure:
                    print("Could not create new model structure, stopping iteration")
                    break
                
                # Check for isomorphism if NetworkX is available
                is_isomorphic = False
                if HAS_NETWORKX:
                    is_isomorphic = self._check_isomorphism(new_structure, new_model)
                
                if is_isomorphic:
                    # Mark the structure as isomorphic for reference
                    new_structure._is_isomorphic = True
                    logger.debug(f"Found an isomorphic model (check #{self.checked_model_count})")
                    
                    # Track number of consecutive isomorphic models found
                    if not hasattr(self, '_isomorphic_attempts'):
                        self._isomorphic_attempts = 0
                    self._isomorphic_attempts += 1
                    
                    # If we've found too many isomorphic models in a row, apply stronger constraints
                    iteration_attempts = self.settings.get('iteration_attempts', 5)
                    if self._isomorphic_attempts >= iteration_attempts:
                        self.escape_attempts += 1
                        
                        # Initialize debug messages list if it doesn't exist
                        if not hasattr(self, 'debug_messages'):
                            self.debug_messages = []
                        
                        if self.escape_attempts >= escape_attempts:
                            self.debug_messages.append(f"Made {escape_attempts} attempts to escape isomorphic models without success. Stopping search.")
                            break
                            
                        # Store the message instead of printing it immediately
                        self.debug_messages.append(f"Skipping after {iteration_attempts} consecutive isomorphic models. Applying stronger constraints (attempt {self.escape_attempts}/{escape_attempts})...")
                        
                        # Create stronger constraints and continue
                        stronger_constraint = self._create_stronger_constraint(new_model)
                        if stronger_constraint is not None:
                            self.solver.add(stronger_constraint)
                            self._isomorphic_attempts = 0  # Reset counter
                            
                            # Add a timeout for this attempt - use a longer timeout for stronger constraints
                            attempt_timeout = min(max_time * 4, 10.0)  # Longer timeout for stronger constraints
                            self.debug_messages.append(f"  Attempting to satisfy stronger constraints (timeout: {attempt_timeout}s)")
                            attempt_start = time.time()
                            
                            # Set solver timeout
                            self.solver.set("timeout", int(attempt_timeout * 1000))
                            
                            # First check immediately
                            result = self.solver.check()
                            if result == z3.sat:
                                self.debug_messages.append("  Found satisfiable model with stronger constraints!")
                                # Continue with the loop to process this model
                                continue
                            
                            # If not immediately satisfiable, try a few more times with short intervals
                            retry_count = 0
                            max_retries = 3
                            while retry_count < max_retries and time.time() - attempt_start < attempt_timeout:
                                retry_count += 1
                                self.debug_messages.append(f"  Retry attempt {retry_count}/{max_retries}...")
                                
                                # Try with different solver seeds or tactics
                                self.solver.push()  # Save the current solver state
                                self.solver.add(z3.Int(f"retry_seed_{retry_count}") == retry_count)  # Add a dummy constraint to change the solver's behavior
                                result = self.solver.check()
                                if result == z3.sat:
                                    self.debug_messages.append("  Found satisfiable model on retry!")
                                    break
                                self.solver.pop()  # Restore the solver state
                                
                                # Brief pause between retries
                                time.sleep(0.1)
                            
                            # If we couldn't satisfy the constraint within timeout, stop
                            if self.solver.check() != z3.sat:
                                self.debug_messages.append("Failed to satisfy stronger constraints, stopping search")
                                break
                        else:
                            self.debug_messages.append("Could not create stronger constraints, stopping search")
                            break
                        continue
                    
                    # Add a non-isomorphism constraint and try again
                    iso_constraint = self._create_non_isomorphic_constraint(new_model)
                    if iso_constraint is not None:  # Check for None explicitly instead of using truth value
                        self.solver.add(iso_constraint)
                        continue  # Skip to next attempt without incrementing
                    else:
                        # Initialize debug messages list if it doesn't exist
                        if not hasattr(self, 'debug_messages'):
                            self.debug_messages = []
                        self.debug_messages.append("Could not create non-isomorphic constraint, stopping search")
                        break
                
                # This is a genuine new model
                new_structure._is_isomorphic = False
                self.distinct_models_found += 1
                
                # Reset counters on successful distinct model
                self._isomorphic_attempts = 0
                self.escape_attempts = 0
                
                # Calculate and store differences for the presentation layer to use
                differences = self._calculate_differences(new_structure, self.model_structures[-1])
                
                # We no longer display differences here - this will be handled by the presentation layer
                # self._display_model_differences(new_structure)
                
                # Add the new model and structure to our results
                self.found_models.append(new_model)
                self.model_structures.append(new_structure)
                self.current_iteration += 1
                
                # Add the new model to the solver constraints to ensure the next model is different
                self.solver.add(self._create_difference_constraint([new_model]))
                
            except Exception as e:
                # Initialize debug messages list if it doesn't exist
                if not hasattr(self, 'debug_messages'):
                    self.debug_messages = []
                self.debug_messages.append(f"Error during iteration: {str(e)}")
                
                # Print the traceback to stderr for debugging but don't show it to the user
                import sys
                print(traceback.format_exc(), file=sys.stderr)
                break
        
        # Return all model structures without printing summary here
        # Summary will be printed by the presentation layer (process_example)
        return self.model_structures
    
    def reset_iterator(self):
        """Reset the iterator to its initial state.
        
        Clears:
        - All found models except the initial one
        - Any added differentiation constraints
        - Iteration counters
        - Status flags
        
        Useful when wanting to start iteration process over with 
        different parameters.
        
        Returns:
            self: For method chaining
        """
        # Keep only the initial model
        if len(self.found_models) > 0:
            initial_model = self.found_models[0]
            self.found_models = [initial_model]
            
        # Keep only the initial model structure
        if len(self.model_structures) > 0:
            initial_structure = self.model_structures[0]
            self.model_structures = [initial_structure]
            
        # Reset all counters and flags
        self.current_iteration = 1
        self._isomorphic_attempts = 0
        self.distinct_models_found = 1
        self.checked_model_count = 1
        self.escape_attempts = 0
        
        # Reset solver to original constraints
        self.solver = self._create_persistent_solver()
        
        # Reset graph representations
        if HAS_NETWORKX:
            if len(self.model_structures) > 0:
                # Keep only the initial model graph
                try:
                    initial_structure = self.model_structures[0]
                    initial_model = self.found_models[0]
                    initial_graph = ModelGraph(initial_structure, initial_model)
                    self.model_graphs = [initial_graph]
                except Exception as e:
                    print(f"Warning: Failed to reset model graphs: {str(e)}")
                    self.model_graphs = []
            else:
                self.model_graphs = []
        
        return self
    
    def _create_extended_constraints(self):
        """Create extended constraints that require difference from all previous models.
        
        Returns:
            list: Z3 constraints requiring difference from all previous models
            
        Raises:
            RuntimeError: If constraint generation fails
        """
        # Get original constraints from the first model
        original_constraints = list(self.build_example.model_structure.solver.assertions())
        
        # Create difference constraints for all previous models
        difference_constraints = []
        for model in self.found_models:
            diff_constraint = self._create_difference_constraint([model])
            difference_constraints.append(diff_constraint)
        
        # Add structural constraints to help find different models
        if HAS_NETWORKX:
            for model in self.found_models:
                iso_constraint = self._create_non_isomorphic_constraint(model)
                if iso_constraint is not None:  # Check for None explicitly instead of using truth value
                    difference_constraints.append(iso_constraint)
        
        return original_constraints + difference_constraints
        
    def _build_new_model_structure(self, z3_model):
        """Build a completely new model structure from a Z3 model.
        
        Instead of updating an existing model structure, this creates a fresh
        model structure from scratch, proper initialization with the Z3 model.
        
        Args:
            z3_model: Z3 model to use for the new structure
            
        Returns:
            ModelStructure: A new model structure built from scratch
        """
        try:
            # Get original build example to extract settings and constraints
            original_build_example = self.build_example
            
            # Create a fresh ModelConstraints instance but without the Z3 model
            model_constraints = original_build_example.model_constraints
            
            # Create a new bare model structure 
            # DO NOT use the constructor that tries to evaluate Z3 values
            klass = original_build_example.model_structure.__class__
            new_structure = object.__new__(klass)
            
            # Initialize only the attributes needed before Z3 model evaluation
            self._initialize_base_attributes(new_structure, model_constraints, original_build_example.settings)
            
            # Now set the Z3 model after basic initialization
            new_structure.z3_model = z3_model
            new_structure.z3_model_status = True
            
            # Transfer runtime from original model structure
            new_structure.z3_model_runtime = original_build_example.model_structure.z3_model_runtime
            
            # Properly initialize Z3-dependent attributes
            self._initialize_z3_dependent_attributes(new_structure, z3_model)
            
            # Interpret sentences
            sentence_objects = new_structure.premises + new_structure.conclusions
            new_structure.interpret(sentence_objects)
            
            return new_structure
            
        except Exception as e:
            print(f"Error building new model structure: {str(e)}")
            print(traceback.format_exc())
            return None
            
    def _initialize_base_attributes(self, model_structure, model_constraints, settings):
        """Initialize basic attributes of a model structure that don't depend on the Z3 model.
        
        This initializes the core attributes needed before Z3 model evaluation,
        following a proper two-phase initialization pattern.
        
        Args:
            model_structure: The model structure to initialize
            model_constraints: The model constraints to use
            settings: The settings to use
        """
        # Define ANSI color codes (copied from ModelDefaults.__init__)
        model_structure.COLORS = {
            "default": "\033[37m",  # WHITE
            "world": "\033[34m",    # BLUE
            "possible": "\033[36m", # CYAN
            "impossible": "\033[35m", # MAGENTA
            "initial": "\033[33m",  # YELLOW
        }
        model_structure.RESET = "\033[0m"
        model_structure.WHITE = model_structure.COLORS["default"]
        
        # Copy attributes from ModelDefaults.__init__
        model_structure.model_constraints = model_constraints
        model_structure.settings = settings
        model_structure.max_time = settings.get("max_time", 1.0)
        model_structure.expectation = settings.get("expectation", True)
        
        # Set semantics and related attributes
        model_structure.semantics = model_constraints.semantics
        model_structure.main_point = model_structure.semantics.main_point
        model_structure.all_states = model_structure.semantics.all_states
        model_structure.N = model_structure.semantics.N
        
        # Set syntax and related attributes
        model_structure.syntax = model_constraints.syntax
        model_structure.start_time = model_structure.syntax.start_time
        model_structure.premises = model_structure.syntax.premises
        model_structure.conclusions = model_structure.syntax.conclusions
        model_structure.sentence_letters = model_structure.syntax.sentence_letters
        
        # Set proposition class and solver
        model_structure.proposition_class = model_constraints.proposition_class
        model_structure.solver = z3.Solver()
        for assertion in model_constraints.all_constraints:
            model_structure.solver.add(assertion)
        
        # Initialize Z3 model attributes as None
        model_structure.z3_model = None
        model_structure.z3_model_status = None
        model_structure.z3_model_runtime = None
        model_structure.timeout = None
        model_structure.unsat_core = None
        
        # Get main world from main_point
        if hasattr(model_structure.main_point, "get"):
            model_structure.main_world = model_structure.main_point.get("world")
        
        # Initialize Z3 values as None
        model_structure.z3_main_world = None
        model_structure.z3_possible_states = None 
        model_structure.z3_world_states = None
        
        # Initialize difference tracking
        model_structure.model_differences = None
        
    def _initialize_z3_dependent_attributes(self, model_structure, z3_model):
        """Initialize attributes that depend on the Z3 model.
        
        This is the second phase of initialization that evaluates Z3 model values.
        
        Args:
            model_structure: The model structure to initialize
            z3_model: The Z3 model to use
        """
        # Initialize main world evaluation
        model_structure.z3_main_world = z3_model.eval(model_structure.main_world, model_completion=True) 
        model_structure.main_point["world"] = model_structure.z3_main_world
        
        # Initialize possible states
        semantics = model_structure.semantics
        model_structure.z3_possible_states = [
            state for state in model_structure.all_states
            if bool(z3_model.eval(semantics.possible(state), model_completion=True))
        ]
        
        # Initialize world states 
        model_structure.z3_world_states = [
            state for state in model_structure.z3_possible_states
            if bool(z3_model.eval(semantics.is_world(state), model_completion=True))
        ]
        
        # Allow theory-specific initialization
        if hasattr(model_structure, 'initialize_from_z3_model'):
            model_structure.initialize_from_z3_model(z3_model)
    
    
    def _calculate_differences(self, new_structure, previous_structure):
        """Calculate differences between two model structures.
        
        Delegates to theory-specific difference detection when available,
        falling back to a generic implementation when not.
        
        Args:
            new_structure: The new model structure
            previous_structure: The previous model structure
            
        Returns:
            dict: Structured differences between the models
        """
        # Try theory-specific difference detection
        if hasattr(new_structure, 'detect_model_differences'):
            try:
                differences = new_structure.detect_model_differences(previous_structure)
                if differences:
                    # Store the differences with the new structure
                    new_structure.model_differences = differences
                    
                    # Store a reference to the previous structure for display purposes
                    new_structure.previous_structure = previous_structure
                    
                    return differences
            except Exception as e:
                logger.warning(f"Error in theory-specific difference detection: {e}")
        
        # Try legacy 'calculate_model_differences' method for backward compatibility
        if hasattr(new_structure, 'calculate_model_differences'):
            try:
                theory_differences = new_structure.calculate_model_differences(previous_structure)
                if theory_differences:
                    # Store the differences with the new structure
                    new_structure.model_differences = theory_differences
                    
                    # Store a reference to the previous structure for display purposes
                    new_structure.previous_structure = previous_structure
                    
                    return theory_differences
            except Exception as e:
                logger.warning(f"Error in legacy theory-specific difference detection: {e}")
        
        # Fall back to generic implementation
        differences = self._calculate_basic_differences(new_structure, previous_structure)
        
        # Store the differences with the new structure
        new_structure.model_differences = differences
        
        # Store a reference to the previous structure for display purposes
        new_structure.previous_structure = previous_structure
        
        return differences
        
    def _calculate_basic_differences(self, new_structure, previous_structure):
        """Fallback method to calculate basic differences when theory-specific detection is not available.
        
        This provides a minimal difference detection focused on sentence letters and Z3 functions,
        without any theory-specific semantic interpretation.
        
        Args:
            new_structure: The new model structure
            previous_structure: The previous model structure to compare against
            
        Returns:
            dict: Basic differences between the models
        """
        # Get Z3 models
        new_model = new_structure.z3_model
        previous_model = previous_structure.z3_model
        
        # Initialize basic differences structure
        differences = {
            "sentence_letters": {},
            "semantic_functions": {}
        }
        
        # Compare sentence letter valuations (common to all theories)
        for letter in self.build_example.model_constraints.sentence_letters:
            try:
                prev_value = previous_model.eval(letter, model_completion=True)
                new_value = new_model.eval(letter, model_completion=True)
                
                if str(prev_value) != str(new_value):
                    differences["sentence_letters"][str(letter)] = {
                        "old": prev_value,
                        "new": new_value
                    }
            except z3.Z3Exception:
                pass
        
        # Compare semantic function interpretations (common to all theories)
        semantics = new_structure.semantics
        for attr_name in dir(semantics):
            if attr_name.startswith('_'):
                continue
                
            attr = getattr(semantics, attr_name)
            if not isinstance(attr, z3.FuncDeclRef):
                continue
                
            arity = attr.arity()
            if arity == 0:
                continue
            
            # For unary and binary functions, check specific values
            if arity <= 2:
                n_worlds = getattr(new_structure, 'num_worlds', 5)  # Default to 5 if not available
                
                func_diffs = {}
                for inputs in self._generate_input_combinations(arity, n_worlds):
                    try:
                        args = [z3.IntVal(i) for i in inputs]
                        prev_value = previous_model.eval(attr(*args), model_completion=True)
                        new_value = new_model.eval(attr(*args), model_completion=True)
                        
                        if str(prev_value) != str(new_value):
                            func_diffs[str(inputs)] = {
                                "old": prev_value,
                                "new": new_value
                            }
                    except z3.Z3Exception:
                        pass
                
                if func_diffs:
                    differences["semantic_functions"][attr_name] = func_diffs
        
        return differences
        
    def _check_isomorphism(self, new_structure, new_model):
        """Check if a model is isomorphic to any previous model.
        
        Args:
            new_structure: The model structure to check
            new_model: The Z3 model to check
            
        Returns:
            bool: True if the model is isomorphic to any previous model
        """
        if not HAS_NETWORKX:
            return False
            
        try:
            # Create a graph representation of the new model
            new_graph = ModelGraph(new_structure, new_model)
            
            # Store the graph with the model structure
            new_structure.model_graph = new_graph
            
            # Check if this model is isomorphic to any previous model
            is_isomorphic = False
            
            # Calculate isomorphism with a timeout
            start_time = time.time()
            iteration_timeout = self.settings.get('iteration_timeout', 1.0)
            
            for prev_graph in self.model_graphs:
                # Check if timeout exceeded
                if time.time() - start_time > iteration_timeout:
                    print("Isomorphism check timed out, skipping further checks.")
                    break
                    
                # Check isomorphism
                if new_graph.is_isomorphic(prev_graph):
                    is_isomorphic = True
                    # Mark the structure as isomorphic
                    new_structure.isomorphic_to_previous = True
                    break
            
            # If not isomorphic, add the graph to our collection
            if not is_isomorphic:
                self.model_graphs.append(new_graph)
                
            return is_isomorphic
            
        except Exception as e:
            print(f"Warning: Isomorphism check failed: {str(e)}")
            return False
    
    def _create_difference_constraint(self, previous_models):
        """Create a Z3 constraint requiring difference from all previous models.
        
        Delegates to theory-specific constraint generation when available,
        falling back to a generic implementation when not.
        
        Args:
            previous_models: List of Z3 models to differ from
            
        Returns:
            z3.ExprRef: Z3 constraint expression
            
        Raises:
            RuntimeError: If constraint generation fails
        """
        logger.debug("\n==== DEBUG: _create_difference_constraint ====")
        logger.debug(f"Creating difference constraints from {len(previous_models)} previous models")
        
        # Get key structures from build_example
        model_structure = self.build_example.model_structure
        model_constraints = self.build_example.model_constraints
        semantics = model_constraints.semantics
        
        # For each previous model, create a constraint requiring at least one difference
        model_diff_constraints = []
        
        for model_idx, prev_model in enumerate(previous_models):
            logger.debug(f"\nProcessing previous model #{model_idx+1}:")
            
            # Try to use theory-specific difference constraints
            if hasattr(semantics, 'create_difference_constraints'):
                try:
                    theory_constraints = semantics.create_difference_constraints(prev_model)
                    if theory_constraints:
                        logger.debug(f"  Using theory-specific difference constraints")
                        model_diff_constraints.append(z3.Or(theory_constraints))
                        continue
                except Exception as e:
                    logger.debug(f"  Error in theory-specific constraints: {e}")
            
            # Fall back to generic implementation if theory-specific not available
            diff_components = []
            
            # 1. Use theory's differentiable functions if available
            if hasattr(semantics, 'get_differentiable_functions'):
                try:
                    diff_funcs = semantics.get_differentiable_functions()
                    print(f"  Using {len(diff_funcs)} theory-provided differentiable functions")
                    
                    for func, arity, description in diff_funcs:
                        print(f"    Function {description} (arity {arity}):")
                        
                        # For unary and binary functions, check specific values
                        if arity <= 2:
                            # Get the domain size (number of worlds)
                            n_worlds = getattr(model_structure, 'num_worlds', 5)  # Default to 5 if not available
                            print(f"      Domain size (num_worlds): {n_worlds}")
                            
                            # Skip if part-whole relation function since it requires bit vectors instead of integers
                            if description == "part-whole relation":
                                print("      Skipping part-whole relation - requires bit vectors instead of integers")
                                continue
                                
                            if func == semantics.is_part_of:
                                print("      Skipping is_part_of - requires bit vectors instead of integers")
                                continue
                            
                            # Create constraints for all relevant inputs
                            input_count = 0
                            for inputs in self._generate_input_combinations(arity, n_worlds):
                                try:
                                    # Check what this function returns in the previous model
                                    args = [z3.IntVal(i) for i in inputs]
                                    prev_value = prev_model.eval(func(*args), model_completion=True)
                                    
                                    # Add constraint requiring it to be different
                                    diff_components.append(func(*args) != prev_value)
                                    input_count += 1
                                    
                                    if input_count <= 3 or input_count % 10 == 0:  # Limit log output
                                        print(f"        Added constraint for input {inputs}: must differ from {prev_value}")
                                except z3.Z3Exception as e:
                                    if input_count <= 3:
                                        print(f"        Skipped input {inputs}: {str(e)}")
                            
                            print(f"      Added {input_count} input constraints for this function")
                except Exception as e:
                    print(f"  Error processing differentiable functions: {e}")
            
            # Create a single constraint for this model requiring at least one difference
            if diff_components:
                model_diff_constraints.append(z3.Or(diff_components))
                print(f"  Total differentiable components for model #{model_idx+1}: {len(diff_components)}")
            else:
                print(f"  WARNING: No differentiable components found for model #{model_idx+1}")
        
        # The new model must be different from ALL previous models
        if model_diff_constraints:
            combined_constraint = z3.And(model_diff_constraints)
            logger.debug(f"\nCreated combined constraint requiring difference from all {len(previous_models)} previous models")
            return combined_constraint
        else:
            logger.error("\nERROR: Could not create any difference constraints")
            raise RuntimeError("Could not create any difference constraints")
    
    def _create_non_isomorphic_constraint(self, z3_model):
        """Create a constraint that forces structural differences to avoid isomorphism.
        
        This uses a different approach from syntactic constraints by forcing
        structural differences like different numbers of edges or different
        distributions of truth values.
        
        Args:
            z3_model: The Z3 model to differ from
        
        Returns:
            z3.ExprRef: Z3 constraint expression or None if creation fails
        """
        logger.debug("\n==== DEBUG: _create_non_isomorphic_constraint ====")
        
        if not HAS_NETWORKX:
            logger.debug("NetworkX not available, skipping isomorphism check")
            print("NetworkX dependency not available; skipping isomorphism check.")
            return None
            
        logger.debug("NetworkX available, creating non-isomorphic constraints")
        
        # Get model structure and constraints
        model_structure = self.build_example.model_structure
        model_constraints = self.build_example.model_constraints
        semantics = model_constraints.semantics
        
        # Create graph for the model and analyze its structure
        try:
            # Get the world states from the model
            world_states = getattr(model_structure, 'z3_world_states', [])
            if not world_states and hasattr(model_structure, 'world_states'):
                world_states = getattr(model_structure, 'world_states', [])
                
            if not world_states:
                logger.debug("No world states found, cannot create non-isomorphic constraints")
                return None
                
            logger.debug(f"Found {len(world_states)} world states")
            
            # Create constraints to force structural differences
            constraints = []
            
            # 1. Force different accessibility relation pattern
            if hasattr(semantics, 'R') and len(world_states) > 0:
                logger.debug("Theory has accessibility relation R, checking existing pattern")
                # Count current accessibility relation pattern
                edge_pattern = {}
                edge_count = 0
                
                for i, w1 in enumerate(world_states):
                    for j, w2 in enumerate(world_states):
                        try:
                            relation_value = bool(z3_model.eval(semantics.R(w1, w2), model_completion=True))
                            edge_pattern[(i, j)] = relation_value
                            if relation_value:
                                edge_count += 1
                        except Exception as e:
                            print(f"  Error evaluating R({w1}, {w2}): {str(e)}")
                
                print(f"  Current model has {edge_count} accessibility edges")
                
                # Create constraints to force different edge patterns
                edge_flip_constraints = []
                for i, w1 in enumerate(world_states):
                    for j, w2 in enumerate(world_states):
                        current_value = edge_pattern.get((i, j), False)
                        # Force this specific edge to be different
                        if current_value:
                            edge_flip_constraints.append(z3.Not(semantics.R(w1, w2)))
                            if i < 3 and j < 3:  # Limit debug output
                                print(f"  Added constraint: R({w1}, {w2}) must be False (currently True)")
                        else:
                            edge_flip_constraints.append(semantics.R(w1, w2))
                            if i < 3 and j < 3:  # Limit debug output
                                print(f"  Added constraint: R({w1}, {w2}) must be True (currently False)")
                
                # Add edge flip constraints
                constraints.extend(edge_flip_constraints)
                print(f"  Added {len(edge_flip_constraints)} accessibility relation constraints")
            
            # 2. Force different truth value patterns at each world
            for i, world in enumerate(world_states):
                world_constraints = []
                for letter in model_constraints.sentence_letters:
                    try:
                        if hasattr(semantics, 'true_at'):
                            # Use semantic evaluation
                            from model_checker.syntactic import Sentence
                            letter_sentence = Sentence(sentence_letter=letter)
                            current_value = bool(z3_model.eval(semantics.true_at(letter_sentence, world), model_completion=True))
                            
                            if current_value:
                                world_constraints.append(z3.Not(semantics.true_at(letter_sentence, world)))
                            else:
                                world_constraints.append(semantics.true_at(letter_sentence, world))
                        else:
                            # Direct evaluation
                            if hasattr(letter, '__call__'):
                                current_value = bool(z3_model.eval(letter(i), model_completion=True))
                                
                                if current_value:
                                    world_constraints.append(z3.Not(letter(i)))
                                else:
                                    world_constraints.append(letter(i))
                            else:
                                current_value = bool(z3_model.eval(letter, model_completion=True))
                                
                                if current_value:
                                    world_constraints.append(z3.Not(letter))
                                else:
                                    world_constraints.append(letter)
                    except Exception:
                        pass
                
                # Add individual letter flip constraints
                constraints.extend(world_constraints)
            
            # 3. Theory-specific structural constraints if available
            if hasattr(model_structure, 'get_structural_constraints'):
                try:
                    theory_constraints = model_structure.get_structural_constraints(z3_model)
                    if theory_constraints:
                        logger.debug(f"  Adding {len(theory_constraints)} theory-specific structural constraints")
                        for i, constraint in enumerate(theory_constraints):
                            constraints.append(constraint)
                            if i < 3:  # Log only a few constraints for debug
                                logger.debug(f"    - Added theory constraint {i+1}")
                except Exception as e:
                    logger.debug(f"  Error getting theory-specific structural constraints: {str(e)}")
            
            # Add the constraints to force a different structure
            if constraints:
                # We need at least one of these constraints to be true to ensure a different structure
                combined_constraint = z3.Or(constraints)
                return combined_constraint
                
        except Exception as e:
            # Initialize debug messages list if it doesn't exist
            if not hasattr(self, 'debug_messages'):
                self.debug_messages = []
            self.debug_messages.append(f"Warning: Failed to create non-isomorphic constraints: {str(e)}")
            
        return None
        
    def _create_stronger_constraint(self, isomorphic_model):
        """Create stronger constraints after multiple isomorphism failures.
        
        This method creates more significant structural difference requirements
        than the regular constraints, to help escape from isomorphic models after
        several consecutive failures. The constraints become progressively stronger
        based on the number of escape attempts.
        
        Args:
            isomorphic_model: The Z3 model that was isomorphic
        
        Returns:
            z3.ExprRef: Z3 constraint expression or None if creation fails
        """
        # Get model structure and constraints
        model_structure = self.build_example.model_structure
        model_constraints = self.build_example.model_constraints
        semantics = model_constraints.semantics

        # Create stronger structural constraints
        constraints = []
        
        # Get current escape attempt number (used to calibrate constraint strength)
        escape_attempt = getattr(self, 'escape_attempts', 1)
        
        try:
            # Get the world states from the model
            world_states = getattr(model_structure, 'z3_world_states', [])
            if not world_states and hasattr(model_structure, 'world_states'):
                world_states = getattr(model_structure, 'world_states', [])
                
            if not world_states:
                logger.debug("No world states found, cannot create non-isomorphic constraints")
                return None
                
            logger.debug(f"Found {len(world_states)} world states")
                
            # 1. Force different number of worlds if possible
            # This constraint becomes more extreme with each escape attempt
            current_world_count = len(world_states)
            max_worlds = len(model_structure.all_states)
            
            # Create a function to count worlds
            def count_worlds():
                count_expr = z3.IntVal(0)
                for state in model_structure.all_states:
                    # Add 1 if this state is a world
                    count_expr = z3.If(semantics.is_world(state), count_expr + 1, count_expr)
                return count_expr
            
            # Scale the difference based on escape attempt
            world_diff = 1 + escape_attempt
            
            # Force either more or fewer worlds with increasing difference
            if current_world_count > world_diff:
                # We can force fewer worlds
                constraints.append(count_worlds() <= current_world_count - world_diff)
            
            # We can also try to force more worlds
            if current_world_count + world_diff <= max_worlds:
                constraints.append(count_worlds() >= current_world_count + world_diff)
                
            # On higher escape attempts, try extreme values
            if escape_attempt >= 2:
                # Try minimum possible worlds
                constraints.append(count_worlds() == 1)
                
                # Try maximum possible worlds
                constraints.append(count_worlds() == max_worlds)
            
            # 2. Force different truth assignment patterns
            # The approach varies based on escape attempt number
            for letter in model_constraints.sentence_letters:
                try:
                    # Create a constraint that flips values for this letter
                    letter_flip_constraints = []
                    for i, world in enumerate(world_states):
                        if hasattr(semantics, 'true_at'):
                            from model_checker.syntactic import Sentence
                            letter_sentence = Sentence(sentence_letter=letter)
                            current_value = bool(isomorphic_model.eval(semantics.true_at(letter_sentence, world), model_completion=True))
                            
                            if current_value:
                                letter_flip_constraints.append(z3.Not(semantics.true_at(letter_sentence, world)))
                            else:
                                letter_flip_constraints.append(semantics.true_at(letter_sentence, world))
                    
                    if letter_flip_constraints:
                        if escape_attempt == 1:
                            # First attempt: flip ALL values for this letter (AND constraint)
                            constraints.append(z3.And(letter_flip_constraints))
                        elif escape_attempt >= 2:
                            # Later attempts: try more extreme patterns
                            # Force ALL letters true at ALL worlds
                            all_true_constraints = []
                            for world in world_states:
                                all_true_constraints.append(semantics.true_at(Sentence(sentence_letter=letter), world))
                            constraints.append(z3.And(all_true_constraints))
                            
                            # Force ALL letters false at ALL worlds
                            all_false_constraints = []
                            for world in world_states:
                                all_false_constraints.append(z3.Not(semantics.true_at(Sentence(sentence_letter=letter), world)))
                            constraints.append(z3.And(all_false_constraints))
                except Exception as e:
                    # Just log and continue - we want to try other constraints
                    if hasattr(logger, 'debug'):
                        logger.debug(f"Error creating letter constraints: {str(e)}")
            
            # 3. Force different accessibility relation structure
            if hasattr(semantics, 'R') and len(world_states) > 0:
                # Get current relation pattern
                edge_pattern = {}
                edge_flip_constraints = []
                
                for i, w1 in enumerate(world_states):
                    for j, w2 in enumerate(world_states):
                        try:
                            relation_value = bool(isomorphic_model.eval(semantics.R(w1, w2), model_completion=True))
                            edge_pattern[(i, j)] = relation_value
                            
                            # Create flip constraint
                            if relation_value:
                                edge_flip_constraints.append(z3.Not(semantics.R(w1, w2)))
                            else:
                                edge_flip_constraints.append(semantics.R(w1, w2))
                        except Exception:
                            pass
                
                if edge_flip_constraints:
                    flip_count = sum(1 for _ in edge_flip_constraints)
                    if flip_count > 0:
                        if escape_attempt == 1:
                            # First attempt: flip half the edges
                            min_different = max(1, flip_count // 2)
                            constraints.append(z3.AtLeast(*edge_flip_constraints, min_different))
                        elif escape_attempt >= 2:
                            # Later attempts: try more extreme patterns
                            # Flip ALL edges (invert the graph)
                            constraints.append(z3.And(edge_flip_constraints))
                            
                            # Try to create a fully connected graph
                            fully_connected = []
                            for w1 in world_states:
                                for w2 in world_states:
                                    fully_connected.append(semantics.R(w1, w2))
                            constraints.append(z3.And(fully_connected))
                            
                            # Try to create a minimal graph (only reflexive edges)
                            minimal_graph = []
                            for w in world_states:
                                for w1 in world_states:
                                    for w2 in world_states:
                                        if w1 == w2:  # Only keep reflexive edges
                                            minimal_graph.append(semantics.R(w1, w2))
                                        else:
                                            minimal_graph.append(z3.Not(semantics.R(w1, w2)))
                            constraints.append(z3.And(minimal_graph))
            
            # 4. Theory-specific stronger constraints if available
            if hasattr(model_structure, 'get_stronger_constraints'):
                try:
                    theory_constraints = model_structure.get_stronger_constraints(isomorphic_model, escape_attempt)
                    if theory_constraints:
                        # Initialize debug messages list if it doesn't exist
                        if not hasattr(self, 'debug_messages'):
                            self.debug_messages = []
                        self.debug_messages.append(f"  Adding {len(theory_constraints)} theory-specific stronger constraints")
                        for i, constraint in enumerate(theory_constraints):
                            constraints.append(constraint)
                            if i < 3:  # Log only a few constraints for debug
                                self.debug_messages.append(f"    - Added theory constraint {i+1}")
                except Exception as e:
                    # Initialize debug messages list if it doesn't exist
                    if not hasattr(self, 'debug_messages'):
                        self.debug_messages = []
                    self.debug_messages.append(f"  Error getting theory-specific stronger constraints: {str(e)}")
                    if hasattr(logger, 'debug'):
                        logger.debug(f"Error getting theory constraints: {str(e)}")
            
            # Add something truly random on desperate attempts
            if escape_attempt >= 3 and hasattr(semantics, 'main_point') and hasattr(semantics.main_point, 'get'):
                try:
                    # Force a different main world
                    current_main = semantics.main_point.get('world')
                    # Try each world as the main world
                    for w in world_states:
                        if w != current_main:
                            constraints.append(semantics.main_point.get('world') == w)
                except Exception:
                    pass
            
            # Combine constraints: more escape attempts = stronger constraints
            if constraints:
                if escape_attempt == 1:
                    # First attempt: any of these constraints might work (OR)
                    return z3.Or(constraints)
                elif escape_attempt == 2:
                    # Second attempt: group constraints by type and require one from each group
                    # This creates a stronger combined constraint
                    grouped_constraints = []
                    
                    # Split the constraints into chunks and require one from each chunk
                    chunk_size = max(1, len(constraints) // 3)
                    for i in range(0, len(constraints), chunk_size):
                        chunk = constraints[i:i+chunk_size]
                        if chunk:
                            grouped_constraints.append(z3.Or(chunk))
                    
                    # Require all grouped constraints
                    if grouped_constraints:
                        return z3.And(grouped_constraints)
                    else:
                        return z3.Or(constraints)  # Fallback
                else:
                    # Desperate attempts: try each constraint individually
                    # Return the first 3 constraints to avoid overwhelming the solver
                    return constraints[0] if constraints else None
                
        except Exception as e:
            # Initialize debug messages list if it doesn't exist
            if not hasattr(self, 'debug_messages'):
                self.debug_messages = []
            self.debug_messages.append(f"Warning: Failed to create stronger constraints: {str(e)}")
            
            # Print the traceback to stderr for debugging but don't show it to the user
            import sys
            import traceback
            print(traceback.format_exc(), file=sys.stderr)
            
        return None
    
    def _get_iteration_settings(self):
        """Extract and validate iteration settings from BuildExample.
        
        Settings:
        - iterate: Maximum number of models to find (int > 0)
        - iterate_timeout: Maximum time to spend on all iterations (optional)
        - iteration_attempts: Maximum consecutive isomorphic models before applying stronger constraints
        - escape_attempts: Maximum attempts to escape from isomorphic models before giving up
        
        Returns:
            dict: Validated iteration settings
            
        Raises:
            ValueError: If settings are invalid
        """
        # Get settings from the build example
        settings = getattr(self.build_example, 'settings', {})
        if not settings:
            # If no settings found, use defaults
            return {
                'iterate': 1,
                'iteration_attempts': 5,
                'escape_attempts': 3
            }
            
        # Validate iterate
        iterate = settings.get('iterate', 1)
        if not isinstance(iterate, int):
            try:
                iterate = int(iterate)
            except (ValueError, TypeError):
                raise ValueError(
                    f"The 'iterate' setting must be an integer, got {type(iterate).__name__}"
                )
                
        if iterate < 1:
            raise ValueError(f"The 'iterate' setting must be positive, got {iterate}")
            
        # Copy settings to avoid modifying the original
        validated_settings = settings.copy()
        validated_settings['iterate'] = iterate
        
        # Note: The difference type setting has been simplified as the current implementation
        # uses a consistent approach for all difference types
        validated_settings['difference_type'] = 'semantic'  # Always use the default approach
        
        # Add and validate iteration_attempts (default to 5)
        # First check for old max_attempts name for backward compatibility
        iteration_attempts = settings.get('iteration_attempts', settings.get('max_attempts', 5))
        if not isinstance(iteration_attempts, int) or iteration_attempts <= 0:
            iteration_attempts = 5
        validated_settings['iteration_attempts'] = iteration_attempts
        
        # Add and validate escape_attempts (default to 3)
        escape_attempts = settings.get('escape_attempts', 3)
        if not isinstance(escape_attempts, int) or escape_attempts <= 0:
            escape_attempts = 3
        validated_settings['escape_attempts'] = escape_attempts
        
        # Add iteration timeout setting (default to 1.0 seconds)
        # First check for old isomorphism_timeout name for backward compatibility
        iteration_timeout = settings.get('iteration_timeout', settings.get('isomorphism_timeout', 1.0))
        if not isinstance(iteration_timeout, (int, float)) or iteration_timeout <= 0:
            iteration_timeout = 1.0
        validated_settings['iteration_timeout'] = iteration_timeout
        
        # Validate iterate_timeout if present (overall timeout)
        if 'iterate_timeout' in settings:
            timeout = settings['iterate_timeout']
            if not isinstance(timeout, (int, float)) or timeout <= 0:
                raise ValueError(
                    f"The 'iterate_timeout' setting must be a positive number, got {timeout}"
                )
                
        return validated_settings
    
    def _generate_input_combinations(self, arity, domain_size):
        """Generate all relevant input combinations for a function of given arity.
        
        Args:
            arity: Number of arguments the function takes
            domain_size: Size of the domain (typically number of worlds)
            
        Returns:
            list: All relevant input combinations
        """
        # For n-ary functions, generate all combinations of inputs
        # from the domain, which is typically the world indices
        domain = range(domain_size)
        return itertools.product(domain, repeat=arity)


# Module-level convenience functions

def iterate_example(build_example, max_iterations=None):
    """Convenience function to iterate an example and find multiple models.
    
    Args:
        build_example: BuildExample instance with a solved model
        max_iterations: Override for maximum iterations (optional)
        
    Returns:
        list: All found model structures
        
    Raises:
        ValueError: If iteration is not possible with this example
    """
    iterator = ModelIterator(build_example)
    
    # Override max_iterations if provided
    if max_iterations is not None:
        if not isinstance(max_iterations, int) or max_iterations < 1:
            raise ValueError(f"max_iterations must be a positive integer, got {max_iterations}")
        iterator.max_iterations = max_iterations
        
    return iterator.iterate()
