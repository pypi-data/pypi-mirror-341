# coding: UTF-8
import sys
bstack1lllll1_opy_ = sys.version_info [0] == 2
bstack11l1111_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l1_opy_ (bstack11l1_opy_):
    global bstack11lll_opy_
    bstack11111_opy_ = ord (bstack11l1_opy_ [-1])
    bstack11llll_opy_ = bstack11l1_opy_ [:-1]
    bstack1111ll_opy_ = bstack11111_opy_ % len (bstack11llll_opy_)
    bstack1l1l_opy_ = bstack11llll_opy_ [:bstack1111ll_opy_] + bstack11llll_opy_ [bstack1111ll_opy_:]
    if bstack1lllll1_opy_:
        bstack1l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1111_opy_ - (bstack1ll11ll_opy_ + bstack11111_opy_) % bstack11ll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack1l1lll_opy_ = str () .join ([chr (ord (char) - bstack11l1111_opy_ - (bstack1ll11ll_opy_ + bstack11111_opy_) % bstack11ll11_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack1l1lll_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111l111ll_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack111111l1l1_opy_:
    bstack1l1111ll111_opy_ = bstack1l1_opy_ (u"ࠣࡤࡨࡲࡨ࡮࡭ࡢࡴ࡮ࠦᔖ")
    context: bstack1111l111ll_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111l111ll_opy_):
        self.context = context
        self.data = dict({bstack111111l1l1_opy_.bstack1l1111ll111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᔗ"), bstack1l1_opy_ (u"ࠪ࠴ࠬᔘ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack11111l1lll_opy_(self, target: object):
        return bstack111111l1l1_opy_.create_context(target) == self.context
    def bstack1ll11l11l1l_opy_(self, context: bstack1111l111ll_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack1ll1ll11ll_opy_(self, key: str, value: timedelta):
        self.data[bstack111111l1l1_opy_.bstack1l1111ll111_opy_][key] += value
    def bstack1lll1lll1ll_opy_(self) -> dict:
        return self.data[bstack111111l1l1_opy_.bstack1l1111ll111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111l111ll_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )