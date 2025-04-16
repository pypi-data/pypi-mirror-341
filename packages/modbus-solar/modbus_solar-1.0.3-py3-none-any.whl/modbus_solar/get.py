# main.py

import minimalmodbus
from datetime import datetime, UTC

def get_all( modbus_device: str = "/dev/ttyUSB0", modbus_slave_address: int = 1):
	instrument = minimalmodbus.Instrument(modbus_device, modbus_slave_address)  # port name, slave address (in decimal)
	instrument.serial.baudrate = 9600
	instrument.serial.bytesize = 8
	instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
	instrument.serial.stopbits = 2
	instrument.serial.timeout  = 1
	instrument.address = modbus_slave_address # this is the slave address number
	instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
	instrument.clear_buffers_before_each_transaction = True

	# # Temperature
	# # The actual value has to be split, the highest bit of each is the +/- sign
	temp = instrument.read_register(0x103)
	if (temp & 0x8000) > 0 : # This is the positive/negative bit for the Controller Temperature
		tempControllerSign = "-"
	else: tempControllerSign = ""
	if (temp & 0x80) > 0 : # This is the positive/negative bit for the Aux Battery Temperature
		tempAuxBattSign = "-"
	else: tempAuxBattSign = ""
	tempController = "{}{}".format(tempControllerSign, int(format(temp & 0x7F00, '016b')[:8], 2)) # Strips the high byte to show Controller Temperature
	tempAuxBatt = "{}{}".format(tempAuxBattSign, (temp & 0x7F)) # Low byte shows Aux Battery Temperature

	# # Charge State
	# # If the bit is "1" then the value is True, comment is from the Renogy Docs
	chargeState = instrument.read_register(0x120)
	chargingNone = (chargeState & 0x1) > 0 # 00H:no charging activated
	chargingSolar = (chargeState & 0x4) > 0 # 02H:mppt charging mode  (solar)
	chargingEqualization = (chargeState & 0x8) > 0 # 03H:Equallization charging stage  (solar/alternator)
	chargingBoost = (chargeState & 0x10) > 0 # 04H:Boost charging stage  (solar/alternator)
	chargingFloat = (chargeState & 0x20) > 0 # 05H:Float charging stage  (solar/alternator)
	chargingLimited = (chargeState & 0x40) > 0 # 06H:current-limited charging stage  (solar/alternator)
	chargingAlt = (chargeState & 0x80) > 0 # 08H:direct charging mode (alternator)

	# # Error Codes
	# # If the bit is "1" then the string is added to the array, comment is from the Renogy Docs
	errors = []
	errorCodesLow = instrument.read_register(0x121)
	if (errorCodesLow & 0x10) > 0 : errors.append("CtrlOverTemp2") # b4:controller inside over temperature 2
	if (errorCodesLow & 0x20) > 0 : errors.append("AltInputOverCurrent") # b5:alternator input overcurrent
	if (errorCodesLow & 0x100) > 0 : errors.append("AltInputOverVoltProtection") # b8：alternator input over voltage protection
	if (errorCodesLow & 0x200) > 0 : errors.append("StarterBatteryReversePolarity") # b9：starter battery reverse polarity
	if (errorCodesLow & 0x400) > 0 : errors.append("BmsOverChargeProtection") # b10：BMS over charge protection
	if (errorCodesLow & 0x800) > 0 : errors.append("AuxLowTempProtection") # b11：auxilliary battery stopped taking charges because of low temperature (lithium battery:0°C, lead acid:-35°C)

	errorCodesHigh = instrument.read_register(0x122)
	if (errorCodesHigh & 0x1) > 0 : errors.append("AuxBatteryOverDischarge") # B0:auxilliary battery over-discharged
	if (errorCodesHigh & 0x2) > 0 : errors.append("AuxBatteryOverVolt") # b1:auxilliary battery over voltage
	if (errorCodesHigh & 0x4) > 0 : errors.append("AuxBatteryUnderVolt") # B2:auxilliary battery under voltage warning
	if (errorCodesHigh & 0x20) > 0 : errors.append("ControllerOverTemp") # B5:controller inside temperature too high
	if (errorCodesHigh & 0x40) > 0 : errors.append("AuxBatteryOverTemp") # B6:auxilliary battery over temperature
	if (errorCodesHigh & 0x80) > 0 : errors.append("SolarInputTooHigh") # B7:solar input too high
	if (errorCodesHigh & 0x200) > 0 : errors.append("SolarInputOverVolt") # B9:solar input over voltage
	if (errorCodesHigh & 0x1000) > 0 : errors.append("SolarReversePolarity") # B12:solar, reversed poliarity

	payload = {
		"device": instrument.read_string(0xc,8),
		"auxSoc": instrument.read_register(0x100), # Auxilliary battery State of charge
		"auxVoltage": instrument.read_register(0x101,1),
		"maxCharge": instrument.read_register(0x102,2), # combined charging current from solar+alternator to the auxilliary battery
		"controllerTemp": int(tempController),
		"auxTemp": int(tempAuxBatt),
		"altVoltage": instrument.read_register(0x104,1),
		"altAmps": instrument.read_register(0x105,2),
		"altWatts": instrument.read_register(0x106),
		"solVoltage": instrument.read_register(0x107,1),
		"solAmps": instrument.read_register(0x108,2),
		"solWatts": instrument.read_register(0x109),
		"lowDailyVolts": instrument.read_register(0x10b)/10, # values returned need to be divided by 10 to transpose to Volts
		"highDailyVolts": instrument.read_register(0x10c)/10, # values returned need to be divided by 10 to transpose to Volts
		"highDailyCurrent": instrument.read_register(0x10d), # solar+alternator
		"highDailyPower": instrument.read_register(0x10f), # solar+alternator
		"highAccumAh": instrument.read_register(0x111), # solar+alternator
		"dailyGeneratedPower": instrument.read_register(0x113), # solar+alternator
		"totalWorkingDays": instrument.read_register(0x115),
		"totalOverdischargedBattery": instrument.read_register(0x116),
		"totalChargedBattery": instrument.read_register(0x117),
		"timestamp": str(datetime.now(UTC)),
		"chargingNone": str(chargingNone),
		"chargingSolar": str(chargingSolar),
		"chargingEqualization": str(chargingEqualization),
		"chargingBoost": str(chargingBoost),
		"chargingFloat": str(chargingFloat),
		"chargingLimited": str(chargingLimited),
		"chargingAlt": str(chargingAlt),
		"errors": errors
	}

	try:
		return payload
	except Exception as e:
		return e
