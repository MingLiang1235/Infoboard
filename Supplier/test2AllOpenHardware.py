#!/usr/bin/python3
# -*- coding:utf-8 -*-
#=====================================================================
#   FileName:  test2AllOpenHardware.py 
#   Purpose:  Test 2 all of openHardwareMonitorlib.dll.
#   Version:  0.1
#   Author:  Jishan                  
#   Email:  unicoder_admin@163.com
#   Date:  2024-12-24 9:36  Modify-Date:  2024-12-24 9:36
#=====================================================================
"""TODO: """
import os
import clr
home_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(home_dir, 'openHardwareMonitorlib.dll')

clr.AddReference(dll_path)  # 一定要有这一个，否则大概率报错

from OpenHardwareMonitor import Hardware
computer = Hardware.Computer()
computer.CPUEnabled = True;
computer.FanControllerEnabled = True;
computer.FansEnabled = True;
computer.GPUEnabled = True;
computer.HDDEnabled = True;
computer.MainboardEnabled = True;
computer.RAMEnabled = True;
computer.Open()

for hard in computer.Hardware:
	print("hard.HardwareType:", hard.HardwareType)
	for subhard in hard.SubHardware:
		print("subhard.HardwareType:", subhard.HardwareType)
		subhard.Update()
		for sensor in hard.Sensors:
			print(sensor.Name, '|', sensor.SensorType, ':', sensor.Value)

computer.Close()