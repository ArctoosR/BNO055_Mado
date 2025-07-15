
# bno055_test.py Simple test program for MicroPython bno055 driver

# Copyright (c) Peter Hinch 2019
# Released under the MIT licence.

import machine
import time
from bno055 import *
# Tested configurations
# Pyboard hardware I2C
# i2c = machine.I2C(1)

# Pico: hard I2C doesn't work without this patch
# https://github.com/micropython/micropython/issues/8167#issuecomment-1013696765

i2c = machine.I2C(1, scl=machine.Pin(21), sda=machine.Pin(23))  # EIO error almost immediately
print(i2c.scan())


# All platforms: soft I2C requires timeout >= 1000μs
# i2c = machine.SoftI2C(sda=machine.Pin(16), scl=machine.Pin(17), timeout=1_000)
# ESP8266 soft I2C
# i2c = machine.SoftI2C(scl=machine.Pin(2), sda=machine.Pin(0), timeout=100_000)
# ESP32 hard I2C
# i2c = machine.I2C(1, scl=machine.Pin(21), sda=machine.Pin(23))
imu = BNO055(i2c , crystal=False )
time.sleep(0.6)
print("Mode:", imu._read(0x3D))  # انتظار داریم 12 ببینیم


calibrated = False
print('Calibration: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))


Offsets= [215, 255, 253, 255, 239, 255, 95, 0, 251, 255, 180, 0, 255, 255, 255,255, 1, 0, 232, 3, 9, 4]
imu.set_offsets(Offsets)

# Accel X: 65495
# Accel Y: 65533
# Accel Z: 65519
# Mag X: 95
# Mag Y: 65531
# Mag Z: 180
# Gyro X: 65535
# Gyro Y: 65535
# Gyro Z: 65533
# Accel Radius: 1000

# مرحله 1: بررسی کالیبراسیون
print("در حال بررسی کالیبراسیون سنسور...")

while True:

    status = imu.cal_status()
    print("System: {}, Gyro: {}, Accel: {}, Mag: {}".format(*status))
    if imu.calibrated():
        print("✅ سنسور کاملاً کالیبره شد!")
        break
    time.sleep(1)

    # مرحله 2: نمایش offsets کالیبراسیون
    offsets = imu.sensor_offsets()
    print("📦 Offsets کالیبراسیون:")
    labels = [
        "Accel X", "Accel Y", "Accel Z",
        "Mag X", "Mag Y", "Mag Z",
        "Gyro X", "Gyro Y", "Gyro Z",
        "Accel Radius", "Mag Radius"
    ]

    for i in range(0, len(offsets), 2):
        value = offsets[i] | (offsets[i + 1] << 8)
        label = labels[i // 2]
        print(f"{label}: {value}")

    # مرحله 3: ارسال داده‌های موقعیت
    print("\n📡 شروع ارسال داده‌های Yaw, Pitch, Roll...")

while True:



    # status = imu.cal_status()
    # print("System: {}, Gyro: {}, Accel: {}, Mag: {}".format(*status))
    # if imu.calibrated():
    #     print("✅ Sensor fully calibrated!")
    #     offsets = imu.sensor_offsets()
    #     print("Offsets:", list(offsets))
    #     break
    # time.sleep(1)
    #
    # time.sleep(1)
    # if not calibrated:
    #     calibrated = imu.calibrated()
    #    print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    # print('Temperature {}°C'.format(imu.temperature()))
    # print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    # print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    # print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    # print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    # print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    # print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
    #
    # time.sleep(1)
    imu.iget(0x1A)  # EULER_DATA
    yaw = imu.x / 16
    pitch = imu.y / 16
    roll = imu.z / 16
    print("{:.2f},{:.2f},{:.2f}".format(yaw, pitch, roll))



    time.sleep(0.1)
