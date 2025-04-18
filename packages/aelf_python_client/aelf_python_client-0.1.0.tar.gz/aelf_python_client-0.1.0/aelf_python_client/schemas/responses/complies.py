from pydantic import BaseModel, ConfigDict

from aelf_python_client.schemas.complies import CompliesModel
from aelf_python_client.schemas.informations import InformationsModel


class CompliesResponseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    informations: InformationsModel
    complies: CompliesModel
