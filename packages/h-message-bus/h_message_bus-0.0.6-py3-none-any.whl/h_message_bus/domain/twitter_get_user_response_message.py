from typing import Type, TypeVar, Dict, Any

from .topics import MessageTopic
from ..domain.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class TwitterGetUserResponseMessage(HaiMessage):
    """Response of Twitter user information request"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, user_id: str, screen_name: str, description: str, followers_count: str, like_count: str, is_verified: str, url: str, bio_urls: [str]) -> 'TwitterGetUserResponseMessage':
        """Create a response message from Twitter user information"""
        return cls.create(
            topic=MessageTopic.AI_TWITTER_GET_USER_RESPONSE,
            payload={
                'id': user_id,
                'screen_name': screen_name,
                'description': description,
                'followers_count': followers_count,
                'like_count': like_count,
                'is_verified': is_verified,
                'url': url,
                'bio_urls': bio_urls
            })
