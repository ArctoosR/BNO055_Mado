# from vpython import box, vector, rate
# import serial
# import math
#
# # اتصال سریال
# ser = serial.Serial('COM4', 115200)
#
# # ساخت جعبه سه‌بعدی
# sensor_box = box(length=2, height=0.5, width=1, color=vector(0, 0.6, 0.8))
#
# def deg_to_rad(deg):
#     return deg * math.pi / 180
#
# while True:
#     rate(50)  # فریم در ثانیه
#     try:
#         line = ser.readline().decode().strip()
#         yaw, pitch, roll = map(float, line.split(","))  # فرض بر اینه که ESP32 این داده‌ها رو می‌فرسته
#
#         # تبدیل به رادیان
#         yaw = 0#deg_to_rad(yaw)
#         pitch =0# deg_to_rad(pitch)
#         roll = 0.7853981625#deg_to_rad(roll)
#
#         # محاسبه جهت‌گیری
#         sensor_box.axis = vector(math.cos(yaw)*math.cos(pitch),
#                                  math.sin(pitch),
#                                  math.sin(yaw)*math.cos(pitch))
#     except Exception as e:
#         print("Error:", e)
###############################################################################
#
# import serial
#
#
# # # اتصال سریال
# ser = serial.Serial('COM4', 115200)
# from vpython import box, vector, rate, scene
# import math
#
# # تنظیم صحنه
# scene.title = "نمایش زاویه‌های Yaw, Pitch, Roll"
# scene.width = 800
# scene.height = 600
# scene.background = vector(0.95, 0.95, 0.95)
#
# # ساخت جعبه
# sensor_box = box(length=2, height=0.5, width=1, color=vector(0.2, 0.6, 0.8))
#
# # تبدیل درجه به رادیان
# def deg_to_rad(deg):
#     return deg * math.pi / 180
#
# # تابع چرخش با زاویه‌های اویلر
# def rotate_box(yaw, pitch, roll):
#     yaw = deg_to_rad(yaw)
#     pitch = deg_to_rad(pitch)
#     roll = deg_to_rad(roll)
#
#     # بردار جهت‌گیری ساده‌شده
#     x = math.cos(yaw) * math.cos(pitch)
#     y = math.sin(pitch)
#     z = math.sin(yaw) * math.cos(pitch)
#     sensor_box.axis = vector(x, y, z)
#
#     # # بردار بالا برای roll
#     # sensor_box.up = vector(
#     #     -math.cos(yaw) * math.sin(roll) * math.sin(pitch) + math.sin(yaw) * math.cos(roll),
#     #     math.cos(pitch) * math.cos(roll),
#     #     -math.sin(yaw) * math.sin(roll) * math.sin(pitch) - math.cos(yaw) * math.cos(roll)
#     # )
#
#     # محاسبه بردار بالا (up) برای Roll
#     # اینجا از ماتریس چرخش استفاده می‌کنیم
#     up_x = math.cos(yaw) * math.sin(roll) * math.sin(pitch) + math.sin(yaw) * math.cos(roll)
#     up_y = math.cos(pitch) * math.cos(roll)
#     up_z = math.sin(yaw) * math.sin(roll) * math.sin(pitch) - math.cos(yaw) * math.cos(roll)
#     sensor_box.up = vector(up_x, up_y, up_z)
# # انیمیشن آهسته برای هر زاویه
# def animate_euler():
#     rotate_box(yaw, pitch , roll)
#     # # Roll
#     # print('1')
#     # for roll in range(0, 91, 1):
#     #     rotate_box(0, 0, roll)
#     #     rate(30)
#     #
#     # # Pitch
#     # print('2')
#     # for pitch in range(0, 91, 1):
#     #     rotate_box(0, pitch, 90)
#     #     rate(30)
#     #
#     # # Yaw
#     # print('3')
#     # for yaw in range(0, 181, 1):
#     #     rotate_box(yaw, 90, 90)
#     #     rate(30)
# print('Start')
# #animate_euler()
#
#
# while True:
#     rate(50)  # فریم در ثانیه
#     try:
#         line = ser.readline().decode().strip()
#         yaw, pitch, roll = map(float, line.split(","))  # فرض بر اینه که ESP32 این داده‌ها رو می‌فرسته
#
#         rotate_box(yaw, pitch , roll)
#
#     except Exception as e:
#         print("Error:", e)
#########################################################################
# from vpython import box, vector, rate, scene
# import math
#
# # تنظیم صحنه
# scene.title = "نمایش چرخش Roll (حول محور طولی)"
# scene.width = 800
# scene.height = 600
# scene.background = vector(0.95, 0.95, 0.95)
#
# # ساخت جعبه
# sensor_box = box(length=2, height=0.5, width=1, color=vector(0.2, 0.6, 0.8))
#
# # تبدیل درجه به رادیان
# def deg_to_rad(deg):
#     return deg * math.pi / 180
#
# # تابع چرخش فقط با Roll
# def rotate_roll(roll_deg):
#     roll = deg_to_rad(roll_deg)
#
#     # محور اصلی ثابت (جعبه به سمت جلو)
#     sensor_box.axis = vector(1, 0, 0)
#
#     # بردار بالا برای Roll
#     sensor_box.up = vector(0, math.cos(roll), math.sin(roll))
#
# # انیمیشن Roll
# def animate_roll():
#     for roll in range(0, 361, 1):  # چرخش کامل 360 درجه
#         rotate_roll(roll)
#         rate(60)
#
# animate_roll()
#########################################################################
import serial
from vpython import box, vector, rate, scene, arrow, label
import math

# اتصال سریال
ser = serial.Serial('COM4', 115200)

# تنظیم صحنه
scene.title = "نمایش زاویه‌های Yaw, Pitch, Roll با رنگ‌بندی محورها"
scene.width = 800
scene.height = 600
scene.background = vector(0.95, 0.95, 0.95)

# ساخت مکعب سنسور
sensor_box = box(length=2, height=0.5, width=1, color=vector(0.2, 0.6, 0.8))

# ساخت محورهای محلی
x_arrow = arrow(pos=sensor_box.pos, axis=vector(1, 0, 0), color=vector(1, 0, 0))      # X قرمز
y_arrow = arrow(pos=sensor_box.pos, axis=vector(0, 1, 0), color=vector(0, 1, 0))      # Y سبز
z_arrow = arrow(pos=sensor_box.pos, axis=vector(0, 0, 1), color=vector(0, 0.4, 1))    # Z آبی

# برچسب‌های رنگی برای زاویه‌ها
label_roll = label(pos=vector(-2.5, 2.5, 0), text="", height=16, box=False, color=vector(1, 0, 0))     # قرمز
label_pitch = label(pos=vector(0, 2.5, 0), text="", height=16, box=False, color=vector(0, 1, 0))       # سبز
label_yaw = label(pos=vector(2.5, 2.5, 0), text="", height=16, box=False, color=vector(0, 0.4, 1))     # آبی

# تبدیل درجه به رادیان
def deg_to_rad(deg):
        return deg * math.pi / 180

# تابع چرخش با زاویه‌های اویلر
# def rotate_box(yaw, pitch, roll):
#     yaw_rad = deg_to_rad(yaw)
#     pitch_rad = deg_to_rad(pitch)
#     roll_rad = deg_to_rad(roll)
#
#     # بردار جهت‌گیری (axis)
#     x = math.cos(yaw_rad) * math.cos(pitch_rad)
#     y = math.sin(pitch_rad)
#     z = math.sin(yaw_rad) * math.cos(pitch_rad)
#     sensor_box.axis = vector(x, y, z)
#
#     # بردار بالا (up) برای Roll
#     up_x = math.cos(yaw_rad) * math.sin(roll_rad) * math.sin(pitch_rad) + math.sin(yaw_rad) * math.cos(roll_rad)
#     up_y = math.cos(pitch_rad) * math.cos(roll_rad)
#     up_z = math.sin(yaw_rad) * math.sin(roll_rad) * math.sin(pitch_rad) - math.cos(yaw_rad) * math.cos(roll_rad)
#     sensor_box.up = vector(up_x, up_y, up_z)
#
#     # بروزرسانی برچسب‌های زاویه
#     label_roll.text = f"Roll: {roll:.1f}°"
#     label_pitch.text = f"Pitch: {pitch:.1f}°"
#     label_yaw.text = f"Yaw: {yaw:.1f}°"
# def rotate_box(yaw, pitch, roll):
#         yaw_rad = deg_to_rad(yaw)
#         pitch_rad = deg_to_rad(pitch)
#         roll_rad = deg_to_rad(roll)
#
#         # ماتریس چرخش ترکیبی (Z-Y-X)
#         cy = math.cos(yaw_rad)
#         sy = math.sin(yaw_rad)
#         cp = math.cos(pitch_rad)
#         sp = math.sin(pitch_rad)
#         cr = math.cos(roll_rad)
#         sr = math.sin(roll_rad)
#
#         # محور جلو (Z محلی) ← جهت نگاه
#         forward_x = cy * cp
#         forward_y = sp
#         forward_z = sy * cp
#         forward = vector(forward_x, forward_y, forward_z)
#
#         # محور بالا (Y محلی)
#         up_x = cy * sr * sp - sy * cr
#         up_y = cp * cr
#         up_z = sy * sr * sp + cy * cr
#         up = vector(up_x, up_y, up_z)
#
#         # محور راست (X محلی)
#         right = forward.cross(up)
#
#         # تنظیم مکعب
#         sensor_box.axis = right.norm() * 2
#         sensor_box.up = up.norm()
#
#         # بروزرسانی محورهای محلی
#         x_arrow.pos = sensor_box.pos
#         y_arrow.pos = sensor_box.pos
#         z_arrow.pos = sensor_box.pos
#
#         x_arrow.axis = right.norm() * 2
#         y_arrow.axis = up.norm() * 2
#         z_arrow.axis = forward.norm() * 2
#
#         # بروزرسانی برچسب‌ها
#         label_roll.text = f"Roll: {roll:.1f}°"
#         label_pitch.text = f"Pitch: {pitch:.1f}°"
#         label_yaw.text = f"Yaw: {yaw:.1f}°"
#
#         # بروزرسانی محورهای محلی
#         x_arrow.pos = sensor_box.pos
#         y_arrow.pos = sensor_box.pos
#         z_arrow.pos = sensor_box.pos
#
#         right = sensor_box.axis.norm()
#         up = sensor_box.up.norm()
#         forward = right.cross(up).norm()
#
#         x_arrow.axis = right * 2
#         y_arrow.axis = up * 2
#         z_arrow.axis = forward * 2
def rotate_box(yaw, pitch, roll):
    yaw_rad = deg_to_rad(yaw)
    pitch_rad = deg_to_rad(pitch)
    roll_rad = deg_to_rad(roll)

    # چرخش حول Z (Yaw)
    Rz = [
        [math.cos(yaw_rad), -math.sin(yaw_rad), 0],
        [math.sin(yaw_rad),  math.cos(yaw_rad), 0],
        [0, 0, 1]
    ]

    # چرخش حول Y (Pitch)
    Ry = [
        [math.cos(pitch_rad), 0, math.sin(pitch_rad)],
        [0, 1, 0],
        [-math.sin(pitch_rad), 0, math.cos(pitch_rad)]
    ]

    # چرخش حول X (Roll)
    Rx = [
        [1, 0, 0],
        [0, math.cos(roll_rad), -math.sin(roll_rad)],
        [0, math.sin(roll_rad),  math.cos(roll_rad)]
    ]

    # ترکیب چرخش‌ها: R = Rz * Ry * Rx
    def mat_mult(A, B):
        return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]

    Rzy = mat_mult(Rz, Ry)
    R = mat_mult(Rzy, Rx)

    # استخراج محورهای محلی از ماتریس چرخش
    right = vector(R[0][0], R[1][0], R[2][0])   # محور X محلی
    up    = vector(R[0][1], R[1][1], R[2][1])   # محور Y محلی
    forward = vector(R[0][2], R[1][2], R[2][2]) # محور Z محلی

    # تنظیم مکعب و فلش‌ها
    sensor_box.axis = right.norm() * 2
    sensor_box.up = up.norm()

    x_arrow.pos = sensor_box.pos
    y_arrow.pos = sensor_box.pos
    z_arrow.pos = sensor_box.pos

    x_arrow.axis = right.norm() * 2
    y_arrow.axis = up.norm() * 2
    z_arrow.axis = forward.norm() * 2

    # بروزرسانی برچسب‌ها
    label_roll.text = f"Roll: {roll:.1f}°"
    label_pitch.text = f"Pitch: {pitch:.1f}°"
    label_yaw.text = f"Yaw: {yaw:.1f}°"

# حلقه دریافت داده و نمایش
print("📡 دریافت داده از ESP32...")
while True:
    rate(50)
    try:
        line = ser.readline().decode().strip()
        if line:
            yaw, pitch, roll = map(float, line.split(","))
            rotate_box(yaw, pitch, roll)
    except Exception as e:
        print("Error:", e)
