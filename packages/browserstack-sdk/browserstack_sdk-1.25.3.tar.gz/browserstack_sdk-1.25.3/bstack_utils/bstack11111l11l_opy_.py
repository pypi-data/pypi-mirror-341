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
from collections import deque
from bstack_utils.constants import *
class bstack11l1l1ll11_opy_:
    def __init__(self):
        self._111ll11ll1l_opy_ = deque()
        self._111ll11ll11_opy_ = {}
        self._111ll11lll1_opy_ = False
    def bstack111ll111l1l_opy_(self, test_name, bstack111ll11llll_opy_):
        bstack111ll1111ll_opy_ = self._111ll11ll11_opy_.get(test_name, {})
        return bstack111ll1111ll_opy_.get(bstack111ll11llll_opy_, 0)
    def bstack111ll11l111_opy_(self, test_name, bstack111ll11llll_opy_):
        bstack111ll111lll_opy_ = self.bstack111ll111l1l_opy_(test_name, bstack111ll11llll_opy_)
        self.bstack111ll11l1ll_opy_(test_name, bstack111ll11llll_opy_)
        return bstack111ll111lll_opy_
    def bstack111ll11l1ll_opy_(self, test_name, bstack111ll11llll_opy_):
        if test_name not in self._111ll11ll11_opy_:
            self._111ll11ll11_opy_[test_name] = {}
        bstack111ll1111ll_opy_ = self._111ll11ll11_opy_[test_name]
        bstack111ll111lll_opy_ = bstack111ll1111ll_opy_.get(bstack111ll11llll_opy_, 0)
        bstack111ll1111ll_opy_[bstack111ll11llll_opy_] = bstack111ll111lll_opy_ + 1
    def bstack11lll11ll1_opy_(self, bstack111ll11l1l1_opy_, bstack111ll111l11_opy_):
        bstack111ll111ll1_opy_ = self.bstack111ll11l111_opy_(bstack111ll11l1l1_opy_, bstack111ll111l11_opy_)
        event_name = bstack11ll11lllll_opy_[bstack111ll111l11_opy_]
        bstack1l1ll1ll1ll_opy_ = bstack1l1_opy_ (u"ࠢࡼࡿ࠰ࡿࢂ࠳ࡻࡾࠤ᳧").format(bstack111ll11l1l1_opy_, event_name, bstack111ll111ll1_opy_)
        self._111ll11ll1l_opy_.append(bstack1l1ll1ll1ll_opy_)
    def bstack1l11l11l1_opy_(self):
        return len(self._111ll11ll1l_opy_) == 0
    def bstack11l1l1l1l_opy_(self):
        bstack111ll11l11l_opy_ = self._111ll11ll1l_opy_.popleft()
        return bstack111ll11l11l_opy_
    def capturing(self):
        return self._111ll11lll1_opy_
    def bstack1l1111ll1l_opy_(self):
        self._111ll11lll1_opy_ = True
    def bstack1l11ll11ll_opy_(self):
        self._111ll11lll1_opy_ = False