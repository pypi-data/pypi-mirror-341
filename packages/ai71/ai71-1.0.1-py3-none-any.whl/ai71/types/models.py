from typing import Literal, Sequence

import pydantic


class Model(pydantic.BaseModel):
    id: str
    name: str
    object: Literal["model"] = "model"
    owned_by: str
    price_per_m_prompt_tokens: float
    price_per_m_completion_tokens: float
    max_tokens: int


class ModelsList(pydantic.BaseModel):
    object: Literal["list"] = "list"
    data: Sequence[Model]
