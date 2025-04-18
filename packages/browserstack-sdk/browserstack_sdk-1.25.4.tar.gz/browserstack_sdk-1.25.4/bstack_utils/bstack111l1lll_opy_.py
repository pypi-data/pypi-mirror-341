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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1l1l1l_opy_ import bstack11lll11llll_opy_
from bstack_utils.constants import *
import json
class bstack1llllll11l_opy_:
    def __init__(self, bstack1ll1ll111_opy_, bstack11lll1l11l1_opy_):
        self.bstack1ll1ll111_opy_ = bstack1ll1ll111_opy_
        self.bstack11lll1l11l1_opy_ = bstack11lll1l11l1_opy_
        self.bstack11lll1l111l_opy_ = None
    def __call__(self):
        bstack11lll1l1ll1_opy_ = {}
        while True:
            self.bstack11lll1l111l_opy_ = bstack11lll1l1ll1_opy_.get(
                bstack1l1ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᙅ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l11ll_opy_ = self.bstack11lll1l111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l11ll_opy_ > 0:
                sleep(bstack11lll1l11ll_opy_ / 1000)
            params = {
                bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᙆ"): self.bstack1ll1ll111_opy_,
                bstack1l1ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨᙇ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l1111_opy_ = bstack1l1ll11_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣᙈ") + bstack11lll11lll1_opy_ + bstack1l1ll11_opy_ (u"ࠢ࠰ࡣࡸࡸࡴࡳࡡࡵࡧ࠲ࡥࡵ࡯࠯ࡷ࠳࠲ࠦᙉ")
            if self.bstack11lll1l11l1_opy_.lower() == bstack1l1ll11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࡴࠤᙊ"):
                bstack11lll1l1ll1_opy_ = bstack11lll11llll_opy_.results(bstack11lll1l1111_opy_, params)
            else:
                bstack11lll1l1ll1_opy_ = bstack11lll11llll_opy_.bstack11lll1l1l11_opy_(bstack11lll1l1111_opy_, params)
            if str(bstack11lll1l1ll1_opy_.get(bstack1l1ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᙋ"), bstack1l1ll11_opy_ (u"ࠪ࠶࠵࠶ࠧᙌ"))) != bstack1l1ll11_opy_ (u"ࠫ࠹࠶࠴ࠨᙍ"):
                break
        return bstack11lll1l1ll1_opy_.get(bstack1l1ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪᙎ"), bstack11lll1l1ll1_opy_)