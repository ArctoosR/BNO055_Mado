import serial
import csv
import time

ser = serial.Serial('COM4', 115200)
label = input("برچسب حرکت را وارد کن (مثلاً up/down/left/right): ")

with open("gesture_data.csv", "a", newline='') as f:
    writer = csv.writer(f)
    print("شروع ضبط داده‌ها برای:", label)
    start = time.time()
    last_sample_time = 0
    sample_interval = 0.05  # هر 50ms = 20Hz

    while time.time() - start < 3:  # ضبط 3 ثانیه
        line = ser.readline().decode().strip()
        now = time.time()
        if now - last_sample_time >= sample_interval:
         try:
            yaw, pitch, roll = map(float, line.split(","))
            writer.writerow([yaw, pitch, roll, label])
            last_sample_time = now
         except:
            continue
print("✅ ضبط داده‌ها تمام شد.")
