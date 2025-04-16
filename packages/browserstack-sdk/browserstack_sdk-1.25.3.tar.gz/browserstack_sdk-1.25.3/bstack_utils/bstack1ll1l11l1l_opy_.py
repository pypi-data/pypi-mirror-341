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
from bstack_utils.bstack111lll1l_opy_ import bstack111l1l1l111_opy_
def bstack111l1l11lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴧ")):
        return bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᴨ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴩ")):
        return bstack1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᴪ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴫ")):
        return bstack1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᴬ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᴭ")):
        return bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᴮ")
def bstack111l1ll111l_opy_(fixture_name):
    return bool(re.match(bstack1l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᴯ"), fixture_name))
def bstack111l1l11ll1_opy_(fixture_name):
    return bool(re.match(bstack1l1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᴰ"), fixture_name))
def bstack111l1l1l1ll_opy_(fixture_name):
    return bool(re.match(bstack1l1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᴱ"), fixture_name))
def bstack111l1l1llll_opy_(fixture_name):
    if fixture_name.startswith(bstack1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᴲ")):
        return bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᴳ"), bstack1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᴴ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᴵ")):
        return bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᴶ"), bstack1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᴷ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᴸ")):
        return bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᴹ"), bstack1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᴺ")
    elif fixture_name.startswith(bstack1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᴻ")):
        return bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᴼ"), bstack1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᴽ")
    return None, None
def bstack111l1l1lll1_opy_(hook_name):
    if hook_name in [bstack1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᴾ"), bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᴿ")]:
        return hook_name.capitalize()
    return hook_name
def bstack111l1l1ll1l_opy_(hook_name):
    if hook_name in [bstack1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᵀ"), bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᵁ")]:
        return bstack1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᵂ")
    elif hook_name in [bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᵃ"), bstack1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᵄ")]:
        return bstack1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᵅ")
    elif hook_name in [bstack1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᵆ"), bstack1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᵇ")]:
        return bstack1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᵈ")
    elif hook_name in [bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᵉ"), bstack1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᵊ")]:
        return bstack1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᵋ")
    return hook_name
def bstack111l1l1l11l_opy_(node, scenario):
    if hasattr(node, bstack1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᵌ")):
        parts = node.nodeid.rsplit(bstack1l1_opy_ (u"ࠦࡠࠨᵍ"))
        params = parts[-1]
        return bstack1l1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᵎ").format(scenario.name, params)
    return scenario.name
def bstack111l1ll1111_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᵏ")):
            examples = list(node.callspec.params[bstack1l1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᵐ")].values())
        return examples
    except:
        return []
def bstack111l1l1l1l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack111l1l11l11_opy_(report):
    try:
        status = bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᵑ")
        if report.passed or (report.failed and hasattr(report, bstack1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᵒ"))):
            status = bstack1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᵓ")
        elif report.skipped:
            status = bstack1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᵔ")
        bstack111l1l1l111_opy_(status)
    except:
        pass
def bstack11lll1l1ll_opy_(status):
    try:
        bstack111l1l11l1l_opy_ = bstack1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᵕ")
        if status == bstack1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᵖ"):
            bstack111l1l11l1l_opy_ = bstack1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᵗ")
        elif status == bstack1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᵘ"):
            bstack111l1l11l1l_opy_ = bstack1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᵙ")
        bstack111l1l1l111_opy_(bstack111l1l11l1l_opy_)
    except:
        pass
def bstack111l1l1ll11_opy_(item=None, report=None, summary=None, extra=None):
    return