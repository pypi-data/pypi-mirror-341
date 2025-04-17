from typing import Any

from .commons_pb2 import OuterContextItem
from .ChatManager_pb2_grpc import ChatManagerStub
from .ChatManager_pb2 import (
    ChatManagerRequest,
    ChatManagerResponse,
)
from .abstract_client import AbstractClient
from .converters import convert_outer_context


class ChatManagerClient(AbstractClient):
    def __init__(self, address) -> None:
        super().__init__(address)
        self._stub = ChatManagerStub(self._channel)

    def __call__(self, text: str, dict_outer_context: dict, request_id: str, resource_id: str) -> str:
        outer_context: OuterContextItem = convert_outer_context(dict_outer_context)

        request = ChatManagerRequest(
            Text=text,
            OuterContext=outer_context,
            RequestId=request_id,
            ResourceId=resource_id,
        )
        response: ChatManagerResponse = self._stub.GetChatResponse(
            request
        )
        replica: dict[str, Any] = {
            "Text": response.Text,
            "ResourceId": response.ResourceId,
            "State": response.State,
            "Action": response.Action,
        }
        return replica
