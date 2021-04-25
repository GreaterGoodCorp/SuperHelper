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

### What's new in 1.1.0?

#### New features

- Added a new built-in module: `CovidTracker`
- Added global debugging mode

#### Bug fixes

**1.1.1**:

- Include `req.json` of built-in modules on packaging

**1.1.2**:

- Fixed a bug that caused logging messages to be printed twice when DEBUG mode is enabled

#### Non-functional changes

- Added a more comprehensive HTML `docs`

#### Notes

*None*

### What's new in 1.2.0?

#### New features

*None*

#### Bug fixes

- Fixed a bug that caused the help messages to be incorrectly formatted (#32)
- Fixed a bug that caused the logger syntax error to occur (#33)

#### Non-functional changes

*None*

#### Notes

*None*
