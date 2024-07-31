import tensorflow as tf
import numpy as np

with open('data/processed.txt', 'r') as file:
    data = file.readlines()

data = [len(line.strip()) for line in data]
data = np.array(data)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(1,)),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

labels = np.random.randint(2, size=len(data))

model.fit(data, labels, epochs=5)

predictions = model.predict(data)

with open('data/classified.txt', 'w') as file:
    for line, prediction in zip(data, predictions):
        file.write(f"{line}\t{prediction}\n")