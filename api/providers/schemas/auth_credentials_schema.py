from pydantic import BaseModel

class AuthCredentialsSchema(BaseModel):
    type: str = "credentials"
    username: str
    password: str
    user_id: int
    
    class Config:
        str_strip_whitespace = True
        str_to_lower = True
        table_name = "auth_credentials"
        orm_mode = True