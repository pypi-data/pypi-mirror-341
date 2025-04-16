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
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack11111ll1ll_opy_,
    bstack1llllllll1l_opy_,
    bstack11111lll1l_opy_,
    bstack1111111l1l_opy_,
    bstack1111l111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lllll11_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_, bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l1ll1l_opy_ import bstack1ll11l11lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll111l1ll1_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1llll111111_opy_(bstack1ll11l11lll_opy_):
    bstack1l1l1ll1l1l_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣጃ")
    bstack1ll111llll1_opy_ = bstack1l1_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤጄ")
    bstack1l1l1llll11_opy_ = bstack1l1_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጅ")
    bstack1l1l1llll1l_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጆ")
    bstack1l1l1l1lll1_opy_ = bstack1l1_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥጇ")
    bstack1ll111111ll_opy_ = bstack1l1_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨገ")
    bstack1l1l1lllll1_opy_ = bstack1l1_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦጉ")
    bstack1l1l1ll1111_opy_ = bstack1l1_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢጊ")
    def __init__(self):
        super().__init__(bstack1ll11l11l11_opy_=self.bstack1l1l1ll1l1l_opy_, frameworks=[bstack1lll1111l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.BEFORE_EACH, bstack1llll111ll1_opy_.POST), self.bstack1l1l11l1111_opy_)
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.PRE), self.bstack1ll1ll111ll_opy_)
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST), self.bstack1ll1ll1l11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        bstack1ll11111lll_opy_ = self.bstack1l1l1111lll_opy_(instance.context)
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጋ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠦࠧጌ"))
        f.bstack11111111ll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, bstack1ll11111lll_opy_)
        bstack1l1l111l11l_opy_ = self.bstack1l1l1111lll_opy_(instance.context, bstack1l1l111ll1l_opy_=False)
        f.bstack11111111ll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1llll11_opy_, bstack1l1l111l11l_opy_)
    def bstack1ll1ll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l1111_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if not f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1lllll1_opy_, False):
            self.__1l1l1111ll1_opy_(f,instance,bstack111111l11l_opy_)
    def bstack1ll1ll1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l1111_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        if not f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1lllll1_opy_, False):
            self.__1l1l1111ll1_opy_(f, instance, bstack111111l11l_opy_)
        if not f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1ll1111_opy_, False):
            self.__1l1l111lll1_opy_(f, instance, bstack111111l11l_opy_)
    def bstack1l1l111l1l1_opy_(
        self,
        f: bstack1lll1111l11_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack111111l11l_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l1l1l1l_opy_(instance):
            return
        if f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1ll1111_opy_, False):
            return
        driver.execute_script(
            bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥግ").format(
                json.dumps(
                    {
                        bstack1l1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጎ"): bstack1l1_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥጏ"),
                        bstack1l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጐ"): {bstack1l1_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ጑"): result},
                    }
                )
            )
        )
        f.bstack11111111ll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1ll1111_opy_, True)
    def bstack1l1l1111lll_opy_(self, context: bstack1111l111ll_opy_, bstack1l1l111ll1l_opy_= True):
        if bstack1l1l111ll1l_opy_:
            bstack1ll11111lll_opy_ = self.bstack1ll11l1l111_opy_(context, reverse=True)
        else:
            bstack1ll11111lll_opy_ = self.bstack1ll11l1llll_opy_(context, reverse=True)
        return [f for f in bstack1ll11111lll_opy_ if f[1].state != bstack11111ll1ll_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1ll1l1111_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def __1l1l111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
    ):
        bstack1ll11111lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጒ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠦࠧጓ"))
            return
        driver = bstack1ll11111lll_opy_[0][0]()
        status = f.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, None)
        if not status:
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጔ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠨࠢጕ"))
            return
        bstack1l1l1ll11ll_opy_ = {bstack1l1_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ጖"): status.lower()}
        bstack1l1l1lll11l_opy_ = f.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, None)
        if status.lower() == bstack1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ጗") and bstack1l1l1lll11l_opy_ is not None:
            bstack1l1l1ll11ll_opy_[bstack1l1_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩጘ")] = bstack1l1l1lll11l_opy_[0][bstack1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ጙ")][0] if isinstance(bstack1l1l1lll11l_opy_, list) else str(bstack1l1l1lll11l_opy_)
        driver.execute_script(
            bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጚ").format(
                json.dumps(
                    {
                        bstack1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጛ"): bstack1l1_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጜ"),
                        bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጝ"): bstack1l1l1ll11ll_opy_,
                    }
                )
            )
        )
        f.bstack11111111ll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1ll1111_opy_, True)
    @measure(event_name=EVENTS.bstack1l1111l1l1_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def __1l1l1111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_]
    ):
        test_name = f.bstack1111l11lll_opy_(instance, TestFramework.bstack1l1l111l1ll_opy_, None)
        if not test_name:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢጞ"))
            return
        bstack1ll11111lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጟ") + str(bstack111111l11l_opy_) + bstack1l1_opy_ (u"ࠥࠦጠ"))
            return
        for bstack1l1ll1l11ll_opy_, bstack1l1l111llll_opy_ in bstack1ll11111lll_opy_:
            if not bstack1lll1111l11_opy_.bstack1ll1l1l1l1l_opy_(bstack1l1l111llll_opy_):
                continue
            driver = bstack1l1ll1l11ll_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጡ").format(
                    json.dumps(
                        {
                            bstack1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጢ"): bstack1l1_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢጣ"),
                            bstack1l1_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጤ"): {bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨጥ"): test_name},
                        }
                    )
                )
            )
        f.bstack11111111ll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1lllll1_opy_, True)
    def bstack1l1llll1lll_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        f: TestFramework,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l1111_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        bstack1ll11111lll_opy_ = [d for d, _ in f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])]
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤጦ"))
            return
        if not bstack1ll111l1ll1_opy_():
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣጧ"))
            return
        for bstack1l1l111l111_opy_ in bstack1ll11111lll_opy_:
            driver = bstack1l1l111l111_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤጨ") + str(timestamp)
            driver.execute_script(
                bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጩ").format(
                    json.dumps(
                        {
                            bstack1l1_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጪ"): bstack1l1_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤጫ"),
                            bstack1l1_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጬ"): {
                                bstack1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢጭ"): bstack1l1_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢጮ"),
                                bstack1l1_opy_ (u"ࠦࡩࡧࡴࡢࠤጯ"): data,
                                bstack1l1_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦጰ"): bstack1l1_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧጱ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll1l1l1_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        f: TestFramework,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l11l1111_opy_(f, instance, bstack111111l11l_opy_, *args, **kwargs)
        bstack1ll11111lll_opy_ = [d for _, d in f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])] + [d for _, d in f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1l1l1llll11_opy_, [])]
        keys = [
            bstack1llll111111_opy_.bstack1ll111llll1_opy_,
            bstack1llll111111_opy_.bstack1l1l1llll11_opy_,
        ]
        bstack1ll11111lll_opy_ = [
            d for key in keys for _, d in f.bstack1111l11lll_opy_(instance, key, [])
        ]
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡲࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤጲ"))
            return
        if f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111111ll_opy_, False):
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡆࡆ࡙ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡤࡴࡨࡥࡹ࡫ࡤࠣጳ"))
            return
        self.bstack1ll1ll1111l_opy_()
        bstack1l1l1llll1_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l1111ll_opy_)
        req.test_framework_version = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll111l111l_opy_)
        req.test_framework_state = bstack111111l11l_opy_[0].name
        req.test_hook_state = bstack111111l11l_opy_[1].name
        req.test_uuid = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
        for driver in bstack1ll11111lll_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣጴ")
                if bstack1lll1111l11_opy_.bstack1111l11lll_opy_(driver, bstack1lll1111l11_opy_.bstack1l1l111ll11_opy_, False)
                else bstack1l1_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤጵ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1lll1111l11_opy_.bstack1111l11lll_opy_(driver, bstack1lll1111l11_opy_.bstack1l1ll111ll1_opy_, bstack1l1_opy_ (u"ࠦࠧጶ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1lll1111l11_opy_.bstack1111l11lll_opy_(driver, bstack1lll1111l11_opy_.bstack1l1ll11lll1_opy_, bstack1l1_opy_ (u"ࠧࠨጷ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll1l1111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll11111lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጸ") + str(kwargs) + bstack1l1_opy_ (u"ࠢࠣጹ"))
            return {}
        if len(bstack1ll11111lll_opy_) > 1:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጺ") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥጻ"))
            return {}
        bstack1l1ll1l11ll_opy_, bstack1l1ll1lll1l_opy_ = bstack1ll11111lll_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጼ") + str(kwargs) + bstack1l1_opy_ (u"ࠦࠧጽ"))
            return {}
        capabilities = f.bstack1111l11lll_opy_(bstack1l1ll1lll1l_opy_, bstack1lll1111l11_opy_.bstack1l1ll11llll_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጾ") + str(kwargs) + bstack1l1_opy_ (u"ࠨࠢጿ"))
            return {}
        return capabilities.get(bstack1l1_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧፀ"), {})
    def bstack1ll1l1llll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs
    ):
        bstack1ll11111lll_opy_ = f.bstack1111l11lll_opy_(instance, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])
        if not bstack1ll11111lll_opy_:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፁ") + str(kwargs) + bstack1l1_opy_ (u"ࠤࠥፂ"))
            return
        if len(bstack1ll11111lll_opy_) > 1:
            self.logger.debug(bstack1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፃ") + str(kwargs) + bstack1l1_opy_ (u"ࠦࠧፄ"))
        bstack1l1ll1l11ll_opy_, bstack1l1ll1lll1l_opy_ = bstack1ll11111lll_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፅ") + str(kwargs) + bstack1l1_opy_ (u"ࠨࠢፆ"))
            return
        return driver