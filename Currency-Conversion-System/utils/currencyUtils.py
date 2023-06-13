import re
import locale

from constants.currencyConstants import currencySymbolToName, currencySymbolToLocale, currencyNameToLocale

from utils.csvUtils import readCSVFile, writeCSVFile, writeCSVFileFromStdin, printCSVFile


def getInputFileCurrencyName(filePath: str) -> str:
    """
    This function reads input CSV file and return the source currency symbol in abbreviated form

    @type filePath: String
    @param filePath: Input CSV File Path

    @rtype: String
    @returns: Source File Currency Symbol Name
    """
    # Read CSV file and find currency column
    csvFileInfo = readCSVFile(filePath, nrows=1)
    csvFileColumns = csvFileInfo[0]
    csvFilePriceColumn = list(
        filter(lambda x: "price" in x.lower(), csvFileColumns))[0]
    csvFilePriceColumnIndex = csvFileColumns.index(csvFilePriceColumn)
    csvFileFirstLine = csvFileInfo[1][0]
    # Read one sample currency data from currency column of first line
    currencyData = csvFileFirstLine[csvFilePriceColumnIndex]
    # Regex to find Currency Symbol and return Abbreviated form
    sourceCurrencySymbol = re.search(r"[^0-9\s,.]+", currencyData).group()
    sourceCurrencySymbolName = currencySymbolToName[sourceCurrencySymbol]
    return sourceCurrencySymbolName


def convertCurrency(sourceCurrency: str, destinationCurrency: str, multiplier: float) -> str:
    """
    This function takes source currency as an input and converts it into destination currency value with locale number formatting

    @type sourceCurrency: String
    @param sourceCurrency: Source Currency Symbol and Value
    @type destinationCurrency: String
    @param destinationCurrency: Destination Currency Symbol
    @type multiplier: Float
    @param multiplier: Float Value of Multiplier

    @rtype: String
    @returns: Destination Currency Symbol and Value
    """

    # Source Currency Processing
    sourceCurrencySymbol = re.search(r"[^0-9\s,.]+", sourceCurrency).group()
    localeOption = currencySymbolToLocale[sourceCurrencySymbol]
    locale.setlocale(locale.LC_ALL, localeOption)
    sourceValue = sourceCurrency.replace(sourceCurrencySymbol, "").strip()
    amount = locale.atof(sourceValue)

    # Destination Currency Processing
    destinationCurrency = destinationCurrency.strip().upper()
    localeOption = currencyNameToLocale[destinationCurrency]
    locale.setlocale(locale.LC_ALL, localeOption)
    convertedAmount = round(amount * multiplier, 2)
    formattedAmount = locale.currency(convertedAmount, grouping=True)
    return formattedAmount


def currencyConvertOperation(field: int, multiplier: float, currencySymbol: str, input: str, output: str) -> list:
    """
    This function does main task of currency conversion according to command line arguments.

    @type field: Integer
    @param field: CSV File Field Number (starts from 1)
    @type multiplier: Float
    @param multiplier: The value to be multiplied to original currency
    @type currencySymbol: String
    @param currencySymbol: Destination Currency Symbol - an abbreviated form Example: EUR for Euro
    @type input: String
    @param input: Input CSV file name
    @type output: String
    @param output: Output CSV file name

    @rtype: List
    @returns: A List of Boolean and String Messages
    """

    # Setting stdin and stdout flags according to command line arguments
    stdin = True if input == "stdin" else False
    stdout = True if output == "stdout" else False

    result = [True, "Currency Conversion Operation is successfully completed"]

    try:
        # Input Case 1: input is stdin
        if stdin:
            result = writeCSVFileFromStdin(currencySymbol, field)
            if not result[0]:
                return result
            input, csvData = result[2], result[3]
        # Input Case 2: input is csv file
        else:
            csvData = readCSVFile(input)

        # Read Data and Convert Currency in each row in CSV file
        csvColumns, csvRows = csvData

        for i, csvRow in enumerate(csvRows):
            sourceCurrency = csvRow[field]
            # Currency Conversion function
            convertedCurrency = convertCurrency(
                sourceCurrency, currencySymbol, multiplier)
            csvRow[field] = convertedCurrency
            csvRows[i] = csvRow
        csvData = [csvColumns, csvRows]

        # Output Case 1: output is CSV file
        fileName = f"data-{currencySymbol}.csv" if stdout else output
        result = writeCSVFile(csvData, fileName)
        if not result[0]:
            return result
        else:
            result[1] = result[1] + f": {fileName}"

        # Output Case 2: output is stdout (in this case CSV is still created)
        if stdout:
            printCSVFile(csvData)

        return result

    except Exception as e:
        result[0] = False
        result[1] = e
        return result
