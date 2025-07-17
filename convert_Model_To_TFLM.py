# import tensorflow as tf
#
# # بارگذاری مدل
# model = tf.keras.models.load_model("gesture_model.h5")
#
# # تبدیل به TFLite
# converter = tf.lite.TFLiteConverter.from_keras_model(model)
# converter.optimizations = [tf.lite.Optimize.DEFAULT]  # فعال‌سازی کوانتیزه‌سازی
#
# tflite_model = converter.convert()
#
# # ذخیره مدل
# with open("gesture_model.tflite", "wb") as f:
#     f.write(tflite_model)
########################################################################################
import tensorflow as tf
import numpy as np
import pandas as pd

# بارگذاری داده‌ها برای کوانتیزه‌سازی
df = pd.read_csv("gesture_data.csv", names=["yaw", "pitch", "roll", "label"])
X = df[["yaw", "pitch", "roll"]].values.astype(np.float32)

# بارگذاری مدل آموزش‌دیده
model = tf.keras.models.load_model("gesture_model.h5")

# تعریف دیتاست نماینده برای کوانتیزه‌سازی
def representative_dataset():
    for i in range(min(100, len(X))):
        yield [X[i:i+1]]

# تبدیل به TFLite با کوانتیزه‌سازی کامل
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

# تبدیل مدل
tflite_model = converter.convert()

# ذخیره مدل
with open("gesture_model.tflite", "wb") as f:
    f.write(tflite_model)

print("✅ مدل کوانتیزه‌شده با موفقیت ذخیره شد.")
