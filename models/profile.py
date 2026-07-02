from dataclasses import dataclass
from typing import Optional

@dataclass
class ProfileData:
    id: int
    username: str
    followers: Optional[int] = None
    following: Optional[int] = None
    posts: Optional[int] = None
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    is_verified: Optional[bool] = None
    category: Optional[str] = None
    full_name: Optional[str] = None
    external_url: Optional[str] = None
    engagement_rate: Optional[float] = None
    average_likes: Optional[int] = None
    average_comments: Optional[int] = None
    last_updated: Optional[str] = None
