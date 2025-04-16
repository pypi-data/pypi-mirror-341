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
from time import sleep
from datetime import datetime
from urllib.parse import urlencode
from bstack_utils.bstack11lll1l1l11_opy_ import bstack11lll1l11l1_opy_
from bstack_utils.constants import *
import json
class bstack1ll11l111l_opy_:
    def __init__(self, bstack111llll1l_opy_, bstack11lll11llll_opy_):
        self.bstack111llll1l_opy_ = bstack111llll1l_opy_
        self.bstack11lll11llll_opy_ = bstack11lll11llll_opy_
        self.bstack11lll1l111l_opy_ = None
    def __call__(self):
        bstack11lll1l11ll_opy_ = {}
        while True:
            self.bstack11lll1l111l_opy_ = bstack11lll1l11ll_opy_.get(
                bstack1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᙄ"),
                int(datetime.now().timestamp() * 1000)
            )
            bstack11lll1l1ll1_opy_ = self.bstack11lll1l111l_opy_ - int(datetime.now().timestamp() * 1000)
            if bstack11lll1l1ll1_opy_ > 0:
                sleep(bstack11lll1l1ll1_opy_ / 1000)
            params = {
                bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᙅ"): self.bstack111llll1l_opy_,
                bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧᙆ"): int(datetime.now().timestamp() * 1000)
            }
            bstack11lll1l1l1l_opy_ = bstack1l1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶ࠾࠴࠵ࠢᙇ") + bstack11lll11lll1_opy_ + bstack1l1_opy_ (u"ࠨ࠯ࡢࡷࡷࡳࡲࡧࡴࡦ࠱ࡤࡴ࡮࠵ࡶ࠲࠱ࠥᙈ")
            if self.bstack11lll11llll_opy_.lower() == bstack1l1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࡳࠣᙉ"):
                bstack11lll1l11ll_opy_ = bstack11lll1l11l1_opy_.results(bstack11lll1l1l1l_opy_, params)
            else:
                bstack11lll1l11ll_opy_ = bstack11lll1l11l1_opy_.bstack11lll1l1111_opy_(bstack11lll1l1l1l_opy_, params)
            if str(bstack11lll1l11ll_opy_.get(bstack1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙊ"), bstack1l1_opy_ (u"ࠩ࠵࠴࠵࠭ᙋ"))) != bstack1l1_opy_ (u"ࠪ࠸࠵࠺ࠧᙌ"):
                break
        return bstack11lll1l11ll_opy_.get(bstack1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᙍ"), bstack11lll1l11ll_opy_)