from eis1600.models.Model import Model
from eis1600.helper.Singleton import singleton


@singleton
class STModel(Model):

    def __init__(self) -> None:
        super().__init__('EIS1600_Pretrained_Models/camelbert-ca-finetuned_person_classification_STN/')
