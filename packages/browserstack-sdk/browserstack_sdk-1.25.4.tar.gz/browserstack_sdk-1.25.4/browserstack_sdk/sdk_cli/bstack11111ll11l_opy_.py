# coding: UTF-8
import sys
bstack1l1llll_opy_ = sys.version_info [0] == 2
bstack11l111l_opy_ = 2048
bstack111l_opy_ = 7
def bstack1l1ll11_opy_ (bstack11111l1_opy_):
    global bstack1l11ll_opy_
    bstack1l111l1_opy_ = ord (bstack11111l1_opy_ [-1])
    bstack1llllll1_opy_ = bstack11111l1_opy_ [:-1]
    bstack1111l_opy_ = bstack1l111l1_opy_ % len (bstack1llllll1_opy_)
    bstack1ll111_opy_ = bstack1llllll1_opy_ [:bstack1111l_opy_] + bstack1llllll1_opy_ [bstack1111l_opy_:]
    if bstack1l1llll_opy_:
        bstack11lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11l111l_opy_ - (bstack1lllll1l_opy_ + bstack1l111l1_opy_) % bstack111l_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack1ll111_opy_)])
    else:
        bstack11lll1l_opy_ = str () .join ([chr (ord (char) - bstack11l111l_opy_ - (bstack1lllll1l_opy_ + bstack1l111l1_opy_) % bstack111l_opy_) for bstack1lllll1l_opy_, char in enumerate (bstack1ll111_opy_)])
    return eval (bstack11lll1l_opy_)
import os
import threading
import os
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from datetime import timedelta
@dataclass
class bstack1111l1l1l1_opy_:
    id: str
    hash: str
    thread_id: int
    process_id: int
    type: str
class bstack1111111l11_opy_:
    bstack1l1111ll111_opy_ = bstack1l1ll11_opy_ (u"ࠤࡥࡩࡳࡩࡨ࡮ࡣࡵ࡯ࠧᔗ")
    context: bstack1111l1l1l1_opy_
    data: Dict[str, Any]
    platform_index: int
    def __init__(self, context: bstack1111l1l1l1_opy_):
        self.context = context
        self.data = dict({bstack1111111l11_opy_.bstack1l1111ll111_opy_: defaultdict(lambda: timedelta(microseconds=0))})
        self.platform_index = int(os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᔘ"), bstack1l1ll11_opy_ (u"ࠫ࠵࠭ᔙ")))
    def ref(self) -> str:
        return str(self.context.id)
    def bstack111111lll1_opy_(self, target: object):
        return bstack1111111l11_opy_.create_context(target) == self.context
    def bstack1ll11l11ll1_opy_(self, context: bstack1111l1l1l1_opy_):
        return context and context.thread_id == self.context.thread_id and context.process_id == self.context.process_id
    def bstack11lll111l_opy_(self, key: str, value: timedelta):
        self.data[bstack1111111l11_opy_.bstack1l1111ll111_opy_][key] += value
    def bstack1llll1lllll_opy_(self) -> dict:
        return self.data[bstack1111111l11_opy_.bstack1l1111ll111_opy_]
    @staticmethod
    def create_context(
        target: object,
        thread_id=threading.get_ident(),
        process_id=os.getpid(),
    ):
        return bstack1111l1l1l1_opy_(
            id=hash(target),
            hash=hash(target),
            thread_id=thread_id,
            process_id=process_id,
            type=target,
        )