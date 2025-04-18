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
from uuid import uuid4
from bstack_utils.helper import bstack1l11111ll_opy_, bstack11l1l111ll1_opy_
from bstack_utils.bstack111111ll_opy_ import bstack111l1l1l1l1_opy_
class bstack111ll11111_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, started_at=None, framework=None, tags=[], scope=[], bstack111l111l1l1_opy_=None, bstack111l1111lll_opy_=True, bstack1l111l1lll1_opy_=None, bstack1l11l11l1_opy_=None, result=None, duration=None, bstack111ll11lll_opy_=None, meta={}):
        self.bstack111ll11lll_opy_ = bstack111ll11lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack111l1111lll_opy_:
            self.uuid = uuid4().__str__()
        self.started_at = started_at
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack111l111l1l1_opy_ = bstack111l111l1l1_opy_
        self.bstack1l111l1lll1_opy_ = bstack1l111l1lll1_opy_
        self.bstack1l11l11l1_opy_ = bstack1l11l11l1_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
        self.hooks = []
    def bstack111l1lllll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11l11111ll_opy_(self, meta):
        self.meta = meta
    def bstack11l111111l_opy_(self, hooks):
        self.hooks = hooks
    def bstack1111llll1l1_opy_(self):
        bstack1111lllll1l_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ᶧ"): bstack1111lllll1l_opy_,
            bstack1l1ll11_opy_ (u"ࠫࡱࡵࡣࡢࡶ࡬ࡳࡳ࠭ᶨ"): bstack1111lllll1l_opy_,
            bstack1l1ll11_opy_ (u"ࠬࡼࡣࡠࡨ࡬ࡰࡪࡶࡡࡵࡪࠪᶩ"): bstack1111lllll1l_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1ll11_opy_ (u"ࠨࡕ࡯ࡧࡻࡴࡪࡩࡴࡦࡦࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸ࠿ࠦࠢᶪ") + key)
            setattr(self, key, val)
    def bstack111l1111111_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᶫ"): self.name,
            bstack1l1ll11_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᶬ"): {
                bstack1l1ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᶭ"): bstack1l1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᶮ"),
                bstack1l1ll11_opy_ (u"ࠫࡨࡵࡤࡦࠩᶯ"): self.code
            },
            bstack1l1ll11_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᶰ"): self.scope,
            bstack1l1ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᶱ"): self.tags,
            bstack1l1ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᶲ"): self.framework,
            bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᶳ"): self.started_at
        }
    def bstack111l111l111_opy_(self):
        return {
         bstack1l1ll11_opy_ (u"ࠩࡰࡩࡹࡧࠧᶴ"): self.meta
        }
    def bstack111l111111l_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᶵ"): {
                bstack1l1ll11_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᶶ"): self.bstack111l111l1l1_opy_
            }
        }
    def bstack111l11111ll_opy_(self, bstack1111llll1ll_opy_, details):
        step = next(filter(lambda st: st[bstack1l1ll11_opy_ (u"ࠬ࡯ࡤࠨᶷ")] == bstack1111llll1ll_opy_, self.meta[bstack1l1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᶸ")]), None)
        step.update(details)
    def bstack1lll1l1l1_opy_(self, bstack1111llll1ll_opy_):
        step = next(filter(lambda st: st[bstack1l1ll11_opy_ (u"ࠧࡪࡦࠪᶹ")] == bstack1111llll1ll_opy_, self.meta[bstack1l1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᶺ")]), None)
        step.update({
            bstack1l1ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᶻ"): bstack1l11111ll_opy_()
        })
    def bstack111lllllll_opy_(self, bstack1111llll1ll_opy_, result, duration=None):
        bstack1l111l1lll1_opy_ = bstack1l11111ll_opy_()
        if bstack1111llll1ll_opy_ is not None and self.meta.get(bstack1l1ll11_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᶼ")):
            step = next(filter(lambda st: st[bstack1l1ll11_opy_ (u"ࠫ࡮ࡪࠧᶽ")] == bstack1111llll1ll_opy_, self.meta[bstack1l1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᶾ")]), None)
            step.update({
                bstack1l1ll11_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᶿ"): bstack1l111l1lll1_opy_,
                bstack1l1ll11_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ᷀"): duration if duration else bstack11l1l111ll1_opy_(step[bstack1l1ll11_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ᷁")], bstack1l111l1lll1_opy_),
                bstack1l1ll11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵ᷂ࠩ"): result.result,
                bstack1l1ll11_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᷃"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack111l111l11l_opy_):
        if self.meta.get(bstack1l1ll11_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪ᷄")):
            self.meta[bstack1l1ll11_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫ᷅")].append(bstack111l111l11l_opy_)
        else:
            self.meta[bstack1l1ll11_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬ᷆")] = [ bstack111l111l11l_opy_ ]
    def bstack1111lllll11_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᷇"): self.bstack111l1lllll_opy_(),
            **self.bstack111l1111111_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack111l111l111_opy_()
        }
    def bstack1111lllllll_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1ll11_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭᷈"): self.bstack1l111l1lll1_opy_,
            bstack1l1ll11_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪ᷉"): self.duration,
            bstack1l1ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶ᷊ࠪ"): self.result.result
        }
        if data[bstack1l1ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ᷋")] == bstack1l1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ᷌"):
            data[bstack1l1ll11_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫࡟ࡵࡻࡳࡩࠬ᷍")] = self.result.bstack1111ll111l_opy_()
            data[bstack1l1ll11_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࠨ᷎")] = [{bstack1l1ll11_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨ᷏ࠫ"): self.result.bstack11l1l111lll_opy_()}]
        return data
    def bstack111l11111l1_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠩࡸࡹ࡮ࡪ᷐ࠧ"): self.bstack111l1lllll_opy_(),
            **self.bstack111l1111111_opy_(),
            **self.bstack1111llll1l1_opy_(),
            **self.bstack1111lllllll_opy_(),
            **self.bstack111l111l111_opy_()
        }
    def bstack111llll111_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1ll11_opy_ (u"ࠪࡗࡹࡧࡲࡵࡧࡧࠫ᷑") in event:
            return self.bstack1111lllll11_opy_()
        elif bstack1l1ll11_opy_ (u"ࠫࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭᷒") in event:
            return self.bstack111l11111l1_opy_()
    def bstack111l1ll111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1l111l1lll1_opy_ = time if time else bstack1l11111ll_opy_()
        self.duration = duration if duration else bstack11l1l111ll1_opy_(self.started_at, self.bstack1l111l1lll1_opy_)
        if result:
            self.result = result
class bstack11l111ll11_opy_(bstack111ll11111_opy_):
    def __init__(self, hooks=[], bstack11l1111ll1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11l1111ll1_opy_ = bstack11l1111ll1_opy_
        super().__init__(*args, **kwargs, bstack1l11l11l1_opy_=bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࠪᷓ"))
    @classmethod
    def bstack111l111l1ll_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1ll11_opy_ (u"࠭ࡩࡥࠩᷔ"): id(step),
                bstack1l1ll11_opy_ (u"ࠧࡵࡧࡻࡸࠬᷕ"): step.name,
                bstack1l1ll11_opy_ (u"ࠨ࡭ࡨࡽࡼࡵࡲࡥࠩᷖ"): step.keyword,
            })
        return bstack11l111ll11_opy_(
            **kwargs,
            meta={
                bstack1l1ll11_opy_ (u"ࠩࡩࡩࡦࡺࡵࡳࡧࠪᷗ"): {
                    bstack1l1ll11_opy_ (u"ࠪࡲࡦࡳࡥࠨᷘ"): feature.name,
                    bstack1l1ll11_opy_ (u"ࠫࡵࡧࡴࡩࠩᷙ"): feature.filename,
                    bstack1l1ll11_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᷚ"): feature.description
                },
                bstack1l1ll11_opy_ (u"࠭ࡳࡤࡧࡱࡥࡷ࡯࡯ࠨᷛ"): {
                    bstack1l1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᷜ"): scenario.name
                },
                bstack1l1ll11_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᷝ"): steps,
                bstack1l1ll11_opy_ (u"ࠩࡨࡼࡦࡳࡰ࡭ࡧࡶࠫᷞ"): bstack111l1l1l1l1_opy_(test)
            }
        )
    def bstack111l1111l1l_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᷟ"): self.hooks
        }
    def bstack111l1111l11_opy_(self):
        if self.bstack11l1111ll1_opy_:
            return {
                bstack1l1ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᷠ"): self.bstack11l1111ll1_opy_
            }
        return {}
    def bstack111l11111l1_opy_(self):
        return {
            **super().bstack111l11111l1_opy_(),
            **self.bstack111l1111l1l_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            **self.bstack111l1111l11_opy_()
        }
    def bstack111l1ll111_opy_(self):
        return bstack1l1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᷡ")
class bstack11l111l1l1_opy_(bstack111ll11111_opy_):
    def __init__(self, hook_type, *args,bstack11l1111ll1_opy_={}, **kwargs):
        self.hook_type = hook_type
        self.bstack1111llllll1_opy_ = None
        self.bstack11l1111ll1_opy_ = bstack11l1111ll1_opy_
        super().__init__(*args, **kwargs, bstack1l11l11l1_opy_=bstack1l1ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࠫᷢ"))
    def bstack111l11lll1_opy_(self):
        return self.hook_type
    def bstack111l1111ll1_opy_(self):
        return {
            bstack1l1ll11_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᷣ"): self.hook_type
        }
    def bstack111l11111l1_opy_(self):
        return {
            **super().bstack111l11111l1_opy_(),
            **self.bstack111l1111ll1_opy_()
        }
    def bstack1111lllll11_opy_(self):
        return {
            **super().bstack1111lllll11_opy_(),
            bstack1l1ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢ࡭ࡩ࠭ᷤ"): self.bstack1111llllll1_opy_,
            **self.bstack111l1111ll1_opy_()
        }
    def bstack111l1ll111_opy_(self):
        return bstack1l1ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᷥ")
    def bstack111llll1ll_opy_(self, bstack1111llllll1_opy_):
        self.bstack1111llllll1_opy_ = bstack1111llllll1_opy_