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
import re
from typing import List, Dict, Any
from bstack_utils.bstack1l11l11lll_opy_ import get_logger
logger = get_logger(__name__)
class bstack1lllllll1l1_opy_:
    bstack1l1_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡸࡸ࡮ࡲࡩࡵࡻࠣࡱࡪࡺࡨࡰࡦࡶࠤࡹࡵࠠࡴࡧࡷࠤࡦࡴࡤࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡧࡺࡹࡴࡰ࡯ࠣࡸࡦ࡭ࠠ࡮ࡧࡷࡥࡩࡧࡴࡢ࠰ࠍࠤࠥࠦࠠࡊࡶࠣࡱࡦ࡯࡮ࡵࡣ࡬ࡲࡸࠦࡴࡸࡱࠣࡷࡪࡶࡡࡳࡣࡷࡩࠥࡳࡥࡵࡣࡧࡥࡹࡧࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡢࡰࡧࠤࡧࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹ࠮ࠋࠢࠣࠤࠥࡋࡡࡤࡪࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥ࡫࡮ࡵࡴࡼࠤ࡮ࡹࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡷࡳࠥࡨࡥࠡࡵࡷࡶࡺࡩࡴࡶࡴࡨࡨࠥࡧࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢ࡮ࡩࡾࡀࠠࡼࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡧ࡫ࡨࡰࡩࡥࡴࡺࡲࡨࠦ࠿ࠦࠢ࡮ࡷ࡯ࡸ࡮ࡥࡤࡳࡱࡳࡨࡴࡽ࡮ࠣ࠮ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡸࡤࡰࡺ࡫ࡳࠣ࠼ࠣ࡟ࡱ࡯ࡳࡵࠢࡲࡪࠥࡺࡡࡨࠢࡹࡥࡱࡻࡥࡴ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࢁࠏࠦࠠࠡࠢࠥࠦࠧᔙ")
    _1l1111l11ll_opy_: Dict[str, Dict[str, Any]] = {}
    _1l1111l1l1l_opy_: Dict[str, Dict[str, Any]] = {}
    @staticmethod
    def set_custom_tag(bstack11l111ll_opy_: str, key_value: str, bstack1l1111l111l_opy_: bool = False) -> None:
        if not bstack11l111ll_opy_ or not key_value or bstack11l111ll_opy_.strip() == bstack1l1_opy_ (u"ࠧࠨᔚ") or key_value.strip() == bstack1l1_opy_ (u"ࠨࠢᔛ"):
            logger.error(bstack1l1_opy_ (u"ࠢ࡬ࡧࡼࡣࡳࡧ࡭ࡦࠢࡤࡲࡩࠦ࡫ࡦࡻࡢࡺࡦࡲࡵࡦࠢࡰࡹࡸࡺࠠࡣࡧࠣࡲࡴࡴ࠭࡯ࡷ࡯ࡰࠥࡧ࡮ࡥࠢࡱࡳࡳ࠳ࡥ࡮ࡲࡷࡽࠧᔜ"))
        values: List[str] = bstack1lllllll1l1_opy_.bstack1l1111l1lll_opy_(key_value)
        bstack1l1111l1l11_opy_ = {bstack1l1_opy_ (u"ࠣࡨ࡬ࡩࡱࡪ࡟ࡵࡻࡳࡩࠧᔝ"): bstack1l1_opy_ (u"ࠤࡰࡹࡱࡺࡩࡠࡦࡵࡳࡵࡪ࡯ࡸࡰࠥᔞ"), bstack1l1_opy_ (u"ࠥࡺࡦࡲࡵࡦࡵࠥᔟ"): values}
        bstack1l1111l1ll1_opy_ = bstack1lllllll1l1_opy_._1l1111l1l1l_opy_ if bstack1l1111l111l_opy_ else bstack1lllllll1l1_opy_._1l1111l11ll_opy_
        if bstack11l111ll_opy_ in bstack1l1111l1ll1_opy_:
            bstack1l1111l1111_opy_ = bstack1l1111l1ll1_opy_[bstack11l111ll_opy_]
            bstack1l11111lll1_opy_ = bstack1l1111l1111_opy_.get(bstack1l1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࡶࠦᔠ"), [])
            for val in values:
                if val not in bstack1l11111lll1_opy_:
                    bstack1l11111lll1_opy_.append(val)
            bstack1l1111l1111_opy_[bstack1l1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࡷࠧᔡ")] = bstack1l11111lll1_opy_
        else:
            bstack1l1111l1ll1_opy_[bstack11l111ll_opy_] = bstack1l1111l1l11_opy_
    @staticmethod
    def bstack1l11lll1lll_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllllll1l1_opy_._1l1111l11ll_opy_
    @staticmethod
    def bstack1l1111l11l1_opy_() -> Dict[str, Dict[str, Any]]:
        return bstack1lllllll1l1_opy_._1l1111l1l1l_opy_
    @staticmethod
    def bstack1l1111l1lll_opy_(bstack1l11111llll_opy_: str) -> List[str]:
        bstack1l1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡗࡵࡲࡩࡵࡵࠣࡸ࡭࡫ࠠࡪࡰࡳࡹࡹࠦࡳࡵࡴ࡬ࡲ࡬ࠦࡢࡺࠢࡦࡳࡲࡳࡡࡴࠢࡺ࡬࡮ࡲࡥࠡࡴࡨࡷࡵ࡫ࡣࡵ࡫ࡱ࡫ࠥࡪ࡯ࡶࡤ࡯ࡩ࠲ࡷࡵࡰࡶࡨࡨࠥࡹࡵࡣࡵࡷࡶ࡮ࡴࡧࡴ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡧࡻࡥࡲࡶ࡬ࡦ࠼ࠣࠫࡦ࠲ࠠࠣࡤ࠯ࡧࠧ࠲ࠠࡥࠩࠣ࠱ࡃ࡛ࠦࠨࡣࠪ࠰ࠥ࠭ࡢ࠭ࡥࠪ࠰ࠥ࠭ࡤࠨ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᔢ")
        pattern = re.compile(bstack1l1_opy_ (u"ࡲࠨࠤࠫ࡟ࡣࠨ࡝ࠫࠫࠥࢀ࠭ࡡ࡞࠭࡟࠮࠭ࠬᔣ"))
        result = []
        for match in pattern.finditer(bstack1l11111llll_opy_):
            if match.group(1) is not None:
                result.append(match.group(1).strip())
            elif match.group(2) is not None:
                result.append(match.group(2).strip())
        return result
    def __new__(cls, *args, **kwargs):
        raise Exception(bstack1l1_opy_ (u"ࠣࡗࡷ࡭ࡱ࡯ࡴࡺࠢࡦࡰࡦࡹࡳࠡࡵ࡫ࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡵ࡫ࡤࡸࡪࡪࠢᔤ"))