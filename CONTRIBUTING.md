This respository uses an Angular based commit messages with the following layout 

> ```type(scope): subject```

- ```type``` [mandatoy] - commit type. 
- ```scope``` [optional] - commit scope.
- ```suject``` [mandatory] - commit header message.

The following commit types can be used:

- ```build``` - Used to identify development changes related to the build system (involving scripts, configurations or tools) and package dependencies.
- ```ci``` - Used to identify development changes related to the continuous integration and deployment system - involving scripts, configurations or tools.
- ```docs``` - Used to identify documentation changes related to the project - whether intended externally for the end users (in case of a library) or internally for the developers.
- ```feat``` - Used to identify production changes related to new backward-compatible abilities or functionality (update ```MINOR``` release).
- ```fix``` - Used to identify production changes related to backward-compatible bug fixes (update ```PATCH``` release).
- ```perf``` - Used to identify production changes related to backward-compatible performance improvements.
- ```refactor``` - Used to identify development changes related to modifying the codebase, which neither adds a feature nor fixes a bug - such as removing redundant code, simplifying the code, renaming variables, etc.
- ```style``` - Used to identify development changes related to styling the codebase, regardless of the meaning - such as indentations, semi-colons, quotes, trailing commas and so on.
- ```test``` - Used to identify development changes related to tests - such as refactoring existing tests or adding new tests.
