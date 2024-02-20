from ultralytics import YOLO as Model

CONST_MODEL = [
    "yolov8n.pt",
    "yolov8s.pt",
    "yolov8s-world.pt",
]

DATASET = [
    "coco8.yaml",
    "coco.yaml",
]



class EngineAI:
    def __init__(self):
        self.model = None
        self.dataset = None
        self.model_name = None
        self.dataset_name = None

    def load_model(self, model_name: str):
        if model_name:
            self.model_name = model_name
            self.model = Model(model_name)
            return True
        return False

    def load_dataset(self, dataset_name: str):
        if dataset_name in DATASET:
            self.dataset_name = dataset_name
            self.dataset = dataset_name
            return True
        return False

    def predict(self, img_path: str, clases: list[str] = []):
        if clases:
            return self.model.predict(img_path, classes=clases)
        return self.model.predict(img_path)
    
    def train(self, epochs=100, imagsz=640, dataset=DATASET[0], path_save='./dip_train/model.pt'):
        # if self.model:
        #     self.model.train(data=dataset, imgsz=imagsz, epochs=epochs)
        #     self.model.save(path_save)
        ...
