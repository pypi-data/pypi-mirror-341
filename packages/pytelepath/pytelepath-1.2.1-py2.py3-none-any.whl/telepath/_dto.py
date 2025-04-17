import dataclasses

import telegram as t



@dataclasses.dataclass(slots=True)
class TgUpd:
    chat_id: int
    user_id: int
    msg_id: int
    text: str = ""
    cbq: str | None = None
    kbm: t.InlineKeyboardMarkup | None = None
    
    
    @staticmethod
    def of(u: t.Update):
        return TgUpd(u.effective_chat.id, u.effective_user.id, u.effective_message.id,
                     u.effective_message.text or u.effective_message.caption,
                     u.callback_query and u.callback_query.data,
                     u.effective_message.reply_markup)
