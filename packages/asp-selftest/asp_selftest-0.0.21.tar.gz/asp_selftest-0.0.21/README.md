asp-selftest
============
In-source test runner for Answer Set Programming (ASP) with Clingo.

Status
------

This tools is still a work in progress.

This Test-Tool has been presented at (Declarative Amsterdam in November 2024)[https://declarative.amsterdam/program-2024]. All the materials, including the presentation, are online and can be found via the given link.

It is currently in transition from `asp-test` towards `clingo-tests`. The latter is a drop-in replacement for `clingo` with the added ability to activate `plugins`. The former is still around.

A plugin for running the in-source unit tests is active by default. A plugin translating clingo (syntax) errors to Python exceptions with ASP source snippets with exact error location is also active.

You can write you own plugins. I have one for reifying rules from theory atoms, for example.

About
-----

With in-source testing, source and tests stay together in the same file, hence the tests are also expressed in ASP.

The tests are as non-obstrusive as possible and and many examples are idiomatic in nature and could have been written in another way. These idioms are merely ways to provide clearer code and avoid mistakes. As such, they have value in themselves.


RUNNING
-------

After installation via pip, run it using:

    $ asp-tests <file.lp> ...

Alternatively you can run it as a module, given that either the working directory of the PYTHONPATH are set to 'src':

    $ python -m asp_selftest <file.lp> ...

There are options to silents the in-source Python tests etc, have a look:

    $ asp-tests -h


TESTING
-------
The code is equiped with in-source Python tests which always run. You can silence them with --silent.


TODO
----
To use the program without the tests: Not Yet Implemented. But you can use the `base` program anywhere of course, since all `#program`s are ignored by default.


IDEA
----

1. Use `#program`'s to identify units and their dependencies. Here we have a unit called `unitA` with a unit test for it called `testunitA`.

       #program unit_A.
    
       #program test_unit_A(unit_A).

   The implicit program `base` (see Clingo Guide) must be referenced explicitly if needed.


2. Extend the notion of `#program` by allowing the use of functions instead of only constants.  This allows `#program` units with constants being tested. Here is a unit `step` that is tested with constant `a` being substituted with `2`:

       #program step(a).
    
       #program test_step(step(2)).   % this feature is no longer present in `clingo-tests`.

   Note that using this feature makes the program incompatible with Clingo. The test runner has an option to transform a extended program back to compatible Clingo without running the tests.


3. Within a test program, use `assert` with `@all` to ensure universal truths that must be in every model. We use `@all` to communicate to the runtime that this particular assert must be checked for presence in every model. Its argument is just a name for identification.

        #program step(n).
        fact(n).

        #program test_step(step(3)).
        assert(@all("step fact"))  :-  fact(3).

   Note that `"step fact"` is just a way of distinquishing the assert. It can be an atom, a string, a number or anything else. Pay attention to the uniqueness in case of variables in the body. Take note of point 5 below.

   You can use `@any` instead of `@all` to assert truths that must be present in at least one model.


4. To enable testing constraints and to guard tests for empty model sets, we use `@models` to check for the expected number of models. In the example above, we would add:

        assert(@models(1)).


5. Care must be taken if variables in the body lead to expansion and conjunctions. See `duplicate_assert.lp`. The system gives a warning for:

        assert(@all(id_uniq))  :-  def_id(Id, _, _),  { def_id(Id, _, _) } = 1.

    Instead you have to write:

        assert(@all(id_uniq(Id)))  :-  def_id(Id, _, _),  { def_id(Id, _, _) } = 1.


