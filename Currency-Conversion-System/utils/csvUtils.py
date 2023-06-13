import chardet
import os
import re
import locale

from constants.currencyConstants import supportedCurrencies, supportedCurrencySymbols, currencySymbolToLocale, currencyNameToLocale
from constants.csvConstants import csvFileBasePath, csvSeprator, csvDefaultEncoding


def getCSVFileEncoding(filePath: str) -> str:
    """
    This function reads CSV file and find the encoding type

    @type filePath: String
    @param filePath: Input CSV File Path

    @rtype: String
    @return: Encoding Type of CSV file
    """
    # Read CSV file in Byte format and use chardet module to detect encoding type
    with open(filePath, 'rb') as csvFile:
        # Reading large chunk of file
        data = csvFile.read(10000000)
        # Detect encoding
        encodingInfo = chardet.detect(data)
        # If not detected encoding then return default CSV encoding
        encoding = encodingInfo['encoding'] if encodingInfo['confidence'] > 0 else csvDefaultEncoding
        return encoding


def getTotalCSVFileColumns(filePath: str) -> int:
    """
    This function returns total number of columns in CSV file

    @type filePath: String
    @param filePath: Input CSV File Path

    @rtype: Integer
    @return: Total number of columns in CSV file
    """

    # Find CSV file encoding
    encoding = getCSVFileEncoding(filePath)

    # Reading CSV file with custom parser and count total columns
    with open(filePath, 'r', newline="\r\n", encoding=encoding) as csvFile:
        totalColumns = len(csvFile.readline().split(csvSeprator))
    return totalColumns


def readCSVFile(fileName: str, nrows: int = -1) -> list:
    """
    This function reads CSV from given input file path

    @type fileName: String
    @param fileName: Input CSV File Name
    @type nrows: Integer
    @param nrows: Number of Rows to read from CSV file (-1 means all rows, 0 to n represent n number of rows)

    @rtype: List
    @return: List of CSV Column Names and All Rows Data
    """

    # Set CSV file path
    csvFilePath = os.path.join(csvFileBasePath, fileName)

    # Find CSV file encoding
    encoding = getCSVFileEncoding(csvFilePath)

    # Reading CSV file with custom parser
    with open(csvFilePath, 'r', newline="\r\n", encoding=encoding) as csvFile:
        csvFileColumns = []
        csvFileRows = []
        for row in csvFile:
            row = row.replace("\r\n", "")
            if all(len(data) == 0 for data in row):
                break
            if not csvFileColumns:
                csvFileColumns = row.split(csvSeprator)
                continue
            csvFileRows.append(row.split(csvSeprator))
            if nrows != -1 and len(csvFileRows) == nrows:
                break

    # Return a pair of columns and rows data
    return [csvFileColumns, csvFileRows]


def writeCSVFile(csvData: list, fileName: str) -> list:
    """
    This function takes csv data as input and writes it into csv file

    @type csvData: List
    @param csvData: List of CSV Columns and Rows
    @type fileName: String
    @param fileName: CSV File Name

    @rtype: List of Boolean and String
    @returns: List of Boolean Status and String Message of operation
    """

    result = [True, "Successfully Created Output CSV file"]

    try:
        # Set CSV file path
        csvFilePath = os.path.join(csvFileBasePath, fileName)
        
        # Writing CSV file with custom parser
        with open(csvFilePath, "w", encoding=csvDefaultEncoding) as csvFile:
            csvColmunNames, csvRowData = csvData
            lineSeprator = "\n"
            csvColmunNames = csvSeprator.join(csvColmunNames) + lineSeprator
            csvRowData = list(
                map(lambda x: csvSeprator.join(x) + lineSeprator, csvRowData))
            csvRowData.insert(0, csvColmunNames)
            csvFile.writelines(csvRowData)

        return result

    except Exception as e:
        result[0] = False
        result[1] = e
        return result


def writeCSVFileFromStdin(currencySymbol: str, field: int) -> list:
    """
    This function takes input from user in console and writes data in csv file 

    @type currencySymbol: String
    @param currencySymbol: Destination Currency Symbol
    @type field: Integer
    @param field: CSV File Currency Column Number

    @rtype: List of Boolean and String
    @returns: List of Boolean Status and String Message of operation
    """

    result = [True, "Successfully created CSV file data from stdin"]
    csvData = [list(), list()]

    try:
        # Take Currency Input and validate it from supported list of currencies
        print("Enter Currency of Data from below options")
        print(f"Supported Currencies: {supportedCurrencies}")
        sourceCurrency = input("Currency: ")
        sourceCurrency = sourceCurrency.strip().upper()
        if not sourceCurrency or sourceCurrency not in supportedCurrencies or sourceCurrency == currencySymbol:
            result[0] = False
            result[1] = "Currency must be from above options only and not equal to destination currency symbol"
            return result

        # Take input of column names and validate field position should have "price" keyword
        print("\nEnter total columns of data in integer")
        columnCount = input("Column Count: ")
        if not columnCount or not columnCount.isdigit():
            result[0] = False
            result[1] = "Column Count must be a valid integer"
            return result
        columnCount = int(columnCount)

        print(f"\nEnter Column names seprated by {csvSeprator} and column name should not contain it. Example: name1|name2|name3|..")
        print("Note: Currency Data Column name should contain 'price' keyword. field command line argument should be currency column")
        csvColumns = input("Column Names: ")
        csvColumns = csvColumns.strip()
        csvColumnNames = csvColumns.split(csvSeprator)
        if not csvColumns or len(csvColumnNames) != columnCount or any(csvColumn.isdigit() for csvColumn in csvColumnNames):
            result[0] = False
            result[1] = f"Column Names must be seprated by {csvSeprator}, must be equal to column count and should not contain only digit"
            return result
        elif not "price" in csvColumnNames[field].lower():
            result[0] = False
            result[1] = "field command line argument column number should contain 'price' keyword"
            return result
        csvColumnNames = list(map(lambda x: x.strip(), csvColumnNames))
        if field > len(csvColumnNames):
            result[0] = False
            result[1] = "Currency Column should be less then total columns count"
            return result
        csvData[0] = csvColumnNames

        # Take input of rows data and it must match with number of columns
        print("\nEnter total rows of data in integer")
        rowCount = input("Row Count: ")
        if not rowCount or not rowCount.isdigit():
            result[0] = False
            result[1] = "Row Count must be a valid integer and greater than 0"
            return result
        rowCount = int(rowCount)
        if rowCount <= 0:
            result[0] = False
            result[1] = "Row Count must be greater than 0"
            return result

        for i in range(rowCount):
            print(f"\nEnter Row {i+1} Data seprated by {csvSeprator} and column data should not contain it. Example: data1|data2|data3|..")
            print("Note: For Currency Data enter value with precision point. It will be converted automatically to locale number formatting")
            print("Example: 22.83 for EUR will be stored as 22,83 € in CSV file")
            csvRows = input(f"Row {i+1} Data: ")
            csvRows = csvRows.strip()
            csvRowData = csvRows.split(csvSeprator)
            if not csvRows or len(csvRowData) != columnCount:
                result[0] = False
                result[1] = f"Row Data must be seprated by {csvSeprator} and must be equal to column count"
                return result
            else:
                for i, columnData in enumerate(csvRowData):
                    if i == field:
                        amount = float(columnData)
                        localeOption = currencyNameToLocale[sourceCurrency]
                        locale.setlocale(locale.LC_ALL, localeOption)
                        formattedAmount = locale.currency(
                            amount, grouping=True)
                        csvRowData[i] = formattedAmount
                csvData[1].append(csvRowData)

        # Create CSV file from csvData
        fileName = f"data-{sourceCurrency}.csv"
        result = writeCSVFile(csvData, fileName)
        if not result[0]:
            return result

        # Validate CSV file data
        csvFilePath = os.path.join(csvFileBasePath, fileName)
        result = validateCSVFile(csvFilePath, field)
        if not result[0]:
            return result
        # Append new file name and csv data
        else:
            result.append(fileName)
            result.append(csvData)

        return result

    except Exception as e:
        result[0] = False
        result[1] = e
        return result


def printCSVFile(csvData: list):
    """
    This function takes CSV data as input and print on console in tabular format

    @type csvData: List
    @param csvData: List of CSV Columns and Row Data
    """

    # distribute csv data to columns and rows
    csvColumns, csvRows = csvData
    
    # Max Rows output in stdout is 5, file is created to view all rows
    maxRowsPrint = 5
    print(f"\nNote: stdout option can only print maximum {maxRowsPrint} rows. refer to output csv file to see more rows.\n")

    # Processing Data to find justification length to print data in console
    columnsWidth = [0 for i in range(len(csvColumns))]
    for i, csvColmun in enumerate(csvColumns):
        columnsWidth[i] = max(columnsWidth[i], len(csvColmun))
    for csvRow in csvRows:
        for i, csvRowData in enumerate(csvRow):
            columnsWidth[i] = max(columnsWidth[i], len(csvRowData))
            if i + 1 == maxRowsPrint:
                break
    
    # Printing CSV Columns
    print("|".join(csvColumn.ljust(width)
          for csvColumn, width in zip(csvColumns, columnsWidth)))

    # Calculating repeat number for hyphen to divide between column names and row data
    hyphenRepeat = 0
    for columnWidth in columnsWidth:
        hyphenRepeat += columnWidth
    hyphenRepeat += (len(columnsWidth) - 1)
    print("-" * hyphenRepeat)

    # Printing CSV Rows
    for csvRow in csvRows:
        if all(len(data) == 0 for data in csvRow):
            break
        print("|".join(csvRowData.ljust(width)
              for csvRowData, width in zip(csvRow, columnsWidth)))
    print("\n")


def validateCSVFile(filePath: str, field: int) -> list:
    """
    This function takes filePath as input, reads it and check whether the file is ready to process or not

    @type filePath: String
    @param filePath: Input CSV File Path
    @type field: Integer
    @param field: CSV File's Currency Column Number

    @rtype: List of Boolean & String
    @return: Boolean Status of File Validation & Error Message in String
    """
    # Find CSV file encoding
    encoding = getCSVFileEncoding(filePath)

    # Pair of Boolean Status and Error Message
    validateInfo = [True, "Valid CSV File. It is ready to be processed"]

    # Reading CSV file with custom parser
    with open(filePath, 'r', newline="\r\n", encoding=encoding) as csvFile:
        csvFileColumns = []
        csvFileRows = []

        # Case 1: Empty CSV file
        firstRow = csvFile.readline().replace("\r\n", "")
        if not firstRow:
            validateInfo[0] = False
            validateInfo[1] = "CSV File is Empty. It must be filled with Column Names and Matching number of rows data"
            return validateInfo
        else:
            csvFileColumns = firstRow.split(csvSeprator)
            if not csvFileColumns[-1]:
                csvFileColumns.pop(-1)

        # Case 2: Atleast one column should contain "price" keyword
        if not any("price" in columnName.lower() for columnName in csvFileColumns):
            validateInfo[0] = False
            validateInfo[1] = "CSV File Columns are invalid. Atleast one column should contain price keyword"
            return validateInfo

        for row in csvFile:
            row = row.replace("\r\n", "")
            csvRowData = row.split(csvSeprator)  # change
            if all(len(data) == 0 for data in csvRowData):
                break
            # Case 3: Row Data contains null
            if any(len(data) == 0 for data in csvRowData):
                validateInfo[0] = False
                validateInfo[1] = "Invalid CSV File. Row Data containts null element"
                return validateInfo
            # Case 4: Row Data is not matching number of columns
            if len(csvRowData) != len(csvFileColumns):
                validateInfo[0] = False
                validateInfo[1] = "Invalid CSV File. Row Data is not matching to total number of columns"
                return validateInfo
            else:
                csvFileRows.append(csvRowData)

        # Case 5: Only Column names in CSV, rows data does not exist
        if len(csvFileRows) == 0:
            validateInfo[0] = False
            validateInfo[1] = "Invalid CSV File. It only contains column names and does not contain rows data"
            return validateInfo

        # Case 6: Currency data should be at proper column and in locale number formatting
        sourceCurrencySymbol = ""
        for csvFileRow in csvFileRows:
            csvFileRow = list(map(lambda x: x.strip(), csvFileRow))
            currencyData = csvFileRow[field]
            sourceCurrencyInfo = re.search(r"[^0-9\s,.]+", currencyData)
            # Case: Currency Columns has no symbol
            if not sourceCurrencyInfo:
                validateInfo[0] = False
                validateInfo[1] = "Invalid CSV File or Input. Currency data is not at proper column in CSV file. Check Command Line argument"
                return validateInfo
            # Case: input CSV file has symbol not supported in this currency conversion system
            if not sourceCurrencySymbol:
                sourceCurrencySymbol = sourceCurrencyInfo.group()
            if sourceCurrencySymbol not in supportedCurrencySymbols:
                validateInfo[0] = False
                print(
                    f"Supported Currency Symbols: {supportedCurrencySymbols}")
                validateInfo[1] = "Invalid CSV File Currency. It should be from supported currency symbols as above"
                return validateInfo
            # Case: csv file has more than one currency symbols
            elif sourceCurrencyInfo.group() != sourceCurrencySymbol:
                print(sourceCurrencyInfo.group(), sourceCurrencySymbol)
                validateInfo[0] = False
                validateInfo[1] = "Invalid CSV File. Multiple Currency Symbols Exist in CSV file. It should contain only one currency"
                return validateInfo
            # Case: Price Column Data is not according to locale number formatting
            else:
                localeOption = currencySymbolToLocale[sourceCurrencySymbol]
                locale.setlocale(locale.LC_ALL, localeOption)
                try:
                    currencyData = currencyData.replace(
                        sourceCurrencySymbol, "")
                    amount = locale.atof(currencyData)
                except Exception as e:
                    validateInfo[0] = False
                    validateInfo[1] = "Invalid CSV File. Currency Value Formatting is not according to locale number formatting"
                    validateInfo[1] += f"\n{e}"
                    return validateInfo

        return validateInfo
