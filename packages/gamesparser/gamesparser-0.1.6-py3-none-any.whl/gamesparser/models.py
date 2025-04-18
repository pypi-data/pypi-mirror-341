from abc import ABC, abstractmethod
import logging
import httpx
from collections.abc import Iterable, Sequence
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Price:
    currency_code: str
    value: float


@dataclass
class ParsedItem:
    id: str
    name: str
    url: str
    discount: int  # discount in percents (0-100)
    prices: dict[str, Price]

    # def as_json_serializable(self) -> dict[str, Any]:
    #     data = asdict(self)
    #     if self.deal_until:
    #         data["deal_until"] = str(self.deal_until)
    #     return data


@dataclass
class XboxParsedItem(ParsedItem):
    with_sub: bool
    preview_img: str
    deal_until: datetime | None = None


@dataclass
class XboxItemDetails:
    description: str
    platforms: list[str]
    media: Sequence[str]


@dataclass
class PsnParsedItem(ParsedItem):
    platforms: list[str]
    with_sub: bool
    media: Sequence[str]


@dataclass
class PsnItemDetails:
    description: str
    deal_until: datetime | None = None


class AbstractParser(ABC):
    def __init__(
        self,
        client: httpx.AsyncClient,
        limit: int | None = None,
        logger: logging.Logger | None = None,
    ):
        self._limit = limit
        self._client = client
        if logger is None:
            logger = logging.getLogger(__name__)
        self._logger = logger

    def _normalize_regions(self, regions: Iterable[str]) -> set[str]:
        assert not isinstance(regions, str), "regions can't be string"
        return set(region.strip().lower() for region in regions)

    @abstractmethod
    async def parse(self, regions: Iterable[str]) -> Sequence[ParsedItem]: ...
