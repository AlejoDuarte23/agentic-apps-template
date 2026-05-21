from pydantic import BaseModel, ConfigDict

class Tool(BaseModel):
    model_config = ConfigDict(extra="forbid")
