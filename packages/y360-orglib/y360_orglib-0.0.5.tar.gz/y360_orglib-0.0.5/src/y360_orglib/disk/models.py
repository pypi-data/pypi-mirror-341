from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field

class Resource(BaseModel):
    public_key: str
    public_url: str
    name: str
    created: str
    modified: str
    path: str
    type: Literal['file', 'dir']
    mime_type: str = ''
    size: int = 0

class PublicResourcesList(BaseModel):
    items: List[Resource]
    limit: int
    offset: int


class BaseAccess(BaseModel):
    macros: List[str] = []
    access_type: str = Field(alias='type')
    rights: List[str] = []
    
class MacroAccess(BaseAccess):
    access_type: Literal['macro'] = Field(alias='type')
    

class UserAccess(BaseAccess):
    access_type: Literal['user', 'group', 'department'] = Field(alias='type')
    org_id: Optional[int] = None
    user_id: int = Field(alias='id')


class PublicSettings(BaseModel):
    available_until: Optional[str]
    public_accesses: List[Union[MacroAccess, UserAccess]] = Field(alias='accesses')
    

    


