import tensorflow as tf
import numpy as np
from PIL import Image

# Cargar protocolo
interpreter = tf.lite.Interpreter(
    model_path="ml_models/dolor/model.tflite"
)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Cargar etiquetas
with open("ml_models/dolor/labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

def predecir_imagen(imagen):
    # Convertir imagen
    img = imagen.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    indice = np.argmax(output)

    return {
        "clase": labels[indice],
        "confianza": float(output[0][indice])
    }
