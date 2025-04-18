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
from collections import deque
from bstack_utils.constants import *
class bstack1ll11llll_opy_:
    def __init__(self):
        self._111ll11llll_opy_ = deque()
        self._111ll11l11l_opy_ = {}
        self._111ll11ll11_opy_ = False
    def bstack111ll11ll1l_opy_(self, test_name, bstack111ll11l1ll_opy_):
        bstack111ll111l11_opy_ = self._111ll11l11l_opy_.get(test_name, {})
        return bstack111ll111l11_opy_.get(bstack111ll11l1ll_opy_, 0)
    def bstack111ll1111ll_opy_(self, test_name, bstack111ll11l1ll_opy_):
        bstack111ll11l1l1_opy_ = self.bstack111ll11ll1l_opy_(test_name, bstack111ll11l1ll_opy_)
        self.bstack111ll111lll_opy_(test_name, bstack111ll11l1ll_opy_)
        return bstack111ll11l1l1_opy_
    def bstack111ll111lll_opy_(self, test_name, bstack111ll11l1ll_opy_):
        if test_name not in self._111ll11l11l_opy_:
            self._111ll11l11l_opy_[test_name] = {}
        bstack111ll111l11_opy_ = self._111ll11l11l_opy_[test_name]
        bstack111ll11l1l1_opy_ = bstack111ll111l11_opy_.get(bstack111ll11l1ll_opy_, 0)
        bstack111ll111l11_opy_[bstack111ll11l1ll_opy_] = bstack111ll11l1l1_opy_ + 1
    def bstack1lll1ll11l_opy_(self, bstack111ll11lll1_opy_, bstack111ll111ll1_opy_):
        bstack111ll11l111_opy_ = self.bstack111ll1111ll_opy_(bstack111ll11lll1_opy_, bstack111ll111ll1_opy_)
        event_name = bstack11ll1l1l1l1_opy_[bstack111ll111ll1_opy_]
        bstack1l1ll1llll1_opy_ = bstack1l1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃ࠭ࡼࡿ᳨ࠥ").format(bstack111ll11lll1_opy_, event_name, bstack111ll11l111_opy_)
        self._111ll11llll_opy_.append(bstack1l1ll1llll1_opy_)
    def bstack1l111111l_opy_(self):
        return len(self._111ll11llll_opy_) == 0
    def bstack1l1l1ll11_opy_(self):
        bstack111ll111l1l_opy_ = self._111ll11llll_opy_.popleft()
        return bstack111ll111l1l_opy_
    def capturing(self):
        return self._111ll11ll11_opy_
    def bstack1lll1111_opy_(self):
        self._111ll11ll11_opy_ = True
    def bstack111111l1l_opy_(self):
        self._111ll11ll11_opy_ = False