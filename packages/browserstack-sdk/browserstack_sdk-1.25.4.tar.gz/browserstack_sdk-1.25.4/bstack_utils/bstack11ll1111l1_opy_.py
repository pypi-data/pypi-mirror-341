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
from browserstack_sdk.bstack1l111lll11_opy_ import bstack1l1l1l1ll1_opy_
from browserstack_sdk.bstack111ll11l1l_opy_ import RobotHandler
def bstack11lll1l111_opy_(framework):
    if framework.lower() == bstack1l1ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᦐ"):
        return bstack1l1l1l1ll1_opy_.version()
    elif framework.lower() == bstack1l1ll11_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ᦑ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1ll11_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨᦒ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1ll11_opy_ (u"ࠩࡸࡲࡰࡴ࡯ࡸࡰࠪᦓ")
def bstack1111111l_opy_():
    import importlib.metadata
    framework_name = []
    framework_version = []
    try:
        from selenium import webdriver
        framework_name.append(bstack1l1ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᦔ"))
        framework_version.append(importlib.metadata.version(bstack1l1ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲࠨᦕ")))
    except:
        pass
    try:
        import playwright
        framework_name.append(bstack1l1ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᦖ"))
        framework_version.append(importlib.metadata.version(bstack1l1ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᦗ")))
    except:
        pass
    return {
        bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᦘ"): bstack1l1ll11_opy_ (u"ࠨࡡࠪᦙ").join(framework_name),
        bstack1l1ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪᦚ"): bstack1l1ll11_opy_ (u"ࠪࡣࠬᦛ").join(framework_version)
    }