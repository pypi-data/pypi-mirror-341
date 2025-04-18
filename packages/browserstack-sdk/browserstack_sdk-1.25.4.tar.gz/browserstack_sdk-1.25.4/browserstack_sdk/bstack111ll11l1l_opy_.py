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
class RobotHandler():
    def __init__(self, args, logger, bstack111l11111l_opy_, bstack1111lll111_opy_):
        self.args = args
        self.logger = logger
        self.bstack111l11111l_opy_ = bstack111l11111l_opy_
        self.bstack1111lll111_opy_ = bstack1111lll111_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111lll11ll_opy_(bstack1111ll1l11_opy_):
        bstack1111ll11l1_opy_ = []
        if bstack1111ll1l11_opy_:
            tokens = str(os.path.basename(bstack1111ll1l11_opy_)).split(bstack1l1ll11_opy_ (u"ࠨ࡟ࠣဌ"))
            camelcase_name = bstack1l1ll11_opy_ (u"ࠢࠡࠤဍ").join(t.title() for t in tokens)
            suite_name, bstack1111ll11ll_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll11l1_opy_.append(suite_name)
        return bstack1111ll11l1_opy_
    @staticmethod
    def bstack1111ll111l_opy_(typename):
        if bstack1l1ll11_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦဎ") in typename:
            return bstack1l1ll11_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥဏ")
        return bstack1l1ll11_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦတ")