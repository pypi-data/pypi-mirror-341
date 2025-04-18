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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111ll11l_opy_ import bstack1111111l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack11l1l11l1_opy_ import bstack1l11l11l11l_opy_
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll11l11l1_opy_,
    bstack1lll1ll11l1_opy_,
    bstack1lll1ll111l_opy_,
    bstack1l11ll11l1l_opy_,
    bstack1lll11llll1_opy_,
)
import traceback
from bstack_utils.helper import bstack1ll11l11111_opy_
from bstack_utils.bstack1lll111l_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.utils.bstack1lll11l1l11_opy_ import bstack1lll111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1lll1_opy_
bstack1l1lll11lll_opy_ = bstack1ll11l11111_opy_()
bstack1ll11111l1l_opy_ = bstack1l1ll11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ፡")
bstack1l11l1l111l_opy_ = bstack1l1ll11_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤ።")
bstack1l11l1lll11_opy_ = bstack1l1ll11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ፣")
bstack1l111l1l1l1_opy_ = 1.0
_1ll111l11l1_opy_ = set()
class PytestBDDFramework(TestFramework):
    bstack1l11ll1lll1_opy_ = bstack1l1ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣ፤")
    bstack1l11ll1l11l_opy_ = bstack1l1ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢ፥")
    bstack1l11l111111_opy_ = bstack1l1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤ፦")
    bstack1l11ll1ll11_opy_ = bstack1l1ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨ፧")
    bstack1l11lll1111_opy_ = bstack1l1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣ፨")
    bstack1l11ll111l1_opy_: bool
    bstack1111l1l1ll_opy_: bstack1111l1lll1_opy_  = None
    bstack1l11l1ll1ll_opy_ = [
        bstack1lll11l11l1_opy_.BEFORE_ALL,
        bstack1lll11l11l1_opy_.AFTER_ALL,
        bstack1lll11l11l1_opy_.BEFORE_EACH,
        bstack1lll11l11l1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11l11lll1_opy_: Dict[str, str],
        bstack1ll1ll1l111_opy_: List[str]=[bstack1l1ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠥ፩")],
        bstack1111l1l1ll_opy_: bstack1111l1lll1_opy_ = None,
        bstack1llll111ll1_opy_=None
    ):
        super().__init__(bstack1ll1ll1l111_opy_, bstack1l11l11lll1_opy_, bstack1111l1l1ll_opy_)
        self.bstack1l11ll111l1_opy_ = any(bstack1l1ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦ፪") in item.lower() for item in bstack1ll1ll1l111_opy_)
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
    def track_event(
        self,
        context: bstack1l11ll11l1l_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        test_hook_state: bstack1lll1ll111l_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll11l11l1_opy_.TEST or test_framework_state in PytestBDDFramework.bstack1l11l1ll1ll_opy_:
            bstack1l11l11l11l_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll11l11l1_opy_.NONE:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤ፫") + str(test_hook_state) + bstack1l1ll11_opy_ (u"ࠤࠥ፬"))
            return
        if not self.bstack1l11ll111l1_opy_:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦ፭") + str(str(self.bstack1ll1ll1l111_opy_)) + bstack1l1ll11_opy_ (u"ࠦࠧ፮"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ፯") + str(kwargs) + bstack1l1ll11_opy_ (u"ࠨࠢ፰"))
            return
        instance = self.__1l11ll11lll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨ፱") + str(args) + bstack1l1ll11_opy_ (u"ࠣࠤ፲"))
            return
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1ll1ll_opy_ and test_hook_state == bstack1lll1ll111l_opy_.PRE:
                bstack1ll1ll11l1l_opy_ = bstack1ll1llllll1_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack1lll1111l_opy_.value)
                name = str(EVENTS.bstack1lll1111l_opy_.name)+bstack1l1ll11_opy_ (u"ࠤ࠽ࠦ፳")+str(test_framework_state.name)
                TestFramework.bstack1l11l1lllll_opy_(instance, name, bstack1ll1ll11l1l_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢ፴").format(e))
        try:
            if test_framework_state == bstack1lll11l11l1_opy_.TEST:
                if not TestFramework.bstack11111l1111_opy_(instance, TestFramework.bstack1l11l1l1lll_opy_) and test_hook_state == bstack1lll1ll111l_opy_.PRE:
                    if not (len(args) >= 3):
                        return
                    test = PytestBDDFramework.__1l11l111l1l_opy_(args)
                    if test:
                        instance.data.update(test)
                        self.logger.debug(bstack1l1ll11_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ፵") + str(test_hook_state) + bstack1l1ll11_opy_ (u"ࠧࠨ፶"))
                if test_hook_state == bstack1lll1ll111l_opy_.PRE and not TestFramework.bstack11111l1111_opy_(instance, TestFramework.bstack1l1lll11l11_opy_):
                    TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1l1lll11l11_opy_, datetime.now(tz=timezone.utc))
                    PytestBDDFramework.__1l11lll1lll_opy_(instance, args)
                    self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ፷") + str(test_hook_state) + bstack1l1ll11_opy_ (u"ࠢࠣ፸"))
                elif test_hook_state == bstack1lll1ll111l_opy_.POST and not TestFramework.bstack11111l1111_opy_(instance, TestFramework.bstack1l1lll11111_opy_):
                    TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1l1lll11111_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ፹") + str(test_hook_state) + bstack1l1ll11_opy_ (u"ࠤࠥ፺"))
            elif test_framework_state == bstack1lll11l11l1_opy_.STEP:
                if test_hook_state == bstack1lll1ll111l_opy_.PRE:
                    PytestBDDFramework.__1l11l11llll_opy_(instance, args)
                elif test_hook_state == bstack1lll1ll111l_opy_.POST:
                    PytestBDDFramework.__1l11l1l11ll_opy_(instance, args)
            elif test_framework_state == bstack1lll11l11l1_opy_.LOG and test_hook_state == bstack1lll1ll111l_opy_.POST:
                PytestBDDFramework.__1l11l11l111_opy_(instance, *args)
            elif test_framework_state == bstack1lll11l11l1_opy_.LOG_REPORT and test_hook_state == bstack1lll1ll111l_opy_.POST:
                self.__1l11l1l1ll1_opy_(instance, *args)
                self.__1l111ll11l1_opy_(instance)
            elif test_framework_state in PytestBDDFramework.bstack1l11l1ll1ll_opy_:
                self.__1l111llll1l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦ፻") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠦࠧ፼"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11ll1l1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in PytestBDDFramework.bstack1l11l1ll1ll_opy_ and test_hook_state == bstack1lll1ll111l_opy_.POST:
                name = str(EVENTS.bstack1lll1111l_opy_.name)+bstack1l1ll11_opy_ (u"ࠧࡀࠢ፽")+str(test_framework_state.name)
                bstack1ll1ll11l1l_opy_ = TestFramework.bstack1l11lll1l11_opy_(instance, name)
                bstack1ll1llllll1_opy_.end(EVENTS.bstack1lll1111l_opy_.value, bstack1ll1ll11l1l_opy_+bstack1l1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ፾"), bstack1ll1ll11l1l_opy_+bstack1l1ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ፿"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᎀ").format(e))
    def bstack1ll1111111l_opy_(self):
        return self.bstack1l11ll111l1_opy_
    def __1l111ll1l11_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1ll11_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᎁ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1l1llllll1l_opy_(rep, [bstack1l1ll11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᎂ"), bstack1l1ll11_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᎃ"), bstack1l1ll11_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᎄ"), bstack1l1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᎅ"), bstack1l1ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᎆ"), bstack1l1ll11_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᎇ")])
        return None
    def __1l11l1l1ll1_opy_(self, instance: bstack1lll1ll11l1_opy_, *args):
        result = self.__1l111ll1l11_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll111l_opy_ = None
        if result.get(bstack1l1ll11_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᎈ"), None) == bstack1l1ll11_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᎉ") and len(args) > 1 and getattr(args[1], bstack1l1ll11_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᎊ"), None) is not None:
            failure = [{bstack1l1ll11_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᎋ"): [args[1].excinfo.exconly(), result.get(bstack1l1ll11_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᎌ"), None)]}]
            bstack1111ll111l_opy_ = bstack1l1ll11_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᎍ") if bstack1l1ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᎎ") in getattr(args[1].excinfo, bstack1l1ll11_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᎏ"), bstack1l1ll11_opy_ (u"ࠥࠦ᎐")) else bstack1l1ll11_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ᎑")
        bstack1l11l1ll11l_opy_ = result.get(bstack1l1ll11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ᎒"), TestFramework.bstack1l111ll1ll1_opy_)
        if bstack1l11l1ll11l_opy_ != TestFramework.bstack1l111ll1ll1_opy_:
            TestFramework.bstack111111l1l1_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11ll1111l_opy_(instance, {
            TestFramework.bstack1l1l1ll1ll1_opy_: failure,
            TestFramework.bstack1l111l1ll1l_opy_: bstack1111ll111l_opy_,
            TestFramework.bstack1l1l1ll111l_opy_: bstack1l11l1ll11l_opy_,
        })
    def __1l11ll11lll_opy_(
        self,
        context: bstack1l11ll11l1l_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        test_hook_state: bstack1lll1ll111l_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll11l11l1_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1llll1_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l111lll1l1_opy_ bstack1l111ll111l_opy_ this to be bstack1l1ll11_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨ᎓")
            if test_framework_state == bstack1lll11l11l1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l11l1ll_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll11l11l1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1ll11_opy_ (u"ࠢ࡯ࡱࡧࡩࠧ᎔"), None), bstack1l1ll11_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣ᎕"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ᎖"), None):
                target = args[0].node.nodeid
            elif getattr(args[0], bstack1l1ll11_opy_ (u"ࠥࡲࡴࡪࡥࡪࡦࠥ᎗"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack11111111l1_opy_(target) if target else None
        return instance
    def __1l111llll1l_opy_(
        self,
        instance: bstack1lll1ll11l1_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        test_hook_state: bstack1lll1ll111l_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111lllll1_opy_ = TestFramework.bstack111111ll11_opy_(instance, PytestBDDFramework.bstack1l11ll1l11l_opy_, {})
        if not key in bstack1l111lllll1_opy_:
            bstack1l111lllll1_opy_[key] = []
        bstack1l11ll1l111_opy_ = TestFramework.bstack111111ll11_opy_(instance, PytestBDDFramework.bstack1l11l111111_opy_, {})
        if not key in bstack1l11ll1l111_opy_:
            bstack1l11ll1l111_opy_[key] = []
        bstack1l11lll11l1_opy_ = {
            PytestBDDFramework.bstack1l11ll1l11l_opy_: bstack1l111lllll1_opy_,
            PytestBDDFramework.bstack1l11l111111_opy_: bstack1l11ll1l111_opy_,
        }
        if test_hook_state == bstack1lll1ll111l_opy_.PRE:
            hook_name = args[1] if len(args) > 1 else None
            hook = {
                bstack1l1ll11_opy_ (u"ࠦࡰ࡫ࡹࠣ᎘"): key,
                TestFramework.bstack1l111ll1lll_opy_: uuid4().__str__(),
                TestFramework.bstack1l11ll11l11_opy_: TestFramework.bstack1l111l1llll_opy_,
                TestFramework.bstack1l11l11111l_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11ll111ll_opy_: [],
                TestFramework.bstack1l111lll11l_opy_: hook_name,
                TestFramework.bstack1l11lll11ll_opy_: bstack1lll111lll1_opy_.bstack1l11l111ll1_opy_()
            }
            bstack1l111lllll1_opy_[key].append(hook)
            bstack1l11lll11l1_opy_[PytestBDDFramework.bstack1l11ll1ll11_opy_] = key
        elif test_hook_state == bstack1lll1ll111l_opy_.POST:
            bstack1l11lll1ll1_opy_ = bstack1l111lllll1_opy_.get(key, [])
            hook = bstack1l11lll1ll1_opy_.pop() if bstack1l11lll1ll1_opy_ else None
            if hook:
                result = self.__1l111ll1l11_opy_(*args)
                if result:
                    bstack1l11l1l1111_opy_ = result.get(bstack1l1ll11_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨ᎙"), TestFramework.bstack1l111l1llll_opy_)
                    if bstack1l11l1l1111_opy_ != TestFramework.bstack1l111l1llll_opy_:
                        hook[TestFramework.bstack1l11ll11l11_opy_] = bstack1l11l1l1111_opy_
                hook[TestFramework.bstack1l111lll1ll_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11lll11ll_opy_] = bstack1lll111lll1_opy_.bstack1l11l111ll1_opy_()
                self.bstack1l11l1111l1_opy_(hook)
                logs = hook.get(TestFramework.bstack1l11l1ll111_opy_, [])
                self.bstack1ll11l1111l_opy_(instance, logs)
                bstack1l11ll1l111_opy_[key].append(hook)
                bstack1l11lll11l1_opy_[PytestBDDFramework.bstack1l11lll1111_opy_] = key
        TestFramework.bstack1l11ll1111l_opy_(instance, bstack1l11lll11l1_opy_)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧ᎚") + str(bstack1l11ll1l111_opy_) + bstack1l1ll11_opy_ (u"ࠢࠣ᎛"))
    def __1l11l1llll1_opy_(
        self,
        context: bstack1l11ll11l1l_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        test_hook_state: bstack1lll1ll111l_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1l1llllll1l_opy_(args[0], [bstack1l1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢ᎜"), bstack1l1ll11_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥ᎝"), bstack1l1ll11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥ᎞"), bstack1l1ll11_opy_ (u"ࠦ࡮ࡪࡳࠣ᎟"), bstack1l1ll11_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᎠ"), bstack1l1ll11_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᎡ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scenario = args[2] if len(args) == 3 else None
        scope = request.scope if hasattr(request, bstack1l1ll11_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᎢ")) else fixturedef.get(bstack1l1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᎣ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1ll11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᎤ")) else None
        node = request.node if hasattr(request, bstack1l1ll11_opy_ (u"ࠥࡲࡴࡪࡥࠣᎥ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1ll11_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᎦ")) else None
        baseid = fixturedef.get(bstack1l1ll11_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᎧ"), None) or bstack1l1ll11_opy_ (u"ࠨࠢᎨ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1ll11_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᎩ")):
            target = PytestBDDFramework.__1l111ll1l1l_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1ll11_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᎪ")) else None
            if target and not TestFramework.bstack11111111l1_opy_(target):
                self.__1l11l11l1ll_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᎫ") + str(test_hook_state) + bstack1l1ll11_opy_ (u"ࠥࠦᎬ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᎭ") + str(target) + bstack1l1ll11_opy_ (u"ࠧࠨᎮ"))
            return None
        instance = TestFramework.bstack11111111l1_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᎯ") + str(target) + bstack1l1ll11_opy_ (u"ࠢࠣᎰ"))
            return None
        bstack1l111ll11ll_opy_ = TestFramework.bstack111111ll11_opy_(instance, PytestBDDFramework.bstack1l11ll1lll1_opy_, {})
        if os.getenv(bstack1l1ll11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᎱ"), bstack1l1ll11_opy_ (u"ࠤ࠴ࠦᎲ")) == bstack1l1ll11_opy_ (u"ࠥ࠵ࠧᎳ"):
            bstack1l111l1ll11_opy_ = bstack1l1ll11_opy_ (u"ࠦ࠿ࠨᎴ").join((scope, fixturename))
            bstack1l11llll11l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll111l_opy_ = {
                bstack1l1ll11_opy_ (u"ࠧࡱࡥࡺࠤᎵ"): bstack1l111l1ll11_opy_,
                bstack1l1ll11_opy_ (u"ࠨࡴࡢࡩࡶࠦᎶ"): PytestBDDFramework.__1l11l1l1l1l_opy_(request.node, scenario),
                bstack1l1ll11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᎷ"): fixturedef,
                bstack1l1ll11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᎸ"): scope,
                bstack1l1ll11_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᎹ"): None,
            }
            try:
                if test_hook_state == bstack1lll1ll111l_opy_.POST and callable(getattr(args[-1], bstack1l1ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᎺ"), None)):
                    bstack1l11lll111l_opy_[bstack1l1ll11_opy_ (u"ࠦࡹࡿࡰࡦࠤᎻ")] = TestFramework.bstack1ll1111l1ll_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1lll1ll111l_opy_.PRE:
                bstack1l11lll111l_opy_[bstack1l1ll11_opy_ (u"ࠧࡻࡵࡪࡦࠥᎼ")] = uuid4().__str__()
                bstack1l11lll111l_opy_[PytestBDDFramework.bstack1l11l11111l_opy_] = bstack1l11llll11l_opy_
            elif test_hook_state == bstack1lll1ll111l_opy_.POST:
                bstack1l11lll111l_opy_[PytestBDDFramework.bstack1l111lll1ll_opy_] = bstack1l11llll11l_opy_
            if bstack1l111l1ll11_opy_ in bstack1l111ll11ll_opy_:
                bstack1l111ll11ll_opy_[bstack1l111l1ll11_opy_].update(bstack1l11lll111l_opy_)
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᎽ") + str(bstack1l111ll11ll_opy_[bstack1l111l1ll11_opy_]) + bstack1l1ll11_opy_ (u"ࠢࠣᎾ"))
            else:
                bstack1l111ll11ll_opy_[bstack1l111l1ll11_opy_] = bstack1l11lll111l_opy_
                self.logger.debug(bstack1l1ll11_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᎿ") + str(len(bstack1l111ll11ll_opy_)) + bstack1l1ll11_opy_ (u"ࠤࠥᏀ"))
        TestFramework.bstack111111l1l1_opy_(instance, PytestBDDFramework.bstack1l11ll1lll1_opy_, bstack1l111ll11ll_opy_)
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᏁ") + str(instance.ref()) + bstack1l1ll11_opy_ (u"ࠦࠧᏂ"))
        return instance
    def __1l11l11l1ll_opy_(
        self,
        context: bstack1l11ll11l1l_opy_,
        test_framework_state: bstack1lll11l11l1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack1111111l11_opy_.create_context(target)
        ob = bstack1lll1ll11l1_opy_(ctx, self.bstack1ll1ll1l111_opy_, self.bstack1l11l11lll1_opy_, test_framework_state)
        TestFramework.bstack1l11ll1111l_opy_(ob, {
            TestFramework.bstack1ll1l1l11ll_opy_: context.test_framework_name,
            TestFramework.bstack1ll11111ll1_opy_: context.test_framework_version,
            TestFramework.bstack1l11llll1l1_opy_: [],
            PytestBDDFramework.bstack1l11ll1lll1_opy_: {},
            PytestBDDFramework.bstack1l11l111111_opy_: {},
            PytestBDDFramework.bstack1l11ll1l11l_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack111111l1l1_opy_(ob, TestFramework.bstack1l111l1l1ll_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack111111l1l1_opy_(ob, TestFramework.bstack1ll11lllll1_opy_, context.platform_index)
        TestFramework.bstack1111l1111l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1ll11_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᏃ") + str(TestFramework.bstack1111l1111l_opy_.keys()) + bstack1l1ll11_opy_ (u"ࠨࠢᏄ"))
        return ob
    @staticmethod
    def __1l11lll1lll_opy_(instance, args):
        request, feature, scenario = args
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1ll11_opy_ (u"ࠧࡪࡦࠪᏅ"): id(step),
                bstack1l1ll11_opy_ (u"ࠨࡶࡨࡼࡹ࠭Ꮖ"): step.name,
                bstack1l1ll11_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᏇ"): step.keyword,
            })
        meta = {
            bstack1l1ll11_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᏈ"): {
                bstack1l1ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏉ"): feature.name,
                bstack1l1ll11_opy_ (u"ࠬࡶࡡࡵࡪࠪᏊ"): feature.filename,
                bstack1l1ll11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᏋ"): feature.description
            },
            bstack1l1ll11_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᏌ"): {
                bstack1l1ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭Ꮝ"): scenario.name
            },
            bstack1l1ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏎ"): steps,
            bstack1l1ll11_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᏏ"): PytestBDDFramework.__1l11l111l11_opy_(request.node)
        }
        instance.data.update(
            {
                TestFramework.bstack1l11ll1l1ll_opy_: meta
            }
        )
    def bstack1l11l1111l1_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡒࡵࡳࡨ࡫ࡳࡴࡧࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡶ࡭ࡲ࡯࡬ࡢࡴࠣࡸࡴࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙࡮ࡩࡴࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦ࠭ࠡࡅ࡫ࡩࡨࡱࡳࠡࡶ࡫ࡩࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬ࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡮ࡴࡳࡪࡦࡨࠤࢃ࠵࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠵ࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡋࡵࡲࠡࡧࡤࡧ࡭ࠦࡦࡪ࡮ࡨࠤ࡮ࡴࠠࡩࡱࡲ࡯ࡤࡲࡥࡷࡧ࡯ࡣ࡫࡯࡬ࡦࡵ࠯ࠤࡷ࡫ࡰ࡭ࡣࡦࡩࡸࠦࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥࠤࡼ࡯ࡴࡩࠢࠥࡌࡴࡵ࡫ࡍࡧࡹࡩࡱࠨࠠࡪࡰࠣ࡭ࡹࡹࠠࡱࡣࡷ࡬࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡎ࡬ࠠࡢࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣࡸ࡭࡫ࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡱࡦࡺࡣࡩࡧࡶࠤࡦࠦ࡭ࡰࡦ࡬ࡪ࡮࡫ࡤࠡࡪࡲࡳࡰ࠳࡬ࡦࡸࡨࡰࠥ࡬ࡩ࡭ࡧ࠯ࠤ࡮ࡺࠠࡤࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡐࡴ࡭ࡅ࡯ࡶࡵࡽࠥࡵࡢ࡫ࡧࡦࡸࠥࡽࡩࡵࡪࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥࡧࡷࡥ࡮ࡲࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡔ࡫ࡰ࡭ࡱࡧࡲ࡭ࡻ࠯ࠤ࡮ࡺࠠࡱࡴࡲࡧࡪࡹࡳࡦࡵࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡲ࡯ࡤࡣࡷࡩࡩࠦࡩ࡯ࠢࡋࡳࡴࡱࡌࡦࡸࡨࡰ࠴ࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡧࡿࠠࡳࡧࡳࡰࡦࡩࡩ࡯ࡩࠣࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣࠢࡺ࡭ࡹ࡮ࠠࠣࡊࡲࡳࡰࡒࡥࡷࡧ࡯࠳ࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࡉࡱࡲ࡯ࡊࡼࡥ࡯ࡶࠥ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡘ࡭࡫ࠠࡤࡴࡨࡥࡹ࡫ࡤࠡࡎࡲ࡫ࡊࡴࡴࡳࡻࠣࡳࡧࡰࡥࡤࡶࡶࠤࡦࡸࡥࠡࡣࡧࡨࡪࡪࠠࡵࡱࠣࡸ࡭࡫ࠠࡩࡱࡲ࡯ࠬࡹࠠࠣ࡮ࡲ࡫ࡸࠨࠠ࡭࡫ࡶࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵ࡯࡬࠼ࠣࡘ࡭࡫ࠠࡦࡸࡨࡲࡹࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡦࡺ࡬ࡷࡹ࡯࡮ࡨࠢ࡯ࡳ࡬ࡹࠠࡢࡰࡧࠤ࡭ࡵ࡯࡬ࠢ࡬ࡲ࡫ࡵࡲ࡮ࡣࡷ࡭ࡴࡴ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰࡱ࡮ࡣࡱ࡫ࡶࡦ࡮ࡢࡪ࡮ࡲࡥࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤࡕࡧࡴࡩࠢࡲࡦ࡯࡫ࡣࡵࡵࠣࡪࡷࡵ࡭ࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡧࡻࡩ࡭ࡦࡢࡰࡪࡼࡥ࡭ࡡࡩ࡭ࡱ࡫ࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡔࡦࡺࡨࠡࡱࡥ࡮ࡪࡩࡴࡴࠢࡩࡶࡴࡳࠠࡵࡪࡨࠤࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠡ࡯ࡲࡲ࡮ࡺ࡯ࡳ࡫ࡱ࡫࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᏐ")
        global _1ll111l11l1_opy_
        platform_index = os.environ[bstack1l1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᏑ")]
        bstack1ll111llll1_opy_ = os.path.join(bstack1l1lll11lll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l11l1l111l_opy_)
        if not os.path.exists(bstack1ll111llll1_opy_) or not os.path.isdir(bstack1ll111llll1_opy_):
            return
        logs = hook.get(bstack1l1ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᏒ"), [])
        with os.scandir(bstack1ll111llll1_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111l11l1_opy_:
                    self.logger.info(bstack1l1ll11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᏓ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1ll11_opy_ (u"ࠣࠤᏔ")
                    log_entry = bstack1lll11llll1_opy_(
                        kind=bstack1l1ll11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᏕ"),
                        message=bstack1l1ll11_opy_ (u"ࠥࠦᏖ"),
                        level=bstack1l1ll11_opy_ (u"ࠦࠧᏗ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1ll1111llll_opy_=entry.stat().st_size,
                        bstack1l1lll1l11l_opy_=bstack1l1ll11_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᏘ"),
                        bstack11lll11_opy_=os.path.abspath(entry.path),
                        bstack1l11l1lll1l_opy_=hook.get(TestFramework.bstack1l111ll1lll_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111l11l1_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮩ")]
        bstack1l11l1111ll_opy_ = os.path.join(bstack1l1lll11lll_opy_, (bstack1ll11111l1l_opy_ + str(platform_index)), bstack1l11l1l111l_opy_, bstack1l11l1lll11_opy_)
        if not os.path.exists(bstack1l11l1111ll_opy_) or not os.path.isdir(bstack1l11l1111ll_opy_):
            self.logger.info(bstack1l1ll11_opy_ (u"ࠢࡏࡱࠣࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࡈࡰࡱ࡮ࡉࡻ࡫࡮ࡵࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡪࡴࡻ࡮ࡥࠢࡤࡸ࠿ࠦࡻࡾࠤᏚ").format(bstack1l11l1111ll_opy_))
        else:
            self.logger.info(bstack1l1ll11_opy_ (u"ࠣࡒࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࡊࡲࡳࡰࡋࡶࡦࡰࡷࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡩࡶࡴࡳࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻ࠽ࠤࢀࢃࠢᏛ").format(bstack1l11l1111ll_opy_))
            with os.scandir(bstack1l11l1111ll_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111l11l1_opy_:
                        self.logger.info(bstack1l1ll11_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᏜ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1ll11_opy_ (u"ࠥࠦᏝ")
                        log_entry = bstack1lll11llll1_opy_(
                            kind=bstack1l1ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᏞ"),
                            message=bstack1l1ll11_opy_ (u"ࠧࠨᏟ"),
                            level=bstack1l1ll11_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᏠ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1ll1111llll_opy_=entry.stat().st_size,
                            bstack1l1lll1l11l_opy_=bstack1l1ll11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᏡ"),
                            bstack11lll11_opy_=os.path.abspath(entry.path),
                            bstack1l1llll1lll_opy_=hook.get(TestFramework.bstack1l111ll1lll_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111l11l1_opy_.add(abs_path)
        hook[bstack1l1ll11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᏢ")] = logs
    def bstack1ll11l1111l_opy_(
        self,
        bstack1ll111ll1l1_opy_: bstack1lll1ll11l1_opy_,
        entries: List[bstack1lll11llll1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1ll11_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᏣ"))
        req.platform_index = TestFramework.bstack111111ll11_opy_(bstack1ll111ll1l1_opy_, TestFramework.bstack1ll11lllll1_opy_)
        req.execution_context.hash = str(bstack1ll111ll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1ll111ll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1ll111ll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack111111ll11_opy_(bstack1ll111ll1l1_opy_, TestFramework.bstack1ll1l1l11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack111111ll11_opy_(bstack1ll111ll1l1_opy_, TestFramework.bstack1ll11111ll1_opy_)
            log_entry.uuid = entry.bstack1l11l1lll1l_opy_
            log_entry.test_framework_state = bstack1ll111ll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᏤ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1ll11_opy_ (u"ࠦࠧᏥ")
            if entry.kind == bstack1l1ll11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏦ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll1111llll_opy_
                log_entry.file_path = entry.bstack11lll11_opy_
        def bstack1l1llll11ll_opy_():
            bstack1l1l1llll_opy_ = datetime.now()
            try:
                self.bstack1llll111ll1_opy_.LogCreatedEvent(req)
                bstack1ll111ll1l1_opy_.bstack11lll111l_opy_(bstack1l1ll11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᏧ"), datetime.now() - bstack1l1l1llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿࢂࠨᏨ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1l1ll_opy_.enqueue(bstack1l1llll11ll_opy_)
    def __1l111ll11l1_opy_(self, instance) -> None:
        bstack1l1ll11_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᏩ")
        bstack1l11lll11l1_opy_ = {bstack1l1ll11_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᏪ"): bstack1lll111lll1_opy_.bstack1l11l111ll1_opy_()}
        TestFramework.bstack1l11ll1111l_opy_(instance, bstack1l11lll11l1_opy_)
    @staticmethod
    def __1l11l11llll_opy_(instance, args):
        request, bstack1l111llllll_opy_ = args
        bstack1l11l11ll11_opy_ = id(bstack1l111llllll_opy_)
        bstack1l11l1ll1l1_opy_ = instance.data[TestFramework.bstack1l11ll1l1ll_opy_]
        step = next(filter(lambda st: st[bstack1l1ll11_opy_ (u"ࠪ࡭ࡩ࠭Ꮻ")] == bstack1l11l11ll11_opy_, bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᏬ")]), None)
        step.update({
            bstack1l1ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᏭ"): datetime.now(tz=timezone.utc)
        })
        index = next((i for i, st in enumerate(bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏮ")]) if st[bstack1l1ll11_opy_ (u"ࠧࡪࡦࠪᏯ")] == step[bstack1l1ll11_opy_ (u"ࠨ࡫ࡧࠫᏰ")]), None)
        if index is not None:
            bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᏱ")][index] = step
        instance.data[TestFramework.bstack1l11ll1l1ll_opy_] = bstack1l11l1ll1l1_opy_
    @staticmethod
    def __1l11l1l11ll_opy_(instance, args):
        bstack1l1ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡸࡪࡨࡲࠥࡲࡥ࡯ࠢࡤࡶ࡬ࡹࠠࡪࡵࠣ࠶࠱ࠦࡩࡵࠢࡶ࡭࡬ࡴࡩࡧ࡫ࡨࡷࠥࡺࡨࡦࡴࡨࠤ࡮ࡹࠠ࡯ࡱࠣࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࡴࠢࡤࡶࡪࠦ࠭ࠡ࡝ࡵࡩࡶࡻࡥࡴࡶ࠯ࠤࡸࡺࡥࡱ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࡢࡴࡪࡷࠥࡧࡲࡦࠢ࠶ࠤࡹ࡮ࡥ࡯ࠢࡷ࡬ࡪࠦ࡬ࡢࡵࡷࠤࡻࡧ࡬ࡶࡧࠣ࡭ࡸࠦࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᏲ")
        bstack1l111l1lll1_opy_ = datetime.now(tz=timezone.utc)
        request = args[0]
        bstack1l111llllll_opy_ = args[1]
        bstack1l11l11ll11_opy_ = id(bstack1l111llllll_opy_)
        bstack1l11l1ll1l1_opy_ = instance.data[TestFramework.bstack1l11ll1l1ll_opy_]
        step = None
        if bstack1l11l11ll11_opy_ is not None and bstack1l11l1ll1l1_opy_.get(bstack1l1ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᏳ")):
            step = next(filter(lambda st: st[bstack1l1ll11_opy_ (u"ࠬ࡯ࡤࠨᏴ")] == bstack1l11l11ll11_opy_, bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏵ")]), None)
            step.update({
                bstack1l1ll11_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬ᏶"): bstack1l111l1lll1_opy_,
            })
        if len(args) > 2:
            exception = args[2]
            step.update({
                bstack1l1ll11_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᏷"): bstack1l1ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᏸ"),
                bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫᏹ"): str(exception)
            })
        else:
            if step is not None:
                step.update({
                    bstack1l1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᏺ"): bstack1l1ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᏻ"),
                })
        index = next((i for i, st in enumerate(bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᏼ")]) if st[bstack1l1ll11_opy_ (u"ࠧࡪࡦࠪᏽ")] == step[bstack1l1ll11_opy_ (u"ࠨ࡫ࡧࠫ᏾")]), None)
        if index is not None:
            bstack1l11l1ll1l1_opy_[bstack1l1ll11_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ᏿")][index] = step
        instance.data[TestFramework.bstack1l11ll1l1ll_opy_] = bstack1l11l1ll1l1_opy_
    @staticmethod
    def __1l11l111l11_opy_(node):
        try:
            examples = []
            if hasattr(node, bstack1l1ll11_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬ᐀")):
                examples = list(node.callspec.params[bstack1l1ll11_opy_ (u"ࠫࡤࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡨࡼࡦࡳࡰ࡭ࡧࠪᐁ")].values())
            return examples
        except:
            return []
    def bstack1l1lll1l1ll_opy_(self, instance: bstack1lll1ll11l1_opy_, bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_]):
        bstack1l11l1l1l11_opy_ = (
            PytestBDDFramework.bstack1l11ll1ll11_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1ll111l_opy_.PRE
            else PytestBDDFramework.bstack1l11lll1111_opy_
        )
        hook = PytestBDDFramework.bstack1l11ll11ll1_opy_(instance, bstack1l11l1l1l11_opy_)
        entries = hook.get(TestFramework.bstack1l11ll111ll_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1l11llll1l1_opy_, []))
        return entries
    def bstack1ll111l111l_opy_(self, instance: bstack1lll1ll11l1_opy_, bstack11111l11ll_opy_: Tuple[bstack1lll11l11l1_opy_, bstack1lll1ll111l_opy_]):
        bstack1l11l1l1l11_opy_ = (
            PytestBDDFramework.bstack1l11ll1ll11_opy_
            if bstack11111l11ll_opy_[1] == bstack1lll1ll111l_opy_.PRE
            else PytestBDDFramework.bstack1l11lll1111_opy_
        )
        PytestBDDFramework.bstack1l111ll1111_opy_(instance, bstack1l11l1l1l11_opy_)
        TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1l11llll1l1_opy_, []).clear()
    @staticmethod
    def bstack1l11ll11ll1_opy_(instance: bstack1lll1ll11l1_opy_, bstack1l11l1l1l11_opy_: str):
        bstack1l11ll1ll1l_opy_ = (
            PytestBDDFramework.bstack1l11l111111_opy_
            if bstack1l11l1l1l11_opy_ == PytestBDDFramework.bstack1l11lll1111_opy_
            else PytestBDDFramework.bstack1l11ll1l11l_opy_
        )
        bstack1l11ll1llll_opy_ = TestFramework.bstack111111ll11_opy_(instance, bstack1l11l1l1l11_opy_, None)
        bstack1l11l11l1l1_opy_ = TestFramework.bstack111111ll11_opy_(instance, bstack1l11ll1ll1l_opy_, None) if bstack1l11ll1llll_opy_ else None
        return (
            bstack1l11l11l1l1_opy_[bstack1l11ll1llll_opy_][-1]
            if isinstance(bstack1l11l11l1l1_opy_, dict) and len(bstack1l11l11l1l1_opy_.get(bstack1l11ll1llll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111ll1111_opy_(instance: bstack1lll1ll11l1_opy_, bstack1l11l1l1l11_opy_: str):
        hook = PytestBDDFramework.bstack1l11ll11ll1_opy_(instance, bstack1l11l1l1l11_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11ll111ll_opy_, []).clear()
    @staticmethod
    def __1l11l11l111_opy_(instance: bstack1lll1ll11l1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡵࡩࡨࡵࡲࡥࡵࠥᐂ"), None)):
            return
        if os.getenv(bstack1l1ll11_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡒࡏࡈࡕࠥᐃ"), bstack1l1ll11_opy_ (u"ࠢ࠲ࠤᐄ")) != bstack1l1ll11_opy_ (u"ࠣ࠳ࠥᐅ"):
            PytestBDDFramework.logger.warning(bstack1l1ll11_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡪࡰࡪࠤࡨࡧࡰ࡭ࡱࡪࠦᐆ"))
            return
        bstack1l111lll111_opy_ = {
            bstack1l1ll11_opy_ (u"ࠥࡷࡪࡺࡵࡱࠤᐇ"): (PytestBDDFramework.bstack1l11ll1ll11_opy_, PytestBDDFramework.bstack1l11ll1l11l_opy_),
            bstack1l1ll11_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࠨᐈ"): (PytestBDDFramework.bstack1l11lll1111_opy_, PytestBDDFramework.bstack1l11l111111_opy_),
        }
        for when in (bstack1l1ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᐉ"), bstack1l1ll11_opy_ (u"ࠨࡣࡢ࡮࡯ࠦᐊ"), bstack1l1ll11_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࠤᐋ")):
            bstack1l11ll11111_opy_ = args[1].get_records(when)
            if not bstack1l11ll11111_opy_:
                continue
            records = [
                bstack1lll11llll1_opy_(
                    kind=TestFramework.bstack1l1lll1l111_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1ll11_opy_ (u"ࠣ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨࠦᐌ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1ll11_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠥᐍ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11111_opy_
                if isinstance(getattr(r, bstack1l1ll11_opy_ (u"ࠥࡱࡪࡹࡳࡢࡩࡨࠦᐎ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l1l11l1_opy_, bstack1l11ll1ll1l_opy_ = bstack1l111lll111_opy_.get(when, (None, None))
            bstack1l11llll111_opy_ = TestFramework.bstack111111ll11_opy_(instance, bstack1l11l1l11l1_opy_, None) if bstack1l11l1l11l1_opy_ else None
            bstack1l11l11l1l1_opy_ = TestFramework.bstack111111ll11_opy_(instance, bstack1l11ll1ll1l_opy_, None) if bstack1l11llll111_opy_ else None
            if isinstance(bstack1l11l11l1l1_opy_, dict) and len(bstack1l11l11l1l1_opy_.get(bstack1l11llll111_opy_, [])) > 0:
                hook = bstack1l11l11l1l1_opy_[bstack1l11llll111_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11ll111ll_opy_ in hook:
                    hook[TestFramework.bstack1l11ll111ll_opy_].extend(records)
                    continue
            logs = TestFramework.bstack111111ll11_opy_(instance, TestFramework.bstack1l11llll1l1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11l111l1l_opy_(args) -> Dict[str, Any]:
        request, feature, scenario = args
        bstack1ll1l11ll1_opy_ = request.node.nodeid
        test_name = PytestBDDFramework.__1l11l111lll_opy_(request.node, scenario)
        bstack1l11lll1l1l_opy_ = feature.filename
        if not bstack1ll1l11ll1_opy_ or not test_name or not bstack1l11lll1l1l_opy_:
            return None
        code = None
        return {
            TestFramework.bstack1ll1ll1111l_opy_: uuid4().__str__(),
            TestFramework.bstack1l11l1l1lll_opy_: bstack1ll1l11ll1_opy_,
            TestFramework.bstack1ll1l111111_opy_: test_name,
            TestFramework.bstack1l1ll1ll11l_opy_: bstack1ll1l11ll1_opy_,
            TestFramework.bstack1l11l11ll1l_opy_: bstack1l11lll1l1l_opy_,
            TestFramework.bstack1l11llll1ll_opy_: PytestBDDFramework.__1l11l1l1l1l_opy_(feature, scenario),
            TestFramework.bstack1l111llll11_opy_: code,
            TestFramework.bstack1l1l1ll111l_opy_: TestFramework.bstack1l111ll1ll1_opy_,
            TestFramework.bstack1l1l111l11l_opy_: test_name
        }
    @staticmethod
    def __1l11l111lll_opy_(node, scenario):
        if hasattr(node, bstack1l1ll11_opy_ (u"ࠫࡨࡧ࡬࡭ࡵࡳࡩࡨ࠭ᐏ")):
            parts = node.nodeid.rsplit(bstack1l1ll11_opy_ (u"ࠧࡡࠢᐐ"))
            params = parts[-1]
            return bstack1l1ll11_opy_ (u"ࠨࡻࡾࠢ࡞ࡿࢂࠨᐑ").format(scenario.name, params)
        return scenario.name
    @staticmethod
    def __1l11l1l1l1l_opy_(feature, scenario) -> List[str]:
        return (list(feature.tags) if hasattr(feature, bstack1l1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᐒ")) else []) + (list(scenario.tags) if hasattr(scenario, bstack1l1ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᐓ")) else [])
    @staticmethod
    def __1l111ll1l1l_opy_(location):
        return bstack1l1ll11_opy_ (u"ࠤ࠽࠾ࠧᐔ").join(filter(lambda x: isinstance(x, str), location))