## v0.5.1 (2025-04-15)

### Refactor

- restructure codebase with separate sync/async services, shared base classes, models and utility functions
- **async**: offload blocking operations to async functions

## v0.5.0 (2025-04-13)

### Feat

- **async**: add initial async support

## v0.4.1 (2025-04-12)

### Feat

- **account**: add methods for logging in and check authentication status

### Refactor

- **meter**: rename functions and update docstrings for clarity
- **meter**: more efficient lookup of meter consumption data

## v0.4.0 (2025-04-10)

### Feat

- **meter**: add method to refresh meter data if due and return success status

### Fix

- replace ambiguous truth value checks to avoid FutureWarning

### Refactor

- added CLI functionality and logic into cli.py
- split monolithic codebase into structured submodules
