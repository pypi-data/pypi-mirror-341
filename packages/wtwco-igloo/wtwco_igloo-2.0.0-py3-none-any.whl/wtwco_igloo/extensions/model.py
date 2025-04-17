class Model(object):
    """Represents a model in Igloo Cloud.

    Attributes:
        id (int): Identifier value of the model.
        model_name (str): Name of the model.
        version_name (str): Version name of the model.
    """

    def __init__(self, model_dict: dict) -> None:
        self.id: int = model_dict["id"]
        self.model_name: str = model_dict["model_name"]
        self.version_name: str = model_dict["version_name"]

    def __str__(self) -> str:
        return f"id: {self.id}, model: {self.model_name}, version: {self.version_name}"
