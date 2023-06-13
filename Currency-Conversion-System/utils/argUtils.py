import os
import argparse

from constants.currencyConstants import supportedCurrencies
from constants.csvConstants import csvFileBasePath

from utils.csvUtils import validateCSVFile, getTotalCSVFileColumns
from utils.currencyUtils import getInputFileCurrencyName


def parseArgs() -> dict:
    """
    This function parse command line arguments from console and returns a dictionary of command line arguments if they are valid

    @rtype: Dictionary
    @returns: Dictionary of Command-Line Arguments Key-Value pairs
    """
    # Parsing Command Line Arguments
    parser = argparse.ArgumentParser(
        description="This program accepts CSV file ot standard input with one currency and coverts into another currency")
    parser.add_argument("--field", metavar="N", dest="field", type=str,
                        required=True, help="Convert CSV field N")
    parser.add_argument("--multiplier", metavar="N", dest="multiplier", type=str,
                        required=True, help="Multiply currency value by N for the current conversion rate")
    parser.add_argument("--symbol", metavar="currency", dest="currencySymbol", type=str,  # choices=supportedCurrencies,
                        required=True, help="Conversion Currency Symbol in abbreviated form. Example: EUR for Euro")
    parser.add_argument("-i", metavar="input", dest="input", type=str,
                        required=True, help="Read from input file (or stdin)")
    parser.add_argument("-o", metavar="output", dest="output", type=str,
                        required=True, help="Write to output file (or stdout)")
    # Parse arguments from console
    args = parser.parse_args()
    # Creating Dictionary of arguments and return
    argsDict = vars(args)
    return argsDict


def validateArgs(field: str, multiplier: str, currencySymbol: str, input: str, output: str) -> list:
    """
    This function takes command line arguments object as an input & validate them

    @type field: String
    @param field: CSV File Field Number (starts from 1)
    @type multiplier: String
    @param multiplier: The value to be multiplied to original currency
    @type currencySymbol: String
    @param currencySymbol: Destination Currency Symbol - an abbreviated form Example: EUR for Euro
    @type input: String
    @param input: Input CSV file name
    @type output: String
    @param output: Output CSV file name

    @rtype: List
    @returns: A List of Boolean, String Messages, and argsDict
    """

    try:
        status = True
        messages = []
        stdin = False

        # Argument: -i input
        # Option 1: Standard Input from Console (stdin)
        input = input.strip()
        if input.lower() == "stdin":
            stdin = True
            input = input.lower()
        # Option 2: Input from CSV file
        else:
            csvFilePath = os.path.join(csvFileBasePath, input)
            # Checking File Name Convention: file-name.csv
            inputInfo = input.split(".")
            if len(inputInfo) != 2 or len(inputInfo[0]) == 0:
                status = False
                messages = "Invalid Input File name. It must be file-name.csv format or stdin"
                return [status, messages]
            # File Extention is not CSV
            elif "csv" != inputInfo[1].lower():
                status = False
                messages = "Invalid extention of Input File name. It must end with .csv extention"
                return [status, messages]
            # File Extention is CSV
            else:
                # Sanitizing input file extention - .CSV / .csV to .csv
                if "csv" != inputInfo[1]:
                    extention = inputInfo[1]
                    input = input.replace(extention, extention.lower())
                # Check Input File - does exist in outer directory or not
                if input not in os.listdir():
                    status = False
                    messages = "Input file does not exist in current directory"
                    return [status, messages]

        # Argument: --field N
        # Check Field Number - it must be a valid integer
        field = field.strip()
        if not field or not field.isdigit():
            status = False
            messages = "Field Must be a valid integer"
            return [status, messages]
        field = int(field) - 1
        if not stdin:
            # Field number must be less then total csv file columns
            totalColumns = getTotalCSVFileColumns(csvFilePath)
            if field > totalColumns:
                status = False
                messages = "Field Number must be less than or equal to total number of columns in CSV file"
                return [status, messages]

        # Argument: --symbol Currency
        # Check if the destination currency is in supported currency list or not
        currencySymbol = currencySymbol.strip().upper()
        if currencySymbol not in supportedCurrencies:
            status = False
            print(f"Supported Currencies: {supportedCurrencies}")
            messages = "Currency Symbol is not valid. It must be from list of above supported options"
            return [status, messages]

        # Validating the Input file
        if not stdin:
            validateInfo = validateCSVFile(csvFilePath, field)
            status = validateInfo[0]
            messages = validateInfo[1]
            if not status:
                return [status, messages]

        # Argument: --multiplier N
        # Check Multiplier Value - it must be a valid float
        multiplier = multiplier.strip()
        if not any(value.isdigit() for value in multiplier.split(".")):
            status = False
            messages = "Multiplier must be an integer or float value"
            return [status, messages]
        multiplier = round(float(multiplier), 2)

        # Argument: --symbol Currency
        # Check if the destination currency is same as input file currency or not
        if not stdin:
            sourceCurrency = getInputFileCurrencyName(csvFilePath)  # change
            if currencySymbol == sourceCurrency:
                status = False
                messages = "Currency Symbol must be different then source currency"
                return [status, messages]

        # Argument: -o output
        # Option 1: Show Output in Console (stdout) -> handled by other function
        # Option 2: Output to CSV file
        output = output.strip()
        if output.lower() != "stdout":
            # Checking File Name Convention: file-name.csv
            outputInfo = output.split(".")
            if len(outputInfo) != 2 or len(outputInfo[0]) == 0:
                status = False
                messages = "Invalid output File name. It must be file-name.csv format or stdout"
                return [status, messages]
            # File Extention is not CSV
            elif "csv" != outputInfo[1].lower():
                status = False
                messages = "Invalid extention of output File name. It must end with .csv extention"
                return [status, messages]
            # File Extention is CSV but not sanitized output
            else:
                # Sanitizing output file extention - .CSV / .csV to .csv
                if "csv" != outputInfo[1]:
                    extention = outputInfo[1]
                    output = output.replace(extention, extention.lower())
        else:
            output = output.lower()

        # return updated command-line arguments
        argsDict = {
            "field": field,  # Integer
            "multiplier": multiplier,  # Float
            "currencySymbol": currencySymbol,  # String
            "input": input,  # String
            "output": output  # String
        }

        return [status, messages, argsDict]

    except Exception as e:
        return [False, e]
