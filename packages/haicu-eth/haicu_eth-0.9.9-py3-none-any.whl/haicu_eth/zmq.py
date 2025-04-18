from datetime import datetime
from typing import Union
import struct
import zmq

CMD_READ_STATUS = 1
CMD_WRITE_REG = 2
CMD_READ_REG = 3
CMD_WRITE_MEM = 4
CMD_READ_MEM = 5

MLD1200_VID = 0x0403
MLD1200_PID = 0x6010

# This must match setting in FPGA, or be lower
FPGA_FIFO_SIZE = 8192

MAX_NUM_TRIES = 3

# Used internally to 'fix' bug in PyFTDI where sometimes after a command we get a NULL read response
#def __read_clear(ftdi_dev: object) -> None:
#    num_tries = 0
#    while(num_tries < MAX_NUM_TRIES):
#        try:
#            ftdi_dev.purge_buffers()
#            ftdi_dev.read_data(1)
#            break
#        except:
#            num_tries = num_tries + 1

class Mld:
    def __init__(self):
       self.context = 0
       self.socket = 0
       self.name = 0

def init(dev_name: str) -> object:
   """Initialize MLD device and returns a handle to it

    Args:
        dev_name (str): Name of MLD device, typically the serial number

    Returns:
        MLD Device object

   """

   print("initializing " + dev_name)
   mld_dev = Mld()
   print("created MLD object")
   mld_dev.name = dev_name
   print("set name")
   mld_dev.context = zmq.Context()
   print("created context")
   mld_dev.socket = mld_dev.context.socket(zmq.REQ)
   print("created socket")
   url = "tcp://" + dev_name + ":5556"
   print("created URL: " + url)
   mld_dev.socket.connect(url)
   print("connected to socket")
   print("init ok")
   return mld_dev

##    url = "ftdi://ftdi:2232:" + dev_name + "/1"
##    
##    ftdi_dev = Ftdi()
##    ftdi_dev.open_mpsse_from_url(url, latency=latency)
##    ftdi_dev.set_bitmode(0, Ftdi.BitMode.SYNCFF)
##    
##        # Two calls (of any type) are necessary on startup
##        # In theory, if we could know ahead of time if we've
##        # sent USB messages to the board (thus turning on the clock
##        # and fixing alignment), we could skip these calls.
##    
##        # Note: Both calls *fail* if this is the first time
##        # init has been called since board power-up
##    
##        # The first call turns on the clock on the FTDI
##        val = read_status(ftdi_dev, 0)
##        if(val == None):
##            # Second call fixes the data alignment
##            read_status(ftdi_dev, 0)
##    
##        return ftdi_dev

def list_devices() -> list[str]:
    """Get a list of available MLD1200 devices connected to host

    Args: None

    Returns:
        List containing serial number of each device found that matched the MLD1200 VID and PID

        Example: `[FT2S5LOX, FT2S5QOA]`

    """
    ret = []
    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            #res = 0
            #res = mld_discover()
            #for r in res:
                #ret.append(r[0].sn)
            ret.append("142.103.52.17")
            break
        except:
            num_tries = num_tries + 1

    return ret

def read_status(mld_dev: object, address: int) -> int:
    """Low-level function to read from status register

    Args:
        mld_dev (object): MLD Device
        address (int): Status register address

    Returns:
        Value contained in status register at given address

    """
    #__read_clear(mld_dev)
    payload = struct.pack("<I", (CMD_READ_STATUS << 24) | (address & 0xFF))
    print("haicu_read_register %d %d %d" % (address, 0, CMD_READ_STATUS) )
    #payload = "READ %d" % (address)
    num_tries = 0
    val = None
    while(num_tries < MAX_NUM_TRIES):
        try:
            #mld_dev.write_data(payload)
            #response = mld_dev.read_data(4)
            mld_dev.socket.send(payload)
            
            message = mld_dev.socket.recv()
            print("Rcvd reply [ %s ]" % message)

            if(len(message) == 8):
                cmd,val = struct.unpack("<II", message)
                break

            num_tries = num_tries + 1
        except:
            num_tries = num_tries + 1
            #print("num_tries", num_tries)
            
    if num_tries >= MAX_NUM_TRIES:
        try:
            # Set LINGER to 0 before closing to prevent hanging
            mld_dev.socket.setsockopt(zmq.LINGER, 0)
            mld_dev.socket.close()
            # Don't terminate the context as it might hang
            print(f"Could not receive message from {mld_dev.name}: closed socket")
        except:
            print(f"Error closing socket for {mld_dev.name}")          

    return val

def read_register(mld_dev: object, address: int) -> int:
    #__read_clear(mld_dev)
    payload = struct.pack("<I", (CMD_READ_REG << 24) | (address & 0xFF))
    print("haicu_read_register %d %d %d" % (address, 0, CMD_READ_REG) )
    num_tries = 0
    val = None
    while(num_tries < MAX_NUM_TRIES):
       #mld_dev.write_data(payload)
       #response = mld_dev.read_data(4)
       mld_dev.socket.send(payload)
       message = mld_dev.socket.recv()
       print("Rcvd reply %d bytes[ %s ] " % (len(message), message) )
       if(len(message) == 8):
          cmd,val = struct.unpack("<II", message)
          break
       num_tries = num_tries + 1
    return val

def write_register(mld_dev: object, address: int, data: int) -> None:
    payload = struct.pack("<II", (CMD_WRITE_REG << 24) | (address & 0xFF), data)
    print("haicu_write_register Reg%d = %d" % (address, data) )
    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            #ftdi_dev.write_data(payload)
            
            mld_dev.socket.send(payload)
            
            # original write did not include any readback
            # but zmq always replies - so take reply
            message = mld_dev.socket.recv()
            print("Rcvd reply %d bytes[ %s ] " % (len(message), message) )
            break
        except:
            num_tries = num_tries + 1

def read_memory(mld_dev: object, address: int, num_words: int) -> list[int]:
    """Low-level function to read from DDR memory

    Args:
        mld_dev (object): MLD Device
        address (int): Address to start reading from (32-bit word accesses)
        num_words (int): Number of 32-bit words to read

    Returns:
        List of 32-bit words read from memory, starting from address given. Empty list returned on error

    """
    #__read_clear(mld_dev)
    ret = []
    if(num_words == 0):
        num_words = 1
        
    num_bytes = (num_words) * 4
    payload = struct.pack("<II", (CMD_READ_MEM << 24) | (address & 0xFFFFFF), num_words)

    num_tries = 0
    while(num_tries < MAX_NUM_TRIES):
        try:
            mld_dev.socket.send(payload)
            message = mld_dev.socket.recv()
            print("Rcvd reply %d bytes[ %s ] " % (len(message), message) )
            print("Require %d bytes\n" % num_bytes)
            if(len(message) == num_bytes):
                for i in range(0, num_bytes, 4):
                    val, = struct.unpack_from("<I", message, i)
                    ret.append(val)
                break
            num_tries = num_tries + 1
        except:
            num_tries = num_tries + 1

    if(num_tries == MAX_NUM_TRIES):
        return []

    return ret

def write_memory(mld_dev: object, address: int, data: Union[int, list[int]]) -> None:
    """Low-level function to write to DDR memory

    Args:
        mld_dev (object): MLD Device
        address (int): Address to start writing to (32-bit word accesses)
        data (int/list): Either an integer value, or a list of integers to write

    """
    if(type(data) is int):
        data = [data]
    else:
        if(type(data[0]) is not int):
            return

    print("Original Data Length %d\n" % len(data))
    tlen = len(data)
    #tlen = len(data) // 4
    #print("Data Length %d\n" % tlen)
    payload = struct.pack("<II", (CMD_WRITE_MEM << 24) | (address & 0xFFFFFF), tlen)
    for n in range(0, tlen):
       payload = payload + struct.pack("<I", data[n])
          
    mld_dev.socket.send(payload)
    message = mld_dev.socket.recv()
    print("Rcvd reply %d bytes[ %s ] " % (len(message), message) )
    print("Write Mem Done\n")

def gather_status_registers(mld_dev: object) -> dict[Union[int, bool, str, float]]:
    """Gather values from all status registers and place them in a dictionary

    Args:
        mld_dev (object): MLD Device

    """
    resp = {}

    try:
        val = read_status(mld_dev, 0)
        resp['program_load'] = bool(val & 0x80000000)
        resp['program_active'] = bool(val & 0x40000000)
        resp['program_armed'] = bool(val & 0x20000000)
        resp['program_ddr_load'] = bool(val & 0x10000000)
        resp['program_ddr_lock'] = bool(val & 0x08000000)
        resp['program_done'] = bool(val & 0x040000000)
        resp['program_error'] = bool(val & 0x02000000)
        resp['fp_status'] = int(val & 0xFF)

        val = read_status(mld_dev, 5)
        resp['program_run_count'] = val
        val = read_status(mld_dev, 6)
        resp['program_error_count'] = val
        val = read_status(mld_dev, 1)
        resp['trigger_active'] = bool(val & 0x80000000)
        resp['trigger_counter'] = val & 0x7FFFFFFF
        val = read_status(mld_dev, 3)
        resp['external_clock_freq'] = val
        val = read_status(mld_dev, 4)
        resp['external_clock_active'] = bool(val & 0x80000000)
        resp['external_clock_counter'] = val & 0x7FFFFFFF
        val = read_status(mld_dev, 2)
        resp['buildtime'] = str(datetime.fromtimestamp(val))

        val = read_status(mld_dev, 7)
        resp['program_run_timer'] = int(val)

        val = read_status(mld_dev, 8)
        resp['uptime'] = int(val)
    except:
        return {}

    return resp

def gather_control_registers(mld_dev: object) -> dict[Union[int, bool, str, float]]:
    """Gather values from all control registers and place them in a dictionary

    Args:
        mld_dev (object): MLD Device

    """

    resp = {}
    try:
        val = read_register(mld_dev, 0)
        resp['program_load'] = bool(val & 0x00000001)

        val = read_register(mld_dev, 1)
        resp['program_numwords'] = val

        val = read_register(mld_dev, 2)
        resp['trigger_invert'] = bool(val & 0x40000000)
        resp['trigger_delay'] = int(val & 0x000000FF)

        val = read_register(mld_dev, 3)
        resp['enable_tunebox1'] = (val & 0x000000FF)
        resp['enable_tunebox2'] = (val & 0x0000FF00) >> 8
        resp['enable_tunebox3'] = (val & 0x00FF0000) >> 16
        resp['enable_tunebox4'] = (val & 0xFF000000) >> 24

        val = read_register(mld_dev, 4)
        resp['enable_tunebox5'] = (val & 0x000000FF)
        resp['enable_tunebox6'] = (val & 0x0000FF00) >> 8
        resp['enable_tunebox7'] = (val & 0x00FF0000) >> 16
        resp['enable_tunebox8'] = (val & 0xFF000000) >> 24

        val = read_register(mld_dev, 5)
        resp['enable_left_address']  = (val & 0x00000FFF)
        resp['enable_right_address'] = (val & 0x0FFF0000) >> 16
        resp['enable_frontpanel'] = ((val & 0xF0000000) >> 24) | ((val & 0x0000F000) >> 12)

        val = read_register(mld_dev, 6)
        resp['invert_tunebox1'] = (val & 0x000000FF)
        resp['invert_tunebox2'] = (val & 0x0000FF00) >> 8
        resp['invert_tunebox3'] = (val & 0x00FF0000) >> 16
        resp['invert_tunebox4'] = (val & 0xFF000000) >> 24

        val = read_register(mld_dev, 7)
        resp['invert_tunebox5'] = (val & 0x000000FF)
        resp['invert_tunebox6'] = (val & 0x0000FF00) >> 8
        resp['invert_tunebox7'] = (val & 0x00FF0000) >> 16
        resp['invert_tunebox8'] = (val & 0xFF000000) >> 24

        val = read_register(mld_dev, 8)
        resp['invert_left_address']  = (val & 0x00000FFF)
        resp['invert_right_address'] = (val & 0x0FFF0000) >> 16
        resp['invert_frontpanel'] = ((val & 0xF0000000) >> 24) | ((val & 0x0000F000) >> 12)
    except:
        return {}

    return resp

def write_control_registers(mld_dev: object, values: dict[str, int]) -> None:
    """Write an dictionary of values to control registers

    Example: write_control_registers(dev, {'trigger_invert': 1, 'trigger_delay': 3})

    Args:
        mld_dev (object): MLD Device
        values (dict): A dictionary of values to write, using the key/pair

    """

    # DO NOT WRITE TO PROGRAM LOAD
    # write_register(mld_dev, 0, int(values['program_load']))

    # DO NOT WRITE TO PROGRAM NUMWORDS!!
    # write_register(mld_dev, 1, values['program_numwords'])
    value = 0
    if 'trigger_invert' in values.keys():
        value = value | ((int(values['trigger_invert'], 0) & 0x1) << 30)
    if 'trigger_delay' in values.keys():
        value = value | (int(values['trigger_delay'], 0) & 0xFF)
    if 'trigger_invert' in values.keys() or 'trigger_delay' in values.keys():
        write_register(mld_dev, 2, value)

    value = 0
    if 'enable_tunebox1' in values.keys():
        value = value | (int(values['enable_tunebox1'], 0) & 0xFF)
    if 'enable_tunebox2' in values.keys():
        value = value | ((int(values['enable_tunebox2'], 0) & 0xFF) << 8)
    if 'enable_tunebox3' in values.keys():
        value = value | ((int(values['enable_tunebox3'], 0) & 0xFF) << 16)
    if 'enable_tunebox4' in values.keys():
        value = value | ((int(values['enable_tunebox4'], 0) & 0xFF) << 24)
    if 'enable_tunebox1' in values.keys() or 'enable_tunebox2' in values.keys() or 'enable_tunebox3' in values.keys() or 'enable_tunebox4' in values.keys():
        write_register(mld_dev, 3, value)

    value = 0
    if 'enable_tunebox5' in values.keys():
        value = value | (int(values['enable_tunebox5'], 0) & 0xFF)
    if 'enable_tunebox6' in values.keys():
        value = value | ((int(values['enable_tunebox6'], 0) & 0xFF) << 8)
    if 'enable_tunebox7' in values.keys():
        value = value | ((int(values['enable_tunebox7'], 0) & 0xFF) << 16)
    if 'enable_tunebox8' in values.keys():
        value = value | ((int(values['enable_tunebox8'], 0) & 0xFF) << 24)
    if 'enable_tunebox5' in values.keys() or 'enable_tunebox6' in values.keys() or 'enable_tunebox7' in values.keys() or 'enable_tunebox8' in values.keys():
        write_register(mld_dev, 4, value)

    value = 0
    if 'enable_left_address' in values.keys():
        value = value | (int(values['enable_left_address'], 0) & 0x00000FFF)
    if 'enable_right_address' in values.keys():
        value = value | ((int(values['enable_right_address'], 0) & 0x00000FFF) << 16)
    if 'enable_frontpanel' in values.keys():
        value = value |  ((int(values['enable_frontpanel'], 0) & 0x0000000F) << 12) | ((int(values['enable_frontpanel'], 0) & 0x000000F0) << 24)
    if 'enable_left_address' in values.keys() or 'enable_right_address' in values.keys() or 'enable_frontpanel' in values.keys():
        write_register(mld_dev, 5, value)

    value = 0
    if 'invert_tunebox1' in values.keys():
        value = value | (int(values['invert_tunebox1'], 0) & 0xFF)
    if 'invert_tunebox2' in values.keys():
        value = value | ((int(values['invert_tunebox2'], 0) & 0xFF) << 8)
    if 'invert_tunebox3' in values.keys():
        value = value | ((int(values['invert_tunebox3'], 0) & 0xFF) << 16)
    if 'invert_tunebox4' in values.keys():
        value = value | ((int(values['invert_tunebox4'], 0) & 0xFF) << 24)
    if 'invert_tunebox1' in values.keys() or 'invert_tunebox2' in values.keys() or 'invert_tunebox3' in values.keys() or 'invert_tunebox4' in values.keys():
        write_register(mld_dev, 6, value)

    value = 0
    if 'invert_tunebox5' in values.keys():
        value = value | (int(values['invert_tunebox5'], 0) & 0xFF)
    if 'invert_tunebox6' in values.keys():
        value = value | ((int(values['invert_tunebox6'], 0) & 0xFF) << 8)
    if 'invert_tunebox7' in values.keys():
        value = value | ((int(values['invert_tunebox7'], 0) & 0xFF) << 16)
    if 'invert_tunebox8' in values.keys():
        value = value | ((int(values['invert_tunebox8'], 0) & 0xFF) << 24)
    if 'invert_tunebox5' in values.keys() or 'invert_tunebox6' in values.keys() or 'invert_tunebox7' in values.keys() or 'invert_tunebox8' in values.keys():
        write_register(mld_dev, 7, value)

    value = 0
    if 'invert_left_address' in values.keys():
        value = value | (int(values['invert_left_address'], 0) & 0x00000FFF)
    if 'invert_right_address' in values.keys():
        value = value | ((int(values['invert_right_address'], 0) & 0x00000FFF) << 16)
    if 'invert_frontpanel' in values.keys():
        value = value |  ((int(values['invert_frontpanel'], 0) & 0x0000000F) << 12) | ((int(values['invert_frontpanel'], 0) & 0x000000F0) << 24)
    if 'invert_left_address' in values.keys() or 'invert_right_address' in values.keys() or 'invert_frontpanel' in values.keys():
        write_register(mld_dev, 8, value)

