import tensorflow as tf
import numpy as np
from PIL import Image

# Cargar protocolo
interpreter = tf.lite.Interpreter(
    model_path="ml_models/dolor/model.tflite"
)
interpreter.allocate_tensors()

modeloOrejas = tf.lite.Interpreter(
    model_path="ml_models/dolor/modelo_orejas.tflite") #epocas:10, tamaño de lote: 16, taza de aprendizaje: 0.0001
modeloOrejas.allocate_tensors()

modeloOjos = tf.lite.Interpreter(
    model_path="ml_models/dolor/modelo_ojos.tflite") 
modeloOjos.allocate_tensors()

modeloNariz = tf.lite.Interpreter(
    model_path="ml_models/dolor/modelo_nariz.tflite") #epocas:10, tamaño de lote: 16, taza de aprendizaje: 0.0001
modeloNariz.allocate_tensors()

modeloCachetes = tf.lite.Interpreter(
    model_path="ml_models/dolor/modelo_cachetes.tflite")
modeloCachetes.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

input_details_orejas = modeloOrejas.get_input_details()
output_details_orejas = modeloOrejas.get_output_details()

input_details_ojos = modeloOjos.get_input_details()
output_details_ojos = modeloOjos.get_output_details()

input_details_nariz = modeloNariz.get_input_details()#--
output_details_nariz = modeloNariz.get_output_details()#--

input_details_cachetes = modeloCachetes.get_input_details()#--
output_details_cachetes = modeloCachetes.get_output_details()#--

def predecir_imagen(imagen):
    # procesar imagen para su analisis
    img = imagen.resize((224, 224))
    img = np.array(img) / 255.0
    img = np.expand_dims(img, axis=0).astype(np.float32)

    # realizar predicción usando el modelo de TensorFlow Lite
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    modeloOrejas.set_tensor(input_details_orejas[0]['index'], img)
    modeloOrejas.invoke()

    modeloOjos.set_tensor(input_details_ojos[0]['index'], img)
    modeloOjos.invoke()

    modeloNariz.set_tensor(input_details_nariz[0]['index'], img)
    modeloNariz.invoke()

    modeloCachetes.set_tensor(input_details_cachetes[0]['index'], img)
    modeloCachetes.invoke()

    # obtener resultados de predicción
    output = interpreter.get_tensor(output_details[0]['index'])
    indice = np.argmax(output)

    output_orejas = modeloOrejas.get_tensor(output_details_orejas[0]['index'])
    indice_orejas = np.argmax(output_orejas)

    output_ojos = modeloOjos.get_tensor(output_details_ojos[0]['index'])
    indice_ojos = np.argmax(output_ojos)

    output_nariz = modeloNariz.get_tensor(output_details_nariz[0]['index'])
    indice_nariz = np.argmax(output_nariz)

    output_cachetes = modeloCachetes.get_tensor(output_details_cachetes[0]['index'])
    indice_cachetes = np.argmax(output_cachetes)

    # Devolver los resultados de la predicción
    return {
        "clase": indice,
        "confianza": float(output[0][indice]),
        "clase_orejas": indice_orejas,
        "confianza_orejas": float(output_orejas[0][indice_orejas]),
        "clase_ojos": indice_ojos,
        "confianza_ojos": float(output_ojos[0][indice_ojos]),
        "clase_nariz": indice_nariz,
        "confianza_nariz": float(output_nariz[0][indice_nariz]),
        "clase_cachetes": indice_cachetes,
        "confianza_cachetes": float(output_cachetes[0][indice_cachetes])
    }
