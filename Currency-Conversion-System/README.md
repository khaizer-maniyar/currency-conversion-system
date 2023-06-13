# Currency Conversion System
Overview: This system does operation of currency conversion either from csv file or from standard input taken from user in application console, it validates the requirements of input file or standard input for currency conversion. if data is suitable then currency conversion is done else it shows respecitve errors. the output is shown either on application console or saved in csv file.

Techbology: Python

## Specifications

1) Input can be CSV file or Standard Input from user in Console
2) Output can be CSV file or Standard Output to user in Console
3) CSV File parsing does not use csv module. A custom parser is built for CSV file processing.
4) The output file can also be used as an input file. So, USD to Euro and Euro to USD is possible.
5) Command Line Arguments can handle some mistyped inputs such as extra space, not specific case characters, etc.
6) System detects CSV file encoding using chardet module else uses default encoding
7) For Unit Testing - data.csv file is given in the folder. To change source currency. Use Microsoft Excel currency options and choose currency symbol from supported list of options. (see below for supported symbols)
```
{ "USD": "$", "EUR": "€", "BRL": "R$", "CNY": "¥", "INR": "₹", "MYR": "RM", "PLN": "zł", "KRW": "₩", "THB": "฿", "GBP": "£", "HKD": "HK$" }
```

## Requirements

1) CSV files must be seprated by pipe symbol ("|"): Reason is this system supports multiple currencies and few currency has comma, period and space for representing place value. Refer to [this](https://support.talkdesk.com/hc/en-us/articles/360047099811-CSV-Files-and-Regional-Settings) article to change CSV File Seprator in Windows and MAC. Change the list operator for Windows and decimal for MAC to to pipe symbol.
2) Python version 3 needs to be installed in system. Visit [this](https://www.python.org/downloads/) to download latest python version.
3) If input is from CSV file, then CSV file must have currency column formatted as Currency from Microsoft Excel. It will allow the data to be saved in locale number formatting.
4) Required few python libraries before running a program. Refer to below instructions.

## Instructions to Run Program

1) **Install required python libraries**: Run below command in Terminal at folder path to install required python libray.

```
pip install chardet==5.1.0
```
or
```
pip3 install chardet==5.1.0
```

2) **Command Line Arguments Help**: Folder has currency_convert.py. This is the entrypoint of currency conversion system. This program takes required command line arguments. To get specifics about it, use below command.

```
python currency_convert.py --help
```
or
```
python currency_convert.py -h
```

It will print out the requirements of command line arguments as below

```
usage: currency_convert.py [-h] --field N --multiplier N --symbol currency -i input -o output

This program accepts CSV file ot standard input with one currency and coverts into another currency

optional arguments:
  -h, --help         show this help message and exit
  --field N          Convert CSV field N (Integer)
  --multiplier N     Multiply currency value by N for the current conversion rate (Float)
  --symbol currency  Conversion Currency Symbol in abbreviated form. Example: EUR for Euro
  -i input           Read from input file (or stdin)
  -o output          Write to output file (or stdout)
```

**Note**: Reason for adding --symbol Currency is to decide destination currency. This system supports multiple currencies from below list. So, it is easy to process python program with this input. Below list is covering currencies of most popular currencies.

#### Supported Currencies Dictionary: 
```
{ "USD": "$", "EUR": "€", "BRL": "R$", "CNY": "¥", "INR": "₹", "MYR": "RM", "PLN": "zł", "KRW": "₩", "THB": "฿", "GBP": "£", "HKD": "HK$" }
```

3) **Run Program with different possible combinations**: This program either takes input from user in application console or from CSV file. Also, it outputs data to user in application console or to CSV file. intput can be file-name.csv or stdin and output can be file-name.csv or stdout.

* **Option 1**: input and output is CSV file. Run below command

```
python currency_convert.py --field N --multiplier N --symbol Currency -i input-file.csv -o output-file.csv
```

Example Command Line Arguments:
```
python currency_convert.py --field 2 --multiplier 0.5 --symbol inr -i data.csv -o data-INR.csv
```

This will either show error messages or success message as output

```
Successfully Created Output CSV file: output-file.csv
```

* **Option 2**: input is CSV file and output is stdout. Run below command

```
python currency_convert.py --field N --multiplier N --symbol Currency -i input-file.csv -o stdout
```

Example Command Line Arguments:
```
python currency_convert.py --field 2 --multiplier 0.5 --symbol inr -i data.csv -o stdout
```

This will either show error messages or success message and data as output on console

```
Note: stdout option can only print maximum 5 rows. refer to output csv file to see more rows.

Feed Name  |Price Per Month|Source Name                            |Last Update|Remote Name               |Local Name
---------------------------------------------------------------------------------------------------------------------
newsmonster|₹ 2,08,213.61  |News Monster                           |1483820220 |/mirror/nm/newsmonster.tgz|/r/nm.tgz
microtech  |₹ 10,179.22    |MicroTech Industries (TODO: Inc.? LLC?)|1483820232 |/dl/mtech.tar.gz          |/r/mt.tgz
fastniche  |₹ 406.84       |Fast Niche® Markets                    |1483820247 |/site/fastniche.zip       |/r/fn.tgz
pivotsense |₹ 14.38        |Pivotal Sense (ltd.)                   |1483820006 |/dl area/pivotsense.tgz   |/r/ps.tgz
woldenheim |₹ 2,015.32     |Woldenheim GmbH                        |1483817526 |/woldenheim/db-new.zip    |/r/wh.tgz


Successfully Created Output CSV file: data-INR.csv
```

* **Option 3**: input is stdin and output is CSV file. Run below command

```
python currency_convert.py --field N --multiplier N --symbol Currency -i stdin -o output-file.csv
```

Example Command Line Arguments:
```
python currency_convert.py --field 2 --multiplier 0.5 --symbol inr -i stdin -o data-INR.csv
```

It will ask for Source Currency Symbol input. Currency is input.

```
Enter Currency of Data from below options
Supported Currencies: ['USD', 'EUR', 'BRL', 'CNY', 'INR', 'MYR', 'PLN', 'KRW', 'THB', 'GBP', 'HKD']
Currency: usd
```

It will ask for total number of columns. Column Count is input.

```
Enter total columns of data in integer
Column Count: 6
```

It will ask for Column Names seprated by CSV file seprator. Column Names is input.

```
Enter Column names seprated by | and column name should not contain it. Example: name1|name2|name3|..
Note: Currency Data Column name should contain 'price' keyword. field command line argument should be currency column
Column Names: Feed Name|Price Per Month|Source Name|Last Update|Remote Name|Locale Name
```

It will ask for total number of rows. Row Count is input.
```
Enter total rows of data in integer
Row Count: 2
```

It will ask Row Count times to enter row data. Row Data is input.
```
Enter Row 1 Data seprated by | and column data should not contain it. Example: data1|data2|data3|..
Note: For Currency Data enter value with precision point. It will be converted automatically to locale number formatting
Example: 22.83 for EUR will be stored as 22,83 € in CSV file
Row Data: newsmonster|7.99|News Monster|1483820220|/mirror/nm/newsmonster.tgz|/r/nm.tgz

Enter Row 2 Data seprated by | and column data should not contain it. Example: data1|data2|data3|..
Note: For Currency Data enter value with precision point. It will be converted automatically to locale number formatting
Example: 22.83 for EUR will be stored as 22,83 € in CSV file
Row Data: woldenheim|5656.23|Woldenheim GmbH|1483817526|/woldenheim/db-new.zip|/r/wh.tgz
```

It will show error messages or success message.
```
Successfully Created Output CSV file: output-file.csv
```

* **Option 4**: input is stdin and output stdout. Run below command

```
python currency_convert.py --field N --multiplier N --symbol Currency -i stdin -o stdout
```

Example Command Line Arguments:
```
python currency_convert.py --field 2 --multiplier 0.5 --symbol inr -i stdin -o stdout
```

It will ask for Source Currency Symbol input. Currency is input.

```
Enter Currency of Data from below options
Supported Currencies: ['USD', 'EUR', 'BRL', 'CNY', 'INR', 'MYR', 'PLN', 'KRW', 'THB', 'GBP', 'HKD']
Currency: usd
```

It will ask for total number of columns. Column Count is input.

```
Enter total columns of data in integer
Column Count: 6
```

It will ask for Column Names seprated by CSV file seprator. Column Names is input.

```
Enter Column names seprated by | and column name should not contain it. Example: name1|name2|name3|..
Note: Currency Data Column name should contain 'price' keyword. field command line argument should be currency column
Column Names: Feed Name|Price Per Month|Source Name|Last Update|Remote Name|Locale Name
```

It will ask for total number of rows. Row Count is input.
```
Enter total rows of data in integer
Row Count: 2
```

It will ask Row Count times to enter row data. Row Data is input.
```
Enter Row 1 Data seprated by | and column data should not contain it. Example: data1|data2|data3|..
Note: For Currency Data enter value with precision point. It will be converted automatically to locale number formatting
Example: 22.83 for EUR will be stored as 22,83 € in CSV file
Row Data: newsmonster|7.99|News Monster|1483820220|/mirror/nm/newsmonster.tgz|/r/nm.tgz

Enter Row 2 Data seprated by | and column data should not contain it. Example: data1|data2|data3|..
Note: For Currency Data enter value with precision point. It will be converted automatically to locale number formatting
Example: 22.83 for EUR will be stored as 22,83 € in CSV file
Row Data: woldenheim|5656.23|Woldenheim GmbH|1483817526|/woldenheim/db-new.zip|/r/wh.tgz
```

It will show error messages or success messages. It will show the output CSV file on console as well as save with data-currency_name.csv format.

```
Note: stdout option can only print maximum 5 rows. refer to output csv file to see more rows.

Feed Name  |Price Per Month|Source Name    |Last Update|Remote Name               |Locale Name
----------------------------------------------------------------------------------------------
newsmonster|₹ 14.38        |News Monster   |1483820220 |/mirror/nm/newsmonster.tgz|/r/nm.tgz
woldenheim |₹ 10,181.21    |Woldenheim GmbH|1483817526 |/woldenheim/db-new.zip    |/r/wh.tgz


Successfully Created Output CSV file: data-INR.csv
```

## Program Structure
```
C:.
|   currency_convert.py
|   data.csv
|   README.md
+---constants
|   |   csvConstants.py
|   |   currencyConstants.py
+---resources
|       flowchart.png
\---utils
    |   argUtils.py
    |   csvUtils.py
    |   currencyUtils.py
```
* Outer Folder: currency_convert.py is the main entrypoint for software. data.csv is sample input file for unit testing. README.md is to get knowledge base for program.

* constants folder: This folder has constants used in application. It has CSV file constants in csvConstants.py and currency related constants in currencyConstants.py file.

* resources folder: This folder has flowchart of the system.

* utils folder: This folder has python files containing utility methods. argUtils.py has utility methods for command-line arguments. csvUtils.py has utility methods for CSV Files. currencyUtils.py has utility methods for currency conversion.

## Flowchart of System
![Flow Chart](/resources/flowchart.png)

## Developer
Maan Mandaliya | maan.mandaliya@dal.ca | [Portfolio](https://maanmandaliya.super.site/)
