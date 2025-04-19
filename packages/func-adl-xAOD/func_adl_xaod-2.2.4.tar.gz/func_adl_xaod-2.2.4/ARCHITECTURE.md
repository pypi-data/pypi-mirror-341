# `func_adl_xAOD` Architecture

This file provides a brief overview of how the repository is layed out and how the various bits of code in it cooperate to produce C++ code from a `func_adl` query.

After some general information, more details on how things work follow below.

## General Theory

At the most general level:

1. Client starts with a `func_adl` query represented as a python `ast.AST`. The query is rendered as a python ast by the `func_adl` library.
1. Client creates a `atlas_xaod_executor` object (or `cms_aod_executor`)
1. Client calls `apply_ast_transformation` method with the `ast`. This does `ast` -> `ast` transformations that simplify and combine `ast` elements.
1. Client calls `write_cpp_files` method with the resulting `ast` from the previous step. The output directory where the C++ files can be written
   need to be given to the method as well.
1. The C++ files produced are ready to run on the input files.

Though only part of the tests, you can see how the template files are run against a file in the `test/utils/base.py` file, specifically the `execute_result_async` method. Given a `func_adl` ast, it calls `atlas_xaod_executor` as above, and then uses a `docker` image to run against some test files.

The `atlas_xaod_executor` doesn't do much - almost all the work is done inside the `query_ast_visitor` object. This object traverses the `ast` and turns each `ast` into some sort of C++ result (see the `cpplib` folder). As it goes it accumulates the appropriate C++ type definitions, temp variables, and variable declarations - including output ROOT files, etc. See below for a more detailed description of this object.

## Package Layout

All the source code for the repository is in the `func_adl_xAOD` directory. This includes code for both CMS Run 1 and ATLAS xAOD Release 21 backends.

- `atlas/xaod` - Contains atlas R21 xAOD unique features for converting `func_adl` to C++.
- `cms/aod` - Contains cms run 1 unique features for converting `func_adl` to C++.
- `common` - Contains common code to doing the conversion. About 80% of the code to do the work is located here. The `atlas` and `cms` directories mostly deal with how to access the experiment's event model.
- `template` - Contains the code 

### Template Code

The files in this directory are templates to run against an ATLAS xAOD or CMS Run 1 data file in an docker container built by the experiment. 

#### Atlas
In the case of atlas, note that these containers contain only Python 2 currently. The upgrade to Python three will come with R22.

- `runner.sh` is the top level file that controls the run, and is the "api" that is used by the ServiceX container when it spins up a container. This script is responsible for:
  - First run, copy over generated C++ files into an ATLAS analysis release directory structure, compile, and then run against the file(s) given on `runner.sh`'s command line.
  - Second and other runs, auto-detect that the compile step has occurred, and run with any new files requested.
- `package_CMakeList.txt` is a template `cmake` file that is filled in by the generation system. It allows the compile to include only packages that are needed by the query to optimize compile time.
- `ATestRun_eljob.py` is the top level configuration file that controls the xAOD analysis job.
- `query.cxx` and `query.h` are the (mostly empty) template files where the generated query code is inserted.

Note that compile time also defines the time between the query and first data out. Currently it takes about 15 seconds to do the build, and about 15 seconds to run over a single file: it is worth keeping the compile time to a minimum.

#### CMS

## C++ Model

### Type System

The type system is needed to do at least rudimentary tracking of types in the query. For example, to reason about objects and collections and terminals (like float). The Python type system is quite rich, though it lacks introspection utilities, and this provides some extensions to that type system.

- `terminal` this is a type that we can't look inside of - a `float` or an `int` or a `bool`, for example. Some objects will get labeled as `terminals` as well. It has a flag to indicate that it isn't just a terminal, but a pointer to a terminal. It tracks the C++ name of the type, not the Python name.

- `collection` is any sort of grouping of common object that can be iterated over. It tracks the interior type. In C++ the expected semantics are that of a forward iteratable collection.

- `tuple` is a funny: it doesn't actually represent a C++ object or type. Rather, it is a way of collecting a group of python types together that represent a tuple in Python. Tuples like this can/do appear in queries.

More recent versions of Python are gaining introspection tools. It could be at some future point the type system could be removed in favor of a pure Python type system.

### Variables

As the query is turned into C++ code, C++ variables and collections are declared. The `cpp_representations` objects tracks these. Every variable has a type and a scope where it is defined.

Scope is a little tricky:

- Scope defines where the variable is defined. Scope mimics/tracks the standard C++ scoping rules (e.g. it is visible below, but not above/outside the current level).
- It can't be redefined once set. However, there are times where query assembly requires one to know the variable before the scope is set.
- See the `Scope` section for more information.

As different types of things have different capabilities, several objects track variables:

- `cpp_value` - A basic value, like a value (double `123`). It contains the type and scope and name of the variable. This is used for constants and also for variables that do not need to be declared (e.g. are globally available).
- `cpp_variable` - a variable that is declared. An iterator for a loop, or a temp storage for the results of a C++ tertiary operator. Besides everything a `cpp_value` tracks, it also tracks an initial value. When the C++ code is emitted, it will be initialized with the given value.
- `cpp_collection` - Represents a `vector<float>` or similar. Any container with forward iterator semantics.
- `cpp_tuple` - a tuple as a container of other values. This has no direct C++ analogy/type. It is never emitted directly to C++ code. Rather it is used to track an ordered list of values during query building.
- `cpp_dict` - a dictionary as a container of other values. This has no direct C++ analogy/type. It is never emitted directly to C++ code. Rather it is used to track a named list of values during query building.
- `cpp_sequence` - basically, an iterator that points to some object in a collection. It contains the variable that is the actual iterator as well as a pointer to the parent collection.

### Statements

Statements are very simple - they contain very little intelligence; by the time the code has been reduced to a C++ statement all variable naming and placement, etc., has been performed.

### Scope and Statements

When variables are declared the scope at which they are defined must be tracked. Since variables are intertwined with statements, these two things go hand-in-hand.

Broadly, there are two kinds of statements - simple statements and compound statements. All statements must support the `emit` method, which is how code is emitted to the strings that are placed in the template files.

Simple Statements:

All statements inherit from an abstract base class: all classes must provide a method to write out the code in a linear order, even though the code isn't always created in that order.

- `arbitrary_statement` - an arbitrary line of code.
- `set_var` - Sets a variable to a particular value (using a boring old `=` sign)
- `push_back` - Pushes a value onto a `vector`
- `container_clear` - Clears a declared `vector` by calling `.clear()`.
- `book_ttree` and `ttree_fill` (these are ATLAS specific statements) - Results are put on a `TTree`. The ATLAS infrastructure is used to store the ROOT `TTree`s (hence the fact that this is ATLAS specific). The variables that are booked are then set via other statement. When the fill is called, it just calls the `Fill` method of `TTree`.

Block Statements:

A block statement is really just a collection of statements enclosed by brackets, `{` and `}`. It has a variable declaration section along with executable statements. In C++ these are interchangeable, but that level of flexibility isn't needed for this, so isn't modeled. Note that during `func_adl` traversal it is often necessary to declare a new variable at an outer context - so the ability to walk back up nested levels is important (for example, think of the Count predicate - encountered while iterating over jets, and the counter variable must be declared outside that iterating loop).

- `block` - The concrete base class. Automatically scopes all code it is responsible for holding onto. Provides for variable declaration and statement holding services.
- `loop` - A type of block that is controlled by a for loop over a container (the `for (auto itr: container) {...}` construct).
- `iftest` and `elsephrase` - Two blocks that are part of an if/else statement.

Scope:

Scope is a way of tracking:

- Where we are currently adding code
- Where a variable was declared
- Ability to walk up and down the scope
- Compare the scoping of a statement and variable to understand if a particular variable is visible at a statement's scope.

For example, implementing the `Count` above, scoping objects provide services so the code can say "Add and initialize this counter variable to zero outside the scope that this jet iterator is declared at".

These services are provided by the `gc_scope` object. It represents a particular `frame` or scope, as well as providing the methods to move up and down and some comparison services. It does this by keeping a private copy of the scope stack: the current scope of the statement/variable and all the scopes above. There is a special kind of scope, called `top_level`, which is represented by a token, and is the global scope at which the whole executor is declared.

During traversal, the main coding object, `generated_code` holds onto the current position that statements are being added. This is a scope object. To add a new statement, the code first finds the current scoping object. It then asks that object to add the statement to the end of its list of statements. For that reason, only a block statement can be pointed to by the scope.

### Function Mapping

There are many functions in C++ that are the same in python. By far the simplest thing to do is map between the two. The math functions are perfect examples of this (e.g. `sin` and `cos`). A lookup table is maintained that holds onto the python name of a function, the C++ name, its return type, and the include file that it is declared in.

These are declared in the `cpp_functions.py` file.

## Traversing the `func_adl` AST

The `func_adl` query comes in as a python AST. A standard python `ast.NodeVisitor` traverses the AST and generates the code (called `query_ast_visitor`). An attempt is made to turn each python `ast` node into a C++ representation (a `crep`). The code takes advantage of python's object extensibility, and stores this as the nodes representation (`node.rep`). Thus, as the `ast` tree is traversed, if any node has already been processed, it will have a `rep` property and that can be used instead of having to re-processes the code below. An `ast` sub-tree can be repeated if the `dataframe_expressions` package decides it refers to the same thing. This occurs, for example, during lambda capture.

The main `ast` traversal is driven by the code in the `ast_to_cpp_translator.py` file. Other than basic operations (unary, binary, indexing, comparisons, etc.), special predicates are supported here.

- Function calls are quite general. There are ones made against a C++ object, like a `reco::Jet` in CMS, or an `xAOD::Jet` in ATLAS. There are also translated functions (see function mapping above). Even generic C++ code is supported here.
- The `Aggregate` operation is supported. This is a function call that operates on each element of a sequence with a function and an accumulator, calling the function repeatedly with the last value of the accumulator and a member of the sequence. `Count` is a very simple form of the aggregate pattern. Also, `Sum`, `Min` and `Max`. These are all supported as syntatic sugar by `func_adl`, and the `ast` is rewritten before traversal to use `Aggregate(0, lambda v, a: v + a)` rather than `Sum()` or similar.
- Special handling is implemented when an `ast` node representing the root dataset is encountered. In many cases, this doesn't exist in C++. For example, both ATLAS and CMS fetch the jets into a local variable, not as members of some `Event` object. While in `func_adl` the jets is just a property of an event object, in C++ the jets container must be explicitly declared and referenced.
- The python `if` expression is supported (`a = <result_true> if <cond> else <result_false>`). It can't be translated to a C++ `?` operator because `result_true` and `result_false` can be arbitrarily complex - and be expanded to multiple lines of C++. Thus python `if` expressions are expanded to C++ `if` statements.
- All expressions terminate by being written to a ROOT file in the C++ translator. The node of the `ast` must be a `AsROOT` term, or one will be inserted. Lists and dictionaries are processed sensibly. For example, if you write out a dictionary, then the dictionary keys are used as `TTree` column names.
- The `Select` and `SelectMany` and `Where` predicates are implemented by unrolling the sequence and applying the function the user has specified. The function is a `lambda`: the arguments are defined in a stack (see scope above), and then processing proceeds. Once the representation is found, it is replaced as the representation for the function call to that `lambda`.
- The `First` predicate is implemented by running a loop in `C++` and caching the first element (and exiting the loop). This is done because there could be some sophisticated filtering done before the `First` predicate: you don't always get to take the zero'th element of an array. You might be taking the first non-zero element of an array, for example.

### Accumulating the Generated Code

The object `generated_code` is responsible for holding onto everything needed as the AST is traversed:

- The current block it is being filled with code
- Track the outer most block (`book_block`) - all code is contained in this block.
- Any variables that need to be declared at class level (e.g. class instance variables). These are variables that need to be kept around between events.
- The current scope
- List of include files that should be added to the code as it is generated.

It can do things like:

- move up and down the scope stack (.e.g pop a level when coming out of a loop)
- Add top level statements - like a `TTree` booking statement.
- emit the C++ code via a C++ formatter, booking statements (as they often have to be placed in a different spot in the template), and class variable declarations.

The emitting of code is done by a very simple object that contains a single method, called `add_line`: it takes a string as an argument. A simple version that supplies automatic indenting, etc., can be found in `atlas_xaod_executor`.

### Event Collections

Event collections are `Jets` and `Tracks`, etc. They are accessed via some custom C++ code. `func_adl` then treats them as a sequence. The exact semantics are experiment dependent, and, sometimes, collection dependent, but they are treated the same way in the `func_adl` language.

The C++ code for the collections is encoded in the files called `event_collections.py` in the ATLAS and CMS sub-directories. They define the names that appear in `func_adl` and the C++ code-behind. In most cases the semantics are the same for all collections, so the code takes advantage of this.
