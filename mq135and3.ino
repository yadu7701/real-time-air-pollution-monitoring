const int mq3Pin = A0; // Analog pin connected to the MQ-3 alcohol sensor
const int mq135Pin = A1; // Analog pin connected to the MQ-135 gas sensor

void setup() {
    Serial.begin(9600); // Initialize serial communication
}

void loop() {
    int mq3Value = analogRead(mq3Pin); // Read MQ-3 alcohol sensor value
    int mq135Value = analogRead(mq135Pin); // Read MQ-135 gas sensor value

    // Convert analog readings to voltages
    float alcoholVoltage = map(mq3Value, 0, 1023, 0, 5);
    float mq135Voltage = map(mq135Value, 0, 1023, 0, 5);

    // Convert voltages to concentrations
    float alcoholConcentration = map(alcoholVoltage, 0, 5, 0, 100);
    float ammoniaConcentration = map(mq135Voltage, 0, 5, 0, 100);
    float carbonDioxideConcentration = map(mq135Voltage, 0, 5, 0, 2000);
    float carbonMonoxideConcentration = map(mq135Voltage, 0, 5, 0, 50);

    // Print sensor readings
    Serial.print("Alcohol concentration: ");
    Serial.print(alcoholConcentration);
    Serial.println(" ppm");

    Serial.print("Ammonia concentration: ");
    Serial.print(ammoniaConcentration);
    Serial.println(" ppm");

    Serial.print("Carbon Dioxide concentration: ");
    Serial.print(carbonDioxideConcentration);
    Serial.println(" ppm");

    Serial.print("Carbon Monoxide concentration: ");
    Serial.print(carbonMonoxideConcentration);
    Serial.println(" ppm");

    delay(1000); // Delay for stability
}
