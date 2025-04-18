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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11ll1111l1l_opy_
from browserstack_sdk.bstack1l111lll11_opy_ import bstack1l1l1l1ll1_opy_
def _11l11ll1111_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11ll1l1l_opy_:
    def __init__(self, handler):
        self._11l11l1ll11_opy_ = {}
        self._11l11ll1l11_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack1l1l1l1ll1_opy_.version()
        if bstack11ll1111l1l_opy_(pytest_version, bstack1l1ll11_opy_ (u"ࠣ࠺࠱࠵࠳࠷ࠢᮭ")) >= 0:
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᮮ")] = Module._register_setup_function_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮯ")] = Module._register_setup_module_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮰")] = Class._register_setup_class_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮱")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮲"))
            Module._register_setup_module_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮳"))
            Class._register_setup_class_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮴"))
            Class._register_setup_method_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪ᮵"))
        else:
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠪࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮶")] = Module._inject_setup_function_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠫࡲࡵࡤࡶ࡮ࡨࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮷")] = Module._inject_setup_module_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"ࠬࡩ࡬ࡢࡵࡶࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮸")] = Class._inject_setup_class_fixture
            self._11l11l1ll11_opy_[bstack1l1ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮹")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠧࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮺ"))
            Module._inject_setup_module_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠨ࡯ࡲࡨࡺࡲࡥࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᮻ"))
            Class._inject_setup_class_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠩࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᮼ"))
            Class._inject_setup_method_fixture = self.bstack11l11ll11l1_opy_(bstack1l1ll11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮽ"))
    def bstack11l11lll111_opy_(self, bstack11l11l1lll1_opy_, hook_type):
        bstack11l11ll1lll_opy_ = id(bstack11l11l1lll1_opy_.__class__)
        if (bstack11l11ll1lll_opy_, hook_type) in self._11l11ll1l11_opy_:
            return
        meth = getattr(bstack11l11l1lll1_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll1l11_opy_[(bstack11l11ll1lll_opy_, hook_type)] = meth
            setattr(bstack11l11l1lll1_opy_, hook_type, self.bstack11l11lll1ll_opy_(hook_type, bstack11l11ll1lll_opy_))
    def bstack11l11ll111l_opy_(self, instance, bstack11l11ll1ll1_opy_):
        if bstack11l11ll1ll1_opy_ == bstack1l1ll11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᮾ"):
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠧࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠨᮿ"))
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠨࡴࡦࡣࡵࡨࡴࡽ࡮ࡠࡨࡸࡲࡨࡺࡩࡰࡰࠥᯀ"))
        if bstack11l11ll1ll1_opy_ == bstack1l1ll11_opy_ (u"ࠢ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠣᯁ"):
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠣࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠢᯂ"))
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲࡵࡤࡶ࡮ࡨࠦᯃ"))
        if bstack11l11ll1ll1_opy_ == bstack1l1ll11_opy_ (u"ࠥࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠥᯄ"):
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡧࡱࡧࡳࡴࠤᯅ"))
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡤ࡮ࡤࡷࡸࠨᯆ"))
        if bstack11l11ll1ll1_opy_ == bstack1l1ll11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᯇ"):
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩࠨᯈ"))
            self.bstack11l11lll111_opy_(instance.obj, bstack1l1ll11_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠥᯉ"))
    @staticmethod
    def bstack11l11lll11l_opy_(hook_type, func, args):
        if hook_type in [bstack1l1ll11_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠ࡯ࡨࡸ࡭ࡵࡤࠨᯊ"), bstack1l1ll11_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡳࡥࡵࡪࡲࡨࠬᯋ")]:
            _11l11ll1111_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11lll1ll_opy_(self, hook_type, bstack11l11ll1lll_opy_):
        def bstack11l11l1ll1l_opy_(arg=None):
            self.handler(hook_type, bstack1l1ll11_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࠫᯌ"))
            result = None
            try:
                bstack1llllllllll_opy_ = self._11l11ll1l11_opy_[(bstack11l11ll1lll_opy_, hook_type)]
                self.bstack11l11lll11l_opy_(hook_type, bstack1llllllllll_opy_, (arg,))
                result = Result(result=bstack1l1ll11_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᯍ"))
            except Exception as e:
                result = Result(result=bstack1l1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᯎ"), exception=e)
                self.handler(hook_type, bstack1l1ll11_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᯏ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll11_opy_ (u"ࠨࡣࡩࡸࡪࡸࠧᯐ"), result)
        def bstack11l11ll11ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1ll11_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࠩᯑ"))
            result = None
            exception = None
            try:
                self.bstack11l11lll11l_opy_(hook_type, self._11l11ll1l11_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1ll11_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᯒ"))
            except Exception as e:
                result = Result(result=bstack1l1ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᯓ"), exception=e)
                self.handler(hook_type, bstack1l1ll11_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᯔ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1ll11_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᯕ"), result)
        if hook_type in [bstack1l1ll11_opy_ (u"ࠧࡴࡧࡷࡹࡵࡥ࡭ࡦࡶ࡫ࡳࡩ࠭ᯖ"), bstack1l1ll11_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡪࡺࡨࡰࡦࠪᯗ")]:
            return bstack11l11ll11ll_opy_
        return bstack11l11l1ll1l_opy_
    def bstack11l11ll11l1_opy_(self, bstack11l11ll1ll1_opy_):
        def bstack11l11l1llll_opy_(this, *args, **kwargs):
            self.bstack11l11ll111l_opy_(this, bstack11l11ll1ll1_opy_)
            self._11l11l1ll11_opy_[bstack11l11ll1ll1_opy_](this, *args, **kwargs)
        return bstack11l11l1llll_opy_