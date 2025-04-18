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
import requests
from urllib.parse import urljoin, urlencode
from datetime import datetime
import os
import logging
import json
logger = logging.getLogger(__name__)
class bstack11lll11llll_opy_:
    @staticmethod
    def results(builder,params=None):
        bstack111l11l1lll_opy_ = urljoin(builder, bstack1l1ll11_opy_ (u"ࠩ࡬ࡷࡸࡻࡥࡴࠩᵠ"))
        if params:
            bstack111l11l1lll_opy_ += bstack1l1ll11_opy_ (u"ࠥࡃࢀࢃࠢᵡ").format(urlencode({bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᵢ"): params.get(bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᵣ"))}))
        return bstack11lll11llll_opy_.bstack111l11l1ll1_opy_(bstack111l11l1lll_opy_)
    @staticmethod
    def bstack11lll1l1l11_opy_(builder,params=None):
        bstack111l11l1lll_opy_ = urljoin(builder, bstack1l1ll11_opy_ (u"࠭ࡩࡴࡵࡸࡩࡸ࠳ࡳࡶ࡯ࡰࡥࡷࡿࠧᵤ"))
        if params:
            bstack111l11l1lll_opy_ += bstack1l1ll11_opy_ (u"ࠢࡀࡽࢀࠦᵥ").format(urlencode({bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᵦ"): params.get(bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᵧ"))}))
        return bstack11lll11llll_opy_.bstack111l11l1ll1_opy_(bstack111l11l1lll_opy_)
    @staticmethod
    def bstack111l11l1ll1_opy_(bstack111l11ll111_opy_):
        bstack111l11l1l11_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᵨ"), os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᵩ"), bstack1l1ll11_opy_ (u"ࠬ࠭ᵪ")))
        headers = {bstack1l1ll11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᵫ"): bstack1l1ll11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪᵬ").format(bstack111l11l1l11_opy_)}
        response = requests.get(bstack111l11ll111_opy_, headers=headers)
        bstack111l11l1l1l_opy_ = {}
        try:
            bstack111l11l1l1l_opy_ = response.json()
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡎࡘࡕࡎࠡࡴࡨࡷࡵࡵ࡮ࡴࡧ࠽ࠤࢀࢃࠢᵭ").format(e))
            pass
        if bstack111l11l1l1l_opy_ is not None:
            bstack111l11l1l1l_opy_[bstack1l1ll11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡱ࡯ࡰࡤࡺࡩ࡮ࡧࠪᵮ")] = response.headers.get(bstack1l1ll11_opy_ (u"ࠪࡲࡪࡾࡴࡠࡲࡲࡰࡱࡥࡴࡪ࡯ࡨࠫᵯ"), str(int(datetime.now().timestamp() * 1000)))
            bstack111l11l1l1l_opy_[bstack1l1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᵰ")] = response.status_code
        return bstack111l11l1l1l_opy_