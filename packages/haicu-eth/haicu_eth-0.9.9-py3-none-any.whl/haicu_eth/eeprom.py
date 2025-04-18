from pyftdi import eeprom

serial_num = "FT2S6LOX"
default_ini = "eeprom/default_eeprom.ini"

def write_eeprom(default_ini: str, serial: str):
    ftdi_eeprom = eeprom.FtdiEeprom()
    ftdi_eeprom.open('ftdi://ftdi:2232h/1')
    with open(default_ini, "rt") as f:
        ftdi_eeprom.load_config(f, 'all')
        ftdi_eeprom.set_serial_number(serial_num)
        ftdi_eeprom.commit(False)
        # eeprom.save_config(f)

if __name__ == "__main__":
    write_eeprom(default_ini, serial_num)
