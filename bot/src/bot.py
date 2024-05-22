from functools import partial

from src.dependencies import Dependencies
from src.handlers import help
from src.models.callback import CallbackData
from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)


def start_bot(deps: Dependencies):

    def partial_deps(func):
        return partial(func, deps=deps)

    application = Application.builder().token(deps.config.bot_token).build()

    application.add_handler(CommandHandler("start", partial_deps(start)))
    application.add_handler(CommandHandler("help", help.help_command))

    application.add_handler(
        CallbackQueryHandler(partial_deps(callback_handler))
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE, deps: Dependencies
):
    await deps.start_handler.handle(update, context)


async def callback_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE, deps: Dependencies
):
    tg_login = update.effective_user.username
    if deps.user_repository.is_user_authorized(tg_login=tg_login):
        query = update.callback_query
        callback_data: CallbackData = CallbackData.from_string(query.data)
        if callback_data.cb_processor == deps.start_handler.name:
            await deps.start_handler.handle_callback(
                update, context, callback_data
            )
        if callback_data.cb_processor == deps.lesson_handler.name:
            if deps.user_state_processor.is_user_online(
                user_id=update.effective_user.username
            ):
                await deps.lesson_handler.handle_callback(
                    update, context, callback_data
                )
            else:
                await deps.start_handler.build_base_menu(
                    update, context, "long_afk"
                )
        if callback_data.cb_processor == deps.repetition_handler.name:
            if deps.user_state_processor.is_user_online(
                user_id=update.effective_user.username
            ):
                await deps.repetition_handler.handle_callback(
                    update, context, callback_data
                )
            else:
                await deps.start_handler.build_base_menu(
                    update, context, "long_afk"
                )
        if callback_data.cb_processor == deps.practice_handler.name:
            if deps.user_state_processor.is_user_online(
                user_id=update.effective_user.username
            ):
                await deps.practice_handler.handle_callback(
                    update, context, callback_data
                )
            else:
                await deps.start_handler.build_base_menu(
                    update, context, "long_afk"
                )
        if callback_data.cb_processor == deps.statistic_handler.name:
            await deps.statistic_handler.handle_callback(
                update, context, callback_data
            )
    else:
        await deps.start_handler.request_authorization(update, context)
