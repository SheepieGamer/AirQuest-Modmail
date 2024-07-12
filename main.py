dev = True
import settings
import discord
import discordbotdash.dash as dbd
from main import bot
from discord.ext import commands
from main.keep_alive import keep_alive


def main(token):
  
    global bot

    @bot.event
    async def on_ready():

        bot.tree.copy_global_to(guild=bot.guilds[0])
        await bot.tree.sync(guild=bot.guilds[0])
        print("Tree loaded successfully")
        
        print(f"User: {bot.user} (ID: {bot.user.id})")

        if not dev:
            dbd.openDash(init_bot=bot, port=1234)
            keep_alive()

    @bot.event
    async def on_message(message):
        empty_array = []
        if message.author == bot.user:
            return
        modmail_channel = discord.utils.get(bot.get_all_channels(),guild__name="AirQuest",name="mod-mail")
        if str(message.channel.type) == "private":
            if message.attachments != empty_array:
                files = message.attachments
                for file in files:
                    await modmail_channel.send(f"{message.author.mention}: {message.content} {file.url}")
            else:
                await modmail_channel.send(f"{message.author.mention}: {message.content}")
        elif str(message.channel) == "mod-mail":
            if message.content.startswith("<@") == False and message.author != bot.user:
                await modmail_channel.send("## Please ping the user you want to reply to.\n### Example:\nUser Message: ``@sheepie0: I need help!!!``\nYour response: ``@sheepie0 what do you need help with?``\n\n:warning: **you must have a space between the ``@sheepie0`` and your message.** :warning:")
                return
            member_object = message.mentions[0]
            if message.attachments != empty_array:
                files = message.attachments
                for file in files:
                    try: index = message.content.index(" ")
                    except ValueError: 
                        await modmail_channel.send("Please include a space between the user's name and your message. If you are only sending attachments, type a space after the ``@mention`` and then type ``.``")
                        return
                    string = message.content
                    mod_message = string[index:]
                    await member_object.send(f"{message.author.display_name}: {mod_message} {file.url}")
            else:
                index = message.content.index(" ")
                string = message.content
                mod_message = string[index:]
                await member_object.send(f"{message.author.display_name}: {mod_message}")

    bot.run(token)

if __name__ == "__main__":
    main(settings.TOKEN)
    