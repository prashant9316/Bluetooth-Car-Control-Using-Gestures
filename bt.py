# simple inquiry example
import bluetooth

def configure_bluetooth_device():
    print("BlueTooth Configuration Started!!")
    print("")
    print("Searching for devices...")
    print("")

    nearby_devices = bluetooth.discover_devices(lookup_names=True)

    num = 0

    print("Found {} devices.".format(len(nearby_devices)))
    print("")
    print("Select your device by entering its corresponding number..")
    for addr, name in nearby_devices:
        num+=1
        print(num, ": ", addr, name)

    selection = input("> ")
    baddr, name = nearby_devices[int(selection)-1][0], nearby_devices[int(selection)-1][1]
    print("You have sected", name)
    
    port = 1

    socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

    return_values =  {
        'socket': socket, # a socket
        'address': baddr, # address for the client
        'port': port, # Port to which it is connected
        'name': name # Client Name
    }
    return return_values

def create_connection(conn):
    try:
        conn['socket'].connect((conn['baddr'], conn['port']))
        return conn['socket'], False, "Connection Established Successfully!"
    except:
        return {}, True, "Connection Failed!"

def send_message(socket, text):
    try:
        socket.send(text)
        return False, "Message Sent Successfully!"
    except:
        return True, "Error Sending Message!"
    
def close_connection(conn):
    conn['socket'].close()