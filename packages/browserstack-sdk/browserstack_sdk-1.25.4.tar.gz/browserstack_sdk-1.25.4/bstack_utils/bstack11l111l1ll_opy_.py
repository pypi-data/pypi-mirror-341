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
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11llll11ll1_opy_, bstack11lllll111l_opy_, bstack1l1ll11lll_opy_, bstack111l11ll1l_opy_, bstack11l1lllll11_opy_, bstack11l1l1l1ll1_opy_, bstack11l1lllll1l_opy_, bstack1l11111ll_opy_, bstack1lllll11_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l11lll1l_opy_ import bstack111l1l1111l_opy_
import bstack_utils.bstack111lllll1_opy_ as bstack111111l1_opy_
from bstack_utils.bstack11l111ll1l_opy_ import bstack1l1llll11_opy_
import bstack_utils.accessibility as bstack1ll11llll1_opy_
from bstack_utils.bstack11ll1l11ll_opy_ import bstack11ll1l11ll_opy_
from bstack_utils.bstack11l111lll1_opy_ import bstack111ll11111_opy_
bstack1111ll111l1_opy_ = bstack1l1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࡨࡵ࡬࡭ࡧࡦࡸࡴࡸ࠭ࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿ࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᷦ")
logger = logging.getLogger(__name__)
class bstack111l111ll_opy_:
    bstack111l11lll1l_opy_ = None
    bs_config = None
    bstack1l1llllll1_opy_ = None
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1l1111l_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def launch(cls, bs_config, bstack1l1llllll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l1llllll1_opy_ = bstack1l1llllll1_opy_
        try:
            cls.bstack1111ll11ll1_opy_()
            bstack11llll111l1_opy_ = bstack11llll11ll1_opy_(bs_config)
            bstack11lllll1111_opy_ = bstack11lllll111l_opy_(bs_config)
            data = bstack111111l1_opy_.bstack1111ll11lll_opy_(bs_config, bstack1l1llllll1_opy_)
            config = {
                bstack1l1ll11_opy_ (u"ࠫࡦࡻࡴࡩࠩᷧ"): (bstack11llll111l1_opy_, bstack11lllll1111_opy_),
                bstack1l1ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᷨ"): cls.default_headers()
            }
            response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"࠭ࡐࡐࡕࡗࠫᷩ"), cls.request_url(bstack1l1ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠸࠯ࡣࡷ࡬ࡰࡩࡹࠧᷪ")), data, config)
            if response.status_code != 200:
                bstack1lllll111l1_opy_ = response.json()
                if bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᷫ")] == False:
                    cls.bstack1111ll1111l_opy_(bstack1lllll111l1_opy_)
                    return
                cls.bstack1111lll1l1l_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᷬ")])
                cls.bstack1111ll11l1l_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᷭ")])
                return None
            bstack1111ll11l11_opy_ = cls.bstack1111llll11l_opy_(response)
            return bstack1111ll11l11_opy_
        except Exception as error:
            logger.error(bstack1l1ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡤࡸ࡭ࡱࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡻࡾࠤᷮ").format(str(error)))
            return None
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def stop(cls, bstack1111ll1ll11_opy_=None):
        if not bstack1l1llll11_opy_.on() and not bstack1ll11llll1_opy_.on():
            return
        if os.environ.get(bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᷯ")) == bstack1l1ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᷰ") or os.environ.get(bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᷱ")) == bstack1l1ll11_opy_ (u"ࠣࡰࡸࡰࡱࠨᷲ"):
            logger.error(bstack1l1ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᷳ"))
            return {
                bstack1l1ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᷴ"): bstack1l1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᷵"),
                bstack1l1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᷶"): bstack1l1ll11_opy_ (u"࠭ࡔࡰ࡭ࡨࡲ࠴ࡨࡵࡪ࡮ࡧࡍࡉࠦࡩࡴࠢࡸࡲࡩ࡫ࡦࡪࡰࡨࡨ࠱ࠦࡢࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠ࡮࡫ࡪ࡬ࡹࠦࡨࡢࡸࡨࠤ࡫ࡧࡩ࡭ࡧࡧ᷷ࠫ")
            }
        try:
            cls.bstack111l11lll1l_opy_.shutdown()
            data = {
                bstack1l1ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ᷸ࠬ"): bstack1l11111ll_opy_()
            }
            if not bstack1111ll1ll11_opy_ is None:
                data[bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡱࡪࡺࡡࡥࡣࡷࡥ᷹ࠬ")] = [{
                    bstack1l1ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯᷺ࠩ"): bstack1l1ll11_opy_ (u"ࠪࡹࡸ࡫ࡲࡠ࡭࡬ࡰࡱ࡫ࡤࠨ᷻"),
                    bstack1l1ll11_opy_ (u"ࠫࡸ࡯ࡧ࡯ࡣ࡯ࠫ᷼"): bstack1111ll1ll11_opy_
                }]
            config = {
                bstack1l1ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ᷽࠭"): cls.default_headers()
            }
            bstack11l1l111l1l_opy_ = bstack1l1ll11_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾ࠱ࡶࡸࡴࡶࠧ᷾").format(os.environ[bstack1l1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈ᷿ࠧ")])
            bstack1111ll1lll1_opy_ = cls.request_url(bstack11l1l111l1l_opy_)
            response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡒࡘࡘࠬḀ"), bstack1111ll1lll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1ll11_opy_ (u"ࠤࡖࡸࡴࡶࠠࡳࡧࡴࡹࡪࡹࡴࠡࡰࡲࡸࠥࡵ࡫ࠣḁ"))
        except Exception as error:
            logger.error(bstack1l1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾࠿ࠦࠢḂ") + str(error))
            return {
                bstack1l1ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫḃ"): bstack1l1ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫḄ"),
                bstack1l1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧḅ"): str(error)
            }
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def bstack1111llll11l_opy_(cls, response):
        bstack1lllll111l1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll11l11_opy_ = {}
        if bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠧ࡫ࡹࡷࠫḆ")) is None:
            os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬḇ")] = bstack1l1ll11_opy_ (u"ࠩࡱࡹࡱࡲࠧḈ")
        else:
            os.environ[bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧḉ")] = bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠫ࡯ࡽࡴࠨḊ"), bstack1l1ll11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪḋ"))
        os.environ[bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫḌ")] = bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḍ"), bstack1l1ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ḏ"))
        logger.info(bstack1l1ll11_opy_ (u"ࠩࡗࡩࡸࡺࡨࡶࡤࠣࡷࡹࡧࡲࡵࡧࡧࠤࡼ࡯ࡴࡩࠢ࡬ࡨ࠿ࠦࠧḏ") + os.getenv(bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨḐ")));
        if bstack1l1llll11_opy_.bstack1111lll1l11_opy_(cls.bs_config, cls.bstack1l1llllll1_opy_.get(bstack1l1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬḑ"), bstack1l1ll11_opy_ (u"ࠬ࠭Ḓ"))) is True:
            bstack111l11l1l11_opy_, build_hashed_id, bstack1111lll1111_opy_ = cls.bstack1111lll11l1_opy_(bstack1lllll111l1_opy_)
            if bstack111l11l1l11_opy_ != None and build_hashed_id != None:
                bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ḓ")] = {
                    bstack1l1ll11_opy_ (u"ࠧ࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠪḔ"): bstack111l11l1l11_opy_,
                    bstack1l1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḕ"): build_hashed_id,
                    bstack1l1ll11_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭Ḗ"): bstack1111lll1111_opy_
                }
            else:
                bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḗ")] = {}
        else:
            bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḘ")] = {}
        if bstack1ll11llll1_opy_.bstack1l111l1111_opy_(cls.bs_config) is True:
            bstack1111lll11ll_opy_, build_hashed_id = cls.bstack1111ll111ll_opy_(bstack1lllll111l1_opy_)
            if bstack1111lll11ll_opy_ != None and build_hashed_id != None:
                bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḙ")] = {
                    bstack1l1ll11_opy_ (u"࠭ࡡࡶࡶ࡫ࡣࡹࡵ࡫ࡦࡰࠪḚ"): bstack1111lll11ll_opy_,
                    bstack1l1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḛ"): build_hashed_id,
                }
            else:
                bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḜ")] = {}
        else:
            bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩḝ")] = {}
        if bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḞ")].get(bstack1l1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ḟ")) != None or bstack1111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬḠ")].get(bstack1l1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḡ")) != None:
            cls.bstack1111ll1llll_opy_(bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠧ࡫ࡹࡷࠫḢ")), bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḣ")))
        return bstack1111ll11l11_opy_
    @classmethod
    def bstack1111lll11l1_opy_(cls, bstack1lllll111l1_opy_):
        if bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḤ")) == None:
            cls.bstack1111lll1l1l_opy_()
            return [None, None, None]
        if bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḥ")][bstack1l1ll11_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬḦ")] != True:
            cls.bstack1111lll1l1l_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḧ")])
            return [None, None, None]
        logger.debug(bstack1l1ll11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪḨ"))
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ḩ")] = bstack1l1ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭Ḫ")
        if bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠩ࡭ࡻࡹ࠭ḫ")):
            os.environ[bstack1l1ll11_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧḬ")] = json.dumps({
                bstack1l1ll11_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭ḭ"): bstack11llll11ll1_opy_(cls.bs_config),
                bstack1l1ll11_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧḮ"): bstack11lllll111l_opy_(cls.bs_config)
            })
        if bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḯ")):
            os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭Ḱ")] = bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪḱ")]
        if bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḲ")].get(bstack1l1ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫḳ"), {}).get(bstack1l1ll11_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨḴ")):
            os.environ[bstack1l1ll11_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭ḵ")] = str(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭Ḷ")][bstack1l1ll11_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨḷ")][bstack1l1ll11_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬḸ")])
        else:
            os.environ[bstack1l1ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪḹ")] = bstack1l1ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣḺ")
        return [bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠫ࡯ࡽࡴࠨḻ")], bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḼ")], os.environ[bstack1l1ll11_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧḽ")]]
    @classmethod
    def bstack1111ll111ll_opy_(cls, bstack1lllll111l1_opy_):
        if bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḾ")) == None:
            cls.bstack1111ll11l1l_opy_()
            return [None, None]
        if bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḿ")][bstack1l1ll11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪṀ")] != True:
            cls.bstack1111ll11l1l_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṁ")])
            return [None, None]
        if bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṂ")].get(bstack1l1ll11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ṃ")):
            logger.debug(bstack1l1ll11_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪṄ"))
            parsed = json.loads(os.getenv(bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨṅ"), bstack1l1ll11_opy_ (u"ࠨࡽࢀࠫṆ")))
            capabilities = bstack111111l1_opy_.bstack1111llll111_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṇ")][bstack1l1ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫṈ")][bstack1l1ll11_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪṉ")], bstack1l1ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪṊ"), bstack1l1ll11_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬṋ"))
            bstack1111lll11ll_opy_ = capabilities[bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬṌ")]
            os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ṍ")] = bstack1111lll11ll_opy_
            if bstack1l1ll11_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦṎ") in bstack1lllll111l1_opy_ and bstack1lllll111l1_opy_.get(bstack1l1ll11_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤṏ")) is None:
                parsed[bstack1l1ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬṐ")] = capabilities[bstack1l1ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ṑ")]
            os.environ[bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧṒ")] = json.dumps(parsed)
            scripts = bstack111111l1_opy_.bstack1111llll111_opy_(bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧṓ")][bstack1l1ll11_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩṔ")][bstack1l1ll11_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪṕ")], bstack1l1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨṖ"), bstack1l1ll11_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬṗ"))
            bstack11ll1l11ll_opy_.bstack111l11lll_opy_(scripts)
            commands = bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬṘ")][bstack1l1ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧṙ")][bstack1l1ll11_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨṚ")].get(bstack1l1ll11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪṛ"))
            bstack11ll1l11ll_opy_.bstack11llllll1ll_opy_(commands)
            bstack11ll1l11ll_opy_.store()
        return [bstack1111lll11ll_opy_, bstack1lllll111l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫṜ")]]
    @classmethod
    def bstack1111lll1l1l_opy_(cls, response=None):
        os.environ[bstack1l1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨṝ")] = bstack1l1ll11_opy_ (u"ࠫࡳࡻ࡬࡭ࠩṞ")
        os.environ[bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩṟ")] = bstack1l1ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫṠ")
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭ṡ")] = bstack1l1ll11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧṢ")
        os.environ[bstack1l1ll11_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨṣ")] = bstack1l1ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣṤ")
        os.environ[bstack1l1ll11_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬṥ")] = bstack1l1ll11_opy_ (u"ࠧࡴࡵ࡭࡮ࠥṦ")
        cls.bstack1111ll1111l_opy_(response, bstack1l1ll11_opy_ (u"ࠨ࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠨṧ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll11l1l_opy_(cls, response=None):
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬṨ")] = bstack1l1ll11_opy_ (u"ࠨࡰࡸࡰࡱ࠭ṩ")
        os.environ[bstack1l1ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧṪ")] = bstack1l1ll11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṫ")
        os.environ[bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨṬ")] = bstack1l1ll11_opy_ (u"ࠬࡴࡵ࡭࡮ࠪṭ")
        cls.bstack1111ll1111l_opy_(response, bstack1l1ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨṮ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1llll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫṯ")] = jwt
        os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭Ṱ")] = build_hashed_id
    @classmethod
    def bstack1111ll1111l_opy_(cls, response=None, product=bstack1l1ll11_opy_ (u"ࠤࠥṱ")):
        if response == None:
            logger.error(product + bstack1l1ll11_opy_ (u"ࠥࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡬ࡡࡪ࡮ࡨࡨࠧṲ"))
        for error in response[bstack1l1ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫṳ")]:
            bstack11l1lll1ll1_opy_ = error[bstack1l1ll11_opy_ (u"ࠬࡱࡥࡺࠩṴ")]
            error_message = error[bstack1l1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧṵ")]
            if error_message:
                if bstack11l1lll1ll1_opy_ == bstack1l1ll11_opy_ (u"ࠢࡆࡔࡕࡓࡗࡥࡁࡄࡅࡈࡗࡘࡥࡄࡆࡐࡌࡉࡉࠨṶ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1ll11_opy_ (u"ࠣࡆࡤࡸࡦࠦࡵࡱ࡮ࡲࡥࡩࠦࡴࡰࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࠤṷ") + product + bstack1l1ll11_opy_ (u"ࠤࠣࡪࡦ࡯࡬ࡦࡦࠣࡨࡺ࡫ࠠࡵࡱࠣࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢṸ"))
    @classmethod
    def bstack1111ll11ll1_opy_(cls):
        if cls.bstack111l11lll1l_opy_ is not None:
            return
        cls.bstack111l11lll1l_opy_ = bstack111l1l1111l_opy_(cls.bstack1111ll1ll1l_opy_)
        cls.bstack111l11lll1l_opy_.start()
    @classmethod
    def bstack111ll1111l_opy_(cls):
        if cls.bstack111l11lll1l_opy_ is None:
            return
        cls.bstack111l11lll1l_opy_.shutdown()
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def bstack1111ll1ll1l_opy_(cls, bstack111ll11l11_opy_, event_url=bstack1l1ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩṹ")):
        config = {
            bstack1l1ll11_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬṺ"): cls.default_headers()
        }
        logger.debug(bstack1l1ll11_opy_ (u"ࠧࡶ࡯ࡴࡶࡢࡨࡦࡺࡡ࠻ࠢࡖࡩࡳࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡹ࡫ࡳࡵࡪࡸࡦࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴࡴࠢࡾࢁࠧṻ").format(bstack1l1ll11_opy_ (u"࠭ࠬࠡࠩṼ").join([event[bstack1l1ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫṽ")] for event in bstack111ll11l11_opy_])))
        response = bstack1l1ll11lll_opy_(bstack1l1ll11_opy_ (u"ࠨࡒࡒࡗ࡙࠭Ṿ"), cls.request_url(event_url), bstack111ll11l11_opy_, config)
        bstack11llll1l111_opy_ = response.json()
    @classmethod
    def bstack1ll11l11l1_opy_(cls, bstack111ll11l11_opy_, event_url=bstack1l1ll11_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨṿ")):
        logger.debug(bstack1l1ll11_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡶࡷࡩࡲࡶࡴࡪࡰࡪࠤࡹࡵࠠࡢࡦࡧࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥẀ").format(bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẁ")]))
        if not bstack111111l1_opy_.bstack1111ll1l1ll_opy_(bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẂ")]):
            logger.debug(bstack1l1ll11_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡒࡴࡺࠠࡢࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦẃ").format(bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẄ")]))
            return
        bstack1ll11ll11_opy_ = bstack111111l1_opy_.bstack1111lll1ll1_opy_(bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẅ")], bstack111ll11l11_opy_.get(bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫẆ")))
        if bstack1ll11ll11_opy_ != None:
            if bstack111ll11l11_opy_.get(bstack1l1ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬẇ")) != None:
                bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭Ẉ")][bstack1l1ll11_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪẉ")] = bstack1ll11ll11_opy_
            else:
                bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫẊ")] = bstack1ll11ll11_opy_
        if event_url == bstack1l1ll11_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ẋ"):
            cls.bstack1111ll11ll1_opy_()
            logger.debug(bstack1l1ll11_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡢࡢࡶࡦ࡬ࠥࡽࡩࡵࡪࠣࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫࠺ࠡࡽࢀࠦẌ").format(bstack111ll11l11_opy_[bstack1l1ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ẍ")]))
            cls.bstack111l11lll1l_opy_.add(bstack111ll11l11_opy_)
        elif event_url == bstack1l1ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨẎ"):
            cls.bstack1111ll1ll1l_opy_([bstack111ll11l11_opy_], event_url)
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def bstack1l11lll1_opy_(cls, logs):
        bstack1111ll11111_opy_ = []
        for log in logs:
            bstack1111lll1lll_opy_ = {
                bstack1l1ll11_opy_ (u"ࠫࡰ࡯࡮ࡥࠩẏ"): bstack1l1ll11_opy_ (u"࡚ࠬࡅࡔࡖࡢࡐࡔࡍࠧẐ"),
                bstack1l1ll11_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬẑ"): log[bstack1l1ll11_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭Ẓ")],
                bstack1l1ll11_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫẓ"): log[bstack1l1ll11_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬẔ")],
                bstack1l1ll11_opy_ (u"ࠪ࡬ࡹࡺࡰࡠࡴࡨࡷࡵࡵ࡮ࡴࡧࠪẕ"): {},
                bstack1l1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẖ"): log[bstack1l1ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ẗ")],
            }
            if bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẘ") in log:
                bstack1111lll1lll_opy_[bstack1l1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẙ")] = log[bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẚ")]
            elif bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẛ") in log:
                bstack1111lll1lll_opy_[bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẜ")] = log[bstack1l1ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẝ")]
            bstack1111ll11111_opy_.append(bstack1111lll1lll_opy_)
        cls.bstack1ll11l11l1_opy_({
            bstack1l1ll11_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẞ"): bstack1l1ll11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪẟ"),
            bstack1l1ll11_opy_ (u"ࠧ࡭ࡱࡪࡷࠬẠ"): bstack1111ll11111_opy_
        })
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def bstack1111ll1l111_opy_(cls, steps):
        bstack1111lll111l_opy_ = []
        for step in steps:
            bstack1111l1lllll_opy_ = {
                bstack1l1ll11_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭ạ"): bstack1l1ll11_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡖࡈࡔࠬẢ"),
                bstack1l1ll11_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩả"): step[bstack1l1ll11_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪẤ")],
                bstack1l1ll11_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨấ"): step[bstack1l1ll11_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩẦ")],
                bstack1l1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨầ"): step[bstack1l1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩẨ")],
                bstack1l1ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫẩ"): step[bstack1l1ll11_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬẪ")]
            }
            if bstack1l1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẫ") in step:
                bstack1111l1lllll_opy_[bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẬ")] = step[bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ậ")]
            elif bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẮ") in step:
                bstack1111l1lllll_opy_[bstack1l1ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨắ")] = step[bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẰ")]
            bstack1111lll111l_opy_.append(bstack1111l1lllll_opy_)
        cls.bstack1ll11l11l1_opy_({
            bstack1l1ll11_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧằ"): bstack1l1ll11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨẲ"),
            bstack1l1ll11_opy_ (u"ࠬࡲ࡯ࡨࡵࠪẳ"): bstack1111lll111l_opy_
        })
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1l11ll111l_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1lllll111_opy_(cls, screenshot):
        cls.bstack1ll11l11l1_opy_({
            bstack1l1ll11_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẴ"): bstack1l1ll11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫẵ"),
            bstack1l1ll11_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭Ặ"): [{
                bstack1l1ll11_opy_ (u"ࠩ࡮࡭ࡳࡪࠧặ"): bstack1l1ll11_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࠬẸ"),
                bstack1l1ll11_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧẹ"): datetime.datetime.utcnow().isoformat() + bstack1l1ll11_opy_ (u"ࠬࡠࠧẺ"),
                bstack1l1ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẻ"): screenshot[bstack1l1ll11_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭Ẽ")],
                bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ"): screenshot[bstack1l1ll11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẾ")]
            }]
        }, event_url=bstack1l1ll11_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨế"))
    @classmethod
    @bstack111l11ll1l_opy_(class_method=True)
    def bstack1ll1lllll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll11l11l1_opy_({
            bstack1l1ll11_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨỀ"): bstack1l1ll11_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩề"),
            bstack1l1ll11_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨỂ"): {
                bstack1l1ll11_opy_ (u"ࠢࡶࡷ࡬ࡨࠧể"): cls.current_test_uuid(),
                bstack1l1ll11_opy_ (u"ࠣ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠢỄ"): cls.bstack11l111l11l_opy_(driver)
            }
        })
    @classmethod
    def bstack111lllll11_opy_(cls, event: str, bstack111ll11l11_opy_: bstack111ll11111_opy_):
        bstack111l1ll1l1_opy_ = {
            bstack1l1ll11_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭ễ"): event,
            bstack111ll11l11_opy_.bstack111l1ll111_opy_(): bstack111ll11l11_opy_.bstack111llll111_opy_(event)
        }
        cls.bstack1ll11l11l1_opy_(bstack111l1ll1l1_opy_)
        result = getattr(bstack111ll11l11_opy_, bstack1l1ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪỆ"), None)
        if event == bstack1l1ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬệ"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬỈ"): bstack1l1ll11_opy_ (u"࠭ࡰࡦࡰࡧ࡭ࡳ࡭ࠧỉ")}
        elif event == bstack1l1ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩỊ"):
            threading.current_thread().bstackTestMeta = {bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨị"): getattr(result, bstack1l1ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩỌ"), bstack1l1ll11_opy_ (u"ࠪࠫọ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỎ"), None) is None or os.environ[bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩỏ")] == bstack1l1ll11_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦỐ")) and (os.environ.get(bstack1l1ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬố"), None) is None or os.environ[bstack1l1ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭Ồ")] == bstack1l1ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢồ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111l111ll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩỔ"): bstack1l1ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧổ"),
            bstack1l1ll11_opy_ (u"ࠬ࡞࠭ࡃࡕࡗࡅࡈࡑ࠭ࡕࡇࡖࡘࡔࡖࡓࠨỖ"): bstack1l1ll11_opy_ (u"࠭ࡴࡳࡷࡨࠫỗ")
        }
        if os.environ.get(bstack1l1ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫỘ"), None):
            headers[bstack1l1ll11_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨộ")] = bstack1l1ll11_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࡾࢁࠬỚ").format(os.environ[bstack1l1ll11_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠢớ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1ll11_opy_ (u"ࠫࢀࢃ࠯ࡼࡿࠪỜ").format(bstack1111ll111l1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1ll11_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠩờ"), None)
    @staticmethod
    def bstack11l111l11l_opy_(driver):
        return {
            bstack11l1lllll11_opy_(): bstack11l1l1l1ll1_opy_(driver)
        }
    @staticmethod
    def bstack1111ll1l11l_opy_(exception_info, report):
        return [{bstack1l1ll11_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩỞ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll111l_opy_(typename):
        if bstack1l1ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࠥở") in typename:
            return bstack1l1ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࡉࡷࡸ࡯ࡳࠤỠ")
        return bstack1l1ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥỡ")