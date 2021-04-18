## Changelog for SuperHelper

### What's new in 1.0.0?

#### New features

- Added new core utilities: `FileOps`
- Added full test suites for the core package (`SuperHelper.Core` and its subpackages)
- Re-written API signature of core utilities
- Added technical documentation for the whole package

#### Bug fixes

- Fixed a bug that caused the tests to fail randomly
- Fixed a bug that caused the program to fail for missing config
- Fixed a bug that caused the tests not to import the required modules

#### Non-functional changes

- Added CI (`TravisCI`) and code coverage (`codecov`) checks
- Added docstrings for all functions & methods provided by the core package

#### Notes

This is a major release and also the first release of the program. Hence, the changes in API are drastically different
from the pre-release versions. As such, the program will certainly and completely backward-incompatible. Please
uninstall the pre-release and install this new version, **DO NOT** use `pip upgrade`!
