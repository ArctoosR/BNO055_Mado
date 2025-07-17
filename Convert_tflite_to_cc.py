# import numpy as np
# import os
#
# def convert_tflite_to_header(tflite_path, output_header_path):
#     with open(tflite_path, 'rb') as tflite_file:
#         tflite_content = tflite_file.read()
#
#     hex_lines = [', '.join([f'0x{byte:02x}' for byte in tflite_content[i:i+12]])
#                  for i in range(0, len(tflite_content), 12)]
#
#     hex_array = ',\n  '.join(hex_lines)
#
#     with open(output_header_path, 'w') as header_file:
#         header_file.write('#ifndef MODEL_H\n#define MODEL_H\n\n')
#         header_file.write(f'const unsigned char model[] = {{\n  {hex_array}\n}};\n\n')
#         header_file.write(f'const int model_len = {len(tflite_content)};\n\n')
#         header_file.write('#endif // MODEL_H\n')
#
# # اجرای تابع
# if __name__ == "__main__":
#     tflite_path = 'gesture_model.tflite'
#     output_header_path = 'model.h'
#     convert_tflite_to_header(tflite_path, output_header_path)
#############################################################################################################

import os

def convert_tflite_to_header(tflite_path, output_dir=".", prefix="model"):
    # استخراج نام فایل بدون پسوند
    model_name = os.path.splitext(os.path.basename(tflite_path))[0]
    array_name = f"{prefix}_{model_name}"

    # خواندن فایل TFLite
    with open(tflite_path, 'rb') as tflite_file:
        tflite_content = tflite_file.read()

    # تبدیل به hex
    hex_lines = [', '.join([f'0x{byte:02x}' for byte in tflite_content[i:i+12]])
                 for i in range(0, len(tflite_content), 12)]
    hex_array = ',\n  '.join(hex_lines)

    # ساخت فایل هدر
    header_path = os.path.join(output_dir, f"{array_name}.h")
    with open(header_path, 'w') as header_file:
        header_file.write(f'#ifndef {array_name.upper()}_H\n#define {array_name.upper()}_H\n\n')
        header_file.write(f'extern const unsigned char {array_name}[];\n')
        header_file.write(f'extern const int {array_name}_len;\n\n')
        header_file.write(f'const unsigned char {array_name}[] = {{\n  {hex_array}\n}};\n\n')
        header_file.write(f'const int {array_name}_len = {len(tflite_content)};\n\n')
        header_file.write(f'#endif // {array_name.upper()}_H\n')

    print(f"✅ فایل هدر ساخته شد: {header_path}")
    print(f"📦 اندازه مدل: {len(tflite_content)} بایت")

# اجرای تابع
if __name__ == "__main__":
    tflite_path = "gesture_model.tflite"  # مسیر فایل مدل
    output_dir = "."  # مسیر خروجی
    prefix = "tflm"   # پیشوند برای نام متغیرها
    convert_tflite_to_header(tflite_path, output_dir, prefix)
