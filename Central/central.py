import keyboard

import asyncio
from bleak import BleakScanner, BleakClient


#VALUES TO BE SET UPON PERPRIPRIAL COMPLETION
PROXIMITY_SERVICE_UUID = "00000000-5EC4-4083-81CD-A10B8D5CF6EC"             
PROXIMITY_CHARACTERISTIC_UUID = "00000001-5EC4-4083-81CD-A10B8D5CF6EC"
DEVICE_NAME = "ProximitySensor"
#VALUES TO BE SET UPON PERPRIPRIAL COMPLETION


# alarm status and range
alarm_set = False #CHANGE BACK TO FALSE
RANGE_NEAR = 0
RANGE_FAR = 230


async def connect_to_device():
    print("Scanning...")
    detected_devices = await BleakScanner.discover()
    alarm_node = None
    alarm_set = False


    for device in detected_devices:

        # the print function is to make it easier to tell what devices are being detected 
        # in case we need said info
        print(f"Device '{device.name}' detected, Address: {device.address}")

        if device.name == DEVICE_NAME:
 
            alarm_node = device
            break
  
  
    if not alarm_node:
        print(f"Alarm sensor: {DEVICE_NAME} not detected, please check device and try again...")
        return
 
 
 
    print(f"Alarm sensor '{DEVICE_NAME}' detected, attempting to connect...")

    async with BleakClient(alarm_node.address) as client:
        print(f"Connected to sensor: {DEVICE_NAME}...")
        print("Beggining setup...")

        for service in client.services:
            print(f"Service UUID: {service.uuid}")

            if service.uuid.lower() == PROXIMITY_SERVICE_UUID.lower():

                for character in service.characteristics:

                    print(f"  Characteristic: {character.uuid} \n     Properties: {character.properties}")
                    #print character.uuid.lower()
                    #print PROXIMITY_CHARACTERISTIC_UUID.lower()
                    
                    if character.uuid.lower() == PROXIMITY_CHARACTERISTIC_UUID.lower(): 

                        print("Setup complete, starting sensor notififcations")

                        def handle_proximity_data(sender, data):


                            ##  CHECK FOR CORRECT VALUE AND ALTER IF NECISSARY  ##
                            
                            #proximity_byte = data
                            #proximity_int = int.from_bytes(proximity_byte, "big")
                            
                            #print("Proximity :", proximity_int)
                            
                            
                            proximity = data.decode("utf-8")

                            #print utf 8 string
                            #print("utf-8:",proximity)
                            
                            proximityINT = int(proximity)

                            #print value of AlarmSet
                            #print(bool(alarm_set))

                            #print int of Proximity
                            print("int:",proximityINT)
                            
                            if  proximityINT <= RANGE_FAR:
                                if proximityINT >= RANGE_NEAR:
                                    if alarm_set == True:
                                       print("ALARM!!! OBJECT DETECTED!!!")


                            

                        await client.start_notify(character.uuid, handle_proximity_data)
                        print("Recieving Data, press A to set/deactivate alarm, Ctrl+C to quit...")
                        try:
                            while True:
                                
                                if keyboard.is_pressed('p'):
                                
                                    if alarm_set == True:
                                        print( "// Alarm is now disabled //")
                                        alarm_set = False
                                    else:
                                        print("// Alarm is now acive //")
                                        alarm_set = True
                                #How often await waits for input.
                                await asyncio.sleep(0.1)
                                   
                        except KeyboardInterrupt:
                            print("\nStopping notifications...")
                            await client.stop_notify(char.uuid)
                            print("Disconnected.")
                            return
                        
                     
                        
                        

        print("Expected services and other information not found, please check for correct device installation")


if __name__ == "__main__":
    asyncio.run(connect_to_device())
      


 

 
 
 





