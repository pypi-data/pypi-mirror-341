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
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import bstack1111111l1l_opy_, bstack11111ll1ll_opy_, bstack1llllllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1llll1l_opy_ import bstack1llll1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll11111l_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll11_opy_ import bstack1lll1111l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11l1ll1_opy_, bstack1llll111ll1_opy_, bstack1llll1111l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll111l1ll1_opy_, bstack1l1lllll1ll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1ll111lll1l_opy_ = [bstack1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᆭ"), bstack1l1_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᆮ"), bstack1l1_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᆯ"), bstack1l1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢᆰ"), bstack1l1_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᆱ")]
bstack1ll11l1111l_opy_ = bstack1l1lllll1ll_opy_()
bstack1ll111l11l1_opy_ = bstack1l1_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᆲ")
bstack1l1lll1ll11_opy_ = {
    bstack1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᆳ"): bstack1ll111lll1l_opy_,
    bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᆴ"): bstack1ll111lll1l_opy_,
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᆵ"): bstack1ll111lll1l_opy_,
    bstack1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᆶ"): bstack1ll111lll1l_opy_,
    bstack1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᆷ"): bstack1ll111lll1l_opy_
    + [
        bstack1l1_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᆸ"),
        bstack1l1_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᆹ"),
        bstack1l1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᆺ"),
        bstack1l1_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᆻ"),
        bstack1l1_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᆼ"),
        bstack1l1_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᆽ"),
        bstack1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᆾ"),
        bstack1l1_opy_ (u"ࠢࡴࡶࡲࡴࠧᆿ"),
        bstack1l1_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥᇀ"),
        bstack1l1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᇁ"),
    ],
    bstack1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤᇂ"): [bstack1l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᇃ"), bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᇄ"), bstack1l1_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᇅ"), bstack1l1_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᇆ")],
    bstack1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᇇ"): [bstack1l1_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᇈ"), bstack1l1_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᇉ")],
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᇊ"): [bstack1l1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᇋ"), bstack1l1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᇌ"), bstack1l1_opy_ (u"ࠢࡧࡷࡱࡧࠧᇍ"), bstack1l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᇎ"), bstack1l1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᇏ"), bstack1l1_opy_ (u"ࠥ࡭ࡩࡹࠢᇐ")],
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥᇑ"): [bstack1l1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᇒ"), bstack1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧᇓ"), bstack1l1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧᇔ")],
    bstack1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᇕ"): [bstack1l1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᇖ"), bstack1l1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᇗ")],
    bstack1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᇘ"): [bstack1l1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᇙ"), bstack1l1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᇚ")],
    bstack1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᇛ"): [bstack1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᇜ"), bstack1l1_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᇝ"), bstack1l1_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᇞ")],
}
_1ll111ll11l_opy_ = set()
class bstack1lll11l1l1l_opy_(bstack1llll1l1111_opy_):
    bstack1l1lll11111_opy_ = bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᇟ")
    bstack1l1llll1l1l_opy_ = bstack1l1_opy_ (u"ࠧࡏࡎࡇࡑࠥᇠ")
    bstack1l1lll1llll_opy_ = bstack1l1_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᇡ")
    bstack1ll111ll1l1_opy_: Callable
    bstack1l1llll11l1_opy_: Callable
    def __init__(self, bstack1lll11lll1l_opy_, bstack1llll1l1ll1_opy_):
        super().__init__()
        self.bstack1ll1ll11ll1_opy_ = bstack1llll1l1ll1_opy_
        if os.getenv(bstack1l1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᇢ"), bstack1l1_opy_ (u"ࠣ࠳ࠥᇣ")) != bstack1l1_opy_ (u"ࠤ࠴ࠦᇤ") or not self.is_enabled():
            self.logger.warning(bstack1l1_opy_ (u"ࠥࠦᇥ") + str(self.__class__.__name__) + bstack1l1_opy_ (u"ࠦࠥࡪࡩࡴࡣࡥࡰࡪࡪࠢᇦ"))
            return
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.PRE), self.bstack1ll1ll111ll_opy_)
        TestFramework.bstack1ll1l1ll11l_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST), self.bstack1ll1ll1l11l_opy_)
        for event in bstack1lll1l1lll1_opy_:
            for state in bstack1llll111ll1_opy_:
                TestFramework.bstack1ll1l1ll11l_opy_((event, state), self.bstack1ll111l1lll_opy_)
        bstack1lll11lll1l_opy_.bstack1ll1l1ll11l_opy_((bstack11111ll1ll_opy_.bstack1llllllll11_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l1lll111l1_opy_)
        self.bstack1ll111ll1l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llllll11_opy_(bstack1lll11l1l1l_opy_.bstack1l1llll1l1l_opy_, self.bstack1ll111ll1l1_opy_)
        self.bstack1l1llll11l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llllll11_opy_(bstack1lll11l1l1l_opy_.bstack1l1lll1llll_opy_, self.bstack1l1llll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1ll11111ll1_opy_() and instance:
            bstack1l1lllllll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack111111l11l_opy_
            if test_framework_state == bstack1lll1l1lll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                bstack1l1l1llll1_opy_ = datetime.now()
                entries = f.bstack1ll11111l1l_opy_(instance, bstack111111l11l_opy_)
                if entries:
                    self.bstack1ll111ll1ll_opy_(instance, entries)
                    instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࠧᇧ"), datetime.now() - bstack1l1l1llll1_opy_)
                    f.bstack1ll111l1l1l_opy_(instance, bstack111111l11l_opy_)
                instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤᇨ"), datetime.now() - bstack1l1lllllll1_opy_)
                return # bstack1l1lll1l1ll_opy_ not send this event with the bstack1l1llllll1l_opy_ bstack1ll1111ll1l_opy_
            elif (
                test_framework_state == bstack1lll1l1lll1_opy_.TEST
                and test_hook_state == bstack1llll111ll1_opy_.POST
                and not f.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
            ):
                self.logger.warning(bstack1l1_opy_ (u"ࠢࡥࡴࡲࡴࡵ࡯࡮ࡨࠢࡧࡹࡪࠦࡴࡰࠢ࡯ࡥࡨࡱࠠࡰࡨࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࠧᇩ") + str(TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)) + bstack1l1_opy_ (u"ࠣࠤᇪ"))
                f.bstack11111111ll_opy_(instance, bstack1lll11l1l1l_opy_.bstack1l1lll11111_opy_, True)
                return # bstack1l1lll1l1ll_opy_ not send this event bstack1l1lll1lll1_opy_ bstack1l1llll1ll1_opy_
            elif (
                f.bstack1111l11lll_opy_(instance, bstack1lll11l1l1l_opy_.bstack1l1lll11111_opy_, False)
                and test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT
                and test_hook_state == bstack1llll111ll1_opy_.POST
                and f.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)
            ):
                self.logger.warning(bstack1l1_opy_ (u"ࠤ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡘࡊ࡙ࡔ࠭ࠢࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡓࡓࡘ࡚ࠠࠣᇫ") + str(TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1111ll11_opy_)) + bstack1l1_opy_ (u"ࠥࠦᇬ"))
                self.bstack1ll111l1lll_opy_(f, instance, (bstack1lll1l1lll1_opy_.TEST, bstack1llll111ll1_opy_.POST), *args, **kwargs)
            bstack1l1l1llll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll111ll111_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᇭ"), None), data.pop(bstack1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᇮ"), {}).values()),
                key=lambda x: x[bstack1l1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᇯ")],
            )
            if bstack1llll111111_opy_.bstack1ll111llll1_opy_ in data:
                data.pop(bstack1llll111111_opy_.bstack1ll111llll1_opy_)
            data.update({bstack1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᇰ"): bstack1ll111ll111_opy_})
            instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠣ࡬ࡶࡳࡳࡀࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇱ"), datetime.now() - bstack1l1l1llll1_opy_)
            bstack1l1l1llll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1lll1l11l_opy_)
            instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᇲ"), datetime.now() - bstack1l1l1llll1_opy_)
            self.bstack1ll1111ll1l_opy_(instance, bstack111111l11l_opy_, event_json=event_json)
            instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᇳ"), datetime.now() - bstack1l1lllllll1_opy_)
    def bstack1ll1ll111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l11l111l1_opy_ import bstack1lll111l1l1_opy_
        bstack1ll1l11ll11_opy_ = bstack1lll111l1l1_opy_.bstack1ll1ll1l111_opy_(EVENTS.bstack11l11ll111_opy_.value)
        self.bstack1ll1ll11ll1_opy_.bstack1l1llll1lll_opy_(instance, f, bstack111111l11l_opy_, *args, **kwargs)
        bstack1lll111l1l1_opy_.end(EVENTS.bstack11l11ll111_opy_.value, bstack1ll1l11ll11_opy_ + bstack1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇴ"), bstack1ll1l11ll11_opy_ + bstack1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇵ"), status=True, failure=None, test_name=None)
    def bstack1ll1ll1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1ll11ll1_opy_.bstack1l1lll1l1l1_opy_(instance, f, bstack111111l11l_opy_, *args, **kwargs)
        self.bstack1ll1111l111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll11l11_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def bstack1ll1111l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1ll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤᇶ"))
            return
        bstack1l1l1llll1_opy_ = datetime.now()
        try:
            r = self.bstack1ll1lllll1l_opy_.TestSessionEvent(req)
            instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣᇷ"), datetime.now() - bstack1l1l1llll1_opy_)
            f.bstack11111111ll_opy_(instance, self.bstack1ll1ll11ll1_opy_.bstack1ll111111ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇸ") + str(r) + bstack1l1_opy_ (u"ࠤࠥᇹ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇺ") + str(e) + bstack1l1_opy_ (u"ࠦࠧᇻ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll111l1_opy_(
        self,
        f: bstack1lll1111l11_opy_,
        _driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        _1ll111l1l11_opy_: Tuple[bstack11111ll1ll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1111l11_opy_.bstack1ll1ll1lll1_opy_(method_name):
            return
        if f.bstack1ll1ll111l1_opy_(*args) == bstack1lll1111l11_opy_.bstack1ll111lll11_opy_:
            bstack1l1lllllll1_opy_ = datetime.now()
            screenshot = result.get(bstack1l1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᇼ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢᇽ"))
                return
            bstack1l1llll1l11_opy_ = self.bstack1ll11111111_opy_(instance)
            if bstack1l1llll1l11_opy_:
                entry = bstack1llll1111l1_opy_(TestFramework.bstack1l1lllll11l_opy_, screenshot)
                self.bstack1ll111ll1ll_opy_(bstack1l1llll1l11_opy_, [entry])
                instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣᇾ"), datetime.now() - bstack1l1lllllll1_opy_)
            else:
                self.logger.warning(bstack1l1_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠣࡿࢂࠨᇿ").format(instance.ref()))
        event = {}
        bstack1l1llll1l11_opy_ = self.bstack1ll11111111_opy_(instance)
        if bstack1l1llll1l11_opy_:
            self.bstack1l1lll11lll_opy_(event, bstack1l1llll1l11_opy_)
            if event.get(bstack1l1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢሀ")):
                self.bstack1ll111ll1ll_opy_(bstack1l1llll1l11_opy_, event[bstack1l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣሁ")])
            else:
                self.logger.info(bstack1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡰࡴ࡭ࡳࠡࡨࡲࡶࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡨࡺࡪࡴࡴࠣሂ"))
    @measure(event_name=EVENTS.bstack1ll11111l11_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def bstack1ll111ll1ll_opy_(
        self,
        bstack1l1llll1l11_opy_: bstack1lll11l1ll1_opy_,
        entries: List[bstack1llll1111l1_opy_],
    ):
        self.bstack1ll1ll1111l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll1l11llll_opy_)
        req.execution_context.hash = str(bstack1l1llll1l11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llll1l11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llll1l11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll1l1111ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll111l111l_opy_)
            log_entry.uuid = TestFramework.bstack1111l11lll_opy_(bstack1l1llll1l11_opy_, TestFramework.bstack1ll1l111lll_opy_)
            log_entry.test_framework_state = bstack1l1llll1l11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦሃ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣሄ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll1111_opy_
                log_entry.file_path = entry.bstack1l11ll1_opy_
        def bstack1l1lllll111_opy_():
            bstack1l1l1llll1_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1lllll11l_opy_:
                    bstack1l1llll1l11_opy_.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦህ"), datetime.now() - bstack1l1l1llll1_opy_)
                elif entry.kind == TestFramework.bstack1l1ll1lllll_opy_:
                    bstack1l1llll1l11_opy_.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧሆ"), datetime.now() - bstack1l1l1llll1_opy_)
                else:
                    bstack1l1llll1l11_opy_.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨሇ"), datetime.now() - bstack1l1l1llll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣለ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1llll_opy_.enqueue(bstack1l1lllll111_opy_)
    @measure(event_name=EVENTS.bstack1ll111l1111_opy_, stage=STAGE.bstack1llll11l1_opy_)
    def bstack1ll1111ll1l_opy_(
        self,
        instance: bstack1lll11l1ll1_opy_,
        bstack111111l11l_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1llll111ll1_opy_],
        event_json=None,
    ):
        self.bstack1ll1ll1111l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l11llll_opy_)
        req.test_framework_name = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l1111ll_opy_)
        req.test_framework_version = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll111l111l_opy_)
        req.test_framework_state = bstack111111l11l_opy_[0].name
        req.test_hook_state = bstack111111l11l_opy_[1].name
        started_at = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111111l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1lll1l11l_opy_)).encode(bstack1l1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥሉ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lllll111_opy_():
            bstack1l1l1llll1_opy_ = datetime.now()
            try:
                self.bstack1ll1lllll1l_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1ll11ll_opy_(bstack1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣሊ"), datetime.now() - bstack1l1l1llll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦላ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1llll_opy_.enqueue(bstack1l1lllll111_opy_)
    def bstack1ll11111111_opy_(self, instance: bstack1111111l1l_opy_):
        bstack1l1lll1ll1l_opy_ = TestFramework.bstack1111111l11_opy_(instance.context)
        for t in bstack1l1lll1ll1l_opy_:
            bstack1ll11111lll_opy_ = TestFramework.bstack1111l11lll_opy_(t, bstack1llll111111_opy_.bstack1ll111llll1_opy_, [])
            if any(instance is d[1] for d in bstack1ll11111lll_opy_):
                return t
    def bstack1ll11l111l1_opy_(self, message):
        self.bstack1ll111ll1l1_opy_(message + bstack1l1_opy_ (u"ࠢ࡝ࡰࠥሌ"))
    def log_error(self, message):
        self.bstack1l1llll11l1_opy_(message + bstack1l1_opy_ (u"ࠣ࡞ࡱࠦል"))
    def bstack1l1llllll11_opy_(self, level, original_func):
        def bstack1ll1111lll1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1lll1ll1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_()
            if not bstack1l1lll1ll1l_opy_:
                return return_value
            bstack1l1llll1l11_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lll1ll1l_opy_
                    if TestFramework.bstack11111llll1_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
                ),
                None,
            )
            if not bstack1l1llll1l11_opy_:
                return
            entry = bstack1llll1111l1_opy_(TestFramework.bstack1ll1111l11l_opy_, message, level)
            self.bstack1ll111ll1ll_opy_(bstack1l1llll1l11_opy_, [entry])
            return return_value
        return bstack1ll1111lll1_opy_
    def bstack1l1lll11lll_opy_(self, event: dict, instance=None) -> None:
        global _1ll111ll11l_opy_
        levels = [bstack1l1_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧሎ"), bstack1l1_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢሏ")]
        bstack1ll1111llll_opy_ = bstack1l1_opy_ (u"ࠦࠧሐ")
        if instance is not None:
            try:
                bstack1ll1111llll_opy_ = TestFramework.bstack1111l11lll_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡵࡪࡦࠣࡪࡷࡵ࡭ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥሑ").format(e))
        bstack1ll111l11ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ሒ")]
                bstack1l1llll11ll_opy_ = os.path.join(bstack1ll11l1111l_opy_, (bstack1ll111l11l1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1llll11ll_opy_):
                    self.logger.info(bstack1l1_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡲࡴࡺࠠࡱࡴࡨࡷࡪࡴࡴࠡࡨࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡗࡩࡸࡺࠠࡢࡰࡧࠤࡇࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠢሓ").format(bstack1l1llll11ll_opy_))
                file_names = os.listdir(bstack1l1llll11ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1llll11ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1l1_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨሔ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1llll111l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1llll111l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧሕ"):
                                entry = bstack1llll1111l1_opy_(
                                    kind=bstack1l1_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧሖ"),
                                    message=bstack1l1_opy_ (u"ࠦࠧሗ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1llll1111_opy_=file_size,
                                    bstack1l1llllllll_opy_=bstack1l1_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧመ"),
                                    bstack1l11ll1_opy_=os.path.abspath(file_path),
                                    bstack111llll1l_opy_=bstack1ll1111llll_opy_
                                )
                            elif level == bstack1l1_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥሙ"):
                                entry = bstack1llll1111l1_opy_(
                                    kind=bstack1l1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤሚ"),
                                    message=bstack1l1_opy_ (u"ࠣࠤማ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1llll1111_opy_=file_size,
                                    bstack1l1llllllll_opy_=bstack1l1_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤሜ"),
                                    bstack1l11ll1_opy_=os.path.abspath(file_path),
                                    bstack1l1lll11ll1_opy_=bstack1ll1111llll_opy_
                                )
                            bstack1ll111l11ll_opy_.append(entry)
                            _1ll111ll11l_opy_.add(abs_path)
                        except Exception as bstack1ll1111l1ll_opy_:
                            self.logger.error(bstack1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠨም").format(bstack1ll1111l1ll_opy_))
        except Exception as e:
            self.logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠢሞ").format(e))
        event[bstack1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥሟ")] = bstack1ll111l11ll_opy_
class bstack1l1lll1l11l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lll1111l_opy_ = set()
        kwargs[bstack1l1_opy_ (u"ࠨࡳ࡬࡫ࡳ࡯ࡪࡿࡳࠣሠ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1lll11l1l_opy_(obj, self.bstack1l1lll1111l_opy_)
def bstack1ll11l11111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1lll11l1l_opy_(obj, bstack1l1lll1111l_opy_=None, max_depth=3):
    if bstack1l1lll1111l_opy_ is None:
        bstack1l1lll1111l_opy_ = set()
    if id(obj) in bstack1l1lll1111l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lll1111l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lll111ll_opy_ = TestFramework.bstack1ll111111l1_opy_(obj)
    bstack1l1lll1l111_opy_ = next((k.lower() in bstack1l1lll111ll_opy_.lower() for k in bstack1l1lll1ll11_opy_.keys()), None)
    if bstack1l1lll1l111_opy_:
        obj = TestFramework.bstack1ll111lllll_opy_(obj, bstack1l1lll1ll11_opy_[bstack1l1lll1l111_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥሡ")):
            keys = getattr(obj, bstack1l1_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦሢ"), [])
        elif hasattr(obj, bstack1l1_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦሣ")):
            keys = getattr(obj, bstack1l1_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧሤ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1_opy_ (u"ࠦࡤࠨሥ"))}
        if not obj and bstack1l1lll111ll_opy_ == bstack1l1_opy_ (u"ࠧࡶࡡࡵࡪ࡯࡭ࡧ࠴ࡐࡰࡵ࡬ࡼࡕࡧࡴࡩࠤሦ"):
            obj = {bstack1l1_opy_ (u"ࠨࡰࡢࡶ࡫ࠦሧ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll11l11111_opy_(key) or str(key).startswith(bstack1l1_opy_ (u"ࠢࡠࠤረ")):
            continue
        if value is not None and bstack1ll11l11111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1lll11l1l_opy_(value, bstack1l1lll1111l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1lll11l1l_opy_(o, bstack1l1lll1111l_opy_, max_depth) for o in value]))
    return result or None