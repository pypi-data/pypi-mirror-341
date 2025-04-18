from svnm.basemodels import ImageDetectionyolobaseModel
class FaceDetection(ImageDetectionyolobaseModel):
    def __init__(self,save=False,save_dir="predictions"):
        super().__init__("FaceDetectionYolo",save,save_dir)
        