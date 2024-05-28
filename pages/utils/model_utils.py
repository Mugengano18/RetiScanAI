import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image  # Correct import
import cv2
import matplotlib.pyplot as plt
import io
import base64

def load_and_preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.models.Model(
        [model.inputs[0]], [model.get_layer(last_conv_layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[0][:, pred_index]
        grads = tape.gradient(class_channel, last_conv_layer_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        last_conv_layer_output = last_conv_layer_output[0]
        heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
        heatmap = tf.squeeze(heatmap)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def display_gradcam(img_path, heatmap, alpha=0.4):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * alpha + img
    superimposed_img = np.uint8(superimposed_img)

    # Create a buffer to store the real image
    real_image_buffer = io.BytesIO()
    real_image = cv2.imencode('.png', img)[1].tobytes()
    real_image_buffer.write(real_image)
    real_image_buffer.seek(0)
    real_image_base64 = base64.b64encode(real_image_buffer.getvalue()).decode('utf-8')

    # Create a buffer to store the Grad-CAM image
    gradcam_buffer = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.imshow(cv2.cvtColor(superimposed_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.savefig(gradcam_buffer, format='png')
    gradcam_buffer.seek(0)
    gradcam_image_base64 = base64.b64encode(gradcam_buffer.getvalue()).decode('utf-8')
    plt.close()

    return real_image_base64, gradcam_image_base64
