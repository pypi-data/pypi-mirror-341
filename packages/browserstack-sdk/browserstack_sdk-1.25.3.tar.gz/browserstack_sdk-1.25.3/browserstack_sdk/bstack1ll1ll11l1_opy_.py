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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack111l111l1_opy_ = {}
        bstack11l11l11ll_opy_ = os.environ.get(bstack1l1_opy_ (u"ࠨࡅࡘࡖࡗࡋࡎࡕࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡉࡇࡔࡂࠩຢ"), bstack1l1_opy_ (u"ࠩࠪຣ"))
        if not bstack11l11l11ll_opy_:
            return bstack111l111l1_opy_
        try:
            bstack11l11l1l11_opy_ = json.loads(bstack11l11l11ll_opy_)
            if bstack1l1_opy_ (u"ࠥࡳࡸࠨ຤") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠦࡴࡹࠢລ")] = bstack11l11l1l11_opy_[bstack1l1_opy_ (u"ࠧࡵࡳࠣ຦")]
            if bstack1l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥວ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥຨ") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠣࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠦຩ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠤࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳࠨສ"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠥࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳࠨຫ")))
            if bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧຬ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥອ") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠦຮ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࠣຯ"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪࠨະ")))
            if bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦັ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦາ") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠧຳ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠢິ"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢີ")))
            if bstack1l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢຶ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧື") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠤࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪࠨຸ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠥࡨࡪࡼࡩࡤࡧູࠥ"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥ຺ࠣ")))
            if bstack1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢົ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧຼ") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨຽ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥ຾"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ຿")))
            if bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨເ") in bstack11l11l1l11_opy_ or bstack1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨແ") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢໂ")] = bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠤໃ"), bstack11l11l1l11_opy_.get(bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤໄ")))
            if bstack1l1_opy_ (u"ࠣࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠥ໅") in bstack11l11l1l11_opy_:
                bstack111l111l1_opy_[bstack1l1_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡘࡤࡶ࡮ࡧࡢ࡭ࡧࡶࠦໆ")] = bstack11l11l1l11_opy_[bstack1l1_opy_ (u"ࠥࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠧ໇")]
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡦࡺࡡ࠻່ࠢࠥ") +  str(error))
        return bstack111l111l1_opy_