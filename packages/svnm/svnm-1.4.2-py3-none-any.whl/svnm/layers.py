from tensorflow.keras.saving import register_keras_serializable
import tensorflow as tf
from tensorflow.keras import layers
@register_keras_serializable()
class ColorScaler(layers.Layer):
    def __init__(self,**kwargs):
        super(ColorScaler,self).__init__(**kwargs)
    def call(self, x):
        x = tf.image.rgb_to_grayscale(x)  # Convert to grayscale
        x = tf.image.grayscale_to_rgb(x)  # Convert back to RGB
        return x
    def get_config(self):
        config=super(ColorScaler,self).get_config()
        return config 