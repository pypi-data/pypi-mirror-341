
from typing import List, Literal
from pydantic import BaseModel, Field


class Contact(BaseModel):
    contact_type: Literal['email', 'phone_extension', 'phone', 'site', 'icq', 'twitter', 'skype', 'staff'] = Field(alias='type')
    value: str
    main: bool = False
    alias: bool = False
    synthetic: bool = False


class ShortUser(BaseModel):
    uid: str = Field(alias="id")
    nickname: str
    department_id: int = Field(alias="departmentId")
    email: str
    gender: str
    position: str
    avatar_id: str = Field(alias="avatarId")

    class Name(BaseModel):
        first: str
        last: str
        middle: str

    name: Name
    

class User(ShortUser):
    is_enabled: bool = Field(alias="isEnabled")
    about: str
    birthday: str
    external_id: str = Field(alias="externalId")
    is_admin: bool = Field(alias="isAdmin")
    is_robot: bool = Field(alias="isRobot")
    is_dismissed: bool = Field(alias="isDismissed")
    timezone: str
    language: str
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    display_name: str = Field(default='', alias="displayName")
    groups: List[int]
    contacts: List[Contact]
    aliases: List[str]


class UsersPage(BaseModel):
    page: int
    pages: int
    per_page: int = Field(alias="perPage")
    total: int
    users: List[User]


class ShortGroup(BaseModel):
    group_id: int = Field(alias="id")
    name: str
    members_count: int= Field(alias="membersCount")


class GroupMember(BaseModel):
    member_id: str = Field(alias="id")
    type: Literal['user', 'group', 'department']


class Group(ShortGroup):
        type: str
        description: str
        label: str
        email: str
        aliases: List[str]
        external_id: str = Field(alias="externalId")
        removed: bool
        members: List[GroupMember]
        member_of: List[int] = Field(alias="memberOf")
        created_at: str= Field(alias="createdAt")
    
    
class GroupsPage(BaseModel):
    groups: list[Group]
    page: int
    pages: int
    per_page: int = Field(alias="perPage")
    total: int


class GroupMembers2(BaseModel):
    groups: List[ShortGroup]
    users: List[ShortUser]


