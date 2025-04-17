import dataclasses
from typing import Any, Callable

import telepath as tp
from . import _callbacks
from ._dto import TgUpd
import copy
import telegram as t
from collections import OrderedDict



# class MessageData(t.Message):
#     def __init__(self, *args, **kwargs):
#         super().__init__(-1, datetime.datetime.now(), t.Chat(-1, "sender"), *args, **kwargs)


@dataclasses.dataclass(slots=True)
class TgBtn:
    text: str = "Button"
    value: Any = None
    _btn_id: str = None
    
    
    def title(self):
        return self.text
    
    
    def pack(self, btn_id, withMsgType):
        cbd = _callbacks.CallBackData(withMsgType, btn_id, self.value).pack()
        return t.InlineKeyboardButton(self.title(), callback_data=cbd)
    
    
    def unpack(self, cbd):
        c = _callbacks.CallBackData().unpack(cbd)
        self._btn_id = c.btn_id
        self.value = c.value
        return self
    
    
    def on_click(self):
        pass


class CheckButton(TgBtn):
    def title(self):
        return tp.with_checked_emoji(self.value, self.text)
    
    
    def on_click(self):
        self.value = not self.value


class _InlineKeyboard:
    
    @staticmethod
    def btn_dict(mu: t.InlineKeyboardMarkup) -> dict[str, TgBtn]:
        btn_dict = OrderedDict()
        for row in mu.inline_keyboard:
            for b in row:
                tgb = TgBtn().unpack(b.callback_data)
                btn_dict[tgb._btn_id] = tgb
        return btn_dict
    
    
    @staticmethod
    def pack(kb_tree, withMsgType) -> t.InlineKeyboardMarkup | None:
        if kb_tree is None:
            return None
        
        rows = []
        for row in kb_tree:
            new_row = [b.pack(b._btn_id, withMsgType) for b in row]
            rows.append(new_row)
        return t.InlineKeyboardMarkup(rows)


SFM_CT = Callable[["SFMessage"], str]


class _SFMessageMeta(type):
    def __init__(cls, name, bases, namespace):
        super().__init__(name, bases, namespace)
        
        for a in cls.__dict__:
            if a.startswith("__"):
                continue
            attr = getattr(cls, a)
            if isinstance(attr, TgBtn):
                setattr(cls, a, attr)
                setattr(attr, "_btn_id", a)


class SFMessage(metaclass=_SFMessageMeta):
    MSG_TYPE = None
    """
    Stateful Message model interface.
    Can pack itself to MessageData and which is mosly like a json but i wanted class.
    Can unpack update, which is mostly set values from keyboard state in callback_data.
    Stateless message would either be set from outer scope or have a specific unpacker i guess,
    since each message can represent different model.

    Since message knows about values, I think, it should know the callback_data format.
    Should we have button class? maybe button info, idknow.

    Next one. Text. It can be dynamic generally. Like count pressed buttons idk.
    so probably we should have text() method to render it.
    Should it be dynamic i.e. get it on the fly, or getter/setter thing.
    So, if i make setText, it seems like the format should some from with-out.
    I don't like it, since I imitate view builder. So I guess it should be

    """
    
    
    def __post_init__(self):
        for a in self.__class__.__dict__:
            if a.startswith("__"):
                continue
            attr = getattr(self, a)
            if isinstance(attr, TgBtn):
                cattr = copy.copy(attr)
    
    
    def text(self):
        return "Message text"
    
    
    def keyboard(self):
        return None
    
    
    def on_cbq(self, cbq):
        pass
    
    
    def pack(self) -> (str, t.InlineKeyboardMarkup):
        msg_type = self.__class__.MSG_TYPE
        mt = msg_type or str(self.__class__)
        return self.text(), _InlineKeyboard.pack(self.keyboard(), msg_type)
    
    
    def unpack(self, u: TgUpd):
        kbd = _InlineKeyboard.btn_dict(u.kbm)
        for btn_id, btn in kbd.items():
            btnattr = getattr(self, btn_id)
            setattr(btnattr, "value", btn.value)
        return self


@dataclasses.dataclass
class MultiChoiceSFMessage(SFMessage):
    complete = TgBtn("Применить")
    
    
    def keyboard(self):
        return [[MultiChoiceSFMessage.complete]]
    
    
    def on_cbq(self, cbq):
        btn = getattr(self, TgBtn().unpack(cbq)._btn_id)
        btn.on_click()
        return btn._btn_id == "complete"
