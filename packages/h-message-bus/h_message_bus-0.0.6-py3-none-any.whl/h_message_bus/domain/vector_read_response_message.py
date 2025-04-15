from typing import Type, TypeVar, Dict, Any

from .topics import MessageTopic
from ..domain.hai_message import HaiMessage

T = TypeVar('T', bound='HaiMessage')

class VectorReadResponseMessage(HaiMessage):
    """Response Message from reading vector data"""

    @classmethod
    def create(cls: Type[T], topic: str, payload: Dict[Any, Any]) -> T:
        """Create a message - inherited from HaiMessage"""
        return super().create(topic=topic, payload=payload)

    @classmethod
    def create_message(cls, results: [str], dimensions: [str]) -> 'VectorReadResponseMessage':
        """Create a message requesting Twitter user data"""
        return cls.create(
            topic=MessageTopic.AI_VECTORS_QUERY_RESPONSE,
            payload={
                "dimensions": dimensions,
                "results": results
            },
        )