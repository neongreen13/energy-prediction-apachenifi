# Apache Nifi Data Pipeline: Predicting A Building's Energy Consumption from Weather Data

In a fast-moving world, the skill of creating a seamless data pipeline to ingest, process, and transfer data is essential. Building a solid pipeline is even more important for computational efficiency and the ease of integrating machine learning models into the pipeline. This exercise below sets up a data pipeline using Apache Nifi to collect real-time weather data, transform it for machine learning modeling, and transfer it to a location for a future downstream business purpose. 

The project takes historical weather data from OpeneatherMap API for the city of Berkely, California, and combines it with the data from a single building’s energy consumption collected through sensors over a two eyar period between . There are two notebooks attached:
-	Exploratory data analysis on historical weather data for Berkeley and the building's energy consumption in the same time period.
-	Train a LSTM model on timeseries data with an inference run to predict the energy consumption based on new weather data (gathered from Apache Nifi)

New data will be gathered via API in Apache Nifi and transformed for real-time predictions.

Here is what the data pipeline looks like in Apache Nifi:
![image](https://github.com/neongreen13/energy-prediction-apachenifi/assets/48419376/a845a0ae-eac0-4abf-992c-70fcad613bda)


___________________________________________________________________________________________________________________________________________

## Apache Nifi Installation and Start Up
1.
Download Binaries (Nifi Standard is the default) and run installation:
https://nifi.apache.org/download/ 
-	Download the zip file, extract the contents, and save the path for later
-	Verify the integrity of the download. This typically involves checking the OpenPGP signatures and hash values (SHA-256 or SHA-512). Instructions for verification are usually provided on the download page.

2.
If you don’t have Java installed on your computer, you will need it to run Nifi.

Download and Install Java:
https://www.oracle.com/java/technologies/downloads/#jdk21-windows
-	X64 Installer is the default
-	Save the path where you downloaded the files

Set JAVA_HOME Path:
After installing Java, set the JAVA_HOME environment variable:
-	Right-click on "This PC" or "Computer" on your desktop or in File Explorer.
-	Select "Properties."
-	Click on "Advanced system settings" on the left.
-	Click the "Environment Variables" button.
-	Under "System variables," click "New" to add a new variable.
-	Set the variable name to JAVA_HOME and the variable value to the path where Java is installed (e.g., C:\Program Files\Java\jdk1.8.0_281).

In your terminal, check the java version:
-	Type ‘java -version’

3.
To run Nifi,
-	Open terminal by going to the Start command and search ‘cmd’
-	Cd into the folder you just saved the zip file
o	Example: C:\Users\name\Downloads\nifi-2.0.0-M1-bin\nifi-2.0.0-M1
o	Nifi README:
	[linux/osx] execute bin/nifi.sh start 
	[windows] execute bin/run-nifi.bat 
	Open ‘nifi-app.log’ to obtain the generated Username and Password from logs/nifi-app.log
-	Open the local host URL: https://localhost:8443/nifi/ and enter Username and Password to log into the system
