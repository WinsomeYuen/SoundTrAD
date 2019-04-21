# SoundTrAD
A desktop application built using PyQt5 aimed to aid novice designers in building auditory displays. This is an open source project that encourages designers/developers to download and further contribute to the development of the application to help the wider community by contributing the ongoing development in research on auditory displays, which has been influenced by the people at the International Community for Auditory Displays. 

The tools have been developed using Doon MacDonald's research: https://smartech.gatech.edu/handle/1853/60074 \
With the aid of Tony Stockman my supervisor and discussions with Doon, the application that I have developed in this short period of time have achieved the core goals I set at the start of this journey. 

## Files Submitted
- Source code folder: containing all the python files I wrote for the application
- Build and dist folder: for the executable file. Below explains programs needed to run it and where to find the application itself in the folders.
- Test notes folder: contains pdf files of the various testing done for the application. Majority of it are raw notes that have just been edited to add a better layout for easier viewing.

## Programs needed to run application
### Python 
Python Version 3.5 - it should work with any Python 3 version or later\
**Note:** Make sure that it is in *PATH* for windows\
https://www.python.org/downloads/release/python-350/

### MySQL
- MySQL Connector Python 8.0 for Python 3.5 = Simplifies installation by installing everything at once
- MySQL Server 8.0
- MySQL Workbench 8.0 CE = used to view database and simplify user setup You will need to create a new user with all access granted this can be done in the workbench by going to `Server > Users and Privileges > Add account`. Once you have filled in the login detail, go to the Administrative Roles tab and check DBA to check all at once and then click apply to save.\

https://dev.mysql.com/downloads/

The application can be located in the folder:\
`SounTrAD > dist > soundtrad`\
It is named soundtrad and should have a logo.
Ensure you have sound files located locally, I have created a sound folder located in the same folder as the application, for where you can keep your sound files in.

## Instructions on using application
1. First login to the MySQL account you have created (or any account you are happy to store location of sound files)
2. Fill in the cue sheet (the table). At least the time and sound file column in the format:
 - Time in 12hr format e.g. 1:02pm
 - Sound file path stored in the cell (Not the soud file name!)\
The sound file can be chosen by clicking on the button saying **"Upload Sound"**, which is next to the respective sound file cell for each row. The Cause and Associated Events determine the sound files suggested to the user.
**Extra:** If you want to test each sound, you click on the sound file cell once for the sound you want to test and it will be loaded in the audio player on the seperate window.
3. Click generate timeline and your cuesheet will be transferred to the timeline, where you can listen to the combined sound created from the cuesheet
4. Save the cuesheet by going

The application has been made into an executable file, however just in case I have listed the libraries you may need to pip install:
- PyQt5 Version 3.5\
`pip install PyQt5`
- PyDub\
`pip install pydub`
- Matplotlib\
`pip install matplotlib`
- MySQLdb\
`pip install mysqlclient`

Downloading PyQt5 has been a bit buggy to download via terminal lately for on windows OS with the recent updates that have rolled out. So, if the above does not work try downloading the exe file from sourceforge: https://sourceforge.net/projects/pyqt/files/PyQt5/

The MySQLdb download may not work above as I am using a windows OS and had to find
a different method, so possibly try these alternatives instead:
```
conda install mysqlclient

brew install mysql-connector-c  (will need to pip install homebrew first)

pip install mysql-python
```


I use Qt creator to view the code, but it is obviously optional. Here is the link to download the opensource version:\
https://www.qt.io/download


## Summary
This has been a very interesting project to work on which combines my programming skills, with my new interest in interaction/ux design. It has made me discover a new world of interacting with technology. The project will now be passed back to Doon to look further into developing this research into something more concrete, so hopefully this has helped aid her in the next steps. 
