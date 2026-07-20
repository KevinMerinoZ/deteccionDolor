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

def predecir_imagen(imagen):
    # procesar imagen para su analisis
    img = imagen.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)

    # realizar predicción usando el modelo de TensorFlow Lite
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    # obtener resultados de predicción
    output = interpreter.get_tensor(output_details[0]['index'])
    indice = np.argmax(output)

    # Devolver los resultados de la predicción
    return {
        "clase": indice,
        "confianza": float(output[0][indice]),
    }
