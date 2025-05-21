import aiosqlite

async def add_join_request(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''
                   INSERT OR REPLACE INTO join_requests (user_id, chat_id)
                   VALUES (?, ?)
               ''', (user_id, chat_id))
            await conn.commit()

async def get_join_requests(user_id):
    async with aiosqlite.connect('join_requests.db') as conn:
        async with conn.execute('SELECT chat_id FROM join_requests WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result

async def add_user_to_whitelist(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''INSERT INTO whitelist (user_id, chat_id) VALUES (?, ?)''', (user_id, chat_id))
            await conn.commit()

async def remove_user_from_whitelist(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''DELETE FROM whitelist WHERE user_id = ? AND chat_id = ?''', (user_id, chat_id))
            await conn.commit()

async def get_user_from_whitelist(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.execute('SELECT 1 FROM whitelist WHERE user_id = ? AND chat_id = ?', (user_id, chat_id)) as cursor:
            result = await cursor.fetchone()
            return result is not None

async def add_user_to_blacklist(user_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''INSERT INTO blacklist (user_id) VALUES (?)''', (user_id,))
            await conn.commit()

async def get_users_from_blacklist(user_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.execute('SELECT 1 FROM blacklist WHERE user_id = ?', (user_id,)) as cursor:
            result = await cursor.fetchone()
            return result is not None

async def add_user_to_one_sub_mode(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('''INSERT INTO one_sub (user_id, chat_id) VALUES (?, ?)''', (user_id, chat_id))
            await conn.commit()

async def get_users_from_one_sub_mode(user_id, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.execute('SELECT 1 FROM one_sub WHERE user_id = ? AND chat_id = ?', (user_id, chat_id)) as cursor:
            result = await cursor.fetchone()
            return result is not None

async def change_one_sub_mode(mode, chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.cursor() as cursor:
            await cursor.execute('INSERT OR REPLACE INTO settings (one_sub_mode, chat_id) VALUES (?, ?)', (mode, chat_id))
            await conn.commit()

async def get_settings_from_one_sub_mode(chat_id):
    async with aiosqlite.connect('reztrlbot.db') as conn:
        async with conn.execute('SELECT one_sub_mode FROM settings WHERE chat_id = ?', (chat_id,)) as cursor:
            result = await cursor.fetchone()
            return result[0]
