# -*- coding: utf-8 -*-
import env
import discord
from discord.utils import get
from discord.ext import commands

guild = discord.Object(id=env.GUILD_ID)
hexAllowedCharacters = "0123456789ABCDEF"

class abot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.sycned = False
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.sycned:
            await tree.sync(guild=guild)
            self.synced = True
        print("Bot is online")

bot = abot()
tree = discord.app_commands.CommandTree(bot)

@tree.command(name="ping", description="Bot odpowie ci pong", guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="author", description="Bot poda ci najważniejsze informacje o autorze", guild=guild)
async def self(interaction: discord.Interaction):
    await interaction.response.send_message("Autorem bocika jest <@386237687008591895>.\n\nGithub: https://github.com/kasztandor\nFacebook: https://www.facebook.com/kasztandor\nReddit: https://www.reddit.com/user/Kasztandor\nInstagram: https://www.instagram.com/kasztandor_art\nInstagram: https://www.instagram.com/kasztandor_photos", suppress_embeds=True)

async def getRoles(interaction):
    roles = []
    for i in interaction.guild.roles:
        if len(i.name) == 7 and i.name[0] == "#":
            flag = True
            color = i.name.removeprefix("#")
            for j in color:
                if j not in hexAllowedCharacters:
                    flag = False
            if flag:
                roles.append(i)
    return roles

async def removeEmpty(roles):
    for i in roles:
        if len(i.members) == 0:
            await i.delete()

async def roleClener(interaction):
    global hexAllowedCharacters
    await interaction.user.remove_roles(*await getRoles(interaction))

@tree.command(name="clearcolor", description="Usuwa kolor", guild=guild)
async def self(interaction: discord.Interaction):
    await roleClener(interaction)
    await removeEmpty(await getRoles(interaction))
    await interaction.response.send_message("Wyczyszczono kolor.")

@tree.command(name="setcolor", description="Wybierz swój kolor!", guild=guild)
async def self(interaction: discord.Interaction, hex:str):
    global hexAllowedCharacters
    color = hex.removeprefix("#").upper()
    if len(color) == 6:
        flag = True
        for i in color:
            if i not in hexAllowedCharacters:
                flag = False
        if flag:
            colorHex = int(color, 16)
            await roleClener(interaction)
            role = None
            for i in await getRoles(interaction):
                if i.name == "#"+color:
                    role = i
                    break
            if role == None:
                pos = interaction.guild.get_member(bot.user.id).top_role.position
                role = await interaction.guild.create_role(name="#"+color, color=colorHex)
                await role.edit(position=pos)
            await interaction.user.add_roles(role)
            await removeEmpty(await getRoles(interaction))
            await interaction.response.send_message("Ustawiono kolor: `#"+color+"`.")
        else:
            await interaction.response.send_message("Hex składa się z liter A-F oraz liczb 0-9.")
    else:
        await interaction.response.send_message("Hex ma 6 znaków długości.")

@bot.event
async def on_message(message):
    guild = message.guild
    msg = message.content
    msgLowercase = msg.lower()
    msgLowercaseNoPolish = msgLowercase.replace("ą","a").replace("ć","c").replace("ę","e").replace("ł","l").replace("ń","n").replace("ó","o").replace("ś","s").replace("ż","z").replace("ź","z")
    sender = message.author

    if (msg == "!sync" and message.author.id == 386237687008591895):
        await tree.sync()
        await message.channel.send("Zsynchronizowano drzewo!")

    if len(message.mentions) > 0 and message.mentions[0] == bot.user and (msgLowercaseNoPolish.find("przedstaw sie") != -1):
        await message.channel.send("Siema! Jestem sobie botem napisanym przez Kasztandora i tak sobie tutaj działam i robię co do mnie należy. Pozdrawiam wszystkich i życzę udanego dnia!")

bot.run(env.TOKEN)
