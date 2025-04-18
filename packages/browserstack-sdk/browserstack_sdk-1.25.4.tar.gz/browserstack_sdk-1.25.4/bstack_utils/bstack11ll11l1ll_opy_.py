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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll11lll1l_opy_, bstack11111111l_opy_, bstack1lllll11_opy_, bstack1llllllll_opy_, \
    bstack11l1l1l1111_opy_
from bstack_utils.measure import measure
def bstack11ll11l111_opy_(bstack111l111llll_opy_):
    for driver in bstack111l111llll_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
@measure(event_name=EVENTS.bstack1l1ll11111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
def bstack11lll1lll_opy_(driver, status, reason=bstack1l1ll11_opy_ (u"ࠧࠨᵳ")):
    bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
    if bstack11llllllll_opy_.bstack1111lllll1_opy_():
        return
    bstack111l1ll1_opy_ = bstack1lll11l111_opy_(bstack1l1ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᵴ"), bstack1l1ll11_opy_ (u"ࠩࠪᵵ"), status, reason, bstack1l1ll11_opy_ (u"ࠪࠫᵶ"), bstack1l1ll11_opy_ (u"ࠫࠬᵷ"))
    driver.execute_script(bstack111l1ll1_opy_)
@measure(event_name=EVENTS.bstack1l1ll11111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
def bstack11l1ll1l1l_opy_(page, status, reason=bstack1l1ll11_opy_ (u"ࠬ࠭ᵸ")):
    try:
        if page is None:
            return
        bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
        if bstack11llllllll_opy_.bstack1111lllll1_opy_():
            return
        bstack111l1ll1_opy_ = bstack1lll11l111_opy_(bstack1l1ll11_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᵹ"), bstack1l1ll11_opy_ (u"ࠧࠨᵺ"), status, reason, bstack1l1ll11_opy_ (u"ࠨࠩᵻ"), bstack1l1ll11_opy_ (u"ࠩࠪᵼ"))
        page.evaluate(bstack1l1ll11_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦᵽ"), bstack111l1ll1_opy_)
    except Exception as e:
        print(bstack1l1ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡻࡾࠤᵾ"), e)
def bstack1lll11l111_opy_(type, name, status, reason, bstack1l1l1ll111_opy_, bstack1ll1l11l_opy_):
    bstack1l1ll11l1l_opy_ = {
        bstack1l1ll11_opy_ (u"ࠬࡧࡣࡵ࡫ࡲࡲࠬᵿ"): type,
        bstack1l1ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶀ"): {}
    }
    if type == bstack1l1ll11_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᶁ"):
        bstack1l1ll11l1l_opy_[bstack1l1ll11_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᶂ")][bstack1l1ll11_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᶃ")] = bstack1l1l1ll111_opy_
        bstack1l1ll11l1l_opy_[bstack1l1ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᶄ")][bstack1l1ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩᶅ")] = json.dumps(str(bstack1ll1l11l_opy_))
    if type == bstack1l1ll11_opy_ (u"ࠬࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᶆ"):
        bstack1l1ll11l1l_opy_[bstack1l1ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶇ")][bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᶈ")] = name
    if type == bstack1l1ll11_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫᶉ"):
        bstack1l1ll11l1l_opy_[bstack1l1ll11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᶊ")][bstack1l1ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᶋ")] = status
        if status == bstack1l1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᶌ") and str(reason) != bstack1l1ll11_opy_ (u"ࠧࠨᶍ"):
            bstack1l1ll11l1l_opy_[bstack1l1ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᶎ")][bstack1l1ll11_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᶏ")] = json.dumps(str(reason))
    bstack1l1llll11l_opy_ = bstack1l1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭ᶐ").format(json.dumps(bstack1l1ll11l1l_opy_))
    return bstack1l1llll11l_opy_
def bstack1l1l1l1111_opy_(url, config, logger, bstack1llll11l11_opy_=False):
    hostname = bstack11111111l_opy_(url)
    is_private = bstack1llllllll_opy_(hostname)
    try:
        if is_private or bstack1llll11l11_opy_:
            file_path = bstack11ll11lll1l_opy_(bstack1l1ll11_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩᶑ"), bstack1l1ll11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᶒ"), logger)
            if os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡑࡓ࡙ࡥࡓࡆࡖࡢࡉࡗࡘࡏࡓࠩᶓ")) and eval(
                    os.environ.get(bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᶔ"))):
                return
            if (bstack1l1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪᶕ") in config and not config[bstack1l1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᶖ")]):
                os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡍࡑࡆࡅࡑࡥࡎࡐࡖࡢࡗࡊ࡚࡟ࡆࡔࡕࡓࡗ࠭ᶗ")] = str(True)
                bstack111l111ll11_opy_ = {bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡮ࡢ࡯ࡨࠫᶘ"): hostname}
                bstack11l1l1l1111_opy_(bstack1l1ll11_opy_ (u"ࠪ࠲ࡧࡹࡴࡢࡥ࡮࠱ࡨࡵ࡮ࡧ࡫ࡪ࠲࡯ࡹ࡯࡯ࠩᶙ"), bstack1l1ll11_opy_ (u"ࠫࡳࡻࡤࡨࡧࡢࡰࡴࡩࡡ࡭ࠩᶚ"), bstack111l111ll11_opy_, logger)
    except Exception as e:
        pass
def bstack1l1l111l_opy_(caps, bstack111l111ll1l_opy_):
    if bstack1l1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᶛ") in caps:
        caps[bstack1l1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᶜ")][bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࠭ᶝ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack1l1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᶞ")][bstack1l1ll11_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᶟ")] = bstack111l111ll1l_opy_
    else:
        caps[bstack1l1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨᶠ")] = True
        if bstack111l111ll1l_opy_:
            caps[bstack1l1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᶡ")] = bstack111l111ll1l_opy_
def bstack111l1l1l11l_opy_(bstack111ll1l1l1_opy_):
    bstack111l111lll1_opy_ = bstack1lllll11_opy_(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡖࡸࡦࡺࡵࡴࠩᶢ"), bstack1l1ll11_opy_ (u"࠭ࠧᶣ"))
    if bstack111l111lll1_opy_ == bstack1l1ll11_opy_ (u"ࠧࠨᶤ") or bstack111l111lll1_opy_ == bstack1l1ll11_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᶥ"):
        threading.current_thread().testStatus = bstack111ll1l1l1_opy_
    else:
        if bstack111ll1l1l1_opy_ == bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᶦ"):
            threading.current_thread().testStatus = bstack111ll1l1l1_opy_