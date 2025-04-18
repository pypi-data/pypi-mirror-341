from svnm.basemodels import ImageClassificationbaseModel
import tensorflow as tf
import numpy as np
import os
class GenderDetection(ImageClassificationbaseModel):
    def __init__(self):
        super().__init__("GenderDetection")
    