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
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack11111l1ll1_opy_ import (
    bstack111111ll1l_opy_,
    bstack111111l11l_opy_,
    bstack11111l1l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll111llll_opy_ import bstack1llllll1l11_opy_
from typing import Tuple, Callable, Any
import grpc
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11ll11_opy_ import bstack1llllll1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import traceback
import os
import time
class bstack1lll1l11l1l_opy_(bstack1llllll1l1l_opy_):
    bstack1ll1l1lllll_opy_ = False
    def __init__(self):
        super().__init__()
        bstack1llllll1l11_opy_.bstack1ll1l1ll1l1_opy_((bstack111111ll1l_opy_.bstack1111l1l111_opy_, bstack111111l11l_opy_.PRE), self.bstack1ll11lll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11lll11l_opy_(
        self,
        f: bstack1llllll1l11_opy_,
        driver: object,
        exec: Tuple[bstack11111l1l1l_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111ll1l_opy_, bstack111111l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        hub_url = f.hub_url(driver)
        if f.bstack1ll11ll1ll1_opy_(hub_url):
            if not bstack1lll1l11l1l_opy_.bstack1ll1l1lllll_opy_:
                self.logger.warning(bstack1l1ll11_opy_ (u"ࠣ࡮ࡲࡧࡦࡲࠠࡴࡧ࡯ࡪ࠲࡮ࡥࡢ࡮ࠣࡪࡱࡵࡷࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࠥࡹࡥࡴࡵ࡬ࡳࡳࡹࠠࡩࡷࡥࡣࡺࡸ࡬࠾ࠤᅺ") + str(hub_url) + bstack1l1ll11_opy_ (u"ࠤࠥᅻ"))
                bstack1lll1l11l1l_opy_.bstack1ll1l1lllll_opy_ = True
            return
        bstack1ll1l11llll_opy_ = f.bstack1ll1l1l1111_opy_(*args)
        bstack1ll11ll1111_opy_ = f.bstack1ll11lll111_opy_(*args)
        if bstack1ll1l11llll_opy_ and bstack1ll1l11llll_opy_.lower() == bstack1l1ll11_opy_ (u"ࠥࡪ࡮ࡴࡤࡦ࡮ࡨࡱࡪࡴࡴࠣᅼ") and bstack1ll11ll1111_opy_:
            framework_session_id = f.session_id(driver)
            locator_type, locator_value = bstack1ll11ll1111_opy_.get(bstack1l1ll11_opy_ (u"ࠦࡺࡹࡩ࡯ࡩࠥᅽ"), None), bstack1ll11ll1111_opy_.get(bstack1l1ll11_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᅾ"), None)
            if not framework_session_id or not locator_type or not locator_value:
                self.logger.warning(bstack1l1ll11_opy_ (u"ࠨࡻࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࢃ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡲࡶࠥࡧࡲࡨࡵ࠱ࡹࡸ࡯࡮ࡨ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡳࡷࠦࡡࡳࡩࡶ࠲ࡻࡧ࡬ࡶࡧࡀࠦᅿ") + str(locator_value) + bstack1l1ll11_opy_ (u"ࠢࠣᆀ"))
                return
            def bstack1llllllll11_opy_(driver, bstack1ll11ll1lll_opy_, *args, **kwargs):
                from selenium.common.exceptions import NoSuchElementException
                try:
                    result = bstack1ll11ll1lll_opy_(driver, *args, **kwargs)
                    response = self.bstack1ll11ll11ll_opy_(
                        framework_session_id=framework_session_id,
                        is_success=True,
                        locator_type=locator_type,
                        locator_value=locator_value,
                    )
                    if response and response.execute_script:
                        driver.execute_script(response.execute_script)
                        self.logger.info(bstack1l1ll11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴ࠯ࡶࡧࡷ࡯ࡰࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࠦᆁ") + str(locator_value) + bstack1l1ll11_opy_ (u"ࠤࠥᆂ"))
                    else:
                        self.logger.warning(bstack1l1ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ࠱ࡳࡵ࠭ࡴࡥࡵ࡭ࡵࡺ࠺ࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫࠽ࡼ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡷࡽࡵ࡫ࡽࠡ࡮ࡲࡧࡦࡺ࡯ࡳࡡࡹࡥࡱࡻࡥ࠾ࡽ࡯ࡳࡨࡧࡴࡰࡴࡢࡺࡦࡲࡵࡦࡿࠣࡶࡪࡹࡰࡰࡰࡶࡩࡂࠨᆃ") + str(response) + bstack1l1ll11_opy_ (u"ࠦࠧᆄ"))
                    return result
                except NoSuchElementException as e:
                    locator = (locator_type, locator_value)
                    return self.__1ll11ll1l1l_opy_(
                        driver, bstack1ll11ll1lll_opy_, e, framework_session_id, locator, *args, **kwargs
                    )
            bstack1llllllll11_opy_.__name__ = bstack1ll1l11llll_opy_
            return bstack1llllllll11_opy_
    def __1ll11ll1l1l_opy_(
        self,
        driver,
        bstack1ll11ll1lll_opy_: Callable,
        exception,
        framework_session_id: str,
        locator: Tuple[str, str],
        *args,
        **kwargs,
    ):
        try:
            locator_type, locator_value = locator
            response = self.bstack1ll11ll11ll_opy_(
                framework_session_id=framework_session_id,
                is_success=False,
                locator_type=locator_type,
                locator_value=locator_value,
            )
            if response and response.execute_script:
                driver.execute_script(response.execute_script)
                self.logger.info(bstack1l1ll11_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡵࡴ࡬࡫࡬࡫ࡲࡦࡦ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࠧᆅ") + str(locator_value) + bstack1l1ll11_opy_ (u"ࠨࠢᆆ"))
                bstack1ll11ll11l1_opy_ = self.bstack1ll11ll111l_opy_(
                    framework_session_id=framework_session_id,
                    locator_type=locator_type,
                )
                self.logger.info(bstack1l1ll11_opy_ (u"ࠢࡧࡣ࡬ࡰࡺࡸࡥ࠮ࡪࡨࡥࡱ࡯࡮ࡨ࠯ࡵࡩࡸࡻ࡬ࡵ࠼ࠣࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦ࠿ࡾࡰࡴࡩࡡࡵࡱࡵࡣࡹࡿࡰࡦࡿࠣࡰࡴࡩࡡࡵࡱࡵࡣࡻࡧ࡬ࡶࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࢁࠥ࡮ࡥࡢ࡮࡬ࡲ࡬ࡥࡲࡦࡵࡸࡰࡹࡃࠢᆇ") + str(bstack1ll11ll11l1_opy_) + bstack1l1ll11_opy_ (u"ࠣࠤᆈ"))
                if bstack1ll11ll11l1_opy_.success and args and len(args) > 1:
                    args[1].update(
                        {
                            bstack1l1ll11_opy_ (u"ࠤࡸࡷ࡮ࡴࡧࠣᆉ"): bstack1ll11ll11l1_opy_.locator_type,
                            bstack1l1ll11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᆊ"): bstack1ll11ll11l1_opy_.locator_value,
                        }
                    )
                    return bstack1ll11ll1lll_opy_(driver, *args, **kwargs)
                elif os.environ.get(bstack1l1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅࡎࡥࡄࡆࡄࡘࡋࠧᆋ"), False):
                    self.logger.info(bstack1lll11l1lll_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡸࡶࡪ࠳ࡨࡦࡣ࡯࡭ࡳ࡭࠭ࡳࡧࡶࡹࡱࡺ࠭࡮࡫ࡶࡷ࡮ࡴࡧ࠻ࠢࡶࡰࡪ࡫ࡰࠩ࠵࠳࠭ࠥࡲࡥࡵࡶ࡬ࡲ࡬ࠦࡹࡰࡷࠣ࡭ࡳࡹࡰࡦࡥࡷࠤࡹ࡮ࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠥࡲ࡯ࡨࡵࠥᆌ"))
                    time.sleep(300)
            else:
                self.logger.warning(bstack1l1ll11_opy_ (u"ࠨࡦࡢ࡫࡯ࡹࡷ࡫࠭࡯ࡱ࠰ࡷࡨࡸࡩࡱࡶ࠽ࠤࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࡀࡿࡱࡵࡣࡢࡶࡲࡶࡤࡺࡹࡱࡧࢀࠤࡱࡵࡣࡢࡶࡲࡶࡤࡼࡡ࡭ࡷࡨࡁࢀࡲ࡯ࡤࡣࡷࡳࡷࡥࡶࡢ࡮ࡸࡩࢂࠦࡲࡦࡵࡳࡳࡳࡹࡥ࠾ࠤᆍ") + str(response) + bstack1l1ll11_opy_ (u"ࠢࠣᆎ"))
        except Exception as err:
            self.logger.warning(bstack1l1ll11_opy_ (u"ࠣࡨࡤ࡭ࡱࡻࡲࡦ࠯࡫ࡩࡦࡲࡩ࡯ࡩ࠰ࡶࡪࡹࡵ࡭ࡶ࠽ࠤࡪࡸࡲࡰࡴ࠽ࠤࠧᆏ") + str(err) + bstack1l1ll11_opy_ (u"ࠤࠥᆐ"))
        raise exception
    @measure(event_name=EVENTS.bstack1ll11ll1l11_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1ll11ll11ll_opy_(
        self,
        framework_session_id: str,
        is_success: bool,
        locator_type: str,
        locator_value: str,
        platform_index=bstack1l1ll11_opy_ (u"ࠥ࠴ࠧᆑ"),
    ):
        self.bstack1ll1lll111l_opy_()
        req = structs.AISelfHealStepRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.is_success = is_success
        req.test_name = bstack1l1ll11_opy_ (u"ࠦࠧᆒ")
        req.locator_type = locator_type
        req.locator_value = locator_value
        try:
            r = self.bstack1llll111ll1_opy_.AISelfHealStep(req)
            self.logger.info(bstack1l1ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆓ") + str(r) + bstack1l1ll11_opy_ (u"ࠨࠢᆔ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᆕ") + str(e) + bstack1l1ll11_opy_ (u"ࠣࠤᆖ"))
            traceback.print_exc()
            raise e
    @measure(event_name=EVENTS.bstack1ll11lll1l1_opy_, stage=STAGE.bstack1ll1111ll1_opy_)
    def bstack1ll11ll111l_opy_(self, framework_session_id: str, locator_type: str, platform_index=bstack1l1ll11_opy_ (u"ࠤ࠳ࠦᆗ")):
        self.bstack1ll1lll111l_opy_()
        req = structs.AISelfHealGetRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_session_id = framework_session_id
        req.locator_type = locator_type
        try:
            r = self.bstack1llll111ll1_opy_.AISelfHealGetResult(req)
            self.logger.info(bstack1l1ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᆘ") + str(r) + bstack1l1ll11_opy_ (u"ࠦࠧᆙ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᆚ") + str(e) + bstack1l1ll11_opy_ (u"ࠨࠢᆛ"))
            traceback.print_exc()
            raise e