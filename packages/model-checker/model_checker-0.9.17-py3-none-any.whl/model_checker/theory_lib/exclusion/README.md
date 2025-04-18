# Model-Checker Instructions

This document provides an overview of the package contents for the _exclusion semantics_ defended by [Bernard and Champollion](https://ling.auf.net/lingbuzz/007730/current.html).
Further documentation can be found in the `docstrings` and comments.

## Modules

The _exclusion semantics_ includes the following modules:

- `README.md` to document usage and changes.
- `__init__.py` to expose definitions to be imported elsewhere.
- `examples.py` defines a number of examples to test.
- `semantic.py` defines the default semantics for the operators included.
- `operators.py` defines the primitive and derived operators.

These  will be discussed below, beginning with `examples.py` in the following section.

## Usage

The following subsections will describe each of the elements involved in basic usage.

## Testing

Run `pytest` from the project directory to quickly evaluate whether the examples included in `examples.py` return the expected result.

### Examples

#### Accessing Examples

You can access examples from this theory using the parent module's functions:

```python
from model_checker.theory_lib import get_examples, get_test_examples, get_semantic_theories

# Get all examples from the exclusion theory
examples = get_examples('exclusion')

# Access a specific example
example = examples['EX_CM_1']
premises, conclusions, settings = example

# Get test examples for automated testing
test_examples = get_test_examples('exclusion')

# Get semantic theory implementations
theories = get_semantic_theories('exclusion')
```

#### Running Examples

Run `model-checker examples.py` from within the project directory to test the examples included the `example_range` defined in `examples.py`.
Here are two such examples:

    # DOUBLE NEGATION ELIMINATION IDENTITY
    EX_CM_1_settings = {
        'N' : 3,
        'possible' : False,
        'contingent' : False,
        'non_empty' : False,
        'non_null' : False,
        'disjoint' : False,
        'fusion_closure' : False,
        'max_time' : 1,
    }
    EX_CM_1_example = [
        [], # premises
        ['(A \\uniequiv \\exclude \\exclude A)'], # conclusions
        EX_CM_1_settings,
    ]

    # DISJUNCTIVE SYLLOGISM
    EX_TH_1_settings = {
        'N' : 3,
        'possible' : False,
        'contingent' : False,
        'non_empty' : False,
        'non_null' : False,
        'disjoint' : False,
        'fusion_closure' : False,
        'max_time' : 1,
    }
    EX_TH_1_example = [
        ['(A \\univee B)', '\\exclude B'], # premises
        ['A'], # conclusions
        EX_TH_1_settings
    ]

Each example defines the settings followed be a list of premises (treated conjunctively) and list of conclusions (treated disjunctively).
These examples may then be included in the following:

    example_range = {
        # Countermodels
        "EX_CM_1" : EX_CM_1_example,
        # Theorems
        # "EX_TH_1" : EX_TH_1_example,
    }

Whereas `EX_CM_1` will be considered, `EX_TH_1` is excluded from consideration on account of including the hash mark '#' at the beginning of the line.
By removing the hash mark from `EX_TH_1`, both examples will be tested in turn.

### Settings

The exclusion semantics defines its own specific set of settings relevant to its semantic theory. There are two types of settings:

#### General Settings

General settings control the output and behavior of the model checker:

```python
DEFAULT_GENERAL_SETTINGS = {
    "print_constraints": False,  # Print constraints when no model is found
    "print_impossible": False,   # Print impossible states
    "print_z3": False,           # Print raw Z3 model
    "save_output": False,        # Prompt to save output
    "maximize": False,           # Use for theory comparison
    # Note: align_vertically is not included as it's only relevant for bimodal theory
}
```

#### Example Settings

Example settings control the behavior of specific examples:

```python
DEFAULT_EXAMPLE_SETTINGS = {
    # Core settings used by all theories
    'N': 3,                   # Number of atomic states
    'max_time': 1,            # Maximum solver time
    
    # Exclusion-specific settings
    'possible': False,        # Whether states must be possible
    'contingent': False,      # Whether propositions must be contingent
    'disjoint': False,        # Whether propositions must have disjoint subject matters
    'non_empty': False,       # Whether propositions must have non-empty verifier/falsifier sets
    'non_null': False,        # Whether null states can be verifiers/falsifiers
    'fusion_closure': False,  # Whether to enforce fusion closure
    
    # Note: 'M' is not included as it's only relevant for temporal theories like bimodal
}
```

If settings are omitted from an example (e.g., no value of `N` is provided), the defaults above will be assumed, with the system issuing a notification to the user.

#### Theory-Specific Settings

The exclusion theory defines several settings not found in other theories:

1. **possible**: Controls whether states must be possible
2. **fusion_closure**: Controls whether fusion closure is enforced
3. **non_empty**: Controls whether propositions must have non-empty verifier/falsifier sets
4. **non_null**: Controls whether null states can be verifiers/falsifiers

Similarly, the exclusion theory excludes settings that don't apply to it, like:
- **M**: Only relevant for theories with a temporal dimension (bimodal)
- **align_vertically**: Only relevant for theories with time-based visualization (bimodal)

If you use command-line flags for settings not defined in the exclusion theory (like `-a` for align_vertically), you'll see a warning that the flag doesn't correspond to a known setting, but the system will continue to run normally.

For a comprehensive overview of the settings management system and how theory-specific settings are handled, please refer to the [Settings Documentation](../../settings/README.md).

### Semantic Theories

The semantic theories over which the examples included in `example_range` are composed of a `semantics`, definition of a `proposition`, and collection of `operators` included in the examples under consideration.
In particular, the `exclusion_theory` is defined as follows:

    exclusion_operators = syntactic.OperatorCollection(
        UniAndOperator, UniOrOperator, ExclusionOperator, # extensional
        UniIdentityOperator, # constitutive
    )

    exclusion_theory = {
        "semantics": ExclusionSemantics,
        "proposition": UnilateralProposition,
        "operators": exclusion_operators,
    }

The `ExclusionSemantics` and `UnilateralProposition` are imported from the `semantic.py` module and the operators included in `exclusion_operators` are imported from `exclusion_operators`.
These modules will be discussed in the [Basic Architecture](#basic-architecture) section below.

Given the `exclusion_theory` defined above, we may evaluate examples over this semantic theory as follows:

    semantic_theories = {
        "ChampollionBernard" : exclusion_theory,
    }

Multiple semantic theories may be provided for systematic comparison.
For instance, we may import elements of the default theory provided by the model-checker:

    default_operators = syntactic.OperatorCollection(
        NegationOperator, AndOperator, OrOperator, # extensional
        IdentityOperator, # constitutive
    )

    default_theory = {
        "semantics": Semantics,
        "proposition": Proposition,
        "operators": default_operators,
        "dictionary": default_dictionary,
    }

    default_dictionary = {
        "\\exclude" : "\\neg",
        "\\uniwedge" : "\\wedge",
        "\\univee" : "\\vee",
        "\\uniequiv" : "\\equiv",
    }

    semantic_theories = {
        "Champollion" : exclusion_theory,
        "Brast-McKie" : default_theory,
    }

The `exclusion_theory` did not include a `dictionary` since the examples to be tested are articulated in terms of the `exclusion_operators` (e.g., `\\exclude`, `\\uniwedge`, etc.).
By contrast, the `default_theory` must provide a translation dictionary in order to specify the corresponding operators (e.g., `\\neg`, `\\wedge`, etc.).
If the examples stated in terms of the operators included in the `default_theory` instead, then the `exclusion_theory` would have to include a dictionary (i.e., the inverse of the `default_dictionary` provided above).

Further semantic theories may be included for comparison by following the pattern provided by the `default_theory` above.
Upon testing, each example will be evaluated over each semantic theory included in `semantic_theories` before moving on to the next example.

## Basic Architecture

The `semantics.py` module consists of two classes which define the models of the language and the theory of propositions over which the language is interpreted.

> TO BE CONTINUED...

### Methodology

#### Settings

TODO: how to use settings

### Semantics

### Propositions

### Operators

## Model Iteration

The exclusion theory includes a powerful model iteration system through the `ExclusionModelIterator` class defined in `iterate.py`. This feature allows you to find multiple distinct semantic models that satisfy the same logical constraints.

### Iteration Framework

The model iteration system is designed specifically for exclusion theory and operates based on:

1. **Exclusion-Specific Difference Detection**: Identifies meaningful differences between models in terms of:
   - World state changes (added or removed worlds)
   - Possible state changes (states that become possible/impossible)
   - Changes in verification of sentence letters (unilateral verification)
   - Changes in exclusion relationships between states

2. **Exclusion Theory Constraints**: Generates Z3 constraints to force the next model to differ from previous ones by requiring at least one change in:
   - Verification of atomic propositions
   - Exclusion relationships between states
   - Possible state or world status

3. **Structural Difference Enforcement**: Forces the creation of structurally different models by:
   - Changing the number of worlds or possible states
   - Modifying verification patterns
   - Altering exclusion relationship patterns
   - Changing coherence relationships

4. **Isomorphism Escape Strategies**: When the solver finds models that are too similar, increasingly stronger constraints are applied:
   - First attempt: Target significantly different world counts or verification patterns
   - Later attempts: Force extreme properties like minimal worlds, total exclusion flips, etc.

### Using Iteration

You can enable model iteration in two ways:

1. **Via Example Settings**:

```python
EX_CM_settings = {
    'N': 3,
    'max_time': 1,
    'iterate': 3,               # Find up to 3 models
    'iteration_timeout': 1.0,   # Set timeout per iteration
    'iteration_attempts': 5     # Number of attempts for difficult cases
}
```

2. **Programmatically**:

```python
from model_checker.theory_lib.exclusion.iterate import iterate_example

# BuildExample instance first
models = iterate_example(example, max_iterations=3)
```

### Understanding Model Differences

When in iteration mode, the system will display differences between successive models:

```
=== DIFFERENCES FROM PREVIOUS MODEL ===

World Changes:
  + 110 (world)
  - 011 (world)

Possible State Changes:
  + 100
  - 001

Proposition Changes:
  A:
    Verifiers: + {100}
    Verifiers: - {001}

Exclusion Relationship Changes:
  100,010: now excludes
  001,110: no longer excludes
```

### Exclusion-Specific Characteristics

The exclusion theory's iteration has some unique characteristics:

1. **Unilateral Verification**: Unlike default theory which tracks both verifiers and falsifiers, exclusion theory only shows changes in verifiers.

2. **Exclusion Relations**: The system tracks changes in the primitive exclusion relationship between states.

3. **Preclusion Functions**: For complex models, the system may display h-functions showing the preclusion mapping that witnesses the falsehood of propositions.

### Performance Notes

- Exclusion theory iteration may require more computation time due to the complexity of exclusion relationships
- Consider increasing `iteration_timeout` for complex constraints or larger values of `N`
- The `iteration_attempts` parameter controls how many attempts the system makes when it encounters isomorphic models
