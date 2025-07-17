import tensorflow as tf

# بارگذاری مدل
model = tf.keras.models.load_model("gesture_model.h5")

# تبدیل به TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]  # فعال‌سازی کوانتیزه‌سازی

tflite_model = converter.convert()

# ذخیره مدل
with open("gesture_model.tflite", "wb") as f:
    f.write(tflite_model)
