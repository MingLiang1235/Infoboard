#!/usr/bin/python3
# -*- coding:utf-8 -*-
#=====================================================================
#   FileName:  clientMeter.py 
#   Purpose:  Meter Instrument supply Client's PC status of Windows
#   Version:  0.0.1
#   Author:  Jishan                  
#   Email:  unicoder@sohu.com
#   Date:  2024-12-01 23:50  Modify-Date:  2024-12-01 23:50
#   Lib:  pythonnet , notice not clr. If you already install clr, uninstall it.
#   Note:  Windows 10 , and Python 3.12 test pass. Do not use Python 3.6 or lower.
#=====================================================================

import helper
# from helper import genValue, getHostFromConfig, getConnectString, DataType
import clr
from time import sleep

clr.AddReference(r'OpenHardwareMonitorLib')

from OpenHardwareMonitor.Hardware import Computer
from OpenHardwareMonitor import Hardware
c = Computer()
c.CPUEnabled = True
c.GPUEnabled = True
c.Open()

def invoke_meter():
	Str = ''
	for s in range(0, len(c.Hardware[0].Sensors)):
			if "/temperature" in str(c.Hardware[0].Sensors[s].Identifier):
				print(c.Hardware[0].Sensors[s].get_Value())
				Str += str(c.Hardware[0].Sensors[s].get_Value()) + '|'
				c.Hardware[0].Update()
	for h in c.Hardware:
		hard_type = str(h.HardwareType)
		if 'GPU' in hard_type.upper():
			h.Update()
			for sensor in h.Sensors:
				if sensor.SensorType == Hardware.SensorType.Temperature:
					Str += str(sensor.Value) + '|'
	return Str  # '39|36|30|52|'
if __name__ == '__main__':
	while True:
		invoke_meter()
		sleep(5)

	# 3 value shown:  Cpu Core #1, Cpu Core #2, Cpu Package.