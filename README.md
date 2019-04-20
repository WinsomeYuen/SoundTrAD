## Files Submitted:
- source code folder: containing all the python files for the application
- build and dist folder: for the executable file. Below explains programs needed to run it and where to find the application itself in the folders.

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
Ensure you have sound files located locally, I have created a sound folder located in the same folder as the application, for where you can keep your sound files in

Instructions on using application:
1. First login to the MySQL account created
2. Fill in the cue sheet (the table). At least the time and sound file column in the format:
 - Time in 12hr format e.g. 1:02pm
 - Sound file path stored in the cell (Not the soud file name!)
The sound file can be chosen by clicking on the button saying "Upload Sound", which is next to the respective sound file cell for each row. The Cause and Associated Events determine the sound files suggested to the user.
Extra: If you want to test each sound, you click on the sound file cell once for the sound you want to test and it will be loaded in the audio player on the seperate window.
3. Click generate timeline and your cuesheet will be transferred to the timeline, where you can listen to the combined sound created from the cuesheet
4. Save the cuesheet by going

The application has been made into an executable file, however just in case I have listed the libraries you may need to pip install:
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
