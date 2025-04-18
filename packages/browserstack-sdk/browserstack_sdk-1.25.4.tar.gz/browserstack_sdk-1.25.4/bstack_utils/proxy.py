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
import os
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111l1111_opy_
bstack11llllllll_opy_ = Config.bstack1l1111llll_opy_()
def bstack111l1ll11ll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll1l11_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll1lll_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1ll1_opy_):
        with open(bstack111l1ll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll11ll_opy_(bstack111l1ll1ll1_opy_):
        pac = get_pac(url=bstack111l1ll1ll1_opy_)
    else:
        raise Exception(bstack1l1ll11_opy_ (u"࠭ࡐࡢࡥࠣࡪ࡮ࡲࡥࠡࡦࡲࡩࡸࠦ࡮ࡰࡶࠣࡩࡽ࡯ࡳࡵ࠼ࠣࡿࢂ࠭ᴂ").format(bstack111l1ll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1ll11_opy_ (u"ࠢ࠹࠰࠻࠲࠽࠴࠸ࠣᴃ"), 80))
        bstack111l1ll1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l1l_opy_ = bstack1l1ll11_opy_ (u"ࠨ࠲࠱࠴࠳࠶࠮࠱ࠩᴄ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1ll1lll_opy_, bstack111l1ll1l1l_opy_)
    return proxy_url
def bstack1lll1l1ll1_opy_(config):
    return bstack1l1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡐࡳࡱࡻࡽࠬᴅ") in config or bstack1l1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧᴆ") in config
def bstack1lll1l1l_opy_(config):
    if not bstack1lll1l1ll1_opy_(config):
        return
    if config.get(bstack1l1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴇ")):
        return config.get(bstack1l1ll11_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᴈ"))
    if config.get(bstack1l1ll11_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴉ")):
        return config.get(bstack1l1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᴊ"))
def bstack1l1lll11l1_opy_(config, bstack111l1ll1lll_opy_):
    proxy = bstack1lll1l1l_opy_(config)
    proxies = {}
    if config.get(bstack1l1ll11_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴋ")) or config.get(bstack1l1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴌ")):
        if proxy.endswith(bstack1l1ll11_opy_ (u"ࠪ࠲ࡵࡧࡣࠨᴍ")):
            proxies = bstack1l1lll111l_opy_(proxy, bstack111l1ll1lll_opy_)
        else:
            proxies = {
                bstack1l1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴎ"): proxy
            }
    bstack11llllllll_opy_.bstack1l1ll11l_opy_(bstack1l1ll11_opy_ (u"ࠬࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠬᴏ"), proxies)
    return proxies
def bstack1l1lll111l_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll1lll_opy_):
    proxies = {}
    global bstack111l1ll11l1_opy_
    if bstack1l1ll11_opy_ (u"࠭ࡐࡂࡅࡢࡔࡗࡕࡘ࡚ࠩᴐ") in globals():
        return bstack111l1ll11l1_opy_
    try:
        proxy = bstack111l1ll1l11_opy_(bstack111l1ll1ll1_opy_, bstack111l1ll1lll_opy_)
        if bstack1l1ll11_opy_ (u"ࠢࡅࡋࡕࡉࡈ࡚ࠢᴑ") in proxy:
            proxies = {}
        elif bstack1l1ll11_opy_ (u"ࠣࡊࡗࡘࡕࠨᴒ") in proxy or bstack1l1ll11_opy_ (u"ࠤࡋࡘ࡙ࡖࡓࠣᴓ") in proxy or bstack1l1ll11_opy_ (u"ࠥࡗࡔࡉࡋࡔࠤᴔ") in proxy:
            bstack111l1lll111_opy_ = proxy.split(bstack1l1ll11_opy_ (u"ࠦࠥࠨᴕ"))
            if bstack1l1ll11_opy_ (u"ࠧࡀ࠯࠰ࠤᴖ") in bstack1l1ll11_opy_ (u"ࠨࠢᴗ").join(bstack111l1lll111_opy_[1:]):
                proxies = {
                    bstack1l1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴘ"): bstack1l1ll11_opy_ (u"ࠣࠤᴙ").join(bstack111l1lll111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴚ"): str(bstack111l1lll111_opy_[0]).lower() + bstack1l1ll11_opy_ (u"ࠥ࠾࠴࠵ࠢᴛ") + bstack1l1ll11_opy_ (u"ࠦࠧᴜ").join(bstack111l1lll111_opy_[1:])
                }
        elif bstack1l1ll11_opy_ (u"ࠧࡖࡒࡐ࡚࡜ࠦᴝ") in proxy:
            bstack111l1lll111_opy_ = proxy.split(bstack1l1ll11_opy_ (u"ࠨࠠࠣᴞ"))
            if bstack1l1ll11_opy_ (u"ࠢ࠻࠱࠲ࠦᴟ") in bstack1l1ll11_opy_ (u"ࠣࠤᴠ").join(bstack111l1lll111_opy_[1:]):
                proxies = {
                    bstack1l1ll11_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᴡ"): bstack1l1ll11_opy_ (u"ࠥࠦᴢ").join(bstack111l1lll111_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1ll11_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᴣ"): bstack1l1ll11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࠨᴤ") + bstack1l1ll11_opy_ (u"ࠨࠢᴥ").join(bstack111l1lll111_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1ll11_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭ᴦ"): proxy
            }
    except Exception as e:
        print(bstack1l1ll11_opy_ (u"ࠣࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧᴧ"), bstack11l111l1111_opy_.format(bstack111l1ll1ll1_opy_, str(e)))
    bstack111l1ll11l1_opy_ = proxies
    return proxies