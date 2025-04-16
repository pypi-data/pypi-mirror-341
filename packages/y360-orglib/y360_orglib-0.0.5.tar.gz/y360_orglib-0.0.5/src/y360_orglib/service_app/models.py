from pydantic import BaseModel

class ServiceAppTokenResponse(BaseModel):
    access_token: str
    expires_in: int = 3600
    issued_token_type: str = ''
    scope: str = ''
    token_type: str = ''
    
   
    @property
    def auth_header(self) -> dict:
        """Return the authorization header format for this token"""
        return {"Authorization": f"{self.token_type.capitalize()} {self.access_token}"}