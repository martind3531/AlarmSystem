
#include <Arduino_APDS9960.h>
#include <ArduinoBLE.h>

#define VALUE_SIZE 20
BLEService proximityService = BLEService("00000000-5EC4-4083-81CD-A10B8D5CF6EC");
BLECharacteristic proximityCharacteristic = BLECharacteristic("00000001-5EC4-4083-81CD-A10B8D5CF6EC", BLERead | BLENotify, VALUE_SIZE);

int oldProxReading = 0;



long previousMillis = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  if (!APDS.begin()) {
    Serial.println("Error initializing APDS-9960 sensor.");
    while(1);
  }
  pinMode(LED_BUILTIN, OUTPUT);

  if (!BLE.begin()){
    Serial.println("Error initializing BLE!");
    while(1);
  }
  BLE.setLocalName("ProximitySensor");
  BLE.setDeviceName("ProximitySensor");
  proximityService.addCharacteristic(proximityCharacteristic);
  BLE.addService(proximityService);

  


  BLE.advertise();
  Serial.println("BLE device active, waiting for connections...");
}
void loop() {
  BLEDevice central = BLE.central();
  int proximity = 0;
  if (central) {
    Serial.print("Connected to central: ");
    Serial.println(central.address());

    digitalWrite(LED_BUILTIN, HIGH);

    while (central.connected()) {
      if (APDS.proximityAvailable()) {
        
        updateProximity();
      }
      delay(100);
    }
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("Disconnected from central.");
  }
}

void updateProximity(){
  int proximity = APDS.readProximity();

  if (proximity != oldProxReading){
    char buffer[VALUE_SIZE];
    int ret = snprintf(buffer, sizeof buffer, "%d", proximity);
    if(ret >= 0){
      proximityCharacteristic.writeValue(buffer);
      oldProxReading = proximity;
      //Testing Output
      Serial.print("Proximity: ");
      Serial.println(proximity);
    }
  }

      //proximityCharacteristic.writeValue((int8_t)proximity);
      //Serial.print("Proximity: ");
      //Serial.println(proximity);
  }

  

