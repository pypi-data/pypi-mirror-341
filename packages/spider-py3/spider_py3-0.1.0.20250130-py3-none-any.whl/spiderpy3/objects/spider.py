from abc import abstractmethod
from typing import Any

from spiderpy3.items.item import Item
from spiderpy3.objects.handler import Handler
from spiderpy3.mixins.protocol import ProtocolMixin
from spiderpy3.models.sqlalchemy_model import SqlalchemyModel


class Spider(Handler, ProtocolMixin):
    Model: SqlalchemyModel

    def logger_success_item(self, item: Item) -> None:
        self.logger.success(item)

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass
