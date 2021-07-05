# created for USERGE-X by @Kakashi_HTK(tg)/@ashwinstr(github)

from userge import Message, userge


@userge.on_cmd(
    "c_users",
    about={
        "header": "find chat users",
        "description": "mention users from any chat",
        "usage": "{tr}c_users [limit] [chat username/id]\n"
        "or {tr}c_users [[limit] or [chat username/id]]\n"
        "or {tr}c_users (default limit 100) (current chat)",
    },
)
async def chat_users_(message: Message):
    """find chat users"""
    input_ = message.input_str
    if not input_:
        limit_ = 100
        chat_ = message.chat.id
    else:
        if len(input_.split()) > 1:
            chat_ = input_.split()[1:]
            limit_ = input_.split()[0]
            try:
                await userge.get_chat(chat_)
            except BaseException:
                await message.edit(f"Chat <code>{chat_}</code> is not a valid chat...")
                return
        else:
            chat_ = input_
            try:
                await userge.get_chat(chat_)
                limit_ = 100
            except BaseException:
                chat_ = message.chat.id
                limit_ = input_
                if int(limit_) > 10000:
                    await message.edit(
                        f"Current limit(<code>{limit_}</code>) can't be more than 10000..."
                    )
                    return
    title = (await userge.get_chat(chat_)).title
    await message.edit(f"Getting <b>{limit_}</b> members of chat <b>{title}</b>...")
    list_ = f"List of <b>{limit_}</b> members in chat <b>{title}</b>:\n\n"
    lim = 0
    async for mem in userge.iter_chat_members(chat_):
        try:
            await userge.get_users(mem.user.id)
            user = " ".join([mem.user.first_name, mem.user.last_name or ""])
        except BaseException:
            user = "<i>DELETED USER</i>"
        list_ += (
            f"• {user} - @{mem.user.username}\n"
            if mem.user.username
            else f"• <a href='tg://user?id={mem.user.id}'>{user}</a>\n"
        )
        lim += 1
        if len(list_) > 4040:
            await message.reply(list_)
            list_ = ""
        if int(limit_) != 10000:
            if lim == limit_:
                break
    if len(list_) != 0:
        await message.reply(list_)
    await message.delete()
