import config, db
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, WebAppInfo, Message

app = Client("reztrlbot", api_hash=config.tg_api_hash, api_id=config.tg_api_id, bot_token=config.bot_token)

def web_app_data_filter(_, __, message: Message):
    return message.web_app_data is not None

filters.web_app_data = filters.create(web_app_data_filter)

async def responseempty(client, message):
    await client.send_message(chat_id=message.chat.id,
                              text="Нету запроса!",
                              reply_to_message_id=message.id)

async def respononesub(client, message):
    await client.send_message(chat_id=message.from_user.id,
                              text="Простите но вы когда заходили в эту группу!\n"
                                   "В ней включен One Sub режим который не позволяет зайти снова после выхода!")

@app.on_message(filters.command("one_sub"))
async def one_sub_handler(client: Client, message: Message):
    command, *args = message.text.split(" ", 1)

    if not args:
        await responseempty(client, message)
        return

    if args[0] == "true":
        await db.change_one_sub_mode(True, chat_id=message.chat.id)
        await client.send_message(chat_id=message.chat.id,
                                  text="One Sub режим включен!")
    elif args[0] == "false":
        await db.change_one_sub_mode(False, chat_id=message.chat.id)
        await client.send_message(chat_id=message.chat.id,
                                  text="One Sub режим выключен!")

@app.on_message(filters.command("whitelist"))
async def whitelist_handler(client: Client, message: Message):
    command, *args = message.text.split(" ", 2)

    if not args:
        await responseempty(client, message)
        return

    if args[0] == "add":
        peer = await app.resolve_peer(args[1])
        await db.add_user_to_whitelist(chat_id=message.chat.id, user_id=peer.user_id)
        await client.send_message(chat_id=message.chat.id,
                                  text=f"Пользователь {args[1]} добавлен в белый список!")
    elif args[0] == "remove":
        peer = await app.resolve_peer(args[1])
        await db.remove_user_from_whitelist(chat_id=message.chat.id, user_id=peer.user_id)
        await client.send_message(chat_id=message.chat.id,
                                  text=f"Пользователь {args[1]} удален из белого списка!")

@app.on_chat_join_request()
async def handle_join_request(client: Client, chat_join_request):
    user_id = chat_join_request.from_user.id
    chat_id = chat_join_request.chat.id

    if await db.get_settings_from_one_sub_mode(chat_id):
        if await db.get_users_from_one_sub_mode(user_id, chat_id):
            await respononesub(client, chat_join_request)
        else:
            await db.add_join_request(user_id, chat_id)

            await client.send_message(
                chat_id=user_id,
                text="Привет! Нажми кнопку ниже, чтобы пройти проверку.",
                reply_markup=ReplyKeyboardMarkup(
                    [
                        [KeyboardButton("Пройти проверку", web_app=WebAppInfo(url="https://rebot.lukiuwu.xyz"))]
                    ],
                    resize_keyboard=True
                )
            )
    else:
        await db.add_join_request(user_id, chat_id)

        await client.send_message(
            chat_id=user_id,
            text="Привет! Нажми кнопку ниже, чтобы пройти проверку.",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton("Пройти проверку", web_app=WebAppInfo(url="https://rebot.lukiuwu.xyz"))]
                ],
                resize_keyboard=True
            )
        )

@app.on_message(filters.web_app_data)
async def handle_web_app_data(client: Client, message: Message):
    user_id = message.from_user.id
    data = message.web_app_data.data

    if data == "verified":
        result = await db.get_join_requests(user_id)

        if result:
            chat_id = result[0]

            try:
                await client.approve_chat_join_request(chat_id, user_id)
                try:
                    if await db.get_settings_from_one_sub_mode(chat_id):
                        if await db.get_user_from_whitelist(chat_id, user_id):
                            await db.add_user_to_one_sub_mode(user_id, chat_id)
                except Exception as e:
                    pass
                await client.send_message(
                    chat_id=user_id,
                    text="Вы успешно прошли проверку и добавлены в чат.",
                    reply_markup=ReplyKeyboardRemove()
                )
            except Exception as e:
                await client.send_message(
                    chat_id=user_id,
                    text=f"Произошла ошибка при одобрении запроса: {e}"
                )
        else:
            await client.send_message(
                chat_id=user_id,
                text="Запрос на присоединение не найден."
            )
    elif data == "error":
        await client.send_message(
            chat_id=user_id,
            text="Вы не прошли проверку.",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await client.send_message(
            chat_id=user_id,
            text="Неверные данные проверки."
        )

app.run()
