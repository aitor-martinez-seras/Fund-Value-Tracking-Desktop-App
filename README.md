# Fund-Value-Tracking-Desktop-App
This git contains the code to run a desktop app written in Python and based on TKinter, whose objective is to centralize
and accelerate the tracking of several investment funds, providing functionalities to store and visualize 
the information related to share purchases of these funds. The app generates a database locally, in the database 
directory, where all the data is contained. The only language available for the GUI currently is Spanish.

## Dependencies

The following packages are needed for the app:

- tkcalendar~=1.6.1
- matplotlib~=3.5.1
- requests~=2.27.1
- beautifulsoup4~=4.10.0

To install the required dependencies, run ``` pip install -r requirements.txt ``` from the base directory. It is
recommended to install the dependencies in a virtual environment.

## Run the app

To start the app the run the following command from the base directory and using the venv:
1. Windows
```
python venv/Scripts/python.exe main.py
```

2. Linux
```
python venv/bin/python.exe main.py
```

