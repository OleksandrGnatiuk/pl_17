from typing import List, Optional

from pydantic import BaseModel, Field
from datetime import datetime

from src.schemas.tag_schemas import TagResponse
from src.schemas.user_schemas import UserResponse


class CommentResponse(BaseModel):
    id: int = 1
    comment: str = 'My comment'

    class Config:
        orm_mode = True


class ServiceAddModel(BaseModel):
    description: str = Field(max_length=500)
    tags: Optional[List[str]]


class ServiceAddTagModel(BaseModel):
    tags: Optional[List[str]]


class ServiceUpdateModel(BaseModel):
    description: str = Field(max_length=500)


class ServiceDb(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagResponse]
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
        exclude = {'updated_at', 'user', 'public_name'}


class ServiceAdminDb(BaseModel):
    id: int
    url: str
    description: str
    tags: List[TagResponse]
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        exclude = {'public_name', 'user_id'}


class ServiceGetResponse(BaseModel):
    image: ServiceDb
    ratings: float
    comments: List[CommentResponse]


class ServiceAdminGetResponse(BaseModel):
    image: ServiceAdminDb
    ratings: float
    comments: List[CommentResponse]


class ServiceGetAllResponse(BaseModel):
    images: List[ServiceGetResponse]


class ServiceAdminGetAllResponse(BaseModel):
    images: List[ServiceAdminGetResponse]


class ServiceAddResponse(BaseModel):
    image: ServiceDb
    detail: str = "Image was successfully added"

    class Config:
        orm_mode = True


class ServiceAddTagResponse(BaseModel):
    id: int
    tags: List[TagResponse]
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True


class ServiceUpdateDescrResponse(BaseModel):
    id: int
    description: str
    detail: str = "Image was successfully updated"

    class Config:
        orm_mode = True


class ServiceDeleteResponse(BaseModel):
    image: ServiceDb
    detail: str = "Image was successfully deleted"
