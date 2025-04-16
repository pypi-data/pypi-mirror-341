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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll1l11l1_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1l1l_opy_ = urljoin(builder, bstack1l1_opy_ (u"ࠨ࡫ࡶࡷࡺ࡫ࡳࠨᵟ"))
        if params:
            bstack111l11l1l1l_opy_ += bstack1l1_opy_ (u"ࠤࡂࡿࢂࠨᵠ").format(urlencode({bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᵡ"): params.get(bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵢ"))}))
        return bstack11lll1l11l1_opy_.bstack111l11l1l11_opy_(bstack111l11l1l1l_opy_)
    @staticmethod
    def bstack11lll1l1111_opy_(builder,params=None):
        bstack111l11l1l1l_opy_ = urljoin(builder, bstack1l1_opy_ (u"ࠬ࡯ࡳࡴࡷࡨࡷ࠲ࡹࡵ࡮࡯ࡤࡶࡾ࠭ᵣ"))
        if params:
            bstack111l11l1l1l_opy_ += bstack1l1_opy_ (u"ࠨ࠿ࡼࡿࠥᵤ").format(urlencode({bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᵥ"): params.get(bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᵦ"))}))
        return bstack11lll1l11l1_opy_.bstack111l11l1l11_opy_(bstack111l11l1l1l_opy_)
    @staticmethod
    def bstack111l11l1l11_opy_(bstack111l11l1ll1_opy_):
        bstack111l11ll111_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᵧ"), os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᵨ"), bstack1l1_opy_ (u"ࠫࠬᵩ")))
        headers = {bstack1l1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᵪ"): bstack1l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᵫ").format(bstack111l11ll111_opy_)}
        response = requests.get(bstack111l11l1ll1_opy_, headers=headers)
        bstack111l11l1lll_opy_ = {}
        try:
            bstack111l11l1lll_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡍࡗࡔࡔࠠࡳࡧࡶࡴࡴࡴࡳࡦ࠼ࠣࡿࢂࠨᵬ").format(e))
            pass
        if bstack111l11l1lll_opy_ is not None:
            bstack111l11l1lll_opy_[bstack1l1_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡰ࡮࡯ࡣࡹ࡯࡭ࡦࠩᵭ")] = response.headers.get(bstack1l1_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᵮ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1lll_opy_[bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᵯ")] = response.status_code
        return bstack111l11l1lll_opy_