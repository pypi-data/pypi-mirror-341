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
from datetime import datetime, timezone
from uuid import uuid4
from typing import Dict, List, Any, Tuple
from browserstack_sdk.sdk_cli.bstack11111l11ll_opy_ import bstack111111l1l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack11l111l11_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    bstack1lll1l1lll1_opy_,
    bstack1lll11l1ll1_opy_,
    bstack1llll111ll1_opy_,
    bstack1l11l1l11l1_opy_,
    bstack1llll1111l1_opy_,
)
from pathlib import Path
import grpc
from browserstack_sdk import sdk_pb2 as structs
from datetime import datetime, timezone
from typing import List, Dict, Any
import traceback
from bstack_utils.helper import bstack1l1lllll1ll_opy_
from bstack_utils.bstack1l11l111l1_opy_ import bstack1lll111l1l1_opy_
from bstack_utils.constants import EVENTS
from browserstack_sdk.sdk_cli.bstack1111l1llll_opy_ import bstack1111l1ll1l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1llllll1l11_opy_ import bstack1lllllll1l1_opy_
from bstack_utils.bstack11l11l1111_opy_ import bstack11llll111l_opy_
bstack1ll11l1111l_opy_ = bstack1l1lllll1ll_opy_()
bstack1l111ll11ll_opy_ = 1.0
bstack1ll111l11l1_opy_ = bstack1l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᐕ")
bstack1l111l11l1l_opy_ = bstack1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᐖ")
bstack1l111l11lll_opy_ = bstack1l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᐗ")
bstack1l111l11l11_opy_ = bstack1l1_opy_ (u"ࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤᐘ")
bstack1l111l1l111_opy_ = bstack1l1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨᐙ")
_1ll111ll11l_opy_ = set()
class bstack1lll1l111ll_opy_(TestFramework):
    bstack1l11l1l1l11_opy_ = bstack1l1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᐚ")
    bstack1l111lll1ll_opy_ = bstack1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠢᐛ")
    bstack1l11l1111l1_opy_ = bstack1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠤᐜ")
    bstack1l11lll11ll_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩࠨᐝ")
    bstack1l11l11ll11_opy_ = bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠣᐞ")
    bstack1l11llll11l_opy_: bool
    bstack1111l1llll_opy_: bstack1111l1ll1l_opy_  = None
    bstack1ll1lllll1l_opy_ = None
    bstack1l11l111111_opy_ = [
        bstack1lll1l1lll1_opy_.BEFORE_ALL,
        bstack1lll1l1lll1_opy_.AFTER_ALL,
        bstack1lll1l1lll1_opy_.BEFORE_EACH,
        bstack1lll1l1lll1_opy_.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lll1l1_opy_: Dict[str, str],
        bstack1ll1l1ll1ll_opy_: List[str]=[bstack1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹࠨᐟ")],
        bstack1111l1llll_opy_: bstack1111l1ll1l_opy_=None,
        bstack1ll1lllll1l_opy_=None
    ):
        super().__init__(bstack1ll1l1ll1ll_opy_, bstack1l111lll1l1_opy_, bstack1111l1llll_opy_)
        self.bstack1l11llll11l_opy_ = any(bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺࠢᐠ") in item.lower() for item in bstack1ll1l1ll1ll_opy_)
        self.bstack1ll1lllll1l_opy_ = bstack1ll1lllll1l_opy_
    def track_event(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll111ll1_opy_,
        *args,
        **kwargs,
    ):
        super().track_event(self, context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == bstack1lll1l1lll1_opy_.TEST or test_framework_state in bstack1lll1l111ll_opy_.bstack1l11l111111_opy_:
            bstack1l11ll11111_opy_(test_framework_state, test_hook_state)
        if test_framework_state == bstack1lll1l1lll1_opy_.NONE:
            self.logger.warning(bstack1l1_opy_ (u"ࠣ࡫ࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠾ࠤᐡ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠤࠥᐢ"))
            return
        if not self.bstack1l11llll11l_opy_:
            self.logger.warning(bstack1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡸࡻࡰࡱࡱࡵࡸࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡀࠦᐣ") + str(str(self.bstack1ll1l1ll1ll_opy_)) + bstack1l1_opy_ (u"ࠦࠧᐤ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            self.logger.warning(bstack1l1_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᐥ") + str(kwargs) + bstack1l1_opy_ (u"ࠨࠢᐦ"))
            return
        instance = self.__1l11l11l111_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if not instance:
            self.logger.debug(bstack1l1_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡢࡴࡪࡷࡂࠨᐧ") + str(args) + bstack1l1_opy_ (u"ࠣࠤᐨ"))
            return
        try:
            if instance!= None and test_framework_state in bstack1lll1l111ll_opy_.bstack1l11l111111_opy_ and test_hook_state == bstack1llll111ll1_opy_.PRE:
                bstack1ll1l11ll11_opy_ = bstack1lll111l1l1_opy_.bstack1ll1ll1l111_opy_(EVENTS.bstack11l1l1lll_opy_.value)
                name = str(EVENTS.bstack11l1l1lll_opy_.name)+bstack1l1_opy_ (u"ࠤ࠽ࠦᐩ")+str(test_framework_state.name)
                TestFramework.bstack1l11l1ll11l_opy_(instance, name, bstack1ll1l11ll11_opy_)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢ࡫ࡳࡴࡱࠠࡦࡴࡵࡳࡷࠦࡰࡳࡧ࠽ࠤࢀࢃࠢᐪ").format(e))
        try:
            if not TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1l111lllll1_opy_) and test_hook_state == bstack1llll111ll1_opy_.PRE:
                test = bstack1lll1l111ll_opy_.__1l11ll111ll_opy_(args[0])
                if test:
                    instance.data.update(test)
                    self.logger.debug(bstack1l1_opy_ (u"ࠦࡱࡵࡡࡥࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᐫ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠧࠨᐬ"))
            if test_framework_state == bstack1lll1l1lll1_opy_.TEST:
                if test_hook_state == bstack1llll111ll1_opy_.PRE and not TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111111l_opy_):
                    TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1111111l_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1_opy_ (u"ࠨࡳࡦࡶࠣࡸࡪࡹࡴ࠮ࡵࡷࡥࡷࡺࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᐭ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠢࠣᐮ"))
                elif test_hook_state == bstack1llll111ll1_opy_.POST and not TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_):
                    TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_, datetime.now(tz=timezone.utc))
                    self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡨࡸࠥࡺࡥࡴࡶ࠰ࡩࡳࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᐯ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠤࠥᐰ"))
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG and test_hook_state == bstack1llll111ll1_opy_.POST:
                bstack1lll1l111ll_opy_.__1l11l11lll1_opy_(instance, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT and test_hook_state == bstack1llll111ll1_opy_.POST:
                self.__1l11ll11lll_opy_(instance, *args)
                self.__1l11lll1ll1_opy_(instance)
            elif test_framework_state in bstack1lll1l111ll_opy_.bstack1l11l111111_opy_:
                self.__1l11l1l111l_opy_(instance, test_framework_state, test_hook_state, *args)
            self.logger.debug(bstack1l1_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢ࡫ࡥࡳࡪ࡬ࡦࡦࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᐱ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠦࠧᐲ"))
        except Exception as e:
            self.logger.error(e)
            traceback.print_exc()
        self.bstack1l11l11111l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
        try:
            if instance!= None and test_framework_state in bstack1lll1l111ll_opy_.bstack1l11l111111_opy_ and test_hook_state == bstack1llll111ll1_opy_.POST:
                name = str(EVENTS.bstack11l1l1lll_opy_.name)+bstack1l1_opy_ (u"ࠧࡀࠢᐳ")+str(test_framework_state.name)
                bstack1ll1l11ll11_opy_ = TestFramework.bstack1l111l1ll1l_opy_(instance, name)
                bstack1lll111l1l1_opy_.end(EVENTS.bstack11l1l1lll_opy_.value, bstack1ll1l11ll11_opy_+bstack1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᐴ"), bstack1ll1l11ll11_opy_+bstack1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᐵ"), True, None, test_framework_state.name)
        except Exception as e:
            self.logger.debug(bstack1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡩࡱࡲ࡯ࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᐶ").format(e))
    def bstack1ll11111ll1_opy_(self):
        return self.bstack1l11llll11l_opy_
    def __1l11l11l11l_opy_(self, *args):
        if len(args) > 2 and callable(getattr(args[2], bstack1l1_opy_ (u"ࠤࡪࡩࡹࡥࡲࡦࡵࡸࡰࡹࠨᐷ"), None)):
            rep = args[2].get_result()
            if rep:
                return TestFramework.bstack1ll111lllll_opy_(rep, [bstack1l1_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᐸ"), bstack1l1_opy_ (u"ࠦࡴࡻࡴࡤࡱࡰࡩࠧᐹ"), bstack1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧᐺ"), bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨᐻ"), bstack1l1_opy_ (u"ࠢࡴ࡭࡬ࡴࡵ࡫ࡤࠣᐼ"), bstack1l1_opy_ (u"ࠣ࡮ࡲࡲ࡬ࡸࡥࡱࡴࡷࡩࡽࡺࠢᐽ")])
        return None
    def __1l11ll11lll_opy_(self, instance: bstack1lll11l1ll1_opy_, *args):
        result = self.__1l11l11l11l_opy_(*args)
        if not result:
            return
        failure = None
        bstack1111ll11l1_opy_ = None
        if result.get(bstack1l1_opy_ (u"ࠤࡲࡹࡹࡩ࡯࡮ࡧࠥᐾ"), None) == bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥᐿ") and len(args) > 1 and getattr(args[1], bstack1l1_opy_ (u"ࠦࡪࡾࡣࡪࡰࡩࡳࠧᑀ"), None) is not None:
            failure = [{bstack1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᑁ"): [args[1].excinfo.exconly(), result.get(bstack1l1_opy_ (u"ࠨ࡬ࡰࡰࡪࡶࡪࡶࡲࡵࡧࡻࡸࠧᑂ"), None)]}]
            bstack1111ll11l1_opy_ = bstack1l1_opy_ (u"ࠢࡂࡵࡶࡩࡷࡺࡩࡰࡰࡈࡶࡷࡵࡲࠣᑃ") if bstack1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦᑄ") in getattr(args[1].excinfo, bstack1l1_opy_ (u"ࠤࡷࡽࡵ࡫࡮ࡢ࡯ࡨࠦᑅ"), bstack1l1_opy_ (u"ࠥࠦᑆ")) else bstack1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧᑇ")
        bstack1l11ll1ll1l_opy_ = result.get(bstack1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑈ"), TestFramework.bstack1l111ll1ll1_opy_)
        if bstack1l11ll1ll1l_opy_ != TestFramework.bstack1l111ll1ll1_opy_:
            TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll1111ll11_opy_, datetime.now(tz=timezone.utc))
        TestFramework.bstack1l11l111lll_opy_(instance, {
            TestFramework.bstack1l1l1ll1l11_opy_: failure,
            TestFramework.bstack1l111lll11l_opy_: bstack1111ll11l1_opy_,
            TestFramework.bstack1l1l1lll1l1_opy_: bstack1l11ll1ll1l_opy_,
        })
    def __1l11l11l111_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll111ll1_opy_,
        *args,
        **kwargs,
    ):
        instance = None
        if test_framework_state == bstack1lll1l1lll1_opy_.SETUP_FIXTURE:
            instance = self.__1l11l1lllll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        else:
            target = None # bstack1l11ll1llll_opy_ bstack1l11l11l1ll_opy_ this to be bstack1l1_opy_ (u"ࠨ࡮ࡰࡦࡨ࡭ࡩࠨᑉ")
            if test_framework_state == bstack1lll1l1lll1_opy_.INIT_TEST:
                target = args[0] if isinstance(args[0], str) else None
                if target:
                    self.__1l11l11l1l1_opy_(context, test_framework_state, target, *args)
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                nodeid = getattr(getattr(args[0], bstack1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᑊ"), None), bstack1l1_opy_ (u"ࠣࡰࡲࡨࡪ࡯ࡤࠣᑋ"), None) if args else None
                if isinstance(nodeid, str):
                    target = nodeid
            elif getattr(args[0], bstack1l1_opy_ (u"ࠤࡱࡳࡩ࡫ࡩࡥࠤᑌ"), None):
                target = args[0].nodeid
            instance = TestFramework.bstack111111lll1_opy_(target) if target else None
        return instance
    def __1l11l1l111l_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll111ll1_opy_,
        *args,
    ):
        key = test_framework_state.name
        bstack1l111ll11l1_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l111lll1ll_opy_, {})
        if not key in bstack1l111ll11l1_opy_:
            bstack1l111ll11l1_opy_[key] = []
        bstack1l11l1l11ll_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l1111l1_opy_, {})
        if not key in bstack1l11l1l11ll_opy_:
            bstack1l11l1l11ll_opy_[key] = []
        bstack1l111lll111_opy_ = {
            bstack1lll1l111ll_opy_.bstack1l111lll1ll_opy_: bstack1l111ll11l1_opy_,
            bstack1lll1l111ll_opy_.bstack1l11l1111l1_opy_: bstack1l11l1l11ll_opy_,
        }
        if test_hook_state == bstack1llll111ll1_opy_.PRE:
            hook = {
                bstack1l1_opy_ (u"ࠥ࡯ࡪࡿࠢᑍ"): key,
                TestFramework.bstack1l11ll1lll1_opy_: uuid4().__str__(),
                TestFramework.bstack1l11l1ll1l1_opy_: TestFramework.bstack1l111l1lll1_opy_,
                TestFramework.bstack1l111ll1111_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l11llll111_opy_: [],
                TestFramework.bstack1l11l1l1lll_opy_: args[1] if len(args) > 1 else bstack1l1_opy_ (u"ࠫࠬᑎ"),
                TestFramework.bstack1l11ll111l1_opy_: bstack1lllllll1l1_opy_.bstack1l11lll1lll_opy_()
            }
            bstack1l111ll11l1_opy_[key].append(hook)
            bstack1l111lll111_opy_[bstack1lll1l111ll_opy_.bstack1l11lll11ll_opy_] = key
        elif test_hook_state == bstack1llll111ll1_opy_.POST:
            bstack1l11ll1l1l1_opy_ = bstack1l111ll11l1_opy_.get(key, [])
            hook = bstack1l11ll1l1l1_opy_.pop() if bstack1l11ll1l1l1_opy_ else None
            if hook:
                result = self.__1l11l11l11l_opy_(*args)
                if result:
                    bstack1l11l111l1l_opy_ = result.get(bstack1l1_opy_ (u"ࠧࡵࡵࡵࡥࡲࡱࡪࠨᑏ"), TestFramework.bstack1l111l1lll1_opy_)
                    if bstack1l11l111l1l_opy_ != TestFramework.bstack1l111l1lll1_opy_:
                        hook[TestFramework.bstack1l11l1ll1l1_opy_] = bstack1l11l111l1l_opy_
                hook[TestFramework.bstack1l11ll11l1l_opy_] = datetime.now(tz=timezone.utc)
                hook[TestFramework.bstack1l11ll111l1_opy_]= bstack1lllllll1l1_opy_.bstack1l11lll1lll_opy_()
                self.bstack1l111llll11_opy_(hook)
                logs = hook.get(TestFramework.bstack1l111llllll_opy_, [])
                if logs: self.bstack1ll111ll1ll_opy_(instance, logs)
                bstack1l11l1l11ll_opy_[key].append(hook)
                bstack1l111lll111_opy_[bstack1lll1l111ll_opy_.bstack1l11l11ll11_opy_] = key
        TestFramework.bstack1l11l111lll_opy_(instance, bstack1l111lll111_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࡂࢁ࡫ࡦࡻࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤ࠾ࡽ࡫ࡳࡴࡱࡳࡠࡵࡷࡥࡷࡺࡥࡥࡿࠣ࡬ࡴࡵ࡫ࡴࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡁࠧᑐ") + str(bstack1l11l1l11ll_opy_) + bstack1l1_opy_ (u"ࠢࠣᑑ"))
    def __1l11l1lllll_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        test_hook_state: bstack1llll111ll1_opy_,
        *args,
        **kwargs,
    ):
        fixturedef = TestFramework.bstack1ll111lllll_opy_(args[0], [bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑒ"), bstack1l1_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᑓ"), bstack1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥᑔ"), bstack1l1_opy_ (u"ࠦ࡮ࡪࡳࠣᑕ"), bstack1l1_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᑖ"), bstack1l1_opy_ (u"ࠨࡢࡢࡵࡨ࡭ࡩࠨᑗ")]) if len(args) > 0 else {}
        request = args[1] if len(args) > 1 else None
        scope = request.scope if hasattr(request, bstack1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᑘ")) else fixturedef.get(bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑙ"), None)
        fixturename = request.fixturename if hasattr(request, bstack1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢᑚ")) else None
        node = request.node if hasattr(request, bstack1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣᑛ")) else None
        target = request.node.nodeid if hasattr(node, bstack1l1_opy_ (u"ࠦࡳࡵࡤࡦ࡫ࡧࠦᑜ")) else None
        baseid = fixturedef.get(bstack1l1_opy_ (u"ࠧࡨࡡࡴࡧ࡬ࡨࠧᑝ"), None) or bstack1l1_opy_ (u"ࠨࠢᑞ")
        if (not target or len(baseid) > 0) and hasattr(request, bstack1l1_opy_ (u"ࠢࡠࡲࡼࡪࡺࡴࡣࡪࡶࡨࡱࠧᑟ")):
            target = bstack1lll1l111ll_opy_.__1l11ll1l111_opy_(request._pyfuncitem.location) if hasattr(request._pyfuncitem, bstack1l1_opy_ (u"ࠣ࡮ࡲࡧࡦࡺࡩࡰࡰࠥᑠ")) else None
            if target and not TestFramework.bstack111111lll1_opy_(target):
                self.__1l11l11l1l1_opy_(context, test_framework_state, target, (target, request._pyfuncitem.location))
                node = request._pyfuncitem
                self.logger.debug(bstack1l1_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡨ࡬ࡼࡹࡻࡲࡦࡡࡨࡺࡪࡴࡴ࠻ࠢࡩࡥࡱࡲࡢࡢࡥ࡮ࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࡁࢀ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࢀࠤࡳࡵࡤࡦ࠿ࡾࡲࡴࡪࡥࡾࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦᑡ") + str(test_hook_state) + bstack1l1_opy_ (u"ࠥࠦᑢ"))
        if not fixturedef or not scope or not target:
            self.logger.warning(bstack1l1_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡪ࡮ࡾࡴࡶࡴࡨࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡪࡥࡧ࠿ࡾࡪ࡮ࡾࡴࡶࡴࡨࡨࡪ࡬ࡽࠡࡵࡦࡳࡵ࡫࠽ࡼࡵࡦࡳࡵ࡫ࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࠤᑣ") + str(target) + bstack1l1_opy_ (u"ࠧࠨᑤ"))
            return None
        instance = TestFramework.bstack111111lll1_opy_(target)
        if not instance:
            self.logger.warning(bstack1l1_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡬ࡩࡹࡶࡸࡶࡪࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥࡨࡡࡴࡧ࡬ࡨࡂࢁࡢࡢࡵࡨ࡭ࡩࢃࠠࡵࡣࡵ࡫ࡪࡺ࠽ࠣᑥ") + str(target) + bstack1l1_opy_ (u"ࠢࠣᑦ"))
            return None
        bstack1l11l1l1l1l_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l1l1l11_opy_, {})
        if os.getenv(bstack1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡇࡋ࡛ࡘ࡚ࡘࡅࡔࠤᑧ"), bstack1l1_opy_ (u"ࠤ࠴ࠦᑨ")) == bstack1l1_opy_ (u"ࠥ࠵ࠧᑩ"):
            bstack1l111l1llll_opy_ = bstack1l1_opy_ (u"ࠦ࠿ࠨᑪ").join((scope, fixturename))
            bstack1l111ll111l_opy_ = datetime.now(tz=timezone.utc)
            bstack1l11lll1l11_opy_ = {
                bstack1l1_opy_ (u"ࠧࡱࡥࡺࠤᑫ"): bstack1l111l1llll_opy_,
                bstack1l1_opy_ (u"ࠨࡴࡢࡩࡶࠦᑬ"): bstack1lll1l111ll_opy_.__1l111ll1l1l_opy_(request.node),
                bstack1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࠣᑭ"): fixturedef,
                bstack1l1_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᑮ"): scope,
                bstack1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᑯ"): None,
            }
            try:
                if test_hook_state == bstack1llll111ll1_opy_.POST and callable(getattr(args[-1], bstack1l1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡳࡧࡶࡹࡱࡺࠢᑰ"), None)):
                    bstack1l11lll1l11_opy_[bstack1l1_opy_ (u"ࠦࡹࡿࡰࡦࠤᑱ")] = TestFramework.bstack1ll111111l1_opy_(args[-1].get_result())
            except Exception as e:
                pass
            if test_hook_state == bstack1llll111ll1_opy_.PRE:
                bstack1l11lll1l11_opy_[bstack1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥᑲ")] = uuid4().__str__()
                bstack1l11lll1l11_opy_[bstack1lll1l111ll_opy_.bstack1l111ll1111_opy_] = bstack1l111ll111l_opy_
            elif test_hook_state == bstack1llll111ll1_opy_.POST:
                bstack1l11lll1l11_opy_[bstack1lll1l111ll_opy_.bstack1l11ll11l1l_opy_] = bstack1l111ll111l_opy_
            if bstack1l111l1llll_opy_ in bstack1l11l1l1l1l_opy_:
                bstack1l11l1l1l1l_opy_[bstack1l111l1llll_opy_].update(bstack1l11lll1l11_opy_)
                self.logger.debug(bstack1l1_opy_ (u"ࠨࡵࡱࡦࡤࡸࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࠢᑳ") + str(bstack1l11l1l1l1l_opy_[bstack1l111l1llll_opy_]) + bstack1l1_opy_ (u"ࠢࠣᑴ"))
            else:
                bstack1l11l1l1l1l_opy_[bstack1l111l1llll_opy_] = bstack1l11lll1l11_opy_
                self.logger.debug(bstack1l1_opy_ (u"ࠣࡵࡤࡺࡪࡪࠠࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࡂࢁࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࢁࠥࡹࡣࡰࡲࡨࡁࢀࡹࡣࡰࡲࡨࢁࠥ࡬ࡩࡹࡶࡸࡶࡪࡃࡻࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࢃࠠࡵࡴࡤࡧࡰ࡫ࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࡀࠦᑵ") + str(len(bstack1l11l1l1l1l_opy_)) + bstack1l1_opy_ (u"ࠤࠥᑶ"))
        TestFramework.bstack11111111ll_opy_(instance, bstack1lll1l111ll_opy_.bstack1l11l1l1l11_opy_, bstack1l11l1l1l1l_opy_)
        self.logger.debug(bstack1l1_opy_ (u"ࠥࡷࡦࡼࡥࡥࠢࡩ࡭ࡽࡺࡵࡳࡧࡶࡁࢀࡲࡥ࡯ࠪࡷࡶࡦࡩ࡫ࡦࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࡷ࠮ࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᑷ") + str(instance.ref()) + bstack1l1_opy_ (u"ࠦࠧᑸ"))
        return instance
    def __1l11l11l1l1_opy_(
        self,
        context: bstack1l11l1l11l1_opy_,
        test_framework_state: bstack1lll1l1lll1_opy_,
        target: Any,
        *args,
    ):
        ctx = bstack111111l1l1_opy_.create_context(target)
        ob = bstack1lll11l1ll1_opy_(ctx, self.bstack1ll1l1ll1ll_opy_, self.bstack1l111lll1l1_opy_, test_framework_state)
        TestFramework.bstack1l11l111lll_opy_(ob, {
            TestFramework.bstack1ll1l1111ll_opy_: context.test_framework_name,
            TestFramework.bstack1ll111l111l_opy_: context.test_framework_version,
            TestFramework.bstack1l11ll11ll1_opy_: [],
            bstack1lll1l111ll_opy_.bstack1l11l1l1l11_opy_: {},
            bstack1lll1l111ll_opy_.bstack1l11l1111l1_opy_: {},
            bstack1lll1l111ll_opy_.bstack1l111lll1ll_opy_: {},
        })
        if len(args) > 1 and isinstance(args[1], tuple):
            TestFramework.bstack11111111ll_opy_(ob, TestFramework.bstack1l11l111ll1_opy_, str(args[1][0]))
        if context.platform_index >= 0:
            TestFramework.bstack11111111ll_opy_(ob, TestFramework.bstack1ll1l11llll_opy_, context.platform_index)
        TestFramework.bstack11111l1l1l_opy_[ctx.id] = ob
        self.logger.debug(bstack1l1_opy_ (u"ࠧࡹࡡࡷࡧࡧࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡣࡵࡺ࠱࡭ࡩࡃࡻࡤࡶࡻ࠲࡮ࡪࡽࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶࡁࠧᑹ") + str(TestFramework.bstack11111l1l1l_opy_.keys()) + bstack1l1_opy_ (u"ࠨࠢᑺ"))
        return ob
    def bstack1ll11111l1l_opy_(self, instance: bstack1lll11l1ll1_opy_, bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_]):
        bstack1l111ll1lll_opy_ = (
            bstack1lll1l111ll_opy_.bstack1l11lll11ll_opy_
            if bstack111111l11l_opy_[1] == bstack1llll111ll1_opy_.PRE
            else bstack1lll1l111ll_opy_.bstack1l11l11ll11_opy_
        )
        hook = bstack1lll1l111ll_opy_.bstack1l11llll1ll_opy_(instance, bstack1l111ll1lll_opy_)
        entries = hook.get(TestFramework.bstack1l11llll111_opy_, []) if isinstance(hook, dict) else []
        entries.extend(TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1l11ll11ll1_opy_, []))
        return entries
    def bstack1ll111l1l1l_opy_(self, instance: bstack1lll11l1ll1_opy_, bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_]):
        bstack1l111ll1lll_opy_ = (
            bstack1lll1l111ll_opy_.bstack1l11lll11ll_opy_
            if bstack111111l11l_opy_[1] == bstack1llll111ll1_opy_.PRE
            else bstack1lll1l111ll_opy_.bstack1l11l11ll11_opy_
        )
        bstack1lll1l111ll_opy_.bstack1l111l1ll11_opy_(instance, bstack1l111ll1lll_opy_)
        TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1l11ll11ll1_opy_, []).clear()
    def bstack1l111llll11_opy_(self, hook: Dict[str, Any]) -> None:
        bstack1l1_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡪࡨࠤࡍࡵ࡯࡬ࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰࠢࡷ࡬ࡪࠦࡊࡢࡸࡤࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡳࡥࡵࡪࡲࡨ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡈ࡮ࡥࡤ࡭ࡶࠤࡹ࡮ࡥࠡࡊࡲࡳࡰࡒࡥࡷࡧ࡯ࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡪࡰࡶ࡭ࡩ࡫ࠠࡿ࠱࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠱ࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡇࡱࡵࠤࡪࡧࡣࡩࠢࡩ࡭ࡱ࡫ࠠࡪࡰࠣ࡬ࡴࡵ࡫ࡠ࡮ࡨࡺࡪࡲ࡟ࡧ࡫࡯ࡩࡸ࠲ࠠࡳࡧࡳࡰࡦࡩࡥࡴࠢࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨࠠࡸ࡫ࡷ࡬ࠥࠨࡈࡰࡱ࡮ࡐࡪࡼࡥ࡭ࠤࠣ࡭ࡳࠦࡩࡵࡵࠣࡴࡦࡺࡨ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠳ࠠࡊࡨࠣࡥࠥ࡬ࡩ࡭ࡧࠣ࡭ࡳࠦࡴࡩࡧࠣࡨ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡭ࡢࡶࡦ࡬ࡪࡹࠠࡢࠢࡰࡳࡩ࡯ࡦࡪࡧࡧࠤ࡭ࡵ࡯࡬࠯࡯ࡩࡻ࡫࡬ࠡࡨ࡬ࡰࡪ࠲ࠠࡪࡶࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡌࡰࡩࡈࡲࡹࡸࡹࠡࡱࡥ࡮ࡪࡩࡴࠡࡹ࡬ࡸ࡭ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡨࡪࡺࡡࡪ࡮ࡶ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡗ࡮ࡳࡩ࡭ࡣࡵࡰࡾ࠲ࠠࡪࡶࠣࡴࡷࡵࡣࡦࡵࡶࡩࡸࠦࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡ࡮ࡲࡧࡦࡺࡥࡥࠢ࡬ࡲࠥࡎ࡯ࡰ࡭ࡏࡩࡻ࡫࡬࠰ࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࡍࡵ࡯࡬ࡇࡹࡩࡳࡺࠠࡣࡻࠣࡶࡪࡶ࡬ࡢࡥ࡬ࡲ࡬ࠦࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦࠥࡽࡩࡵࡪࠣࠦࡍࡵ࡯࡬ࡎࡨࡺࡪࡲ࠯ࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠨ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠲ࠦࡔࡩࡧࠣࡧࡷ࡫ࡡࡵࡧࡧࠤࡑࡵࡧࡆࡰࡷࡶࡾࠦ࡯ࡣ࡬ࡨࡧࡹࡹࠠࡢࡴࡨࠤࡦࡪࡤࡦࡦࠣࡸࡴࠦࡴࡩࡧࠣ࡬ࡴࡵ࡫ࠨࡵࠣࠦࡱࡵࡧࡴࠤࠣࡰ࡮ࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡩࡱࡲ࡯࠿ࠦࡔࡩࡧࠣࡩࡻ࡫࡮ࡵࠢࡧ࡭ࡨࡺࡩࡰࡰࡤࡶࡾࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡲ࡯ࡨࡵࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥ࡯࡮ࡧࡱࡵࡱࡦࡺࡩࡰࡰ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࡫ࡳࡴࡱ࡟࡭ࡧࡹࡩࡱࡥࡦࡪ࡮ࡨࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡑࡣࡷ࡬ࠥࡵࡢ࡫ࡧࡦࡸࡸࠦࡦࡳࡱࡰࠤࡹ࡮ࡥࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡣࡷ࡬ࡰࡩࡥ࡬ࡦࡸࡨࡰࡤ࡬ࡩ࡭ࡧࡶ࠾ࠥࡒࡩࡴࡶࠣࡳ࡫ࠦࡐࡢࡶ࡫ࠤࡴࡨࡪࡦࡥࡷࡷࠥ࡬ࡲࡰ࡯ࠣࡸ࡭࡫ࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠤࡲࡵ࡮ࡪࡶࡲࡶ࡮ࡴࡧ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᑻ")
        global _1ll111ll11l_opy_
        platform_index = os.environ[bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᑼ")]
        bstack1l1llll11ll_opy_ = os.path.join(bstack1ll11l1111l_opy_, (bstack1ll111l11l1_opy_ + str(platform_index)), bstack1l111l11l11_opy_)
        if not os.path.exists(bstack1l1llll11ll_opy_) or not os.path.isdir(bstack1l1llll11ll_opy_):
            self.logger.info(bstack1l1_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡦࡺ࡬ࡷࡹࡹࠠࡵࡱࠣࡴࡷࡵࡣࡦࡵࡶࠤࢀࢃࠢᑽ").format(bstack1l1llll11ll_opy_))
            return
        logs = hook.get(bstack1l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᑾ"), [])
        with os.scandir(bstack1l1llll11ll_opy_) as entries:
            for entry in entries:
                abs_path = os.path.abspath(entry.path)
                if abs_path in _1ll111ll11l_opy_:
                    self.logger.info(bstack1l1_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤᑿ").format(abs_path))
                    continue
                if entry.is_file():
                    try:
                        timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                    except Exception:
                        timestamp = bstack1l1_opy_ (u"ࠧࠨᒀ")
                    log_entry = bstack1llll1111l1_opy_(
                        kind=bstack1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᒁ"),
                        message=bstack1l1_opy_ (u"ࠢࠣᒂ"),
                        level=bstack1l1_opy_ (u"ࠣࠤᒃ"),
                        timestamp=timestamp,
                        fileName=entry.name,
                        bstack1l1llll1111_opy_=entry.stat().st_size,
                        bstack1l1llllllll_opy_=bstack1l1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᒄ"),
                        bstack1l11ll1_opy_=os.path.abspath(entry.path),
                        bstack1l11llll1l1_opy_=hook.get(TestFramework.bstack1l11ll1lll1_opy_)
                    )
                    logs.append(log_entry)
                    _1ll111ll11l_opy_.add(abs_path)
        platform_index = os.environ[bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒅ")]
        bstack1l111llll1l_opy_ = os.path.join(bstack1ll11l1111l_opy_, (bstack1ll111l11l1_opy_ + str(platform_index)), bstack1l111l11l11_opy_, bstack1l111l1l111_opy_)
        if not os.path.exists(bstack1l111llll1l_opy_) or not os.path.isdir(bstack1l111llll1l_opy_):
            self.logger.info(bstack1l1_opy_ (u"ࠦࡓࡵࠠࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࡌࡴࡵ࡫ࡆࡸࡨࡲࡹࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࠦࡡࡵ࠼ࠣࡿࢂࠨᒆ").format(bstack1l111llll1l_opy_))
        else:
            self.logger.info(bstack1l1_opy_ (u"ࠧࡖࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࡎ࡯ࡰ࡭ࡈࡺࡪࡴࡴࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡦࡳࡱࡰࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿ࠺ࠡࡽࢀࠦᒇ").format(bstack1l111llll1l_opy_))
            with os.scandir(bstack1l111llll1l_opy_) as entries:
                for entry in entries:
                    abs_path = os.path.abspath(entry.path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1l1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᒈ").format(abs_path))
                        continue
                    if entry.is_file():
                        try:
                            timestamp = datetime.fromtimestamp(entry.stat().st_mtime, tz=timezone.utc).isoformat()
                        except Exception:
                            timestamp = bstack1l1_opy_ (u"ࠢࠣᒉ")
                        log_entry = bstack1llll1111l1_opy_(
                            kind=bstack1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᒊ"),
                            message=bstack1l1_opy_ (u"ࠤࠥᒋ"),
                            level=bstack1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᒌ"),
                            timestamp=timestamp,
                            fileName=entry.name,
                            bstack1l1llll1111_opy_=entry.stat().st_size,
                            bstack1l1llllllll_opy_=bstack1l1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᒍ"),
                            bstack1l11ll1_opy_=os.path.abspath(entry.path),
                            bstack1l1lll11ll1_opy_=hook.get(TestFramework.bstack1l11ll1lll1_opy_)
                        )
                        logs.append(log_entry)
                        _1ll111ll11l_opy_.add(abs_path)
        hook[bstack1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᒎ")] = logs
    def bstack1ll111ll1ll_opy_(
        self,
        bstack1l1llll1l11_opy_: bstack1lll11l1ll1_opy_,
        entries: List[bstack1llll1111l1_opy_],
    ):
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = os.environ.get(bstack1l1_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡅࡍࡓࡥࡓࡆࡕࡖࡍࡔࡔ࡟ࡊࡆࠥᒏ"))
        req.platform_index = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll1l11llll_opy_)
        req.execution_context.hash = str(bstack1l1llll1l11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll1l11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll1l11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll1l1111ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll111l111l_opy_)
            log_entry.uuid = entry.bstack1l11llll1l1_opy_
            log_entry.test_framework_state = bstack1l1llll1l11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᒐ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            log_entry.level = bstack1l1_opy_ (u"ࠣࠤᒑ")
            if entry.kind == bstack1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᒒ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll1111_opy_
                log_entry.file_path = entry.bstack1l11ll1_opy_
        def bstack1l1lllll111_opy_():
            bstack1l1l1llll1_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll1l_opy_.LogCreatedEvent(req)
                bstack1l1llll1l11_opy_.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᒓ"), datetime.now() - bstack1l1l1llll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡿࠥᒔ").format(str(e)))
                traceback.print_exc()
        self.bstack1111l1llll_opy_.enqueue(bstack1l1lllll111_opy_)
    def __1l11lll1ll1_opy_(self, instance) -> None:
        bstack1l1_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᒕ")
        bstack1l111lll111_opy_ = {bstack1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᒖ"): bstack1lllllll1l1_opy_.bstack1l11lll1lll_opy_()}
        from browserstack_sdk.sdk_cli.test_framework import TestFramework
        TestFramework.bstack1l11l111lll_opy_(instance, bstack1l111lll111_opy_)
    @staticmethod
    def bstack1l11llll1ll_opy_(instance: bstack1lll11l1ll1_opy_, bstack1l111ll1lll_opy_: str):
        bstack1l11ll1l1ll_opy_ = (
            bstack1lll1l111ll_opy_.bstack1l11l1111l1_opy_
            if bstack1l111ll1lll_opy_ == bstack1lll1l111ll_opy_.bstack1l11l11ll11_opy_
            else bstack1lll1l111ll_opy_.bstack1l111lll1ll_opy_
        )
        bstack1l11l1111ll_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1l111ll1lll_opy_, None)
        bstack1l11ll1l11l_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1l11ll1l1ll_opy_, None) if bstack1l11l1111ll_opy_ else None
        return (
            bstack1l11ll1l11l_opy_[bstack1l11l1111ll_opy_][-1]
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11l1111ll_opy_, [])) > 0
            else None
        )
    @staticmethod
    def bstack1l111l1ll11_opy_(instance: bstack1lll11l1ll1_opy_, bstack1l111ll1lll_opy_: str):
        hook = bstack1lll1l111ll_opy_.bstack1l11llll1ll_opy_(instance, bstack1l111ll1lll_opy_)
        if isinstance(hook, dict):
            hook.get(TestFramework.bstack1l11llll111_opy_, []).clear()
    @staticmethod
    def __1l11l11lll1_opy_(instance: bstack1lll11l1ll1_opy_, *args):
        if len(args) < 2 or not callable(getattr(args[1], bstack1l1_opy_ (u"ࠢࡨࡧࡷࡣࡷ࡫ࡣࡰࡴࡧࡷࠧᒗ"), None)):
            return
        if os.getenv(bstack1l1_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡍࡑࡊࡗࠧᒘ"), bstack1l1_opy_ (u"ࠤ࠴ࠦᒙ")) != bstack1l1_opy_ (u"ࠥ࠵ࠧᒚ"):
            bstack1lll1l111ll_opy_.logger.warning(bstack1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴ࡬ࡲ࡬ࠦࡣࡢࡲ࡯ࡳ࡬ࠨᒛ"))
            return
        bstack1l11l1ll111_opy_ = {
            bstack1l1_opy_ (u"ࠧࡹࡥࡵࡷࡳࠦᒜ"): (bstack1lll1l111ll_opy_.bstack1l11lll11ll_opy_, bstack1lll1l111ll_opy_.bstack1l111lll1ll_opy_),
            bstack1l1_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࠣᒝ"): (bstack1lll1l111ll_opy_.bstack1l11l11ll11_opy_, bstack1lll1l111ll_opy_.bstack1l11l1111l1_opy_),
        }
        for when in (bstack1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࠨᒞ"), bstack1l1_opy_ (u"ࠣࡥࡤࡰࡱࠨᒟ"), bstack1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᒠ")):
            bstack1l11ll11l11_opy_ = args[1].get_records(when)
            if not bstack1l11ll11l11_opy_:
                continue
            records = [
                bstack1llll1111l1_opy_(
                    kind=TestFramework.bstack1ll1111l11l_opy_,
                    message=r.message,
                    level=r.levelname if hasattr(r, bstack1l1_opy_ (u"ࠥࡰࡪࡼࡥ࡭ࡰࡤࡱࡪࠨᒡ")) and r.levelname else None,
                    timestamp=(
                        datetime.fromtimestamp(r.created, tz=timezone.utc)
                        if hasattr(r, bstack1l1_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠧᒢ")) and r.created
                        else None
                    ),
                )
                for r in bstack1l11ll11l11_opy_
                if isinstance(getattr(r, bstack1l1_opy_ (u"ࠧࡳࡥࡴࡵࡤ࡫ࡪࠨᒣ"), None), str) and r.message.strip()
            ]
            if not records:
                continue
            bstack1l11l1lll11_opy_, bstack1l11ll1l1ll_opy_ = bstack1l11l1ll111_opy_.get(when, (None, None))
            bstack1l11lll11l1_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1l11l1lll11_opy_, None) if bstack1l11l1lll11_opy_ else None
            bstack1l11ll1l11l_opy_ = TestFramework.bstack1111l11lll_opy_(instance, bstack1l11ll1l1ll_opy_, None) if bstack1l11lll11l1_opy_ else None
            if isinstance(bstack1l11ll1l11l_opy_, dict) and len(bstack1l11ll1l11l_opy_.get(bstack1l11lll11l1_opy_, [])) > 0:
                hook = bstack1l11ll1l11l_opy_[bstack1l11lll11l1_opy_][-1]
                if isinstance(hook, dict) and TestFramework.bstack1l11llll111_opy_ in hook:
                    hook[TestFramework.bstack1l11llll111_opy_].extend(records)
                    continue
            logs = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1l11ll11ll1_opy_, [])
            logs.extend(records)
    @staticmethod
    def __1l11ll111ll_opy_(test) -> Dict[str, Any]:
        bstack11ll1111ll_opy_ = bstack1lll1l111ll_opy_.__1l11ll1l111_opy_(test.location) if hasattr(test, bstack1l1_opy_ (u"ࠨ࡬ࡰࡥࡤࡸ࡮ࡵ࡮ࠣᒤ")) else getattr(test, bstack1l1_opy_ (u"ࠢ࡯ࡱࡧࡩ࡮ࡪࠢᒥ"), None)
        test_name = test.name if hasattr(test, bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᒦ")) else None
        bstack1l11l11llll_opy_ = test.fspath.strpath if hasattr(test, bstack1l1_opy_ (u"ࠤࡩࡷࡵࡧࡴࡩࠤᒧ")) and test.fspath else None
        if not bstack11ll1111ll_opy_ or not test_name or not bstack1l11l11llll_opy_:
            return None
        code = None
        if hasattr(test, bstack1l1_opy_ (u"ࠥࡳࡧࡰࠢᒨ")):
            try:
                import inspect
                code = inspect.getsource(test.obj)
            except:
                pass
        bstack1l111l1l11l_opy_ = []
        try:
            bstack1l111l1l11l_opy_ = bstack11llll111l_opy_.bstack111lll11ll_opy_(test)
        except:
            bstack1lll1l111ll_opy_.logger.warning(bstack1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡧ࡫ࡱࡨࠥࡺࡥࡴࡶࠣࡷࡨࡵࡰࡦࡵ࠯ࠤࡹ࡫ࡳࡵࠢࡶࡧࡴࡶࡥࡴࠢࡺ࡭ࡱࡲࠠࡣࡧࠣࡶࡪࡹ࡯࡭ࡸࡨࡨࠥ࡯࡮ࠡࡅࡏࡍࠧᒩ"))
        return {
            TestFramework.bstack1ll1l111lll_opy_: uuid4().__str__(),
            TestFramework.bstack1l111lllll1_opy_: bstack11ll1111ll_opy_,
            TestFramework.bstack1ll1l1l1ll1_opy_: test_name,
            TestFramework.bstack1l1ll1llll1_opy_: getattr(test, bstack1l1_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᒪ"), None),
            TestFramework.bstack1l11l1l1111_opy_: bstack1l11l11llll_opy_,
            TestFramework.bstack1l11l1lll1l_opy_: bstack1lll1l111ll_opy_.__1l111ll1l1l_opy_(test),
            TestFramework.bstack1l11l111l11_opy_: code,
            TestFramework.bstack1l1l1lll1l1_opy_: TestFramework.bstack1l111ll1ll1_opy_,
            TestFramework.bstack1l1l111l1ll_opy_: bstack11ll1111ll_opy_,
            TestFramework.bstack1l111l11ll1_opy_: bstack1l111l1l11l_opy_
        }
    @staticmethod
    def __1l111ll1l1l_opy_(test) -> List[str]:
        return (
            [getattr(f, bstack1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᒫ"), None) for f in test.own_markers if getattr(f, bstack1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᒬ"), None)]
            if isinstance(getattr(test, bstack1l1_opy_ (u"ࠣࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸࠨᒭ"), None), list)
            else []
        )
    @staticmethod
    def __1l11ll1l111_opy_(location):
        return bstack1l1_opy_ (u"ࠤ࠽࠾ࠧᒮ").join(filter(lambda x: isinstance(x, str), location))