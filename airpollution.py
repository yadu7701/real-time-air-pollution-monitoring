
import serial
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import datetime

# Initialize serial connection
ser = serial.Serial('COM3', 9600)  # Change 'COM3' to the port your Arduino is connected to

# Create an empty DataFrame to store sensor readings
sensor_data = pd.DataFrame(columns=['alcohol_concentration', 'ammonia_concentration', 'carbon_dioxide_concentration',
                                    'carbon_monoxide_concentration'])

# Define the number of samples to collect
num_samples = 10

# Collect sensor data
for _ in range(num_samples):
    # Read sensor data from Arduino
    arduino_data = ser.readline().decode().strip()

    # Split Arduino data by ':' to separate the sensor type and reading
    sensor_readings = arduino_data.split(': ')

    # Check if the number of elements in sensor_readings is valid
    if len(sensor_readings) != 2:
        print("Error: Invalid Arduino data format")
        continue

    # Extract sensor type and reading
    sensor_type = sensor_readings[0]
    sensor_reading = float(sensor_readings[1].split()[0])  # Extract the numerical reading

    # Update the corresponding column in the DataFrame based on sensor type
    if sensor_type == 'Alcohol concentration':
        sensor_data.loc[len(sensor_data), 'alcohol_concentration'] = sensor_reading
    elif sensor_type == 'Ammonia concentration':
        sensor_data.loc[len(sensor_data), 'ammonia_concentration'] = sensor_reading
    elif sensor_type == 'Carbon Dioxide concentration':
        sensor_data.loc[len(sensor_data), 'carbon_dioxide_concentration'] = sensor_reading
    elif sensor_type == 'Carbon Monoxide concentration':
        sensor_data.loc[len(sensor_data), 'carbon_monoxide_concentration'] = sensor_reading
    else:
        print("Error: Unknown sensor type")

# Close serial connection
ser.close()

print(sensor_data)
pd.set_option('future.no_silent_downcasting', True)  # Set the option

# Get the current date and time
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Construct the file name with the timestamp
file_name = f"sensor_data_{timestamp}.xlsx"

# Fill missing values with zero and update the DataFrame
sensor_data = sensor_data.fillna(0)

# Save DataFrame to Excel file with the timestamped file name
sensor_data.to_excel(file_name, index=False)

# Define thresholds for each pollutant concentration
thresholds = {
    'alcohol_concentration': 50,
    'ammonia_concentration': 10,
    'carbon_dioxide_concentration': 1000,
    'carbon_monoxide_concentration': 20
}

# Determine pollution status based on sensor readings
def determine_pollution_status(reading):
    for pollutant, threshold in thresholds.items():
        if reading[pollutant] > threshold:
            return 'Polluted'
    return 'Not Polluted'

# Apply determine_pollution_status function to each row of sensor_data
sensor_data['pollution_status'] = sensor_data.apply(determine_pollution_status, axis=1)

# Separate features (X) and labels (y)
X = sensor_data.drop('pollution_status', axis=1)  # Features
y = sensor_data['pollution_status']  # Labels

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a machine learning model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Print the predicted labels
print("Predicted labels:", y_pred)
