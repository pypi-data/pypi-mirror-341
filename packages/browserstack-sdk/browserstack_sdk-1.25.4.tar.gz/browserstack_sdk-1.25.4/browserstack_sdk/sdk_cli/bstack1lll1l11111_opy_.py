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
import time
from datetime import datetime, timezone
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
    bstack1111l11111_opy_,
    bstack11111l1l1l_opy_,
    bstack1111l1l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llllll1l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_, bstack1lll1ll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll11l11lll_opy_
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import bstack1ll11111111_opy_
from browserstack_sdk import sdk_pb2 as structs
from bstack_utils.measure import measure
from bstack_utils.constants import *
from typing import Tuple, List, Any
class bstack1lll1l1111l_opy_(bstack1ll11l11lll_opy_):
    bstack1l1l1lllll1_opy_ = bstack1l1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡴ࡬ࡺࡪࡸࡳࠣጃ")
    bstack1ll111ll111_opy_ = bstack1l1ll11_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤጄ")
    bstack1l1l1ll11ll_opy_ = bstack1l1ll11_opy_ (u"ࠦࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨጅ")
    bstack1l1l1lll11l_opy_ = bstack1l1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡷࠧጆ")
    bstack1l1l1lll1l1_opy_ = bstack1l1ll11_opy_ (u"ࠨࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡤࡸࡥࡧࡵࠥጇ")
    bstack1ll111111ll_opy_ = bstack1l1ll11_opy_ (u"ࠢࡤࡤࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤࡩࡲࡦࡣࡷࡩࡩࠨገ")
    bstack1l1l1ll1lll_opy_ = bstack1l1ll11_opy_ (u"ࠣࡥࡥࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥ࡮ࡢ࡯ࡨࠦጉ")
    bstack1l1l1ll11l1_opy_ = bstack1l1ll11_opy_ (u"ࠤࡦࡦࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡴࡶࡤࡸࡺࡹࠢጊ")
    def __init__(self):
        super().__init__(bstack1ll11l1l1l1_opy_=self.bstack1l1l1lllll1_opy_, frameworks=[bstack1llllll1l11_opy_.NAME])
        if not self.is_enabled():
            return
        TestFramework.bstack1ll1l1ll1l1_opy_((bstack1lll11l11l1_opy_.BEFORE_EACH, bstack1lll1ll111l_opy_.POST), self.bstack1l1l111l1ll_opy_)
        TestFramework.bstack1ll1l1ll1l1_opy_((bstack1lll11l11l1_opy_.TEST, bstack1lll1ll111l_opy_.PRE), self.bstack1ll1l111lll_opy_)
        TestFramework.bstack1ll1l1ll1l1_opy_((bstack1lll11l11l1_opy_.TEST, bstack1lll1ll111l_opy_.POST), self.bstack1ll1l111l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        bstack1l1lllll1ll_opy_ = self.bstack1l1l111lll1_opy_(instance.context)
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጋ") + str(bstack11111l11ll_opy_) + bstack1l1ll11_opy_ (u"ࠦࠧጌ"))
        f.bstack111111l1l1_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, bstack1l1lllll1ll_opy_)
        bstack1l1l111ll11_opy_ = self.bstack1l1l111lll1_opy_(instance.context, bstack1l1l111llll_opy_=False)
        f.bstack111111l1l1_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11ll_opy_, bstack1l1l111ll11_opy_)
    def bstack1ll1l111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll1lll_opy_, False):
            self.__1l1l111ll1l_opy_(f,instance,bstack11111l11ll_opy_)
    def bstack1ll1l111l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        if not f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll1lll_opy_, False):
            self.__1l1l111ll1l_opy_(f, instance, bstack11111l11ll_opy_)
        if not f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11l1_opy_, False):
            self.__1l1l111l111_opy_(f, instance, bstack11111l11ll_opy_)
    def bstack1l1l1111ll1_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance = exec[0]
        if not f.bstack1ll1l11l1ll_opy_(instance):
            return
        if f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11l1_opy_, False):
            return
        driver.execute_script(
            bstack1l1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥግ").format(
                json.dumps(
                    {
                        bstack1l1ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጎ"): bstack1l1ll11_opy_ (u"ࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥጏ"),
                        bstack1l1ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጐ"): {bstack1l1ll11_opy_ (u"ࠤࡶࡸࡦࡺࡵࡴࠤ጑"): result},
                    }
                )
            )
        )
        f.bstack111111l1l1_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11l1_opy_, True)
    def bstack1l1l111lll1_opy_(self, context: bstack1111l1l1l1_opy_, bstack1l1l111llll_opy_= True):
        if bstack1l1l111llll_opy_:
            bstack1l1lllll1ll_opy_ = self.bstack1ll11l1lll1_opy_(context, reverse=True)
        else:
            bstack1l1lllll1ll_opy_ = self.bstack1ll11l1l11l_opy_(context, reverse=True)
        return [f for f in bstack1l1lllll1ll_opy_ if f[1].state != bstack111111ll1l_opy_.QUIT]
    @measure(event_name=EVENTS.bstack1l1ll11111_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def __1l1l111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
    ):
        bstack1l1lllll1ll_opy_ = f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡷࡪࡺ࡟ࡢࡥࡷ࡭ࡻ࡫࡟ࡥࡴ࡬ࡺࡪࡸࡳ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࠨጒ") + str(bstack11111l11ll_opy_) + bstack1l1ll11_opy_ (u"ࠦࠧጓ"))
            return
        driver = bstack1l1lllll1ll_opy_[0][0]()
        status = f.bstack111111ll11_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_, None)
        if not status:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡹࡥࡵࡡࡤࡧࡹ࡯ࡶࡦࡡࡧࡶ࡮ࡼࡥࡳࡵ࠽ࠤࡳࡵࠠࡴࡶࡤࡸࡺࡹࠠࡧࡱࡵࠤࡹ࡫ࡳࡵ࠮ࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࠢጔ") + str(bstack11111l11ll_opy_) + bstack1l1ll11_opy_ (u"ࠨࠢጕ"))
            return
        bstack1l1l1llll11_opy_ = {bstack1l1ll11_opy_ (u"ࠢࡴࡶࡤࡸࡺࡹࠢ጖"): status.lower()}
        bstack1l1l1l1ll1l_opy_ = f.bstack111111ll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, None)
        if status.lower() == bstack1l1ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ጗") and bstack1l1l1l1ll1l_opy_ is not None:
            bstack1l1l1llll11_opy_[bstack1l1ll11_opy_ (u"ࠩࡵࡩࡦࡹ࡯࡯ࠩጘ")] = bstack1l1l1l1ll1l_opy_[0][bstack1l1ll11_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ጙ")][0] if isinstance(bstack1l1l1l1ll1l_opy_, list) else str(bstack1l1l1l1ll1l_opy_)
        driver.execute_script(
            bstack1l1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጚ").format(
                json.dumps(
                    {
                        bstack1l1ll11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጛ"): bstack1l1ll11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠤጜ"),
                        bstack1l1ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጝ"): bstack1l1l1llll11_opy_,
                    }
                )
            )
        )
        f.bstack111111l1l1_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11l1_opy_, True)
    @measure(event_name=EVENTS.bstack1l11lll11l_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def __1l1l111ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_]
    ):
        test_name = f.bstack111111ll11_opy_(instance, TestFramework.bstack1l1l111l11l_opy_, None)
        if not test_name:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢጞ"))
            return
        bstack1l1lllll1ll_opy_ = f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡶࡩࡹࡥࡡࡤࡶ࡬ࡺࡪࡥࡤࡳ࡫ࡹࡩࡷࡹ࠺ࠡࡰࡲࠤࡸࡺࡡࡵࡷࡶࠤ࡫ࡵࡲࠡࡶࡨࡷࡹ࠲ࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࠦጟ") + str(bstack11111l11ll_opy_) + bstack1l1ll11_opy_ (u"ࠥࠦጠ"))
            return
        for bstack1l1ll1ll111_opy_, bstack1l1l111l1l1_opy_ in bstack1l1lllll1ll_opy_:
            if not bstack1llllll1l11_opy_.bstack1ll1l11l1ll_opy_(bstack1l1l111l1l1_opy_):
                continue
            driver = bstack1l1ll1ll111_opy_()
            if not driver:
                continue
            driver.execute_script(
                bstack1l1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࡾࠤጡ").format(
                    json.dumps(
                        {
                            bstack1l1ll11_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࠧጢ"): bstack1l1ll11_opy_ (u"ࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢጣ"),
                            bstack1l1ll11_opy_ (u"ࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥጤ"): {bstack1l1ll11_opy_ (u"ࠣࡰࡤࡱࡪࠨጥ"): test_name},
                        }
                    )
                )
            )
        f.bstack111111l1l1_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll1lll_opy_, True)
    def bstack1ll111l1ll1_opy_(
        self,
        instance: bstack1lll1ll11l1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        bstack1l1lllll1ll_opy_ = [d for d, _ in f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])]
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤጦ"))
            return
        if not bstack1ll11111111_opy_():
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣጧ"))
            return
        for bstack1l1l11l1111_opy_ in bstack1l1lllll1ll_opy_:
            driver = bstack1l1l11l1111_opy_()
            if not driver:
                continue
            timestamp = int(time.time() * 1000)
            data = bstack1l1ll11_opy_ (u"ࠦࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࡗࡾࡴࡣ࠻ࠤጨ") + str(timestamp)
            driver.execute_script(
                bstack1l1ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠥጩ").format(
                    json.dumps(
                        {
                            bstack1l1ll11_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨጪ"): bstack1l1ll11_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤጫ"),
                            bstack1l1ll11_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦጬ"): {
                                bstack1l1ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢጭ"): bstack1l1ll11_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢጮ"),
                                bstack1l1ll11_opy_ (u"ࠦࡩࡧࡴࡢࠤጯ"): data,
                                bstack1l1ll11_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦጰ"): bstack1l1ll11_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧጱ")
                            }
                        }
                    )
                )
            )
    def bstack1l1lll111l1_opy_(
        self,
        instance: bstack1lll1ll11l1_opy_,
        f: TestFramework,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs,
    ):
        self.bstack1l1l111l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        bstack1l1lllll1ll_opy_ = [d for _, d in f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])] + [d for _, d in f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1l1l1ll11ll_opy_, [])]
        keys = [
            bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_,
            bstack1lll1l1111l_opy_.bstack1l1l1ll11ll_opy_,
        ]
        bstack1l1lllll1ll_opy_ = [
            d for key in keys for _, d in f.bstack111111ll11_opy_(instance, key, [])
        ]
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤ࡫࡯࡮ࡥࠢࡤࡲࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࡳࠡࡶࡲࠤࡱ࡯࡮࡬ࠤጲ"))
            return
        if f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111111ll_opy_, False):
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡆࡆ࡙ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡤࡴࡨࡥࡹ࡫ࡤࠣጳ"))
            return
        self.bstack1ll1lll111l_opy_()
        bstack1l1l1llll_opy_ = datetime.now()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll11lllll1_opy_)
        req.test_framework_name = TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll1l1l11ll_opy_)
        req.test_framework_version = TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll11111ll1_opy_)
        req.test_framework_state = bstack11111l11ll_opy_[0].name
        req.test_hook_state = bstack11111l11ll_opy_[1].name
        req.test_uuid = TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1ll1ll1111l_opy_)
        for driver in bstack1l1lllll1ll_opy_:
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠣጴ")
                if bstack1llllll1l11_opy_.bstack111111ll11_opy_(driver, bstack1llllll1l11_opy_.bstack1l1l1111lll_opy_, False)
                else bstack1l1ll11_opy_ (u"ࠥࡹࡳࡱ࡮ࡰࡹࡱࡣ࡬ࡸࡩࡥࠤጵ")
            )
            session.ref = driver.ref()
            session.hub_url = bstack1llllll1l11_opy_.bstack111111ll11_opy_(driver, bstack1llllll1l11_opy_.bstack1l1ll1111l1_opy_, bstack1l1ll11_opy_ (u"ࠦࠧጶ"))
            session.framework_name = driver.framework_name
            session.framework_version = driver.framework_version
            session.framework_session_id = bstack1llllll1l11_opy_.bstack111111ll11_opy_(driver, bstack1llllll1l11_opy_.bstack1l1ll11lll1_opy_, bstack1l1ll11_opy_ (u"ࠧࠨጷ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        return req
    def bstack1ll11llllll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lllll1ll_opy_ = f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤጸ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠢࠣጹ"))
            return {}
        if len(bstack1l1lllll1ll_opy_) > 1:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦጺ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠤࠥጻ"))
            return {}
        bstack1l1ll1ll111_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1lllll1ll_opy_[0]
        driver = bstack1l1ll1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጼ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠦࠧጽ"))
            return {}
        capabilities = f.bstack111111ll11_opy_(bstack1l1ll1l1ll1_opy_, bstack1llllll1l11_opy_.bstack1l1ll1l1111_opy_)
        if not capabilities:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧጾ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠨࠢጿ"))
            return {}
        return capabilities.get(bstack1l1ll11_opy_ (u"ࠢࡢ࡮ࡺࡥࡾࡹࡍࡢࡶࡦ࡬ࠧፀ"), {})
    def bstack1ll1ll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll11l1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_],
        *args,
        **kwargs
    ):
        bstack1l1lllll1ll_opy_ = f.bstack111111ll11_opy_(instance, bstack1lll1l1111l_opy_.bstack1ll111ll111_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦፁ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠤࠥፂ"))
            return
        if len(bstack1l1lllll1ll_opy_) > 1:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨፃ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠦࠧፄ"))
        bstack1l1ll1ll111_opy_, bstack1l1ll1l1ll1_opy_ = bstack1l1lllll1ll_opy_[0]
        driver = bstack1l1ll1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡤࡳ࡫ࡹࡩࡷࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢፅ") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠨࠢፆ"))
            return
        return driver