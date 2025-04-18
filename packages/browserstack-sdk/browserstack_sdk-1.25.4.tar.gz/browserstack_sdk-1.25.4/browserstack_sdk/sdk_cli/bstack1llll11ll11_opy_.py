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
import logging
import abc
from browserstack_sdk.sdk_cli.bstack1111l1l1ll_opy_ import bstack1111l1lll1_opy_
class bstack1llllll1l1l_opy_(abc.ABC):
    bin_session_id: str
    bstack1111l1l1ll_opy_: bstack1111l1lll1_opy_
    def __init__(self):
        self.bstack1llll111ll1_opy_ = None
        self.config = None
        self.bin_session_id = None
        self.bstack1111l1l1ll_opy_ = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging.INFO)
    def bstack1lllllll1ll_opy_(self):
        return (self.bstack1llll111ll1_opy_ != None and self.bin_session_id != None and self.bstack1111l1l1ll_opy_ != None)
    def configure(self, bstack1llll111ll1_opy_, config, bin_session_id: str, bstack1111l1l1ll_opy_: bstack1111l1lll1_opy_):
        self.bstack1llll111ll1_opy_ = bstack1llll111ll1_opy_
        self.config = config
        self.bin_session_id = bin_session_id
        self.bstack1111l1l1ll_opy_ = bstack1111l1l1ll_opy_
        if self.bin_session_id:
            self.logger.debug(bstack1l1ll11_opy_ (u"ࠢ࡜ࡽ࡬ࡨ࠭ࡹࡥ࡭ࡨࠬࢁࡢࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡦࡦࠣࡱࡴࡪࡵ࡭ࡧࠣࡿࡸ࡫࡬ࡧ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣ࠳ࡥ࡟࡯ࡣࡰࡩࡤࡥࡽ࠻ࠢࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࡀࠦᆜ") + str(self.bin_session_id) + bstack1l1ll11_opy_ (u"ࠣࠤᆝ"))
    def bstack1ll1lll111l_opy_(self):
        if not self.bin_session_id:
            raise ValueError(bstack1l1ll11_opy_ (u"ࠤࡥ࡭ࡳࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡪࡦࠣࡧࡦࡴ࡮ࡰࡶࠣࡦࡪࠦࡎࡰࡰࡨࠦᆞ"))
    @abc.abstractmethod
    def is_enabled(self) -> bool:
        return False