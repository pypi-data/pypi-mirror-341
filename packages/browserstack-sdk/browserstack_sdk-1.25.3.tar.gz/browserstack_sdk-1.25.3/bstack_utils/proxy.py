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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack11l111l1l11_opy_
bstack11llllll1_opy_ = Config.bstack111111ll_opy_()
def bstack111l1ll1l11_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack111l1ll11l1_opy_(bstack111l1ll1ll1_opy_, bstack111l1lll111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack111l1ll1ll1_opy_):
        with open(bstack111l1ll1ll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack111l1ll1l11_opy_(bstack111l1ll1ll1_opy_):
        pac = get_pac(url=bstack111l1ll1ll1_opy_)
    else:
        raise Exception(bstack1l1_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᴁ").format(bstack111l1ll1ll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᴂ"), 80))
        bstack111l1ll1l1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack111l1ll1l1l_opy_ = bstack1l1_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᴃ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack111l1lll111_opy_, bstack111l1ll1l1l_opy_)
    return proxy_url
def bstack11l11l1ll1_opy_(config):
    return bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᴄ") in config or bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᴅ") in config
def bstack1lll11l111_opy_(config):
    if not bstack11l11l1ll1_opy_(config):
        return
    if config.get(bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᴆ")):
        return config.get(bstack1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᴇ"))
    if config.get(bstack1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᴈ")):
        return config.get(bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᴉ"))
def bstack11ll1llll_opy_(config, bstack111l1lll111_opy_):
    proxy = bstack1lll11l111_opy_(config)
    proxies = {}
    if config.get(bstack1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᴊ")) or config.get(bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᴋ")):
        if proxy.endswith(bstack1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᴌ")):
            proxies = bstack1l111ll1_opy_(proxy, bstack111l1lll111_opy_)
        else:
            proxies = {
                bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴍ"): proxy
            }
    bstack11llllll1_opy_.bstack1llllll1l1_opy_(bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᴎ"), proxies)
    return proxies
def bstack1l111ll1_opy_(bstack111l1ll1ll1_opy_, bstack111l1lll111_opy_):
    proxies = {}
    global bstack111l1ll11ll_opy_
    if bstack1l1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᴏ") in globals():
        return bstack111l1ll11ll_opy_
    try:
        proxy = bstack111l1ll11l1_opy_(bstack111l1ll1ll1_opy_, bstack111l1lll111_opy_)
        if bstack1l1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᴐ") in proxy:
            proxies = {}
        elif bstack1l1_opy_ (u"ࠢࡉࡖࡗࡔࠧᴑ") in proxy or bstack1l1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᴒ") in proxy or bstack1l1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᴓ") in proxy:
            bstack111l1ll1lll_opy_ = proxy.split(bstack1l1_opy_ (u"ࠥࠤࠧᴔ"))
            if bstack1l1_opy_ (u"ࠦ࠿࠵࠯ࠣᴕ") in bstack1l1_opy_ (u"ࠧࠨᴖ").join(bstack111l1ll1lll_opy_[1:]):
                proxies = {
                    bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴗ"): bstack1l1_opy_ (u"ࠢࠣᴘ").join(bstack111l1ll1lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴙ"): str(bstack111l1ll1lll_opy_[0]).lower() + bstack1l1_opy_ (u"ࠤ࠽࠳࠴ࠨᴚ") + bstack1l1_opy_ (u"ࠥࠦᴛ").join(bstack111l1ll1lll_opy_[1:])
                }
        elif bstack1l1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᴜ") in proxy:
            bstack111l1ll1lll_opy_ = proxy.split(bstack1l1_opy_ (u"ࠧࠦࠢᴝ"))
            if bstack1l1_opy_ (u"ࠨ࠺࠰࠱ࠥᴞ") in bstack1l1_opy_ (u"ࠢࠣᴟ").join(bstack111l1ll1lll_opy_[1:]):
                proxies = {
                    bstack1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᴠ"): bstack1l1_opy_ (u"ࠤࠥᴡ").join(bstack111l1ll1lll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᴢ"): bstack1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᴣ") + bstack1l1_opy_ (u"ࠧࠨᴤ").join(bstack111l1ll1lll_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᴥ"): proxy
            }
    except Exception as e:
        print(bstack1l1_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᴦ"), bstack11l111l1l11_opy_.format(bstack111l1ll1ll1_opy_, str(e)))
    bstack111l1ll11ll_opy_ = proxies
    return proxies