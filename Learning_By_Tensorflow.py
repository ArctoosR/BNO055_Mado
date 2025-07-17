import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# خواندن داده‌ها
df = pd.read_csv("gesture_data.csv", names=["yaw", "pitch", "roll", "label"])
X = df[["yaw", "pitch", "roll"]].values
y = LabelEncoder().fit_transform(df["label"])

# تقسیم داده‌ها
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# ساخت مدل
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(len(set(y)), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))

# ذخیره مدل
model.save("gesture_model.h5")
