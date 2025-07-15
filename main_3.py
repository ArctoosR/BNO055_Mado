# import machine
# import time
# from bno055 import BNO055
#
# # راه‌اندازی I2C و تأخیر برای آماده‌سازی سنسور
# i2c = machine.I2C(1, scl=machine.Pin(21), sda=machine.Pin(23))
# time.sleep(2)
#
# imu = BNO055(i2c)
#
# # حلقه خواندن داده‌ها و وضعیت کالیبراسیون
# while True:
#     sys_cal, gyro_cal, accel_cal, mag_cal = imu.cal_status()
#     print("✅ وضعیت کالیبراسیون:")
#     print(f"  System: {sys_cal}, Gyro: {gyro_cal}, Accel: {accel_cal}, Mag: {mag_cal}")
#
#     if imu.calibrated():
#         print("✅ سنسور کاملاً کالیبره شده، داده‌ها واقعی هستن!")
#     else:
#         print("❌ کالیبراسیون کامل نیست، حرکت بده تا آماده بشه...")
#
#     print(f"🌡️ دما: {imu.temperature()}°C")
#     heading, roll, pitch = imu.euler()
#     print(f"🧭 Heading: {heading}, Roll: {roll}, Pitch: {pitch}")
#     print("-" * 40)
#
#     time.sleep(2)


########################################################################################
# import machine
# import time
# from bno055 import BNO055
# from bno055 import NDOF_MODE
#
#
# i2c = machine.I2C(1, scl=machine.Pin(21), sda=machine.Pin(23))
# time.sleep(1)  # زمان راه‌اندازی سنسور
# imu = BNO055(i2c)
#
# imu.mode(NDOF_MODE)
#
# print("Mode:", imu.mode())
# print("Temp:", imu.temperature())
# print("Euler:", imu.euler())
#
# # حلقه بررسی کالیبراسیون
# while True:
#     sys, gyro, accel, mag = imu.cal_status()
#
#     print("🔍 وضعیت کالیبراسیون:")
#     print(f"  سیستم: {sys} | ژیروسکوپ: {gyro} | شتاب‌سنج: {accel} | مغناطیس‌سنج: {mag}")
#
#     # پیشنهاد حرکتی بسته به بخش‌های ناکالیبره
#     if sys < 3:
#         print("📌 کل سنسور نیاز به تنظیم دارد—سنسور را در همه جهت‌ها بچرخان.")
#     elif gyro < 3:
#         print("📌 سنسور را به آرامی بچرخان و بچرخان (مانند محور Z).")
#     elif accel < 3:
#         print("📌 سنسور را روی سطح صاف بگذار و کمی تکان بده.")
#     elif mag < 3:
#         print("📌 سنسور را به شکل دایره‌ای در هوا حرکت بده (مانند قطب‌نما).")
#
#     if imu.calibrated():
#         print("🎉 سنسور BNO055 کاملاً کالیبره شد! حالا داده‌ها دقیق هستن.")
#
#     print("-" * 50)
#     time.sleep(2)

###############################################################
from machine import I2C, Pin
from time import sleep
import ustruct
import utime as time
from micropython import const

# -------------------------------
# کلاس پایه BNO055_BASE
# -------------------------------

_CHIP_ID = const(0xa0)
_CONFIG_MODE = const(0)
_NDOF_MODE = const(0x0c)
_MODE_REGISTER = const(0x3d)
_PAGE_REGISTER = const(0x07)
_TRIGGER_REGISTER = const(0x3f)
_POWER_REGISTER = const(0x3e)
_ID_REGISTER = const(0x00)
_CALIBRATION_REGISTER = const(0x35)

class BNO055_BASE:
    def __init__(self, i2c, address=0x28, crystal=True):
        self._i2c = i2c
        self.address = address
        self.crystal = crystal
        self._mode = _CONFIG_MODE
        chip_id = self._read(_ID_REGISTER)
        if chip_id != _CHIP_ID:
            raise RuntimeError("bad chip id (%x != %x)" % (chip_id, _CHIP_ID))
        self.reset()

    def reset(self):
        self.mode(_CONFIG_MODE)
        try:
            self._write(_TRIGGER_REGISTER, 0x20)
        except OSError:
            pass
        time.sleep_ms(700)
        self._write(_POWER_REGISTER, 0x00)
        self._write(_PAGE_REGISTER, 0x00)
        self._write(_TRIGGER_REGISTER, 0x80 if self.crystal else 0)
        time.sleep_ms(500 if self.crystal else 10)
        self.mode(_NDOF_MODE)

    def _read(self, memaddr, buf=bytearray(1)):
        self._i2c.readfrom_mem_into(self.address, memaddr, buf)
        return buf[0]

    def _write(self, memaddr, data, buf=bytearray(1)):
        buf[0] = data
        self._i2c.writeto_mem(self.address, memaddr, buf)

    def _readn(self, buf, memaddr):
        self._i2c.readfrom_mem_into(self.address, memaddr, buf)
        return buf

    def mode(self, new_mode=None):
        old_mode = self._read(_MODE_REGISTER)
        if new_mode is not None:
            self._write(_MODE_REGISTER, _CONFIG_MODE)
            time.sleep_ms(20)
            if new_mode != _CONFIG_MODE:
                self._write(_MODE_REGISTER, new_mode)
                time.sleep_ms(10)
        self._mode = new_mode
        return old_mode

# -------------------------------
# کلاس توسعه‌یافته BNO055
# -------------------------------

CONFIG_MODE = const(0x00)
EULER_DATA = const(0x1a)

class BNO055(BNO055_BASE):
    def __init__(self, i2c, address=0x28, crystal=True, transpose=(0, 1, 2), sign=(0, 0, 0)):
        super().__init__(i2c, address, crystal)
        self.transpose = transpose
        self.sign = sign
        self.buf6 = bytearray(6)
        self.buf8 = bytearray(8)
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0

    def _bytes_toint(self, lsb, msb):
        if not msb & 0x80:
            return msb << 8 | lsb
        return -(((msb ^ 255) << 8) | (lsb ^ 255) + 1)

    def iget(self, reg):
        if reg == 0x20:
            n = 4
            buf = self.buf8
        else:
            n = 3
            buf = self.buf6
        self._i2c.readfrom_mem_into(self.address, reg, buf)
        if n == 4:
            self.w = self._bytes_toint(buf[0], buf[1])
            i = 2
        else:
            self.w = 0
            i = 0
        self.x = self._bytes_toint(buf[i], buf[i+1])
        self.y = self._bytes_toint(buf[i+2], buf[i+3])
        self.z = self._bytes_toint(buf[i+4], buf[i+5])

# -------------------------------
# اجرای برنامه
# -------------------------------

# راه‌اندازی I2C برای ESP32
i2c = I2C(0, scl=Pin(21), sda=Pin(23))
print(i2c.scan())
# راه‌اندازی سنسور
sensor = BNO055(i2c , crystal=False)




# تنظیم حالت به NDOF
sensor.reset()  # ریست کامل
sensor.mode(_NDOF_MODE)
sleep(0.1)
mode_now = sensor._read(_MODE_REGISTER)
print("Mode register value:", mode_now)






print("Mode:", sensor.mode())



# حلقه خواندن داده‌ها
while True:
    sensor.iget(EULER_DATA)
    yaw = sensor.x / 16
    pitch = sensor.y / 16
    roll = sensor.z / 16
    print("Yaw: {:.2f}, Pitch: {:.2f}, Roll: {:.2f}".format(yaw, pitch, roll))
    sleep(0.5)
