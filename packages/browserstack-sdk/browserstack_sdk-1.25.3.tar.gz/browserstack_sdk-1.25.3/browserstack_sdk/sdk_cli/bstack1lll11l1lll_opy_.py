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
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack11111ll1ll_opy_,
    bstack1llllllll1l_opy_,
    bstack1111111l1l_opy_,
    bstack1111l111ll_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll111l1ll1_opy_, bstack11111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll11_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_, bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1llll1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll1l_opy_ import bstack1ll11l11lll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack111lll1l_opy_ import bstack11ll1lll1_opy_, bstack1ll1llll1_opy_, bstack11111ll1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class bstack1llll1ll111_opy_(bstack1ll11l11lll_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧ቟")
    bstack1ll111llll1_opy_ = bstack1l1_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨበ")
    bstack1l1l1llll11_opy_ = bstack1l1_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥቡ")
    bstack1l1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤቢ")
    bstack1l1l1l1lll1_opy_ = bstack1l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢባ")
    bstack1ll111111ll_opy_ = bstack1l1_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥቤ")
    bstack1l1l1lllll1_opy_ = bstack1l1_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣብ")
    bstack1l1l1ll1111_opy_ = bstack1l1_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦቦ")
    def __init__(self):
        super().__init__(bstack1ll11l11l11_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1111l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll111ll1_opy_.POST), self.bstack1l1l1ll1ll1_opy_)
        if bstack11111l1l1_opy_():
            TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST), self.bstack1ll1ll111ll_opy_)
        else:
            TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.PRE), self.bstack1ll1ll111ll_opy_)
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST), self.bstack1ll1ll1l11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1l1ll1lll_opy_ = self.bstack1l1l1lll1ll_opy_(instance.context)
        if not bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧቧ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠣࠤቨ"))
            return
        f.bstack11111111ll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111llll1_opy_, bstack1l1l1ll1lll_opy_)
    def bstack1l1l1lll1ll_opy_(self, context: bstack1111l111ll_opy_, bstack1l1l1ll11l1_opy_= True):
        if bstack1l1l1ll11l1_opy_:
            bstack1l1l1ll1lll_opy_ = self.bstack1ll11l1l111_opy_(context, reverse=True)
        else:
            bstack1l1l1ll1lll_opy_ = self.bstack1ll11l1llll_opy_(context, reverse=True)
        return [f for f in bstack1l1l1ll1lll_opy_ if f[1].state != bstack11111ll1ll_opy_.QUIT]
    def bstack1ll1ll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if not bstack1ll111l1ll1_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቩ") + str(kwargs) + bstack1l1_opy_ (u"ࠥࠦቪ"))
            return
        bstack1l1l1ll1lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢቫ") + str(kwargs) + bstack1l1_opy_ (u"ࠧࠨቬ"))
            return
        if len(bstack1l1l1ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lllllll1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣቭ"))
        bstack1l1l1l1ll1l_opy_, bstack1l1ll1lll1l_opy_ = bstack1l1l1ll1lll_opy_[0]
        page = bstack1l1l1l1ll1l_opy_()
        if not page:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢቮ") + str(kwargs) + bstack1l1_opy_ (u"ࠣࠤቯ"))
            return
        bstack1lll11ll_opy_ = getattr(args[0], bstack1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤተ"), None)
        try:
            page.evaluate(bstack1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦቱ"),
                        bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠧ࠲ࠠࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ࠿ࠦࡻࠣࡰࡤࡱࡪࠨ࠺ࠨቲ") + json.dumps(
                            bstack1lll11ll_opy_) + bstack1l1_opy_ (u"ࠧࢃࡽࠣታ"))
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡࡽࢀࠦቴ"), e)
    def bstack1ll1ll1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if not bstack1ll111l1ll1_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࡹࠦࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥት") + str(kwargs) + bstack1l1_opy_ (u"ࠣࠤቶ"))
            return
        bstack1l1l1ll1lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቷ") + str(kwargs) + bstack1l1_opy_ (u"ࠥࠦቸ"))
            return
        if len(bstack1l1l1ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lllllll1ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡵࡧࡧࡦࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࢀࡱࡷࡢࡴࡪࡷࢂࠨቹ"))
        bstack1l1l1l1ll1l_opy_, bstack1l1ll1lll1l_opy_ = bstack1l1l1ll1lll_opy_[0]
        page = bstack1l1l1l1ll1l_opy_()
        if not page:
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡴࡦ࡭ࡥࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቺ") + str(kwargs) + bstack1l1_opy_ (u"ࠨࠢቻ"))
            return
        status = f.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1l1_opy_ (u"ࠢ࡯ࡱࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡵࡧࡶࡸ࠱ࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࠥቼ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠣࠤች"))
            return
        bstack1l1l1ll11ll_opy_ = {bstack1l1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤቾ"): status.lower()}
        bstack1l1l1lll11l_opy_ = f.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, None)
        if status.lower() == bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪቿ") and bstack1l1l1lll11l_opy_ is not None:
            bstack1l1l1ll11ll_opy_[bstack1l1_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫኀ")] = bstack1l1l1lll11l_opy_[0][bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨኁ")][0] if isinstance(bstack1l1l1lll11l_opy_, list) else str(bstack1l1l1lll11l_opy_)
        try:
              page.evaluate(
                    bstack1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢኂ"),
                    bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࠬኃ")
                    + json.dumps(bstack1l1l1ll11ll_opy_)
                    + bstack1l1_opy_ (u"ࠣࡿࠥኄ")
                )
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡻࡾࠤኅ"), e)
    def bstack1l1llll1lll_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        f: TestFramework,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if not bstack1ll111l1ll1_opy_:
            self.logger.debug(
                bstack1lllllll1ll_opy_ (u"ࠥࡱࡦࡸ࡫ࡠࡱ࠴࠵ࡾࡥࡳࡺࡰࡦ࠾ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦኆ"))
            return
        bstack1l1l1ll1lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኇ") + str(kwargs) + bstack1l1_opy_ (u"ࠧࠨኈ"))
            return
        if len(bstack1l1l1ll1lll_opy_) > 1:
            self.logger.debug(
                bstack1lllllll1ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࡻ࡬ࡹࡤࡶ࡬ࡹࡽࠣ኉"))
        bstack1l1l1l1ll1l_opy_, bstack1l1ll1lll1l_opy_ = bstack1l1l1ll1lll_opy_[0]
        page = bstack1l1l1l1ll1l_opy_()
        if not page:
            self.logger.debug(bstack1l1_opy_ (u"ࠢ࡮ࡣࡵ࡯ࡤࡵ࠱࠲ࡻࡢࡷࡾࡴࡣ࠻ࠢࡱࡳࠥࡶࡡࡨࡧࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኊ") + str(kwargs) + bstack1l1_opy_ (u"ࠣࠤኋ"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1_opy_ (u"ࠤࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࡕࡼࡲࡨࡀࠢኌ") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦኍ"),
                bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠩ኎").format(
                    json.dumps(
                        {
                            bstack1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧ኏"): bstack1l1_opy_ (u"ࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣነ"),
                            bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥኑ"): {
                                bstack1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨኒ"): bstack1l1_opy_ (u"ࠤࡄࡲࡳࡵࡴࡢࡶ࡬ࡳࡳࠨና"),
                                bstack1l1_opy_ (u"ࠥࡨࡦࡺࡡࠣኔ"): data,
                                bstack1l1_opy_ (u"ࠦࡱ࡫ࡶࡦ࡮ࠥን"): bstack1l1_opy_ (u"ࠧࡪࡥࡣࡷࡪࠦኖ")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡲ࠵࠶ࡿࠠࡢࡰࡱࡳࡹࡧࡴࡪࡱࡱࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࢁࡽࠣኗ"), e)
    def bstack1l1lll1l1l1_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        f: TestFramework,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l1ll1ll1_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if f.bstack1111l11lll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111111ll_opy_, False):
            return
        self.bstack1ll1ll1111l_opy_()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l1111ll_opy_)
        req.test_framework_version = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll111l111l_opy_)
        req.test_framework_state = bstack111111l11l_opy_[0].name
        req.test_hook_state = bstack111111l11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        for bstack1l1l1ll111l_opy_ in bstack1llll1l11ll_opy_.bstack11111l1l1l_opy_.values():
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠨኘ")
                if bstack1ll111l1ll1_opy_
                else bstack1l1_opy_ (u"ࠣࡷࡱ࡯ࡳࡵࡷ࡯ࡡࡪࡶ࡮ࡪࠢኙ")
            )
            session.ref = bstack1l1l1ll111l_opy_.ref()
            session.hub_url = bstack1llll1l11ll_opy_.bstack1111l11lll_opy_(bstack1l1l1ll111l_opy_, bstack1llll1l11ll_opy_.bstack1l1ll111ll1_opy_, bstack1l1_opy_ (u"ࠤࠥኚ"))
            session.framework_name = bstack1l1l1ll111l_opy_.framework_name
            session.framework_version = bstack1l1l1ll111l_opy_.framework_version
            session.framework_session_id = bstack1llll1l11ll_opy_.bstack1111l11lll_opy_(bstack1l1l1ll111l_opy_, bstack1llll1l11ll_opy_.bstack1l1ll11lll1_opy_, bstack1l1_opy_ (u"ࠥࠦኛ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1l1l1ll1lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡤࡪࡲࡪࡸࡨࡶ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧኜ") + str(kwargs) + bstack1l1_opy_ (u"ࠧࠨኝ"))
            return
        if len(bstack1l1l1ll1lll_opy_) > 1:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡽ࡯ࡩࡳ࠮ࡰࡢࡩࡨࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኞ") + str(kwargs) + bstack1l1_opy_ (u"ࠢࠣኟ"))
        bstack1l1l1l1ll1l_opy_, bstack1l1ll1lll1l_opy_ = bstack1l1l1ll1lll_opy_[0]
        page = bstack1l1l1l1ll1l_opy_()
        if not page:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣአ") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥኡ"))
            return
        return page
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs
    ):
        caps = {}
        bstack1l1l1l1llll_opy_ = {}
        for bstack1l1l1ll111l_opy_ in bstack1llll1l11ll_opy_.bstack11111l1l1l_opy_.values():
            caps = bstack1llll1l11ll_opy_.bstack1111l11lll_opy_(bstack1l1l1ll111l_opy_, bstack1llll1l11ll_opy_.bstack1l1ll11llll_opy_, bstack1l1_opy_ (u"ࠥࠦኢ"))
        bstack1l1l1l1llll_opy_[bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠤኣ")] = caps.get(bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࠨኤ"), bstack1l1_opy_ (u"ࠨࠢእ"))
        bstack1l1l1l1llll_opy_[bstack1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨኦ")] = caps.get(bstack1l1_opy_ (u"ࠣࡱࡶࠦኧ"), bstack1l1_opy_ (u"ࠤࠥከ"))
        bstack1l1l1l1llll_opy_[bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧኩ")] = caps.get(bstack1l1_opy_ (u"ࠦࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣኪ"), bstack1l1_opy_ (u"ࠧࠨካ"))
        bstack1l1l1l1llll_opy_[bstack1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠢኬ")] = caps.get(bstack1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠤክ"), bstack1l1_opy_ (u"ࠣࠤኮ"))
        return bstack1l1l1l1llll_opy_
    def bstack1ll1l111l11_opy_(self, page: object, bstack1ll11llll11_opy_, args={}):
        try:
            bstack1l1l1lll111_opy_ = bstack1l1_opy_ (u"ࠤࠥࠦ࠭࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠠࠩ࠰࠱࠲ࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡺࡵࡳࡰࠣࡲࡪࡽࠠࡑࡴࡲࡱ࡮ࡹࡥࠩࠪࡵࡩࡸࡵ࡬ࡷࡧ࠯ࠤࡷ࡫ࡪࡦࡥࡷ࠭ࠥࡃ࠾ࠡࡽࡾࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡦࡸࡺࡡࡤ࡭ࡖࡨࡰࡇࡲࡨࡵ࠱ࡴࡺࡹࡨࠩࡴࡨࡷࡴࡲࡶࡦࠫ࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀ࠭ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࢃࠩࠩࡽࡤࡶ࡬ࡥࡪࡴࡱࡱࢁ࠮ࠨࠢࠣኯ")
            bstack1ll11llll11_opy_ = bstack1ll11llll11_opy_.replace(bstack1l1_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨኰ"), bstack1l1_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦ኱"))
            script = bstack1l1l1lll111_opy_.format(fn_body=bstack1ll11llll11_opy_, arg_json=json.dumps(args))
            return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮ࠣࠦኲ") + str(e) + bstack1l1_opy_ (u"ࠨࠢኳ"))