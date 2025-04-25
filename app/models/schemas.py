from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    id: str
    name: Optional[str] = None
    picture: Optional[Dict[str, Any]] = None
    link: Optional[str] = None
    email: Optional[str] = None

class PostBase(BaseModel):
    id: str
    message: Optional[str] = None
    created_time: Optional[datetime] = None
    permalink_url: Optional[str] = None

class CommentBase(BaseModel):
    id: str
    message: Optional[str] = None
    created_time: Optional[datetime] = None
    from_user: Optional[UserBase] = Field(None, alias="from")
    like_count: Optional[int] = None
    post_id: str

class LikeBase(BaseModel):
    id: str
    name: str
    picture: Optional[Dict[str, Any]] = None
    link: Optional[str] = None
    email: Optional[str] = None
    post_id: str

class FollowBase(BaseModel):
    id: str
    name: Optional[str] = None

class MentionBase(BaseModel):
    id: str
    message: Optional[str] = None
    created_time: Optional[datetime] = None
    from_user: Optional[UserBase] = Field(None, alias="from")
    story: Optional[str] = None

class MessageBase(BaseModel):
    id: str
    message: Optional[str] = None
    created_time: Optional[datetime] = None
    from_user: Optional[UserBase] = Field(None, alias="from")

class ConversationBase(BaseModel):
    id: str
    link: Optional[str] = None
    updated_time: Optional[datetime] = None
    messages: Optional[Dict[str, Any]] = None

class PostResponse(BaseModel):
    data: List[PostBase]
    paging: Optional[dict] = None

class CommentResponse(BaseModel):
    data: List[CommentBase]
    paging: Optional[dict] = None

class LikeResponse(BaseModel):
    data: List[LikeBase]
    paging: Optional[dict] = None

class FollowResponse(BaseModel):
    data: List[Dict[str, Any]]
    paging: Optional[dict] = None

class MentionResponse(BaseModel):
    data: List[MentionBase]
    paging: Optional[dict] = None

class ConversationResponse(BaseModel):
    data: List[ConversationBase]
    paging: Optional[dict] = None

class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    details: Optional[str] = None
