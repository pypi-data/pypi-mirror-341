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
class RobotHandler():
    def __init__(self, args, logger, bstack1111lll1ll_opy_, bstack1111llll11_opy_):
        self.args = args
        self.logger = logger
        self.bstack1111lll1ll_opy_ = bstack1111lll1ll_opy_
        self.bstack1111llll11_opy_ = bstack1111llll11_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack111lll11ll_opy_(bstack1111ll1l11_opy_):
        bstack1111ll111l_opy_ = []
        if bstack1111ll1l11_opy_:
            tokens = str(os.path.basename(bstack1111ll1l11_opy_)).split(bstack1l1_opy_ (u"ࠨ࡟ࠣဌ"))
            camelcase_name = bstack1l1_opy_ (u"ࠢࠡࠤဍ").join(t.title() for t in tokens)
            suite_name, bstack1111ll11ll_opy_ = os.path.splitext(camelcase_name)
            bstack1111ll111l_opy_.append(suite_name)
        return bstack1111ll111l_opy_
    @staticmethod
    def bstack1111ll11l1_opy_(typename):
        if bstack1l1_opy_ (u"ࠣࡃࡶࡷࡪࡸࡴࡪࡱࡱࠦဎ") in typename:
            return bstack1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࡊࡸࡲࡰࡴࠥဏ")
        return bstack1l1_opy_ (u"࡙ࠥࡳ࡮ࡡ࡯ࡦ࡯ࡩࡩࡋࡲࡳࡱࡵࠦတ")