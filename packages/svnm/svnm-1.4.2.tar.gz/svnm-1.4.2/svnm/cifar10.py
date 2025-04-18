
from svnm.config import modelinfo
from svnm.utils import download_model
from tensorflow.keras.models import load_model
from svnm.preprocessing import load_and_preprocess_image
import os
import numpy as np
from svnm.basemodels import ImageClassificationbaseModel
class Cifar10(ImageClassificationbaseModel):
    def __init__(self):
        super().__init__("Cifar10")