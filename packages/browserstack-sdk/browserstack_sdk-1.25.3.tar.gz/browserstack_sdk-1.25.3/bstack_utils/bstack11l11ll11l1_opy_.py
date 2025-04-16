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
from _pytest import fixtures
from _pytest.python import _call_with_optional_argument
from pytest import Module, Class
from bstack_utils.helper import Result, bstack11l1l1111ll_opy_
from browserstack_sdk.bstack1l1ll1l111_opy_ import bstack111111l11_opy_
def _11l11l1llll_opy_(method, this, arg):
    arg_count = method.__code__.co_argcount
    if arg_count > 1:
        method(this, arg)
    else:
        method(this)
class bstack11l11lll1l1_opy_:
    def __init__(self, handler):
        self._11l11ll1ll1_opy_ = {}
        self._11l11ll1lll_opy_ = {}
        self.handler = handler
        self.patch()
        pass
    def patch(self):
        pytest_version = bstack111111l11_opy_.version()
        if bstack11l1l1111ll_opy_(pytest_version, bstack1l1_opy_ (u"ࠢ࠹࠰࠴࠲࠶ࠨᮬ")) >= 0:
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࡢࡪ࡮ࡾࡴࡶࡴࡨࠫᮭ")] = Module._register_setup_function_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠩࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮮ")] = Module._register_setup_module_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠪࡧࡱࡧࡳࡴࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮯ")] = Class._register_setup_class_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮰")] = Class._register_setup_method_fixture
            Module._register_setup_function_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠬ࡬ࡵ࡯ࡥࡷ࡭ࡴࡴ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨ᮱"))
            Module._register_setup_module_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"࠭࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮲"))
            Class._register_setup_class_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠧࡤ࡮ࡤࡷࡸࡥࡦࡪࡺࡷࡹࡷ࡫ࠧ᮳"))
            Class._register_setup_method_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮴"))
        else:
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠩࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬ᮵")] = Module._inject_setup_function_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠪࡱࡴࡪࡵ࡭ࡧࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮶")] = Module._inject_setup_module_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠫࡨࡲࡡࡴࡵࡢࡪ࡮ࡾࡴࡶࡴࡨࠫ᮷")] = Class._inject_setup_class_fixture
            self._11l11ll1ll1_opy_[bstack1l1_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪ࠭᮸")] = Class._inject_setup_method_fixture
            Module._inject_setup_function_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"࠭ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩ᮹"))
            Module._inject_setup_module_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠧ࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᮺ"))
            Class._inject_setup_class_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠨࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᮻ"))
            Class._inject_setup_method_fixture = self.bstack11l11lll11l_opy_(bstack1l1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᮼ"))
    def bstack11l11ll1l11_opy_(self, bstack11l11ll111l_opy_, hook_type):
        bstack11l11ll1111_opy_ = id(bstack11l11ll111l_opy_.__class__)
        if (bstack11l11ll1111_opy_, hook_type) in self._11l11ll1lll_opy_:
            return
        meth = getattr(bstack11l11ll111l_opy_, hook_type, None)
        if meth is not None and fixtures.getfixturemarker(meth) is None:
            self._11l11ll1lll_opy_[(bstack11l11ll1111_opy_, hook_type)] = meth
            setattr(bstack11l11ll111l_opy_, hook_type, self.bstack11l11lll111_opy_(hook_type, bstack11l11ll1111_opy_))
    def bstack11l11l1ll1l_opy_(self, instance, bstack11l11lll1ll_opy_):
        if bstack11l11lll1ll_opy_ == bstack1l1_opy_ (u"ࠥࡪࡺࡴࡣࡵ࡫ࡲࡲࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᮽ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠦࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠧᮾ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠧࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠤᮿ"))
        if bstack11l11lll1ll_opy_ == bstack1l1_opy_ (u"ࠨ࡭ࡰࡦࡸࡰࡪࡥࡦࡪࡺࡷࡹࡷ࡫ࠢᯀ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠢࡴࡧࡷࡹࡵࡥ࡭ࡰࡦࡸࡰࡪࠨᯁ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠣࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡱࡴࡪࡵ࡭ࡧࠥᯂ"))
        if bstack11l11lll1ll_opy_ == bstack1l1_opy_ (u"ࠤࡦࡰࡦࡹࡳࡠࡨ࡬ࡼࡹࡻࡲࡦࠤᯃ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠥࡷࡪࡺࡵࡱࡡࡦࡰࡦࡹࡳࠣᯄ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠦࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡣ࡭ࡣࡶࡷࠧᯅ"))
        if bstack11l11lll1ll_opy_ == bstack1l1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࡤ࡬ࡩࡹࡶࡸࡶࡪࠨᯆ"):
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠨࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠧᯇ"))
            self.bstack11l11ll1l11_opy_(instance.obj, bstack1l1_opy_ (u"ࠢࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠤᯈ"))
    @staticmethod
    def bstack11l11l1ll11_opy_(hook_type, func, args):
        if hook_type in [bstack1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡧࡷ࡬ࡴࡪࠧᯉ"), bstack1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡲ࡫ࡴࡩࡱࡧࠫᯊ")]:
            _11l11l1llll_opy_(func, args[0], args[1])
            return
        _call_with_optional_argument(func, args[0])
    def bstack11l11lll111_opy_(self, hook_type, bstack11l11ll1111_opy_):
        def bstack11l11l1lll1_opy_(arg=None):
            self.handler(hook_type, bstack1l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࠪᯋ"))
            result = None
            try:
                bstack1111111lll_opy_ = self._11l11ll1lll_opy_[(bstack11l11ll1111_opy_, hook_type)]
                self.bstack11l11l1ll11_opy_(hook_type, bstack1111111lll_opy_, (arg,))
                result = Result(result=bstack1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫᯌ"))
            except Exception as e:
                result = Result(result=bstack1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᯍ"), exception=e)
                self.handler(hook_type, bstack1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࠬᯎ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷ࠭ᯏ"), result)
        def bstack11l11ll11ll_opy_(this, arg=None):
            self.handler(hook_type, bstack1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࠨᯐ"))
            result = None
            exception = None
            try:
                self.bstack11l11l1ll11_opy_(hook_type, self._11l11ll1lll_opy_[hook_type], (this, arg))
                result = Result(result=bstack1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᯑ"))
            except Exception as e:
                result = Result(result=bstack1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᯒ"), exception=e)
                self.handler(hook_type, bstack1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࠪᯓ"), result)
                raise e.with_traceback(e.__traceback__)
            self.handler(hook_type, bstack1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᯔ"), result)
        if hook_type in [bstack1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᯕ"), bstack1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡩࡹ࡮࡯ࡥࠩᯖ")]:
            return bstack11l11ll11ll_opy_
        return bstack11l11l1lll1_opy_
    def bstack11l11lll11l_opy_(self, bstack11l11lll1ll_opy_):
        def bstack11l11ll1l1l_opy_(this, *args, **kwargs):
            self.bstack11l11l1ll1l_opy_(this, bstack11l11lll1ll_opy_)
            self._11l11ll1ll1_opy_[bstack11l11lll1ll_opy_](this, *args, **kwargs)
        return bstack11l11ll1l1l_opy_