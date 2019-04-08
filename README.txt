Programs needed to run application:
- Python Version 3.5
Make sure that it is in PATH
https://www.python.org/downloads/release/python-350/
- MySQL Connector Python 8.0 for Python 3.5 = used to install everything
- MySQL Server 8.0
- MySQL Workbench 8.0 CE = used to view database and simplify user setup
You will need to create a new user with all accessed granted this can be
done in the workbench by going to Server > Users and Privileges > Add account
Once you have filled in the login detail, go to the Administrative Roles tab
and check DBA to check all at once and then click apply to save.

The application can be located in the folder:
SounTrAD > dist > soundtrad
It is named soundtrad and should have a logo
Instructions on using application:
1. First login to the MySQL account created
2. 





Libraries you need to pip install:
- PyQt5 Version 3.5: pip install PyQt5
- PyDub: pip install pydub
- Matplotlib: pip install matplotlib
- MySQLdb: pip install mysqlclient
The MySQLdb download may not work above as I am using a windows OS and had to find
a different method, so possibly try instead:
conda install mysqlclient
brew install mysql-connector-c  (will need to pip install homebrew first)
pip install mysql-python


I use Qt creator to view the code, but it is obviously
optional. Here is the link to download the opensource version:
https://www.qt.io/download
