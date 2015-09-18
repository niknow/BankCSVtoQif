BankCSVtoQif
============
.. image:: https://travis-ci.org/niknow/BankCSVtoQif.svg?branch=master
    :target: https://travis-ci.org/niknow/BankCSVtoQif

.. image:: https://coveralls.io/repos/niknow/BankCSVtoQif/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/niknow/BankCSVtoQif?branch=master


BankCSVtoQif consists of a Python library and a command line interface that allows to convert a \*.csv-file
of transactions downloaded from a certain bank account generate a \*.qif-file as an output. The \*.qif-file can then be
imported from financial software like gnucash. The advantage of qif over csv is that qif allows to store the target
account of the transaction. In addition to the technical conversion, you can configure replacements that automatically
relabel the description of a transaction if a certain string is matched and book this transaction to a pre-configured
account. The rationale behind this is that many transactions occur regularly and thus can be booked automatically. 

A list of supported banks is provided by the folder `bankcsvtoqif/banks`, see developers_ section to add more banks.

**Recommended Python version:** Python 3.4.3

Installation
------------

* Clone this repo::

    git clone https://github.com/niknow/BankCSVtoQif.git

* Switch into BankCSVtoQif and install the python library::

    cd BankCSVtoQif
    python setup.py install

* Use the command line interface to display help::

    python b2q.py -h


Example: Deutsche Bank Checking Account
---------------------------------------
Download the \*.csv-file from your online banking interface to the location of the `b2q.py`. We assume this file
is named `transaction_data.csv`. Invoke::

    python b2q.py db_giro transaction_data.csv

A file named `transaction_data.qif` will be created in the same directory. You can modify the name of the output
file if you wish::

    python b2q.py db_giro transaction_data.csv my_fancy_transactions.qif

The \*.qif-file is now ready to be imported into your financial sofware, for instance gnucash.


Using automatic Replacements
----------------------------
During the conversion process you can use the `-r` option to conduct automatic replacements::

    python b2q.py db_giro transaction_data.csv -r

The replacements are configured in `replacements.ini`. You can also choose another file via::

    python b2q.py db_giro transaction_data.csv --replacements my_replacement_config.ini

The `replacements.ini` contains a list of replacements to be conducted automatically for each bank account type. For
instance, the `db_giro` list contains::

    ["cryptic number 123", "Rent", "Expenses:Flat:Rent", 1]

That means that whenever a description of a transaction contains the string "cryptic number 123", it will be
replaced by "Rent" (in case you specify the empty string here, the description will not be modified). The target
account of that transaction will be set to "Expenses:Flat:Rent". The append flag '1' will append the year and the month
('0' won't append anything and '2' appends the next month). You can add as many replacements as you want for all of your
bank account types. If you import the resulting qif into gnucash, the transaction will be booked automatically to the
specified target account. All in all this achieves that you don't have to manually book a regular transaction every time.

.. _developers:

For developers: Creating new bank account types
-----------------------------------------------
In case you are a customer of a bank, which is not in the list yet, you can have to options of adding it.

Open an issue on github
~~~~~~~~~~~~~~~~~~~~~~~
State which bank you would like to add and supply a csv-file with a dummy bank statement, i.e. a typical csv bank statement of this bank, but with anonymized data. This can be obtained easily by taking a real bank statement, deleting all but a few transactions and replacing sensitive information like name, account number, customer identifiers in descriptions etc. by dummy data like `ABC` or `1.23`. **Please do not send us any sensitive financial data.**

Add the bank to the `banks` folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implement a csv parser for your bank. For that you have to fork and clone the repo andthen  add a file, e.g. `my_bank.py` in the banks folder::


    bankcsvtoqif\\banks
    __init__.py
    ...
    db_giro.py
    ...
    my_bank.py

You can use an existing bank like `db_giro.py` as a blueprint. The abstract class `BankAccountConfig` in `__init__.py` contains more information. It is a good idea to also supply a unit test `test_my_bank.py` for your bank in::

    bankcsvtoqif\\tests\\banks
    __init__.py
    ...
    test_db_giro.py
    test_my_bank.py

You can use an existing test like `test_db_giro.py` as a blueprint. Test your bank on your local machine an make a pull request when you are finished.

Uninstallation
--------------
To remove BankCSVtoQif uninstall the python library by deleting all its files. You can get a list of these via::

    python setup.py install --record files.txt
    cat files.txt

