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
from bstack_utils.bstack11ll11l1ll_opy_ import bstack111l1l1l11l_opy_
def bstack111l1l1llll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴨ")):
        return bstack1l1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᴩ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡸ࡫ࡴࡶࡲࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴪ")):
        return bstack1l1ll11_opy_ (u"ࠬࡹࡥࡵࡷࡳ࠱ࡲࡵࡤࡶ࡮ࡨࠫᴫ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴬ")):
        return bstack1l1ll11_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯࠯ࡩࡹࡳࡩࡴࡪࡱࡱࠫᴭ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭ᴮ")):
        return bstack1l1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᴯ")
def bstack111l1l1l1ll_opy_(fixture_name):
    return bool(re.match(bstack1l1ll11_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟ࠩࡨࡸࡲࡨࡺࡩࡰࡰࡿࡱࡴࡪࡵ࡭ࡧࠬࡣ࡫࡯ࡸࡵࡷࡵࡩࡤ࠴ࠪࠨᴰ"), fixture_name))
def bstack111l1l11ll1_opy_(fixture_name):
    return bool(re.match(bstack1l1ll11_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᴱ"), fixture_name))
def bstack111l1l11lll_opy_(fixture_name):
    return bool(re.match(bstack1l1ll11_opy_ (u"ࠬࡤ࡟ࡹࡷࡱ࡭ࡹࡥࠨࡴࡧࡷࡹࡵࢂࡴࡦࡣࡵࡨࡴࡽ࡮ࠪࡡࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࡡ࠱࠮ࠬᴲ"), fixture_name))
def bstack111l1l1l111_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1ll11_opy_ (u"࠭࡟ࡹࡷࡱ࡭ࡹࡥࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴳ")):
        return bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠳ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᴴ"), bstack1l1ll11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᴵ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠩࡢࡼࡺࡴࡩࡵࡡࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴶ")):
        return bstack1l1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱ࠯ࡰࡳࡩࡻ࡬ࡦࠩᴷ"), bstack1l1ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᴸ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴹ")):
        return bstack1l1ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᴺ"), bstack1l1ll11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᴻ")
    elif fixture_name.startswith(bstack1l1ll11_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᴼ")):
        return bstack1l1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱ࠱ࡲࡵࡤࡶ࡮ࡨࠫᴽ"), bstack1l1ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᴾ")
    return None, None
def bstack111l1ll111l_opy_(hook_name):
    if hook_name in [bstack1l1ll11_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࠪᴿ"), bstack1l1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴࠧᵀ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1ll1111_opy_(hook_name):
    if hook_name in [bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᵁ"), bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᵂ")]:
        return bstack1l1ll11_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᵃ")
    elif hook_name in [bstack1l1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡲࡨࡺࡲࡥࠨᵄ"), bstack1l1ll11_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠨᵅ")]:
        return bstack1l1ll11_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌࠨᵆ")
    elif hook_name in [bstack1l1ll11_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᵇ"), bstack1l1ll11_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࡠ࡯ࡨࡸ࡭ࡵࡤࠨᵈ")]:
        return bstack1l1ll11_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᵉ")
    elif hook_name in [bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠪᵊ"), bstack1l1ll11_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪᵋ")]:
        return bstack1l1ll11_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠭ᵌ")
    return hook_name
def bstack111l1l11l1l_opy_(node, scenario):
    if hasattr(node, bstack1l1ll11_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᵍ")):
        parts = node.nodeid.rsplit(bstack1l1ll11_opy_ (u"ࠧࡡࠢᵎ"))
        params = parts[-1]
        return bstack1l1ll11_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᵏ").format(scenario.name, params)
    return scenario.name
def bstack111l1l1l1l1_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1ll11_opy_ (u"ࠧࡤࡣ࡯ࡰࡸࡶࡥࡤࠩᵐ")):
            examples = list(node.callspec.params[bstack1l1ll11_opy_ (u"ࠨࡡࡳࡽࡹ࡫ࡳࡵࡡࡥࡨࡩࡥࡥࡹࡣࡰࡴࡱ࡫ࠧᵑ")].values())
        return examples
    except:
        return []
def bstack111l1l1lll1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l1ll1l_opy_(report):
    try:
        status = bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᵒ")
        if report.passed or (report.failed and hasattr(report, bstack1l1ll11_opy_ (u"ࠥࡻࡦࡹࡸࡧࡣ࡬ࡰࠧᵓ"))):
            status = bstack1l1ll11_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᵔ")
        elif report.skipped:
            status = bstack1l1ll11_opy_ (u"ࠬࡹ࡫ࡪࡲࡳࡩࡩ࠭ᵕ")
        bstack111l1l1l11l_opy_(status)
    except:
        pass
def bstack1lllll11ll_opy_(status):
    try:
        bstack111l1l1ll11_opy_ = bstack1l1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᵖ")
        if status == bstack1l1ll11_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᵗ"):
            bstack111l1l1ll11_opy_ = bstack1l1ll11_opy_ (u"ࠨࡲࡤࡷࡸ࡫ࡤࠨᵘ")
        elif status == bstack1l1ll11_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᵙ"):
            bstack111l1l1ll11_opy_ = bstack1l1ll11_opy_ (u"ࠪࡷࡰ࡯ࡰࡱࡧࡧࠫᵚ")
        bstack111l1l1l11l_opy_(bstack111l1l1ll11_opy_)
    except:
        pass
def bstack111l1l11l11_opy_(item=None, report=None, summary=None, extra=None):
    return