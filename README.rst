BankCSVtoQif
=======

The Python library BankCSVtoQif supports the creation of scripts that take as an input a *.csv-file of transactions
downloaded from a certain bank account generate a *.qif-file as an output. The *.qif-file can then be imported
from financial software like gnucash. The advantage of qif over csv is that qif allows to store the target account
of the transaction. In addition to the technical conversion, you can configure replacements that automatically
relabel the description of a transaction if a certain string is matched and book this transaction to a pre-configured
account. The rationale behind this is that many transactions occur regularly and thus can be booked automatically.

**Project status:** Experimental.


Installation
-------

* Clone this repo::

    git clone https://github.com/niknow/BankCSVtoQif.git

* Switch into BankCSVtoQif and install the python library::

    cd BankCSVtoQif
    python setup.py install

* You can start using the example scripts `db_giro.py`, `db_master.py` or `lloyds.py` for a checking account at
 Deutsche Bank, a Deutsche Bank Mastercard or a Lloyds bank checking account.


Example: Deutsche Bank Chechking Account
-------
Download the *.csv-file from your online banking interface to the location of the `db_giro.py`. We assume this file
is named `transaction_data.csv`. Invoke::

    python db_giro.py transaction_data.csv

A file named `transaction_data.qif` will be created in the same directory. You can modify the name of the output
file if you wish::

    python db_giro.py transaction_data.csv my_fancy_transactions.qif

The *.qif-file is now ready to be imported into your financial sofware, for instance gnucash.


Using automatic Replacements
-------
In the `db_giro.py`, you can comment in the following lines::

    replacements = [
        Replacement('cryptic number 12345', 'Rent', 'Expenses:Flat:Rent', 1),
        ]

This will have the following effect on the conversion: Whenever a transaction is found whose description contains
the string 'cryptic number 12345', its description will be replaced by the term 'Rent' and the target account
'Expenses:Flat:Rent' will be chosen to book that transaction. The numer '1' will append the year and the month
(see class definition for more details on that flag). You can add as many replacements as you want. If you import
the resulting qif into gnucash, the transaction will be booked automatically to the configured target account. So
you don't have to book regular transactions manually every time.

Creating a new script
~~~~~~~
In case you are a customer of any other bank than the examples above, you can use the `db_giro.py` script as a
template to create your own script. In the class::

    class DBGiroParserFunctions(BankAccountParserFunctions):

you have to adapt the functions to make them parse a line of the csv of from bank. Next, you have to configure::

    db_giro.delimiter = ';'     #delimiter character to parse the csv
    db_giro.quotechar = '"'     #quotation character to parse the csv
    db_giro.dropped_lines = 5   #number of initial lines in the csv that do not contain transaction data
    db_giro.source_account = 'Assets:Current Assets:Checking Account'   #use the same name as in your software (e.g. gnucash)
    db_giro.target_account = 'Imbalance-EUR'    #use the same name as in your software (e.g. gnucash)

That's basically it. Optionally you can configure replacements as described above.

Uninstallation
-------
To remove BankCSVtoQif uninstall the python library by deleting all its files. You can get a list of these via::

    python setup.py install --record files.txt
    cat files.txt

Of course you can also all scripts created with that library.
