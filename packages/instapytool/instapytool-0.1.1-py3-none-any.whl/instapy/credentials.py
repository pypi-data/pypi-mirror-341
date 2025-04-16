from pydantic import BaseModel

class UserCredentials(BaseModel):
    username: str
    session_id: str
