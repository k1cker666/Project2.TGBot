from telegram import InlineKeyboardButton, KeyboardButton

def build_menu(
    buttons: list[InlineKeyboardButton | KeyboardButton],
    n_cols: int,
    header_buttons: InlineKeyboardButton | KeyboardButton = None,
    footer_buttons: InlineKeyboardButton | KeyboardButton = None
    ) -> list[list[InlineKeyboardButton | KeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu