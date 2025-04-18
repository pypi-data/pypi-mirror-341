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
import re
from typing import List, Dict, Any
from bstack_utils.bstack111l1l111_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lll111lll1_opy_:
    bstack1l1ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࡉࡵࡴࡶࡲࡱ࡙ࡧࡧࡎࡣࡱࡥ࡬࡫ࡲࠡࡲࡵࡳࡻ࡯ࡤࡦࡵࠣࡹࡹ࡯࡬ࡪࡶࡼࠤࡲ࡫ࡴࡩࡱࡧࡷࠥࡺ࡯ࠡࡵࡨࡸࠥࡧ࡮ࡥࠢࡵࡩࡹࡸࡩࡦࡸࡨࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࠡ࡯ࡨࡸࡦࡪࡡࡵࡣ࠱ࠎࠥࠦࠠࠡࡋࡷࠤࡲࡧࡩ࡯ࡶࡤ࡭ࡳࡹࠠࡵࡹࡲࠤࡸ࡫ࡰࡢࡴࡤࡸࡪࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵ࡭ࡪࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡱࡨࠥࡨࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࡳ࠯ࠌࠣࠤࠥࠦࡅࡢࡥ࡫ࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡥ࡯ࡶࡵࡽࠥ࡯ࡳࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࡸࡴࠦࡢࡦࠢࡶࡸࡷࡻࡣࡵࡷࡵࡩࡩࠦࡡࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣ࡯ࡪࡿ࠺ࠡࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧࡀࠠࠣ࡯ࡸࡰࡹ࡯࡟ࡥࡴࡲࡴࡩࡵࡷ࡯ࠤ࠯ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤࡹࡥࡱࡻࡥࡴࠤ࠽ࠤࡠࡲࡩࡴࡶࠣࡳ࡫ࠦࡴࡢࡩࠣࡺࡦࡲࡵࡦࡵࡠࠎࠥࠦࠠࠡࠢࠣࠤࢂࠐࠠࠡࠢࠣࠦࠧࠨᔚ")
    _1l1111l111l_opy_: Dict[str, Dict[str, Any]] = {}
    _1l11111llll_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack111l1l1ll_opy_: str, key_value: str, bstack1l1111l1ll1_opy_: bool = False) -> None:
        if not bstack111l1l1ll_opy_ or not key_value or bstack111l1l1ll_opy_.strip() == bstack1l1ll11_opy_ (u"ࠨࠢᔛ") or key_value.strip() == bstack1l1ll11_opy_ (u"ࠢࠣᔜ"):
            logger.error(bstack1l1ll11_opy_ (u"ࠣ࡭ࡨࡽࡤࡴࡡ࡮ࡧࠣࡥࡳࡪࠠ࡬ࡧࡼࡣࡻࡧ࡬ࡶࡧࠣࡱࡺࡹࡴࠡࡤࡨࠤࡳࡵ࡮࠮ࡰࡸࡰࡱࠦࡡ࡯ࡦࠣࡲࡴࡴ࠭ࡦ࡯ࡳࡸࡾࠨᔝ"))
        values: List[str] = bstack1lll111lll1_opy_.bstack1l1111l1111_opy_(key_value)
        bstack1l1111l1lll_opy_ = {bstack1l1ll11_opy_ (u"ࠤࡩ࡭ࡪࡲࡤࡠࡶࡼࡴࡪࠨᔞ"): bstack1l1ll11_opy_ (u"ࠥࡱࡺࡲࡴࡪࡡࡧࡶࡴࡶࡤࡰࡹࡱࠦᔟ"), bstack1l1ll11_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᔠ"): values}
        bstack1l1111l11l1_opy_ = bstack1lll111lll1_opy_._1l11111llll_opy_ if bstack1l1111l1ll1_opy_ else bstack1lll111lll1_opy_._1l1111l111l_opy_
        if bstack111l1l1ll_opy_ in bstack1l1111l11l1_opy_:
            bstack1l11111lll1_opy_ = bstack1l1111l11l1_opy_[bstack111l1l1ll_opy_]
            bstack1l1111l1l11_opy_ = bstack1l11111lll1_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᔡ"), [])
            for val in values:
                if val not in bstack1l1111l1l11_opy_:
                    bstack1l1111l1l11_opy_.append(val)
            bstack1l11111lll1_opy_[bstack1l1ll11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࡸࠨᔢ")] = bstack1l1111l1l11_opy_
        else:
            bstack1l1111l11l1_opy_[bstack111l1l1ll_opy_] = bstack1l1111l1lll_opy_
    @staticmethod
    def bstack1l11l111ll1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll111lll1_opy_._1l1111l111l_opy_
    @staticmethod
    def bstack1l1111l1l1l_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lll111lll1_opy_._1l11111llll_opy_
    @staticmethod
    def bstack1l1111l1111_opy_(bstack1l1111l11ll_opy_: str) -> List[str]:
        bstack1l1ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡶ࡬ࡪࡶࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡴࡺࡺࠠࡴࡶࡵ࡭ࡳ࡭ࠠࡣࡻࠣࡧࡴࡳ࡭ࡢࡵࠣࡻ࡭࡯࡬ࡦࠢࡵࡩࡸࡶࡥࡤࡶ࡬ࡲ࡬ࠦࡤࡰࡷࡥࡰࡪ࠳ࡱࡶࡱࡷࡩࡩࠦࡳࡶࡤࡶࡸࡷ࡯࡮ࡨࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡨࡼࡦࡳࡰ࡭ࡧ࠽ࠤࠬࡧࠬࠡࠤࡥ࠰ࡨࠨࠬࠡࡦࠪࠤ࠲ࡄࠠ࡜ࠩࡤࠫ࠱ࠦࠧࡣ࠮ࡦࠫ࠱ࠦࠧࡥࠩࡠࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᔣ")
        pattern = re.compile(bstack1l1ll11_opy_ (u"ࡳࠩࠥࠬࡠࡤࠢ࡞ࠬࠬࠦࢁ࠮࡛࡟࠮ࡠ࠯࠮࠭ᔤ"))
        result = []
        for match in pattern.finditer(bstack1l1111l11ll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l1ll11_opy_ (u"ࠤࡘࡸ࡮ࡲࡩࡵࡻࠣࡧࡱࡧࡳࡴࠢࡶ࡬ࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡶ࡬ࡥࡹ࡫ࡤࠣᔥ"))