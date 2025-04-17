# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["SpanListParams"]


class SpanListParams(TypedDict, total=False):
    ending_before: Optional[str]

    from_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    limit: int

    parents_only: Optional[bool]

    starting_after: Optional[str]

    to_ts: Annotated[Union[str, datetime, None], PropertyInfo(format="iso8601")]

    trace_id: Optional[str]
