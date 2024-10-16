"""
Class wrapper for dl3021 and pyvisa
"""
import random
import time

class dl3021(object):
    #class varible - to be shared across object instances
    #likely not needed unless we end iup using multiple digital loads

    # query load methods
    def query_voltage(self):
        self.voltage = float(self.inst.query(":MEAS:VOLT?").partition("\n")[0])
        return self.voltage

    def query_current(self):
        self.current = float(self.inst.query(":MEAS:CURR?").partition("\n")[0])
        return self.current

    def query_resistance(self):
        self.resistance = float(self.inst.query(":MEAS:RES?").partition("\n")[0])
        return self.resistance

    def query_power(self):
        self.power = float(self.inst.query(":MEAS:POW?").partition("\n")[0])
        return self.power

    def query_status(self):
        # is it on or off?
        self.status = int(self.inst.query(":SOUR:INP:STAT?").partition("\n")[0])
        return self.status

    def query_function(self):
        # is it in CC, CR, CV or CP
        self.function = self.inst.query(":SOUR:FUNC?").partition("\n")[0]
        return self.function

    def query_function_mode(self):
        # FIX, LST, WAV or BATT
        self.function_mode = self.inst.query(":SOUR:FUNC:MODE?").partition("\n")[0]
        return self.function_mode

    def query_function_current(self):
        self.current_ref = float(self.inst.query(":SOUR:CURR:LEV:IMM?"))
        return self.current_ref

    def query_function_voltage(self):
        self.voltage_ref = float(self.inst.query(":SOUR:VOLT:LEV:IMM?"))
        return self.voltage_ref

    def query_function_power(self):
        self.power_ref = float(self.inst.query(":SOUR:POW:LEV:IMM?"))
        return self.power_ref

#TODO query_function_resistance

    def query_time(self):
        self.t_last = time.monotonic()

    # set load methods
    def set_disable(self):
        self.inst.write(":SOUR:INP:STAT 0")

    def set_enable(self):
        self.inst.write(":SOUR:INP:STAT 1")

    def set_function(self, function):
        """
        Set load function to C0(CC), 1(CV), 2(CR), 3(CP)
        """
        if function == 0:
            self.inst.write(":SOUR:FUNC CURR")
        elif function == 1:
            self.inst.write(":SOUR:FUNC VOLT")
        elif function == 2:
            self.inst.write(":SOUR:FUNC RES")
        elif function == 3:
            self.inst.write(":SOUR:FUNC POW")
        else:
            warning("input must be 0(CC), 1(CV), 2(CR), 3(CP)")

    def set_function_mode(self, mode=0): #TODO FIGURE WHAT THIS IS ALL ABOUT?!
        """
        set load function mode to 0(FIX), 1(LIST), 2(WAV), 3(BATT)
        """
        if mode == 0:
            self.inst.write(":SOUR:FUNC:MODE FIX")
        elif mode == 1:
            self.inst.write(":SOUR:FUNC:MODE LIST")
        elif mode == 2:
            self.inst.write(":SOUR:FUNC:MODE WAV")
        elif mode == 3:
            self.inst.write(":SOUR:FUNC:MODE BATT")
        else:
            warning("input must be 0(FIX), 1(LIST), 2(WAV), 3(BATT)")


    def set_function_power(self, ref_power):
        """
        set reference power (ref_power) for constant power function
        """
        self.inst.write(f':SOUR:POW:LEV:IMM {ref_power}')

#TODO set_function_voltage
#TODO set_function_current
#TODO set_function_resistance

    def set_reset(self):
        self.inst.write("*RST")
        print("dl3021 reset...")

    #default init
    def __init__(self, inst):
        self.inst = inst
        self.voltage = 0.0
        self.current = 0.0
        self.resistance = 0.0
        self.power = 0.0
        self.status = 0
        self.function = "" #TODO update these fields in query & set
        self.function_mode = "" #TODO update these fields in query & set
        self.current_ref = 0.0
        self.voltage_ref = 0.0
        self.power_ref = 0.0
        self.t_ini = time.monotonic() # internal time reference
        self.t_last = self.t_ini
        self.set_reset()


