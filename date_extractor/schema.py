from pydantic import BaseModel
from typing import List

class ExtractionResult(BaseModel):
    dates: List[str]
    message: str
