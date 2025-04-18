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
from filelock import FileLock
import json
import os
import time
import uuid
import logging
from typing import Dict, List, Optional
from bstack_utils.bstack111l1l111_opy_ import get_logger
logger = get_logger(__name__)
bstack111l1lll1l1_opy_: Dict[str, float] = {}
bstack111ll111111_opy_: List = []
bstack111l1llll11_opy_ = 5
bstack1l1l1l1l1l_opy_ = os.path.join(os.getcwd(), bstack1l1ll11_opy_ (u"ࠩ࡯ࡳ࡬࠭ᳩ"), bstack1l1ll11_opy_ (u"ࠪ࡯ࡪࡿ࠭࡮ࡧࡷࡶ࡮ࡩࡳ࠯࡬ࡶࡳࡳ࠭ᳪ"))
logging.getLogger(bstack1l1ll11_opy_ (u"ࠫ࡫࡯࡬ࡦ࡮ࡲࡧࡰ࠭ᳫ")).setLevel(logging.WARNING)
lock = FileLock(bstack1l1l1l1l1l_opy_+bstack1l1ll11_opy_ (u"ࠧ࠴࡬ࡰࡥ࡮ࠦᳬ"))
class bstack111l1llll1l_opy_:
    duration: float
    name: str
    startTime: float
    worker: int
    status: bool
    failure: str
    details: Optional[str]
    entryType: str
    platform: Optional[int]
    command: Optional[str]
    hookType: Optional[str]
    cli: Optional[bool]
    def __init__(self, duration: float, name: str, start_time: float, bstack111l1lllll1_opy_: int, status: bool, failure: str, details: Optional[str] = None, platform: Optional[int] = None, command: Optional[str] = None, test_name: Optional[str] = None, hook_type: Optional[str] = None, cli: Optional[bool] = False) -> None:
        self.duration = duration
        self.name = name
        self.startTime = start_time
        self.worker = bstack111l1lllll1_opy_
        self.status = status
        self.failure = failure
        self.details = details
        self.entryType = bstack1l1ll11_opy_ (u"ࠨ࡭ࡦࡣࡶࡹࡷ࡫᳭ࠢ")
        self.platform = platform
        self.command = command
        self.testName = test_name
        self.hookType = hook_type
        self.cli = cli
class bstack1ll1llllll1_opy_:
    global bstack111l1lll1l1_opy_
    @staticmethod
    def bstack1ll1ll1l11l_opy_(key: str):
        bstack1ll1ll11l1l_opy_ = bstack1ll1llllll1_opy_.bstack11lll1lll1l_opy_(key)
        bstack1ll1llllll1_opy_.mark(bstack1ll1ll11l1l_opy_+bstack1l1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᳮ"))
        return bstack1ll1ll11l1l_opy_
    @staticmethod
    def mark(key: str) -> None:
        try:
            bstack111l1lll1l1_opy_[key] = time.time_ns() / 1000000
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸ࠺ࠡࡽࢀࠦᳯ").format(e))
    @staticmethod
    def end(label: str, start: str, end: str, status: bool, failure: Optional[str] = None, hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            bstack1ll1llllll1_opy_.mark(end)
            bstack1ll1llllll1_opy_.measure(label, start, end, status, failure, hook_type, details, command, test_name)
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡰ࡫ࡹࠡ࡯ࡨࡸࡷ࡯ࡣࡴ࠼ࠣࡿࢂࠨᳰ").format(e))
    @staticmethod
    def measure(label: str, start: str, end: str, status: bool, failure: Optional[str], hook_type: Optional[str] = None, details: Optional[str] = None, command: Optional[str] = None, test_name: Optional[str] = None) -> None:
        try:
            if start not in bstack111l1lll1l1_opy_ or end not in bstack111l1lll1l1_opy_:
                logger.debug(bstack1l1ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡴࡢࡴࡷࠤࡰ࡫ࡹࠡࡹ࡬ࡸ࡭ࠦࡶࡢ࡮ࡸࡩࠥࢁࡽࠡࡱࡵࠤࡪࡴࡤࠡ࡭ࡨࡽࠥࡽࡩࡵࡪࠣࡺࡦࡲࡵࡦࠢࡾࢁࠧᳱ").format(start,end))
                return
            duration: float = bstack111l1lll1l1_opy_[end] - bstack111l1lll1l1_opy_[start]
            bstack111l1lll1ll_opy_ = os.environ.get(bstack1l1ll11_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆࡎࡔࡁࡓ࡛ࡢࡍࡘࡥࡒࡖࡐࡑࡍࡓࡍࠢᳲ"), bstack1l1ll11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦᳳ")).lower() == bstack1l1ll11_opy_ (u"ࠨࡴࡳࡷࡨࠦ᳴")
            bstack111ll11111l_opy_: bstack111l1llll1l_opy_ = bstack111l1llll1l_opy_(duration, label, bstack111l1lll1l1_opy_[start], os.getpid(), status, failure, details, os.environ.get(bstack1l1ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠢᳵ"), 0), command, test_name, hook_type, bstack111l1lll1ll_opy_)
            del bstack111l1lll1l1_opy_[start]
            del bstack111l1lll1l1_opy_[end]
            bstack1ll1llllll1_opy_.bstack111l1llllll_opy_(bstack111ll11111l_opy_)
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡦࡣࡶࡹࡷ࡯࡮ࡨࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹ࠺ࠡࡽࢀࠦᳶ").format(e))
    @staticmethod
    def bstack111l1llllll_opy_(bstack111ll11111l_opy_):
        os.makedirs(os.path.dirname(bstack1l1l1l1l1l_opy_)) if not os.path.exists(os.path.dirname(bstack1l1l1l1l1l_opy_)) else None
        bstack1ll1llllll1_opy_.bstack111ll1111l1_opy_()
        try:
            with lock:
                with open(bstack1l1l1l1l1l_opy_, bstack1l1ll11_opy_ (u"ࠤࡵ࠯ࠧ᳷"), encoding=bstack1l1ll11_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ᳸")) as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        data = []
                    data.append(bstack111ll11111l_opy_.__dict__)
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file, indent=4)
        except FileNotFoundError as bstack111l1lll11l_opy_:
            logger.debug(bstack1l1ll11_opy_ (u"ࠦࡋ࡯࡬ࡦࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠥࢁࡽࠣ᳹").format(bstack111l1lll11l_opy_))
            with lock:
                with open(bstack1l1l1l1l1l_opy_, bstack1l1ll11_opy_ (u"ࠧࡽࠢᳺ"), encoding=bstack1l1ll11_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧ᳻")) as file:
                    data = [bstack111ll11111l_opy_.__dict__]
                    json.dump(data, file, indent=4)
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢ࡮ࡩࡾࠦ࡭ࡦࡶࡵ࡭ࡨࡹࠠࡢࡲࡳࡩࡳࡪࠠࡼࡿࠥ᳼").format(str(e)))
        finally:
            if os.path.exists(bstack1l1l1l1l1l_opy_+bstack1l1ll11_opy_ (u"ࠣ࠰࡯ࡳࡨࡱࠢ᳽")):
                os.remove(bstack1l1l1l1l1l_opy_+bstack1l1ll11_opy_ (u"ࠤ࠱ࡰࡴࡩ࡫ࠣ᳾"))
    @staticmethod
    def bstack111ll1111l1_opy_():
        attempt = 0
        while (attempt < bstack111l1llll11_opy_):
            attempt += 1
            if os.path.exists(bstack1l1l1l1l1l_opy_+bstack1l1ll11_opy_ (u"ࠥ࠲ࡱࡵࡣ࡬ࠤ᳿")):
                time.sleep(0.5)
            else:
                break
    @staticmethod
    def bstack11lll1lll1l_opy_(label: str) -> str:
        try:
            return bstack1l1ll11_opy_ (u"ࠦࢀࢃ࠺ࡼࡿࠥᴀ").format(label,str(uuid.uuid4().hex)[:6])
        except Exception as e:
            logger.debug(bstack1l1ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵ࠾ࠥࢁࡽࠣᴁ").format(e))