# Project Architecture

The absolute root path of this project repository on this Windows machine is located at:
- `\OSINTRepository\`

The absolute root path of this project on this Windows machine is located at:
- `\OSINTRepository\OSINTProject\`

Relative paths from the project root path are as follows:
- **api**: `\OSINTRepository\OSINTProject\src\api\`
- **backend**: `\OSINTRepository\OSINTProject\src\backend\`
- **core**: `\OSINTRepository\OSINTProject\src\core\`
- **database**: `\OSINTRepository\OSINTProject\src\database\`
- **projectDocs**: `\OSINTRepository\OSINTProject\projectDocs\`
- **reports**: `\OSINTRepository\OSINTProject\src\reports\`
- **scraping**: `\OSINTRepository\OSINTProject\src\scraping\`
- **services**: `\OSINTRepository\OSINTProject\src\services\`
- **utils**: `\OSINTRepository\OSINTProject\src\utils\`
- **unit tests**: `\OSINTRepository\OSINTProject\tests\unitTests`
- **integration tests**: `\OSINTRepository\OSINTProject\tests\integrationTests`

## Code Style & Architecture
- **Type Hinting**: Include type hints for all function arguments and return types. Use `typing` structures or Python 3.10+ native types (e.g., `str | None`).
- **Docstrings**: Document all public modules, functions, classes, and methods using Google Style or Sphinx format.
- **Async Execution**: Prefer standard library `asyncio` for I/O-bound tasks. Use type-safe event loops.
- **Error Handling**: Avoid bare `except:` clauses. Always catch specific exceptions and log stack traces using the `logging` module.

## File & Directory Operations
- **Cross-Platform Paths**: Use `pathlib.Path` instead of manual string concatenation or `os.path` manipulations.
- **Context Managers**: Always handle file openings using `with open(...)` blocks to ensure proper file descriptor closure.

## Path Search Formatting (Strict Requirement)
- **No Escaping Backslashes**: When writing target paths or strings intended for file-searching  or file -writing utilities, commands, or system scripts, **do not automatically add escaping backslashes (`\\`) to target paths**.

## Unit test debugging
- **Analyse test files recursively**: When trying to understand why a test is failing, analyse the test and all related and refrences classes used in the test - not just the **system under test**. If the test contains assignements, references or calling to support objects. For example, test_extractionEngineTests.py tests ExtractionEngine, but many tests assign to SessionManager from session_manager.py. When debugging a test from test_extractionEngineTests.py, you must check extractionEngine.py's ExtractionEngine - but you mys also check SessionManager, and any other relevant Types referenced in the test. Do not just assume the test is failing because the SUT is lacking something.