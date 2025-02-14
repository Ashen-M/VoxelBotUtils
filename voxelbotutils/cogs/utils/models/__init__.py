import discord

from ..interactions.components.action_row import MessageComponents


_original_message = discord.Message
_original_webhook_message = discord.WebhookMessage


class ComponentMessage(_original_message):

    __slots__ = _original_message.__slots__ + ("components",)

    def __init__(self, *, state, channel, data):
        self.components = MessageComponents.from_dict(data.get("components", list()))
        super().__init__(state=state, channel=channel, data=data)


class ComponentWebhookMessage(ComponentMessage, _original_webhook_message):
    pass
