import telegram as ptb



IKB = ptb.InlineKeyboardButton
IKCB = lambda text, cbd: ptb.InlineKeyboardButton(text, callback_data=cbd)
IKM = ptb.InlineKeyboardMarkup


def one_row_ikbm(btns: list):
    kb = [[ptb.InlineKeyboardButton(btn[0], callback_data=btn[1]) for btn in btns]]
    return ptb.InlineKeyboardMarkup(kb)


def one_col_ikbm(btns: list):
    kb = [[ptb.InlineKeyboardButton(btn[0], callback_data=btn[1])] for btn in btns]
    return ptb.InlineKeyboardMarkup(kb)


def with_checked_emoji(checked, text):
    return f"{'✅ ' if checked else ''}{text}"


def with_correct_taped_emoji(text, is_correct, is_taped):
    prepend = ""
    if is_correct:
        prepend = "✅ "
    elif is_taped:
        prepend = "❌ "
    nice_text = f"{prepend}{text}"
    return nice_text
