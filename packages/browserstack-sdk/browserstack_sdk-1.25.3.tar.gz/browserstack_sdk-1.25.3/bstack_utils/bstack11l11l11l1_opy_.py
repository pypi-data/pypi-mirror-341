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
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11llll1l1l1_opy_, bstack11llll11l11_opy_, bstack111lll111_opy_, bstack111l1ll1l1_opy_, bstack11l1l1l1l1l_opy_, bstack11l1llllll1_opy_, bstack11l1l111l11_opy_, bstack11l1l11ll1_opy_, bstack1l1l11l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111l1l111ll_opy_ import bstack111l11lllll_opy_
import bstack_utils.bstack1l1ll111l_opy_ as bstack111ll1lll_opy_
from bstack_utils.bstack11l11l1111_opy_ import bstack11llll111l_opy_
import bstack_utils.accessibility as bstack1l1l11l11_opy_
from bstack_utils.bstack11ll111l1_opy_ import bstack11ll111l1_opy_
from bstack_utils.bstack111lllll11_opy_ import bstack111ll1111l_opy_
bstack1111llll11l_opy_ = bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡧࡴࡲ࡬ࡦࡥࡷࡳࡷ࠳࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮ࠩᷥ")
logger = logging.getLogger(__name__)
class bstack111111l1_opy_:
    bstack111l1l111ll_opy_ = None
    bs_config = None
    bstack1ll1111l11_opy_ = None
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1l11111_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def launch(cls, bs_config, bstack1ll1111l11_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1111l11_opy_ = bstack1ll1111l11_opy_
        try:
            cls.bstack1111ll1l11l_opy_()
            bstack11llll111l1_opy_ = bstack11llll1l1l1_opy_(bs_config)
            bstack11llll1ll1l_opy_ = bstack11llll11l11_opy_(bs_config)
            data = bstack111ll1lll_opy_.bstack1111lll11l1_opy_(bs_config, bstack1ll1111l11_opy_)
            config = {
                bstack1l1_opy_ (u"ࠪࡥࡺࡺࡨࠨᷦ"): (bstack11llll111l1_opy_, bstack11llll1ll1l_opy_),
                bstack1l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᷧ"): cls.default_headers()
            }
            response = bstack111lll111_opy_(bstack1l1_opy_ (u"ࠬࡖࡏࡔࡖࠪᷨ"), cls.request_url(bstack1l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠷࠵ࡢࡶ࡫࡯ࡨࡸ࠭ᷩ")), data, config)
            if response.status_code != 200:
                bstack1ll1llllll1_opy_ = response.json()
                if bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᷪ")] == False:
                    cls.bstack1111ll1ll11_opy_(bstack1ll1llllll1_opy_)
                    return
                cls.bstack1111ll1llll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᷫ")])
                cls.bstack1111ll1l1ll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᷬ")])
                return None
            bstack1111ll1ll1l_opy_ = cls.bstack1111lll11ll_opy_(response)
            return bstack1111ll1ll1l_opy_
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡣࡷ࡬ࡰࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࢁࡽࠣᷭ").format(str(error)))
            return None
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def stop(cls, bstack1111ll11lll_opy_=None):
        if not bstack11llll111l_opy_.on() and not bstack1l1l11l11_opy_.on():
            return
        if os.environ.get(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᷮ")) == bstack1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᷯ") or os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᷰ")) == bstack1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᷱ"):
            logger.error(bstack1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᷲ"))
            return {
                bstack1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᷳ"): bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᷴ"),
                bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᷵"): bstack1l1_opy_ (u"࡚ࠬ࡯࡬ࡧࡱ࠳ࡧࡻࡩ࡭ࡦࡌࡈࠥ࡯ࡳࠡࡷࡱࡨࡪ࡬ࡩ࡯ࡧࡧ࠰ࠥࡨࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦ࡭ࡪࡩ࡫ࡸࠥ࡮ࡡࡷࡧࠣࡪࡦ࡯࡬ࡦࡦࠪ᷶")
            }
        try:
            cls.bstack111l1l111ll_opy_.shutdown()
            data = {
                bstack1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷ᷷ࠫ"): bstack11l1l11ll1_opy_()
            }
            if not bstack1111ll11lll_opy_ is None:
                data[bstack1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡰࡩࡹࡧࡤࡢࡶࡤ᷸ࠫ")] = [{
                    bstack1l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨ᷹"): bstack1l1_opy_ (u"ࠩࡸࡷࡪࡸ࡟࡬࡫࡯ࡰࡪࡪ᷺ࠧ"),
                    bstack1l1_opy_ (u"ࠪࡷ࡮࡭࡮ࡢ࡮ࠪ᷻"): bstack1111ll11lll_opy_
                }]
            config = {
                bstack1l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬ᷼"): cls.default_headers()
            }
            bstack11l1l1l1lll_opy_ = bstack1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡷࡳࡵ᷽࠭").format(os.environ[bstack1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠦ᷾")])
            bstack1111ll11l11_opy_ = cls.request_url(bstack11l1l1l1lll_opy_)
            response = bstack111lll111_opy_(bstack1l1_opy_ (u"ࠧࡑࡗࡗ᷿ࠫ"), bstack1111ll11l11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1l1_opy_ (u"ࠣࡕࡷࡳࡵࠦࡲࡦࡳࡸࡩࡸࡺࠠ࡯ࡱࡷࠤࡴࡱࠢḀ"))
        except Exception as error:
            logger.error(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡳࡵࠦࡢࡶ࡫࡯ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡴࡰࠢࡗࡩࡸࡺࡈࡶࡤ࠽࠾ࠥࠨḁ") + str(error))
            return {
                bstack1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪḂ"): bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪḃ"),
                bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ḅ"): str(error)
            }
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack1111lll11ll_opy_(cls, response):
        bstack1ll1llllll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1111ll1ll1l_opy_ = {}
        if bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"࠭ࡪࡸࡶࠪḅ")) is None:
            os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫḆ")] = bstack1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ḇ")
        else:
            os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ḉ")] = bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠪ࡮ࡼࡺࠧḉ"), bstack1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩḊ"))
        os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪḋ")] = bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḌ"), bstack1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬḍ"))
        logger.info(bstack1l1_opy_ (u"ࠨࡖࡨࡷࡹ࡮ࡵࡣࠢࡶࡸࡦࡸࡴࡦࡦࠣࡻ࡮ࡺࡨࠡ࡫ࡧ࠾ࠥ࠭Ḏ") + os.getenv(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧḏ")));
        if bstack11llll111l_opy_.bstack1111ll1lll1_opy_(cls.bs_config, cls.bstack1ll1111l11_opy_.get(bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫḐ"), bstack1l1_opy_ (u"ࠫࠬḑ"))) is True:
            bstack111l11ll111_opy_, build_hashed_id, bstack1111llll111_opy_ = cls.bstack1111ll11l1l_opy_(bstack1ll1llllll1_opy_)
            if bstack111l11ll111_opy_ != None and build_hashed_id != None:
                bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḒ")] = {
                    bstack1l1_opy_ (u"࠭ࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠩḓ"): bstack111l11ll111_opy_,
                    bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḔ"): build_hashed_id,
                    bstack1l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬḕ"): bstack1111llll111_opy_
                }
            else:
                bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḖ")] = {}
        else:
            bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪḗ")] = {}
        if bstack1l1l11l11_opy_.bstack11l11111l_opy_(cls.bs_config) is True:
            bstack1111ll1111l_opy_, build_hashed_id = cls.bstack1111ll1l111_opy_(bstack1ll1llllll1_opy_)
            if bstack1111ll1111l_opy_ != None and build_hashed_id != None:
                bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḘ")] = {
                    bstack1l1_opy_ (u"ࠬࡧࡵࡵࡪࡢࡸࡴࡱࡥ࡯ࠩḙ"): bstack1111ll1111l_opy_,
                    bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨḚ"): build_hashed_id,
                }
            else:
                bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḛ")] = {}
        else:
            bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨḜ")] = {}
        if bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḝ")].get(bstack1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬḞ")) != None or bstack1111ll1ll1l_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫḟ")].get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḠ")) != None:
            cls.bstack1111ll111l1_opy_(bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"࠭ࡪࡸࡶࠪḡ")), bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḢ")))
        return bstack1111ll1ll1l_opy_
    @classmethod
    def bstack1111ll11l1l_opy_(cls, bstack1ll1llllll1_opy_):
        if bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḣ")) == None:
            cls.bstack1111ll1llll_opy_()
            return [None, None, None]
        if bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩḤ")][bstack1l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫḥ")] != True:
            cls.bstack1111ll1llll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫḦ")])
            return [None, None, None]
        logger.debug(bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩḧ"))
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬḨ")] = bstack1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬḩ")
        if bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠨ࡬ࡺࡸࠬḪ")):
            os.environ[bstack1l1_opy_ (u"ࠩࡆࡖࡊࡊࡅࡏࡖࡌࡅࡑ࡙࡟ࡇࡑࡕࡣࡈࡘࡁࡔࡊࡢࡖࡊࡖࡏࡓࡖࡌࡒࡌ࠭ḫ")] = json.dumps({
                bstack1l1_opy_ (u"ࠪࡹࡸ࡫ࡲ࡯ࡣࡰࡩࠬḬ"): bstack11llll1l1l1_opy_(cls.bs_config),
                bstack1l1_opy_ (u"ࠫࡵࡧࡳࡴࡹࡲࡶࡩ࠭ḭ"): bstack11llll11l11_opy_(cls.bs_config)
            })
        if bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧḮ")):
            os.environ[bstack1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬḯ")] = bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩḰ")]
        if bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨḱ")].get(bstack1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪḲ"), {}).get(bstack1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧḳ")):
            os.environ[bstack1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬḴ")] = str(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬḵ")][bstack1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧḶ")][bstack1l1_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫḷ")])
        else:
            os.environ[bstack1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩḸ")] = bstack1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢḹ")
        return [bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠪ࡮ࡼࡺࠧḺ")], bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ḻ")], os.environ[bstack1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭Ḽ")]]
    @classmethod
    def bstack1111ll1l111_opy_(cls, bstack1ll1llllll1_opy_):
        if bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ḽ")) == None:
            cls.bstack1111ll1l1ll_opy_()
            return [None, None]
        if bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧḾ")][bstack1l1_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩḿ")] != True:
            cls.bstack1111ll1l1ll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩṀ")])
            return [None, None]
        if bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪṁ")].get(bstack1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬṂ")):
            logger.debug(bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡘࡻࡣࡤࡧࡶࡷ࡫ࡻ࡬ࠢࠩṃ"))
            parsed = json.loads(os.getenv(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧṄ"), bstack1l1_opy_ (u"ࠧࡼࡿࠪṅ")))
            capabilities = bstack111ll1lll_opy_.bstack1111ll111ll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨṆ")][bstack1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪṇ")][bstack1l1_opy_ (u"ࠪࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩṈ")], bstack1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩṉ"), bstack1l1_opy_ (u"ࠬࡼࡡ࡭ࡷࡨࠫṊ"))
            bstack1111ll1111l_opy_ = capabilities[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫṋ")]
            os.environ[bstack1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬṌ")] = bstack1111ll1111l_opy_
            if bstack1l1_opy_ (u"ࠣࡣࡸࡸࡴࡳࡡࡵࡧࠥṍ") in bstack1ll1llllll1_opy_ and bstack1ll1llllll1_opy_.get(bstack1l1_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣṎ")) is None:
                parsed[bstack1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫṏ")] = capabilities[bstack1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬṐ")]
            os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ṑ")] = json.dumps(parsed)
            scripts = bstack111ll1lll_opy_.bstack1111ll111ll_opy_(bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭Ṓ")][bstack1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨṓ")][bstack1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩṔ")], bstack1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧṕ"), bstack1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࠫṖ"))
            bstack11ll111l1_opy_.bstack1l111l1ll1_opy_(scripts)
            commands = bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫṗ")][bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭Ṙ")][bstack1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࡕࡱ࡚ࡶࡦࡶࠧṙ")].get(bstack1l1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩṚ"))
            bstack11ll111l1_opy_.bstack11llll1llll_opy_(commands)
            bstack11ll111l1_opy_.store()
        return [bstack1111ll1111l_opy_, bstack1ll1llllll1_opy_[bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪṛ")]]
    @classmethod
    def bstack1111ll1llll_opy_(cls, response=None):
        os.environ[bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧṜ")] = bstack1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨṝ")
        os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨṞ")] = bstack1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪṟ")
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬṠ")] = bstack1l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ṡ")
        os.environ[bstack1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧṢ")] = bstack1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢṣ")
        os.environ[bstack1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫṤ")] = bstack1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤṥ")
        cls.bstack1111ll1ll11_opy_(response, bstack1l1_opy_ (u"ࠧࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠧṦ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll1l1ll_opy_(cls, response=None):
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫṧ")] = bstack1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬṨ")
        os.environ[bstack1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ṩ")] = bstack1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧṪ")
        os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧṫ")] = bstack1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩṬ")
        cls.bstack1111ll1ll11_opy_(response, bstack1l1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧṭ"))
        return [None, None, None]
    @classmethod
    def bstack1111ll111l1_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪṮ")] = jwt
        os.environ[bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬṯ")] = build_hashed_id
    @classmethod
    def bstack1111ll1ll11_opy_(cls, response=None, product=bstack1l1_opy_ (u"ࠣࠤṰ")):
        if response == None:
            logger.error(product + bstack1l1_opy_ (u"ࠤࠣࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡫ࡧࡩ࡭ࡧࡧࠦṱ"))
        for error in response[bstack1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪṲ")]:
            bstack11l1lll11ll_opy_ = error[bstack1l1_opy_ (u"ࠫࡰ࡫ࡹࠨṳ")]
            error_message = error[bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ṵ")]
            if error_message:
                if bstack11l1lll11ll_opy_ == bstack1l1_opy_ (u"ࠨࡅࡓࡔࡒࡖࡤࡇࡃࡄࡇࡖࡗࡤࡊࡅࡏࡋࡈࡈࠧṵ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1l1_opy_ (u"ࠢࡅࡣࡷࡥࠥࡻࡰ࡭ࡱࡤࡨࠥࡺ࡯ࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࠣṶ") + product + bstack1l1_opy_ (u"ࠣࠢࡩࡥ࡮ࡲࡥࡥࠢࡧࡹࡪࠦࡴࡰࠢࡶࡳࡲ࡫ࠠࡦࡴࡵࡳࡷࠨṷ"))
    @classmethod
    def bstack1111ll1l11l_opy_(cls):
        if cls.bstack111l1l111ll_opy_ is not None:
            return
        cls.bstack111l1l111ll_opy_ = bstack111l11lllll_opy_(cls.bstack1111ll11111_opy_)
        cls.bstack111l1l111ll_opy_.start()
    @classmethod
    def bstack111l1l11l1_opy_(cls):
        if cls.bstack111l1l111ll_opy_ is None:
            return
        cls.bstack111l1l111ll_opy_.shutdown()
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack1111ll11111_opy_(cls, bstack111lll1ll1_opy_, event_url=bstack1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨṸ")):
        config = {
            bstack1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫṹ"): cls.default_headers()
        }
        logger.debug(bstack1l1_opy_ (u"ࠦࡵࡵࡳࡵࡡࡧࡥࡹࡧ࠺ࠡࡕࡨࡲࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡸࡪࡹࡴࡩࡷࡥࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺࡳࠡࡽࢀࠦṺ").format(bstack1l1_opy_ (u"ࠬ࠲ࠠࠨṻ").join([event[bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪṼ")] for event in bstack111lll1ll1_opy_])))
        response = bstack111lll111_opy_(bstack1l1_opy_ (u"ࠧࡑࡑࡖࡘࠬṽ"), cls.request_url(event_url), bstack111lll1ll1_opy_, config)
        bstack11llllll111_opy_ = response.json()
    @classmethod
    def bstack1l111lll1l_opy_(cls, bstack111lll1ll1_opy_, event_url=bstack1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧṾ")):
        logger.debug(bstack1l1_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡁࡵࡶࡨࡱࡵࡺࡩ࡯ࡩࠣࡸࡴࠦࡡࡥࡦࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤṿ").format(bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧẀ")]))
        if not bstack111ll1lll_opy_.bstack1111lll1111_opy_(bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẁ")]):
            logger.debug(bstack1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡑࡳࡹࠦࡡࡥࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥẂ").format(bstack111lll1ll1_opy_[bstack1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪẃ")]))
            return
        bstack1lll11l1ll_opy_ = bstack111ll1lll_opy_.bstack1111ll11ll1_opy_(bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫẄ")], bstack111lll1ll1_opy_.get(bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪẅ")))
        if bstack1lll11l1ll_opy_ != None:
            if bstack111lll1ll1_opy_.get(bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫẆ")) != None:
                bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬẇ")][bstack1l1_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩẈ")] = bstack1lll11l1ll_opy_
            else:
                bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪẉ")] = bstack1lll11l1ll_opy_
        if event_url == bstack1l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬẊ"):
            cls.bstack1111ll1l11l_opy_()
            logger.debug(bstack1l1_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡷࡳࠥࡨࡡࡵࡥ࡫ࠤࡼ࡯ࡴࡩࠢࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪࡀࠠࡼࡿࠥẋ").format(bstack111lll1ll1_opy_[bstack1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬẌ")]))
            cls.bstack111l1l111ll_opy_.add(bstack111lll1ll1_opy_)
        elif event_url == bstack1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧẍ"):
            cls.bstack1111ll11111_opy_([bstack111lll1ll1_opy_], event_url)
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack1ll1l1l1l1_opy_(cls, logs):
        bstack1111lll1l11_opy_ = []
        for log in logs:
            bstack1111lll111l_opy_ = {
                bstack1l1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨẎ"): bstack1l1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡏࡓࡌ࠭ẏ"),
                bstack1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫẐ"): log[bstack1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬẑ")],
                bstack1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪẒ"): log[bstack1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫẓ")],
                bstack1l1_opy_ (u"ࠩ࡫ࡸࡹࡶ࡟ࡳࡧࡶࡴࡴࡴࡳࡦࠩẔ"): {},
                bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫẕ"): log[bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬẖ")],
            }
            if bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẗ") in log:
                bstack1111lll111l_opy_[bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ẘ")] = log[bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẙ")]
            elif bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẚ") in log:
                bstack1111lll111l_opy_[bstack1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩẛ")] = log[bstack1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẜ")]
            bstack1111lll1l11_opy_.append(bstack1111lll111l_opy_)
        cls.bstack1l111lll1l_opy_({
            bstack1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨẝ"): bstack1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩẞ"),
            bstack1l1_opy_ (u"࠭࡬ࡰࡩࡶࠫẟ"): bstack1111lll1l11_opy_
        })
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack1111lll1lll_opy_(cls, steps):
        bstack1111l1lllll_opy_ = []
        for step in steps:
            bstack1111lll1l1l_opy_ = {
                bstack1l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬẠ"): bstack1l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡕࡇࡓࠫạ"),
                bstack1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨẢ"): step[bstack1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩả")],
                bstack1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧẤ"): step[bstack1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨấ")],
                bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧẦ"): step[bstack1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨầ")],
                bstack1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪẨ"): step[bstack1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࠫẩ")]
            }
            if bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪẪ") in step:
                bstack1111lll1l1l_opy_[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫẫ")] = step[bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬẬ")]
            elif bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ậ") in step:
                bstack1111lll1l1l_opy_[bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẮ")] = step[bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨắ")]
            bstack1111l1lllll_opy_.append(bstack1111lll1l1l_opy_)
        cls.bstack1l111lll1l_opy_({
            bstack1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭Ằ"): bstack1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧằ"),
            bstack1l1_opy_ (u"ࠫࡱࡵࡧࡴࠩẲ"): bstack1111l1lllll_opy_
        })
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1ll11l1l11_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def bstack1ll1lll11_opy_(cls, screenshot):
        cls.bstack1l111lll1l_opy_({
            bstack1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩẳ"): bstack1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪẴ"),
            bstack1l1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬẵ"): [{
                bstack1l1_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭Ặ"): bstack1l1_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࠫặ"),
                bstack1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭Ẹ"): datetime.datetime.utcnow().isoformat() + bstack1l1_opy_ (u"ࠫ࡟࠭ẹ"),
                bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ẻ"): screenshot[bstack1l1_opy_ (u"࠭ࡩ࡮ࡣࡪࡩࠬẻ")],
                bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧẼ"): screenshot[bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨẽ")]
            }]
        }, event_url=bstack1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧẾ"))
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack1lll11lll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l111lll1l_opy_({
            bstack1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧế"): bstack1l1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨỀ"),
            bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧề"): {
                bstack1l1_opy_ (u"ࠨࡵࡶ࡫ࡧࠦỂ"): cls.current_test_uuid(),
                bstack1l1_opy_ (u"ࠢࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸࠨể"): cls.bstack11l111ll11_opy_(driver)
            }
        })
    @classmethod
    def bstack11l1111l1l_opy_(cls, event: str, bstack111lll1ll1_opy_: bstack111ll1111l_opy_):
        bstack111l1ll1ll_opy_ = {
            bstack1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬỄ"): event,
            bstack111lll1ll1_opy_.bstack111lll111l_opy_(): bstack111lll1ll1_opy_.bstack111lll1l11_opy_(event)
        }
        cls.bstack1l111lll1l_opy_(bstack111l1ll1ll_opy_)
        result = getattr(bstack111lll1ll1_opy_, bstack1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩễ"), None)
        if event == bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫỆ"):
            threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫệ"): bstack1l1_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭Ỉ")}
        elif event == bstack1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨỉ"):
            threading.current_thread().bstackTestMeta = {bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧỊ"): getattr(result, bstack1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨị"), bstack1l1_opy_ (u"ࠩࠪỌ"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧọ"), None) is None or os.environ[bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨỎ")] == bstack1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥỏ")) and (os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫỐ"), None) is None or os.environ[bstack1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬố")] == bstack1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨỒ")):
            return False
        return True
    @staticmethod
    def bstack1111ll1l1l1_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111111l1_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨồ"): bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ổ"),
            bstack1l1_opy_ (u"ࠫ࡝࠳ࡂࡔࡖࡄࡇࡐ࠳ࡔࡆࡕࡗࡓࡕ࡙ࠧổ"): bstack1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪỖ")
        }
        if os.environ.get(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪỗ"), None):
            headers[bstack1l1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧỘ")] = bstack1l1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࡽࢀࠫộ").format(os.environ[bstack1l1_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙ࠨỚ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1l1_opy_ (u"ࠪࡿࢂ࠵ࡻࡾࠩớ").format(bstack1111llll11l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢࡹࡺ࡯ࡤࠨỜ"), None)
    @staticmethod
    def bstack11l111ll11_opy_(driver):
        return {
            bstack11l1l1l1l1l_opy_(): bstack11l1llllll1_opy_(driver)
        }
    @staticmethod
    def bstack1111lll1ll1_opy_(exception_info, report):
        return [{bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨờ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1111ll11l1_opy_(typename):
        if bstack1l1_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࠤỞ") in typename:
            return bstack1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣở")
        return bstack1l1_opy_ (u"ࠣࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠤỠ")