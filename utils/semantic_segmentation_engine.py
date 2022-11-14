import pixellib
from pixellib.semantic import semantic_segmentation
# import pixellib
# from pixellib.torchbackend.instance import instanceSegmentation


class SemanticSegmentationEngine:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SingletonClass, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        segment_image = semantic_segmentation()
        segment_image.load_pascalvoc_model("tf_model.h5")


    def process(self, input_image_path, output_image_path):
        segment_image.segmentAsPascalvoc(input_image_path, output_image_name = output_image_path)


with SemanticSegmentationEngine() as sse:
    sse.process("res/img1.jpg", "output.jpg")
