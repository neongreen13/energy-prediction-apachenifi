# Code formats real-time weather data from OpenWeatherMap API extracted with Apache Nifi pipeline
# Logistic regression model predicts binary high/low building energy consumption from weather features 
# Define your data and model paths to run

import os
import pandas as pd
import pickle 

class WeatherProcessor:
    def __init__(self, folder_path, model_path, model_filename):
        """
        Initialize the WeatherProcessor object.

        Parameters:
        - folder_path (str): Path to the folder containing CSV files.
        - model_path (str): Path to the folder containing the model file.
        - model_filename (str): Name of the model file.
        """
        self.folder_path = folder_path
        self.model_path = model_path
        self.model_filename = model_filename

    def process_weather_columns(self, df):
        """
        Extract weather-related columns from csv retrieved from Apache Nifi pipeline.

        Parameters:
        - df (pd.DataFrame): Input DataFrame containing 'wind' and 'main' columns.

        Returns:
        - pd.DataFrame: Processed DataFrame with selected weather-related columns.
        """
        
        # Process 'wind' column
        df['wind_string'] = df['wind'].str.extract(r'MapRecord\[{(.*?)}\]')
        df['wind_string'] = df['wind_string'].astype(str)
        df[['wind_speed', 'wind_deg', 'wind_gust']] = df['wind_string'].str.split(',', n=3, expand=True)
        df['wind_speed'] = df['wind_speed'].str.replace('speed=', '')
        df['wind_speed'] = df['wind_speed'].astype(float)

        # Process 'main' column
        df['main_string'] = df['main'].str.extract(r'MapRecord\[{(.*?)}\]')
        df['main_string'] = df['main_string'].astype(str)
        df[['temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity']] = df['main_string'].str.split(',', n=6, expand=True)
        df['temp'] = df['temp'].str.replace('temp=', '')
        df['pressure'] = df['pressure'].str.replace('pressure=', '')
        df['humidity'] = df['humidity'].str.replace('humidity=', '')
        df['temp'] = df['temp'].astype(float)
        df['pressure'] = df['pressure'].astype(int)
        df['humidity'] = df['humidity'].astype(int)

        df = df[['timestamp','wind_speed','temp','pressure','humidity']]

        return df

    def kelvin_to_fahrenheit(self, kelvin_temp):
        """
        Convert temperature from Kelvin to Fahrenheit.

        Parameters:
        - kelvin_temp (float): Temperature in Kelvin.

        Returns:
        - float: Temperature in Fahrenheit.
        """
        fahrenheit_temp = (kelvin_temp - 273.15) * 9/5 + 32
        return fahrenheit_temp

    def convert_meters_per_sec_to_mph(self, mps):
        """
        Convert wind speed from meters per second to miles per hour.

        Parameters:
        - mps (float): Wind speed in meters per second.

        Returns:
        - float: Wind speed in miles per hour.
        """
        mph = round(2.23694 * mps, 2)
        return mph
        

    def load_model_objects(self):
        """
        Load the saved model and related objects from the specified file.
        """
        with open(os.path.join(self.model_path, self.model_filename), 'rb') as file:
            saved_objects = pickle.load(file)

        self.loaded_model = saved_objects['model']
        self.loaded_X_train_columns = saved_objects['X_train_columns']

    def run_prediction(self):
        """
        Run predictions on the weather data and save the results to a CSV file.
        """
        concatenated_data = pd.DataFrame()

        csv_files = [file for file in os.listdir(self.folder_path) if file.endswith('.csv')]

        for csv_file in csv_files:
            file_path = os.path.join(self.folder_path, csv_file)
            timestamp = pd.to_datetime(csv_file.split('.')[0], format='%Y%m%d%H%M%S')
            df = pd.read_csv(file_path)
            df['timestamp'] = timestamp
            concatenated_data = pd.concat([concatenated_data, df], ignore_index=True)

        data_df = self.process_weather_columns(concatenated_data)
        data_df['temp'] = data_df['temp'].apply(self.kelvin_to_fahrenheit)
        data_df['wind_speed'] = data_df['wind_speed'].apply(self.convert_meters_per_sec_to_mph)

        X_deploy = data_df[self.loaded_X_train_columns]
        data_df['predicted_class'] = self.loaded_model.predict(X_deploy)
        
        # Get predicted probabilities for each class
        pred_proba = self.loaded_model.predict_proba(X_deploy)

        # Add columns for each class's predicted probability
        for i, class_label in enumerate(self.loaded_model.classes_):
            data_df[f'pred_proba_{class_label}'] = pred_proba[:, i]

        data_df.to_csv(os.path.join(self.model_path, 'weather_predictions.csv'), index=False)

def main():
    folder_path = 'define_path'
    model_path = os.getcwd()
    model_filename = 'logistic_regression_model.pkl'

    weather_processor = WeatherProcessor(folder_path, model_path, model_filename)
    weather_processor.load_model_objects()
    weather_processor.run_prediction()

if __name__ == "__main__":
    main()