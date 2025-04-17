import poecoh_instek as instek

devices = instek.find()
if len(devices) == 0:
    print("No devices found")
    exit()
ps: instek.GPD3303 = devices[0]
ps._comm.debug = True
ps.baud(9600)
ind = ps.independent()
ind.ch1.voltage = 1
ind.ch2.voltage = 2
ind.ch1.current = 1
ind.ch2.current = 2
ind.ch1.voltage
ind.ch1.current
ind.ch1.cc
ind.ch2.voltage
ind.ch2.current
ind.ch2.cc

ps.baud(57600)
ser = ps.series()
ser.voltage = 60
ser.current = 3
ser.voltage
ser.current
ser.cc

ps.baud(115200)
par = ps.parallel()
par.voltage = 30
par.current = 6
par.voltage
par.current
par.cc
