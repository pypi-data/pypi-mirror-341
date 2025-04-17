import poecoh_instek as instek

devices = instek.find()
if len(devices) == 0:
    exit

ps: instek.GPD3303 = devices[0]
print(ps.firmware, ps.model, ps.manufacturer, ps.serial)
ps.output = False

ind = ps.independent()
ind.ch1.voltage = 30
ind.ch1.current = 3
ind.output = True

ser = ps.series()
ser.voltage = 60
ser.current = 3
ser.output = True

# shared common
ser_com = ps.series_common()
ser_com.voltage = 60
ser_com.ch1.current = 3
ser_com.ch2.current = 3

par = ps.parallel()
par.voltage = 3
par.current = 6
par.output = True