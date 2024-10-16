#imports
import pyvisa
import time
import math
import dl3000 as rdl
import sys
import util
import os

RIGOL_DL3021_ID = 'USB0::6833::3601::DL3A251700335::0::INSTR'
SAMPLE_PERIOD = 1 # second

def main():
    #pyvisa rigol setup
    print("connecting to RIGOL_DL3021")
    rm = pyvisa.ResourceManager()
    dl = rdl.dl3021(rm.open_resource(RIGOL_DL3021_ID))
    time.sleep(0.5)
    dl.set_function(3)
    dl.set_function_power(90)
    dl.set_enable()
    filename = os.getcwd() + os.sep + "logs" + os.sep + "18650_logger_"
    log = util.logger(name=filename)
    t_0 = time.monotonic()
    v_cutoff = 14.0
    v_now = 20
    t_elapsed = 0

    while v_now > v_cutoff:
        t_1 = time.monotonic()
        try:
            t_elapsed = t_1-t_0
            v_now = dl.query_voltage()
            print(f'run time: {t_elapsed:.2f} - voltage: {v_now:.2f} V')
            log.log_data([round(t_elapsed,2), v_now, dl.query_current(), dl.query_power()])
            t_delta = time.monotonic()-t_1
            if t_delta >= SAMPLE_PERIOD:
                continue # if the iteration ran long, continue onto the next
            time.sleep(SAMPLE_PERIOD-t_delta)
        except KeyboardInterrupt:
            print("execution interupted, disabling dl3021...")
            dl.set_disable()
            break
    print(f'voltage cuff-off: {v_cutoff} V reached')
    dl.set_disable()

"""
what this code should do
1) Connect a raspberry pi to a rigol digital load (using PyVisa)
2) Set the data collection mode of the DL
    a) constant power
    b) constant current
    c) list power
3) Set the relevant parameters for the data collection mode
4) Run a testing session
    a) Log data to csv during the session
    b) Run for preset duration or until battery dies
    c) Recharge the battery
5) Safely stop after completing the session
6) Upload data to known location

In order to do this
1) make a class wrapper that works with dl3000
2) make a data logging class
3) maybe make a battery class?
"""
if __name__ == "__main__":
    main()
