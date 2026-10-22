import unittest
import sys
import os

# Add project root to path so imports work correctly regardless of where the script is called from.
current_dir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 1. Stores the unit tests path (adjust if your folder structure differs)
UNIT_TESTS = "tests/unit_test"

def main():
    if len(sys.argv) > 1:
        # 3. If a command line argument exists, check it against files in UNIT_TESTS
        test_name = sys.argv[1]
        full_path = os.path.join(UNIT_TESTS, test_name)

        if os.path.exists(full_path):
            # Run the specific file provided via CLI 
            loader = unittest.TestLoader()
            suite = loader.discover(os.path.dirname(full_path), pattern=f"*{test_name}*")
            unittest.TextTestRunner().run(suite)
        else:
            print(f"Error: Test file '{test_name}' not found in {UNIT_TESTS}")
            sys.exit(1)
    else:
        # 4. If no command line arguments, run all tests discovered in the UNIT_TESTS directory
        loader = unittest.TestLoader()
        suite = loader.discover(UNIT_TESTS)
        unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    main()