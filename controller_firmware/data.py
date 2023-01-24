
MAX_IN_PACKET = 1024 # Maximum packet size of 1kb
MESSAGE_LEN = 8*13 + 2*2

def write_float(_in: float) -> float:
    return "{:012.5f}=".format(_in)

def write_bool_int(_in: int) -> str:
    return str(_in) + "="

def readpacket(sock):
    pack = bytearray()
    for i in range(0, MAX_IN_PACKET):
        byte = sock.recv(1)
        if byte == b'\n':
            return pack
        
        pack += bytearray(byte)
        
    # Maybe clear the socket input buffer here
    return pack

class ControllerData:
    def __init__(self): 
        self.x: float = 0
        self.y: float = 0
        
        self.sw1: int = 0
        self.sw2: int = 0
        
        self.ax: float = 0 
        self.ay: float = 0 
        self.az: float = 0 
        
        self.gx: float = 0
        self.gy: float = 0 
        self.gz: float = 0 
        
    def writeMESSAGE(self):
        MESSAGE = ""
        MESSAGE = write_float(self.x)
        MESSAGE += write_float(self.y)
        MESSAGE += write_bool_int(self.sw1)
        MESSAGE += write_bool_int(self.sw2)
        
        MESSAGE += write_float(self.ax)
        MESSAGE += write_float(self.ay)
        MESSAGE += write_float(self.az)
        
        MESSAGE += write_float(self.gx)
        MESSAGE += write_float(self.gy)
        MESSAGE += write_float(self.gz)
        
        MESSAGE += "\n"
        
        return MESSAGE
        #print(f"{MESSAGE}")
    
    def readMESSAGE(self, message):
        
        if len(message) < MESSAGE_LEN:
            return print(f"{len(message)}/{MESSAGE_LEN}")
        
        MESSAGE = message.split('=')
        
        self.x = float(MESSAGE[0]) 
        self.y = float(MESSAGE[1])
        self.sw1 = int(MESSAGE[2])
        self.sw2 = int(MESSAGE[3])
        
        self.ax = float(MESSAGE[4])
        self.ay = float(MESSAGE[5])
        self.az = float(MESSAGE[6])
        
        self.gx = float(MESSAGE[7])
        self.gy = float(MESSAGE[8])
        self.gz = float(MESSAGE[9])
        
    def data_tuple(self):
        return self.x, self.y,self.sw1,self.sw2,self.ax, self.ay, self.az, self.gx, self.gy, self.gz