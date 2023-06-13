import sys

from utils.argUtils import parseArgs, validateArgs
from utils.currencyUtils import currencyConvertOperation


def main():
    """
    This function takes command line arguments as an input, parse & validate them and handle the currency conversion operation
    """
    # Step 1: Parsing Command Line Arguments
    argsDict = parseArgs()

    # Step 2: Validate Command Line Arguments to ensure proper formatting
    result = validateArgs(**argsDict)
    if not result[0]:
        messages = result[1]
        for i, message in enumerate(messages if isinstance(messages, list) else [messages]):
            print(f"Error Message {i+1}: {message}")
        sys.exit(0)
    else:
        argsDict = result[2]

    # Step 3: Process Currency Conversion Operation and output the result
    result = currencyConvertOperation(**argsDict)
    print(result[1])
    if not result[0]:
        print(result[1])


if __name__ == "__main__":
    main()
