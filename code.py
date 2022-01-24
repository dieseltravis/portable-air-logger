# SPDX-FileCopyrightText: 2021 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# modified by Travis Hardiman, 2022

import time
import board
import digitalio
import adafruit_scd4x
import adafruit_sgp40
import adafruit_sdcard
import busio
import storage
import adafruit_pcf8523

#  setup for I2C
i2c = board.I2C()
#  setup for SCD40
scd4x = adafruit_scd4x.SCD4X(i2c)
#  setup for SGP40
sgp = adafruit_sgp40.SGP40(i2c)
#  setup for RTC
rtc = adafruit_pcf8523.PCF8523(i2c)
#  start measuring co2 with SCD40
scd4x.start_periodic_measurement()

#  list of days to print to the text file on boot
days = (
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday")

# SPI SD_CS pin
SD_CS = board.D10

#  SPI setup for SD card
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sd")
    print("sd card mounted")
except ValueError:
    print("no SD card")

#  to update the RTC, change set_clock to True
#  otherwise RTC will remain set
#  it should only be needed after the initial set
#  if you've removed the coincell battery
set_clock = False

if set_clock:
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022,   1,   22,   14,  27,  00,    0,   -1,    -1))

    print("Setting time to:", t)
    rtc.datetime = t
    print()

#  variable to hold RTC datetime
t = rtc.datetime
print('Current date: {} {}-{}-{}'.format(
    days[t.tm_wday],
    t.tm_year,
    '%0*d' % (2, t.tm_mon),
    '%0*d' % (2, t.tm_mday)
    ))
print('Current time: {}:{}:{}'.format(
    '%0*d' % (2, t.tm_hour),
    '%0*d' % (2, t.tm_min),
    '%0*d' % (2, t.tm_sec)
    ))

time.sleep(10)

#  check air levels
if scd4x.data_ready:
    print('CO2 ppm: ', scd4x.CO2)
    temperature = scd4x.temperature
    print('Temperature C: ', temperature)
    humidity = scd4x.relative_humidity
    print('Humidity %: ', humidity)
    print('Raw Gas: ', sgp.raw)
    measured = sgp.measure_raw(temperature=temperature, relative_humidity=humidity)
    print('Adjusted Gas: ', measured)
    print()

#  initial write to the SD card on startup
try:
    with open("/sd/air.txt", "a") as f:
        #  writes the date
        f.write('The date is {} {}-{}-{}\n'.format(
            days[t.tm_wday],
            t.tm_year,
            '%0*d' % (2, t.tm_mon),
            '%0*d' % (2, t.tm_mday)
            ))
        #  writes the start time
        f.write('Start time: {}:{}:{}\n'.format(
            '%0*d' % (2, t.tm_hour),
            '%0*d' % (2, t.tm_min),
            '%0*d' % (2, t.tm_sec)
            ))
        #  headers for data, comma-delimited
        f.write('CO2,TemperatureC,Humidity,Raw,Measured,Date,Time\n')
        #  debug statement for REPL
        print("initial write to SD card complete, starting to log")
except ValueError:
    print("initial write to SD card failed - check card")

while True:
    try:
        #  variable for RTC datetime
        t = rtc.datetime
        #  append SD card text file
        with open("/sd/air.txt", "a") as f:
            #  read co2 data from SCD40
            co2 = scd4x.CO2
            temperature = scd4x.temperature
            humidity = scd4x.relative_humidity
            gas = sgp.raw
            measured = sgp.measure_raw(temperature=temperature, relative_humidity=humidity)
            #  write co2 data followed by the time, comma-delimited
            f.write('{},{},{},{},{},{}-{}-{},{}:{}:{}\n'.format(
                co2,
                temperature,
                humidity,
                gas,
                measured,
                t.tm_year,
                '%0*d' % (2, t.tm_mon),
                '%0*d' % (2, t.tm_mday),
                '%0*d' % (2, t.tm_hour),
                '%0*d' % (2, t.tm_min),
                '%0*d' % (2, t.tm_sec)
                ))
            print("data written to sd card")
        #  repeat every 60 seconds
        time.sleep(60)
    except ValueError:
        print("data error - cannot write to SD card")
        time.sleep(10)