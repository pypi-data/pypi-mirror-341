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
from browserstack_sdk.bstack1l1ll1l111_opy_ import bstack111111l11_opy_
from browserstack_sdk.bstack111l11l1ll_opy_ import RobotHandler
def bstack1l1lll11ll_opy_(framework):
    if framework.lower() == bstack1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᦏ"):
        return bstack111111l11_opy_.version()
    elif framework.lower() == bstack1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬᦐ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1_opy_ (u"ࠧࡣࡧ࡫ࡥࡻ࡫ࠧᦑ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1_opy_ (u"ࠨࡷࡱ࡯ࡳࡵࡷ࡯ࠩᦒ")
def bstack11l1l1l1ll_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᦓ"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱࠧᦔ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᦕ"))
        framework_version.append(importlib.metadata.version(bstack1l1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᦖ")))
    except:
        pass
    return {
        bstack1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᦗ"): bstack1l1_opy_ (u"ࠧࡠࠩᦘ").join(framework_name),
        bstack1l1_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࠩᦙ"): bstack1l1_opy_ (u"ࠩࡢࠫᦚ").join(framework_version)
    }