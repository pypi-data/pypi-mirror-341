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
import threading
import os
import logging
from uuid import uuid4
from bstack_utils.bstack111lllll11_opy_ import bstack111llll1ll_opy_, bstack11l11111l1_opy_
from bstack_utils.bstack11l11l1111_opy_ import bstack11llll111l_opy_
from bstack_utils.helper import bstack1l1l11l1l_opy_, bstack11l1l11ll1_opy_, Result
from bstack_utils.bstack11l11l11l1_opy_ import bstack111111l1_opy_
from bstack_utils.capture import bstack11l11l111l_opy_
from bstack_utils.constants import *
logger = logging.getLogger(__name__)
class bstack111ll1111_opy_:
    def __init__(self):
        self.bstack11l111ll1l_opy_ = bstack11l11l111l_opy_(self.bstack11l111l1l1_opy_)
        self.tests = {}
    @staticmethod
    def bstack11l111l1l1_opy_(log):
        if not (log[bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ້࠭")] and log[bstack1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫໊ࠧ")].strip()):
            return
        active = bstack11llll111l_opy_.bstack11l1111l11_opy_()
        log = {
            bstack1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ໋࠭"): log[bstack1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ໌")],
            bstack1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬໍ"): bstack11l1l11ll1_opy_(),
            bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ໎"): log[bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ໏")],
        }
        if active:
            if active[bstack1l1_opy_ (u"ࠬࡺࡹࡱࡧࠪ໐")] == bstack1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࠫ໑"):
                log[bstack1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ໒")] = active[bstack1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ໓")]
            elif active[bstack1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧ໔")] == bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨ໕"):
                log[bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ໖")] = active[bstack1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ໗")]
        bstack111111l1_opy_.bstack1ll1l1l1l1_opy_([log])
    def start_test(self, attrs):
        test_uuid = uuid4().__str__()
        self.tests[test_uuid] = {}
        self.bstack11l111ll1l_opy_.start()
        driver = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬ໘"), None)
        bstack111lllll11_opy_ = bstack11l11111l1_opy_(
            name=attrs.scenario.name,
            uuid=test_uuid,
            started_at=bstack11l1l11ll1_opy_(),
            file_path=attrs.feature.filename,
            result=bstack1l1_opy_ (u"ࠢࡱࡧࡱࡨ࡮ࡴࡧࠣ໙"),
            framework=bstack1l1_opy_ (u"ࠨࡄࡨ࡬ࡦࡼࡥࠨ໚"),
            scope=[attrs.feature.name],
            bstack11l111l11l_opy_=bstack111111l1_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {},
            meta={},
            tags=attrs.scenario.tags
        )
        self.tests[test_uuid][bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬ໛")] = bstack111lllll11_opy_
        threading.current_thread().current_test_uuid = test_uuid
        bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫໜ"), bstack111lllll11_opy_)
    def end_test(self, attrs):
        bstack111lllllll_opy_ = {
            bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤໝ"): attrs.feature.name,
            bstack1l1_opy_ (u"ࠧࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠥໞ"): attrs.feature.description
        }
        current_test_uuid = threading.current_thread().current_test_uuid
        bstack111lllll11_opy_ = self.tests[current_test_uuid][bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩໟ")]
        meta = {
            bstack1l1_opy_ (u"ࠢࡧࡧࡤࡸࡺࡸࡥࠣ໠"): bstack111lllllll_opy_,
            bstack1l1_opy_ (u"ࠣࡵࡷࡩࡵࡹࠢ໡"): bstack111lllll11_opy_.meta.get(bstack1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨ໢"), []),
            bstack1l1_opy_ (u"ࠥࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠧ໣"): {
                bstack1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ໤"): attrs.feature.scenarios[0].name if len(attrs.feature.scenarios) else None
            }
        }
        bstack111lllll11_opy_.bstack111lllll1l_opy_(meta)
        bstack111lllll11_opy_.bstack111llll11l_opy_(bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡵࠪ໥"), []))
        bstack11l11111ll_opy_, exception = self._11l1111111_opy_(attrs)
        bstack11l111l1ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l111lll1_opy_=[bstack11l11111ll_opy_])
        self.tests[threading.current_thread().current_test_uuid][bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡩࡧࡴࡢࠩ໦")].stop(time=bstack11l1l11ll1_opy_(), duration=int(attrs.duration)*1000, result=bstack11l111l1ll_opy_)
        bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ໧"), self.tests[threading.current_thread().current_test_uuid][bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໨")])
    def bstack1lllllll1_opy_(self, attrs):
        bstack111llll1l1_opy_ = {
            bstack1l1_opy_ (u"ࠩ࡬ࡨࠬ໩"): uuid4().__str__(),
            bstack1l1_opy_ (u"ࠪ࡯ࡪࡿࡷࡰࡴࡧࠫ໪"): attrs.keyword,
            bstack1l1_opy_ (u"ࠫࡸࡺࡥࡱࡡࡤࡶ࡬ࡻ࡭ࡦࡰࡷࠫ໫"): [],
            bstack1l1_opy_ (u"ࠬࡺࡥࡹࡶࠪ໬"): attrs.name,
            bstack1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ໭"): bstack11l1l11ll1_opy_(),
            bstack1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ໮"): bstack1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ໯"),
            bstack1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ໰"): bstack1l1_opy_ (u"ࠪࠫ໱")
        }
        self.tests[threading.current_thread().current_test_uuid][bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧ໲")].add_step(bstack111llll1l1_opy_)
        threading.current_thread().current_step_uuid = bstack111llll1l1_opy_[bstack1l1_opy_ (u"ࠬ࡯ࡤࠨ໳")]
    def bstack1l1ll1ll1_opy_(self, attrs):
        current_test_id = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪ໴"), None)
        current_step_uuid = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡵࡷࡩࡵࡥࡵࡶ࡫ࡧࠫ໵"), None)
        bstack11l11111ll_opy_, exception = self._11l1111111_opy_(attrs)
        bstack11l111l1ll_opy_ = Result(result=attrs.status.name, exception=exception, bstack11l111lll1_opy_=[bstack11l11111ll_opy_])
        self.tests[current_test_id][bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫ໶")].bstack11l111111l_opy_(current_step_uuid, duration=int(attrs.duration)*1000, result=bstack11l111l1ll_opy_)
        threading.current_thread().current_step_uuid = None
    def bstack11l1ll11l_opy_(self, name, attrs):
        try:
            bstack111llllll1_opy_ = uuid4().__str__()
            self.tests[bstack111llllll1_opy_] = {}
            self.bstack11l111ll1l_opy_.start()
            scopes = []
            driver = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ໷"), None)
            current_thread = threading.current_thread()
            if not hasattr(current_thread, bstack1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱࡳࠨ໸")):
                current_thread.current_test_hooks = []
            current_thread.current_test_hooks.append(bstack111llllll1_opy_)
            if name in [bstack1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ໹"), bstack1l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ໺")]:
                file_path = os.path.join(attrs.config.base_dir, attrs.config.environment_file)
                scopes = [attrs.config.environment_file]
            elif name in [bstack1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ໻"), bstack1l1_opy_ (u"ࠢࡢࡨࡷࡩࡷࡥࡦࡦࡣࡷࡹࡷ࡫ࠢ໼")]:
                file_path = attrs.filename
                scopes = [attrs.name]
            else:
                file_path = attrs.filename
                if hasattr(attrs, bstack1l1_opy_ (u"ࠨࡨࡨࡥࡹࡻࡲࡦࠩ໽")):
                    scopes =  [attrs.feature.name]
            hook_data = bstack111llll1ll_opy_(
                name=name,
                uuid=bstack111llllll1_opy_,
                started_at=bstack11l1l11ll1_opy_(),
                file_path=file_path,
                framework=bstack1l1_opy_ (u"ࠤࡅࡩ࡭ࡧࡶࡦࠤ໾"),
                bstack11l111l11l_opy_=bstack111111l1_opy_.bstack11l111ll11_opy_(driver) if driver and driver.session_id else {},
                scope=scopes,
                result=bstack1l1_opy_ (u"ࠥࡴࡪࡴࡤࡪࡰࡪࠦ໿"),
                hook_type=name
            )
            self.tests[bstack111llllll1_opy_][bstack1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠢༀ")] = hook_data
            current_test_id = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣࡺࡻࡩࡥࠤ༁"), None)
            if current_test_id:
                hook_data.bstack11l111llll_opy_(current_test_id)
            if name == bstack1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ༂"):
                threading.current_thread().before_all_hook_uuid = bstack111llllll1_opy_
            threading.current_thread().current_hook_uuid = bstack111llllll1_opy_
            bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"ࠢࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠣ༃"), hook_data)
        except Exception as e:
            logger.debug(bstack1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡸࡥࡥࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤ࡭ࡵ࡯࡬ࠢࡨࡺࡪࡴࡴࡴ࠮ࠣ࡬ࡴࡵ࡫ࠡࡰࡤࡱࡪࡀࠠࠦࡵ࠯ࠤࡪࡸࡲࡰࡴ࠽ࠤࠪࡹࠢ༄"), name, e)
    def bstack11l111111_opy_(self, attrs):
        bstack11l111l111_opy_ = bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༅"), None)
        hook_data = self.tests[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༆")]
        status = bstack1l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ༇")
        exception = None
        bstack11l11111ll_opy_ = None
        if hook_data.name == bstack1l1_opy_ (u"ࠧࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠣ༈"):
            self.bstack11l111ll1l_opy_.reset()
            bstack11l1111lll_opy_ = self.tests[bstack1l1l11l1l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࡢ࡬ࡴࡵ࡫ࡠࡷࡸ࡭ࡩ࠭༉"), None)][bstack1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡪࡡࡵࡣࠪ༊")].result.result
            if bstack11l1111lll_opy_ == bstack1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ་"):
                if attrs.hook_failures == 1:
                    status = bstack1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ༌")
                elif attrs.hook_failures == 2:
                    status = bstack1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ།")
            elif attrs.bstack11l1111ll1_opy_:
                status = bstack1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦ༎")
            threading.current_thread().before_all_hook_uuid = None
        else:
            if hook_data.name == bstack1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࡤࡧ࡬࡭ࠩ༏") and attrs.hook_failures == 1:
                status = bstack1l1_opy_ (u"ࠨࡦࡢ࡫࡯ࡩࡩࠨ༐")
            elif hasattr(attrs, bstack1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠧ༑")) and attrs.error_message:
                status = bstack1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣ༒")
            bstack11l11111ll_opy_, exception = self._11l1111111_opy_(attrs)
        bstack11l111l1ll_opy_ = Result(result=status, exception=exception, bstack11l111lll1_opy_=[bstack11l11111ll_opy_])
        hook_data.stop(time=bstack11l1l11ll1_opy_(), duration=0, result=bstack11l111l1ll_opy_)
        bstack111111l1_opy_.bstack11l1111l1l_opy_(bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ༓"), self.tests[bstack11l111l111_opy_][bstack1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭༔")])
        threading.current_thread().current_hook_uuid = None
    def _11l1111111_opy_(self, attrs):
        try:
            import traceback
            bstack1l11lllll_opy_ = traceback.format_tb(attrs.exc_traceback)
            bstack11l11111ll_opy_ = bstack1l11lllll_opy_[-1] if bstack1l11lllll_opy_ else None
            exception = attrs.exception
        except Exception:
            logger.debug(bstack1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡴࡨࡨࠥࡽࡨࡪ࡮ࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡩࡵࡴࡶࡲࡱࠥࡺࡲࡢࡥࡨࡦࡦࡩ࡫ࠣ༕"))
            bstack11l11111ll_opy_ = None
            exception = None
        return bstack11l11111ll_opy_, exception