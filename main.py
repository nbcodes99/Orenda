import discord, time
import math, random
# import pywhatkit 
import json, datetime
import discord.ui, io
import requests, aiohttp
import asyncio, json, os
import logging
from dotenv import load_dotenv
from covid import Covid
from discord import app_commands
import sqlite3, contextlib
from googletrans import Translator
from discord.ext.commands import cooldown, BucketType, guild_only
from discord.ext import commands, tasks

token = "MTAwMzEyMzY2MjcxNjY3NDA4OA.GP9bOV.iwKhRKFaQ9Gk0Estrz-wpZdrQiLcTU3wq5YFdo"

handler = logging.FileHandler(filename='orenda.log', encoding='utf-8', mode='w')

# def get_prefix(ctx):
#     db = sqlite3.connect('prefixes.db')
#     c = db.cursor()
#     # cursor.execute("""CREATE TABLE prefixes (
#     #     guild_ID INTEGER,
#     #     prefix TEXT
#     # )""")
#     c.execute(f'SELECT prefix FROM prefixes WHERE guild_ID = {ctx.guild.id}')
#     res = c.fetchall()

#     if res:
#         prefix = (res[0])
#     if res:
#         prefix = 'o!'

#     db.commit()
#     c.close()
#     db.close()

#     return prefix

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = commands.when_mentioned_or('o!'), case_sensitive=True, intents=intents)

client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.dnd, activity=discord.Game("Visual Studio Code"))
    print(f"Logged In! {client.user.name}")
    await client.tree.sync()
    print("All tree commands synced!")

# @client.event
# async def on_guild_join(guild):
#     global prefix
#     db = sqlite3.connect('prefixes.db')
#     c = db.cursor()
#     c.execute(f'SELECT * prefix FROM prefixes WHERE guild_ID = {guild.id}')
#     res = c.fetchall()

#     if not res:
#         c.execute(f'INSERT INTO prefixes(guild_ID, prefix) VALUES(?, ?)', {guild.id, 'o!'})

#     if res:
#         c.execute('UPDATE prefixes SET prefix = ? WHERE guild_ID = ?', {'o!', guild.id})

# @client.command(aliases=['changeprefix'])
# async def setprefix(ctx, prefix: str):
#     if len(prefix) > 3:
#         errPrefix = discord.Embed(title="Error", description=f"{ctx.author.mention}, prefix can't be longer that 3 characters!")
#         await ctx.reply(embed=errPrefix)
#     db = sqlite3.connect('prefixes.db')
#     c = db.cursor()
#     c.execute(f'SELECT * prefix FROM prefixes WHERE guild_ID = {ctx.guild.id}')
#     res = c.fetchone()

#     if not res:
#         c.execute("INSERT INTO prefixes(guild_ID, prefix) VALUES(?, ?)", {ctx.guild.id, prefix})
#     if res: 
#         c.execute('UPDATE prefixes SET prefix = ? WHERE guild_id = ?', {prefix, ctx.guild.id})

#     db.commit()
#     c.close()
#     db.close()

#     prefixEmbed = discord.Embed(title="New Prefix", description=f"New prefix is `{prefix}` !!", color=0xbdc8ff)
#     await ctx.send(embed=prefixEmbed)
#     return prefix

@client.event
async def on_message(message):
    ping = f"<@{client.user.id}>"
    words = ['fuck you', 'mf', 'motherfucker', 'bitch', 'blowjob', 'handjob', 'meth', 'dumbass']
    with open('content.txt', 'w') as mes:
        mes.write(message.content)
        mes.close()

    if message.content == ping:
        pingView = discord.ui.View()
        pingItem = discord.ui.Button(style=discord.ButtonStyle.link, label=" ➕ Invite", url="https://discord.com/oauth2/authorize?client_id=1003123662716674088&permissions=0&scope=applications.commands%20bot")
        pingView.add_item(item=pingItem)
        pingEmbed = discord.Embed(title="Need help?", description=f"use the following for help:\n `o!help` or <@!{client.user.id}> `help`\n My prefixes are: `o!` and <@{client.user.id}>", color=0x66e212)
        await message.channel.send(embed=pingEmbed, view=pingView)
    if message.content == 'wow':
        await message.channel.send("Just wow!")

    for word in words:
        if message.content == word:
            await message.channel.purge(limit=1)
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    await member.send('New member!')

@client.command(aliases=['mc', 'mcount'])
async def membercount(ctx):
    memberCount = ctx.guild.member_count
    mcEmbed = discord.Embed(title=f"Member Count", description=memberCount, color=0x855eb5)
    mcEmbed.set_footer(text="Aliases: `mc, mcount`", icon_url=ctx.guild.icon)
    mcEmbed.timestamp = datetime.datetime.now()
    await ctx.send(embed=mcEmbed)

@client.tree.command(name="membercount", description="Shows the current number of members in a server.")
async def membercount(interaction: discord.Interaction):
    memberCount = interaction.guild.member_count
    mcEmbed = discord.Embed(title=f"Member Count", description=memberCount, color=0x855eb5)
    mcEmbed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon)
    mcEmbed.timestamp = datetime.datetime.now()
    await interaction.response.send_message(embed=mcEmbed)

@client.tree.command(name="translate", description="Translate text into any language with Google Translate")
async def translate(interaction: discord.Interaction, lang: str, content: str):
    translator = Translator()
    translation = translator.translate(content, dest=lang)
    tranEmbed = discord.Embed(title="Google Translate", description=f"**{translation.text}**", color=0xcceab8)
    tranEmbed.timestamp = datetime.datetime.now()
    tranEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/826712558890516511/1010376420763115560/image_search_1660962898839.gif")
    tranEmbed.set_footer(text=f"Translated to {lang}", icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=tranEmbed)

@client.command(aliases=['trans'])
async def translate(ctx, lang, *, content):
    translator = Translator()
    translation = translator.translate(content, dest=lang)
    tranEmbed = discord.Embed(title="Orenda Translator", description=f"**{translation.text}**", color=0xcceab8)
    tranEmbed.timestamp = datetime.datetime.now()
    tranEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/826712558890516511/1010376420763115560/image_search_1660962898839.gif")
    tranEmbed.set_footer(text=f"Translated to {lang} | Alias: `trans`", icon_url=ctx.author.avatar.url)
    await ctx.reply(embed=tranEmbed)

@client.tree.command(name='google', description="A dictionary that searches all word.")
@commands.cooldown(6, 60, commands.BucketType.user)
async def google(interaction: discord.Interaction, word: str):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 404:
        await interaction.response.send_message("Word not found!", ephemeral=True)
        return
    else:
        wordx = response.json()
        the_dictionary = wordx[0]
        meanings = the_dictionary['meanings']
        definitions = meanings[0]
        definition = definitions['definitions']
        meaningg = definition[0]
        meaning = meaningg['definition']
        example = meaningg.get('example', ['None'])
        synonymslist = meaningg.get('synonyms', ['None'])

        if isinstance(synonymslist, str):
            synonymslist = [synonymslist]
        synonyms = ', '.join(synonymslist)

        definal = discord.Embed(title=f"Word Searched: `{word}`", color=0x979c9f)
        definal.add_field(name="Definition", value=f"`{meaning}`", inline=False)
        definal.add_field(name="Example", value=f"`{example}`", inline=False)
        definal.add_field(name="Synonyms", value=f"`{synonyms}`", inline=False)

        definal.timestamp = datetime.datetime.now()
        defgif = ["https://cdn.discordapp.com/attachments/939661225602740224/1011241710459822110/image_search_1661169187328.gif",
        "https://cdn.discordapp.com/attachments/939661225602740224/1011241232116232202/image_search_1661169089196.gif"]
        defgifs = random.choice(defgif)
        definal.set_thumbnail(url=defgifs)
        definal.set_footer(text=f'{interaction.user.name}', icon_url=f"{interaction.user.avatar.url}")

        await interaction.response.send_message(embed=definal)

@client.command(name='google')
@commands.cooldown(6, 60, commands.BucketType.user)
async def google(ctx, *, word):
    response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
    if response.status_code == 404:
        await ctx.send("Word not found!")
        return
    else:
        wordx = response.json()
        the_dictionary = wordx[0]
        meanings = the_dictionary['meanings']
        definitions = meanings[0]
        definition = definitions['definitions']
        meaningg = definition[0]
        meaning = meaningg['definition']
        example = meaningg.get('example', ['None'])
        synonymslist = meaningg.get('synonyms', ['None'])

        if isinstance(synonymslist, str):
            synonymslist = [synonymslist]
        synonyms = ', '.join(synonymslist)

        definal = discord.Embed(title=f"Word Searched: `{word}`", color=0x979c9f)
        definal.add_field(name="Definition", value=f"`{meaning}`", inline=False)
        definal.add_field(name="Example", value=f"`{example}`", inline=False)
        definal.add_field(name="Synonyms", value=f"`{synonyms}`", inline=False)

        definal.timestamp = datetime.datetime.now()
        defgif = ["https://cdn.discordapp.com/attachments/939661225602740224/1011241710459822110/image_search_1661169187328.gif",
        "https://cdn.discordapp.com/attachments/939661225602740224/1011241232116232202/image_search_1661169089196.gif"]
        defgifs = random.choice(defgif)
        definal.set_thumbnail(url=defgifs)
        definal.set_footer(text=f'{ctx.author.name}', icon_url=f"{ctx.author.avatar.url}")

        await ctx.send(embed=definal)

@google.error
async def define_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Word to search/define not given.")

@client.command()
async def eval(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    if ctx.author.id == 736972265987637361:
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await ctx.send(f"""```
            {e.__class__.__name__}: {e}

            Finished in {round(client.latency * 1000)}ms```""")
        await ctx.send(f"""```python
        {str_obj.getvalue()}
        Finished in {round(client.latency * 1000)}ms```""")
    else: 
        await ctx.reply("You can't use this command.")

# Catching Errors !!

@client.event
async def on_command_error(ctx, error):
    cool = ["Slow it down bro.", "You're on cooldown.", "Whoa! Whoa!"]
    cools = random.choice(cool)
    recool = ["Try again in", "Retry after", "Re-run after", "Retry in"]
    recools = random.choice(recool)

    if isinstance(error, commands.CommandNotFound):
        print("No command found!")

    elif isinstance(error, commands.CommandOnCooldown):
        cooldownEmbed = discord.Embed(title=cools, description=f"{recools} `{error.retry_after:.2f} secs.`", color=0xee651b)
        await ctx.reply(embed=cooldownEmbed)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to use this command.")
    
    elif isinstance(error, commands.CommandInvokeError):
        print("An error occurred.")

    elif isinstance(error, commands.BadArgument):
        print("Bad argument")

# Mod Commands!

@client.command(aliases=['clear'])
async def purge(ctx, *, number: int=None):
	if ctx.message.author.guild_permissions.manage_messages:
		try:
			if number is None:
				await ctx.reply(f"""Syntax: ```
m!purge [NumberOfMessages]
m!purge 20
Alias: clear```""")
			else:
				deleted = await ctx.message.channel.purge(limit=number+1)
				await ctx.send(f"{len(deleted)} messages were purged! by {ctx.author.mention} {round(client.latency * 1000)}ms")
				time.sleep(3)
				await ctx.message.channel.purge(limit=1)
		except:
			await ctx.reply("I can't purge messages here!")
	else:
		await ctx.reply("You don't have permission to use this command!")

@client.command()
async def kick(ctx, user: discord.Member, *, reason=None):
    kickEmbed = discord.Embed(title="Kick Case", description=f"{user.name} has been Kicked!", color=0xe74c3c)
    kickEmbed.add_field(name="Responsible Moderator", value=ctx.author)
    kickEmbed.add_field(name="Reason", value=f"{reason}")

    if user == ctx.message.author:
       await ctx.reply("You cannot kick yourself.")

    elif user.guild_permissions.kick_members or user.guild_permissions.ban_members:
        await ctx.reply(f"{user.name} is a mod or admin.")

    elif ctx.message.author.guild_permissions.kick_members or ctx.message.author.guild_permissions.ban_members:
        if reason is None:
            await ctx.guild.kick(user=user, reason='Not Given.')
            await ctx.send(embed=kickEmbed)
        else:
            await ctx.guild.kick(user=user, reason=reason)
            await ctx.send(embed=kickEmbed)
    else:
        await ctx.reply("You don't have permission to use this command!")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("""Syntax: ```
.kick [member] [reason]```""")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("This user is not in this server.")

# class Unban(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.value = None

#     @discord.ui.button(label="Unban", style=discord.ButtonStyle.blurple)
#     async def unban(self, button: discord.ui.Button, interaction: discord.Interaction):
#         unbanUser = 
#         await interaction.response.guild.unban(unbanUser)
#         await interaction.response.send_message("{user} successfully unbanned!", ephemeral=True)

@client.command()
async def ban(ctx, user: discord.Member, *, reason=None):
    banEmbed = discord.Embed(title="Ban Case", description=f"{user} has been banned!", color=0xe74c3c)
    banEmbed.set_footer(text=ctx.author.id, icon_url=ctx.author.avatar.url)
    banEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/826712558890516511/1010379855914868876/image_search_1660963234022.gif")
    banEmbed.add_field(name="Reason", value=f"{reason}", inline=False)
    banEmbed.add_field(name="Responsible Moderator", value=ctx.author, inline=False)

    if user.guild_permissions.kick_members or user.guild_permissions.ban_members:
        await ctx.reply(f"{user.name} is a mod or admin.")

    elif ctx.message.author.guild_permissions.ban_members:
        if reason == None:
            await ctx.guild.ban(user=user, reason='Not Given.')
            await ctx.send(embed=banEmbed)
        else:
            await ctx.guild.ban(user=user, reason=reason)
            await ctx.send(embed=banEmbed)

    else:
        await ctx.reply("You don't have permission to use this command!")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("""Syntax: ```
.ban [member] [reason]```""")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("This user is already banned.")

# Unban Command

@client.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    unbanEmbed = discord.Embed(title="Unban Case", description=f"{user.mention} is succesfully unbanned.", color=0x619e91)
    unbanEmbed.add_field(name="Responsible Moderator", value=ctx.author)
    unbanEmbed.set_footer(text=user, icon_url=user.avatar.url)
    unbanEmbed.timestamp = datetime.datetime.now()
    await ctx.reply(embed=unbanEmbed)

@client.tree.command(name="id", description="Get a specific user ID")
async def id(interaction: discord.Interaction, user: discord.Member=None):
    if user == None:
        await interaction.response.send_message(f"Your ID: {interaction.user.id}", ephemeral=True)
    else:   
        await interaction.response.send_message("{} {}".format(f"{user.name}'s ID:", {user.id}), ephemeral=True)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("""Syntax: ```
.unban [ID]```""")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.reply("This user is not banned.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permission to do that.")

# UTILITY COMMANDS !!

# @client.command(aliases=['yt'])
# @commands.cooldown(1, 15, commands.BucketType.user)
# async def youtube(ctx, *, search):
# 	await ctx.reply(pywhatkit.playonyt(search, open_video=False))

# @client.tree.command(name="youtube", description="Finds a video from youtube.")
# @commands.cooldown(1, 15, commands.BucketType.user)
# async def youtube(interaction: discord.Interaction, search: str):
# 	await interaction.response.send_message(pywhatkit.playonyt(search, open_video=False))

# @youtube.error
# async def youtube_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.reply("""Syntax: ```
# o!youtube [search]
# Ex: o!youtube MrBeast
# You can also search a video by writing the video title.```
#         """)

@client.command(aliases=['si', 'sicon', 'servericon', 'svicon'])
async def serverIcon(ctx):
    icon = ctx.guild.icon

    siEmbed = discord.Embed(title=f"{ctx.guild.name}'s icon", url=icon, color=0xd8d5d5)
    siEmbed.set_image(url=icon)
    siEmbed.timestamp = datetime.datetime.now()
    siEmbed.set_footer(text=f"Aliases: si, sicon, svicon", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=siEmbed)

@client.tree.command(name="servericon", description="Display the server icon.")
async def serverIcon(interaction: discord.Interaction):
    icon = interaction.guild.icon
    siEmbed = discord.Embed(title=f"{interaction.guild.name}'s icon", url=icon, color=0xd8d5d5)
    siEmbed.set_image(url=icon)
    siEmbed.timestamp = datetime.datetime.now()
    siEmbed.set_footer(text=f"Aliases: `si, sicon, svicon`", icon_url=interaction.user.avatar.url)
    await interaction.response.send_message(embed=siEmbed)

@client.command()
async def banner(ctx):
    await ctx.send(ctx.guild.banner_url)

@client.command(aliases=['rm'])
async def remind(ctx, time, *, about):
    try:
        try:
            long = int(time)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'w':604800, 'mth': 2678400, 'y': 31536000, 'S':1, 'M':60, 'H':3600, 'D':86400, 'W':604800, 'MTH': 2678400, 'Y': 31536000}
            long = int(time[:-1]) * convertTimeList[time[-1]]
        if long > 31536000:
            await ctx.reply("I can't remind you something over a year.")
            return
        if long <= 0:
            await ctx.reply("Invalid time inserted.")
            return
        if long >= 2678400:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long//2678400} months.")
        elif long >= 604800:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long//604800} weeks.")
        elif long >= 86400:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long//86400} days.")
        elif long >= 3600:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long//3600} hours.")
        elif long >= 60:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long//60} minutes.")
        elif long < 60:
            reminder = await ctx.reply(f"Alright {ctx.author.name}, i'll remind you about `{about}` in {long} seconds.")
        while True:
            try:
                await asyncio.sleep(10)
                long -= 10
                if long <= 0:
                    reEmbed = discord.Embed(title=f"Your reminder ends!", description=f"Hi {ctx.author.name}! {time} ago, you asked me to remind you about [{about}]({reminder.jump_url}).", color=0x1a53ff)
                    reDm = await ctx.author.create_dm()
                    await reDm.send(embed=reEmbed)
                    break
            except:
                break
    except:
        await ctx.reply(f"Retry with a valid time input.")

@remind.error
async def remind_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f""" Syntax: ```
.remind [time][about]
Example:
o!remind 10s test

use `mth` for month not `m`.```
    """)

@client.command(aliases=['ui', 'whois', 'uinfo'])
async def userinfo(ctx, user: discord.Member=None):
    date_format = "%a, %d %b %Y %I:%M %p"
    if user == None:
        user = ctx.author

    userEmbed = discord.Embed(color=0xadefff, timestamp=ctx.message.created_at)
    userView = discord.ui.View()
    userItem = discord.ui.Button(style=discord.ButtonStyle.link, label="Avatar Link", url=user.avatar.url, emoji="🖼️")
    userView.add_item(item=userItem)
    userEmbed.set_author(name=f"{user.name}'s Information", icon_url=user.avatar.url)
    userEmbed.set_thumbnail(url=user.avatar.url),
    userEmbed.set_footer(text=f"Aliases: `ui, whois, uinfo`", icon_url=f"{client.user.avatar.url}")

    userEmbed.add_field(name="ID", value=f"{user.id}", inline=False)
    userEmbed.add_field(name="Name", value=f"{user}", inline=False)
    userEmbed.add_field(name="Registered At", value=f"{user.created_at.strftime(date_format)}", inline=False)
    userEmbed.add_field(name="Joined At", value=f"{user.joined_at.strftime(date_format)}", inline=False)
    # userEmbed.add_field(name="", value="", inline=False)
    userEmbed.add_field(name="Nick", value=user.nick, inline=True)
    # userEmbed.add_field(name="Invoice", value=user.voice_state, inline=False)
    userEmbed.add_field(name="Status", value=user.status, inline=True)
    userEmbed.add_field(name="Game", value=user.activity, inline=False)
    userEmbed.add_field(name="Top Role", value=f"{user.top_role.mention}", inline=False)
    userEmbed.add_field(name="Bot?", value=f"`{user.bot}`", inline=False)

    await ctx.send(embed=userEmbed, view=userView)

@client.command()
@commands.has_permissions(ban_members=True)
async def say(ctx, *, message):
    try:
        await ctx.message.channel.purge(limit=1)
        await ctx.send(message)
    except:
        await ctx.reply("""Syntax: ```
o!say [content]
Ex: o!say This is a test!```
        """)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("""Syntax: ```
o!say [content]
Ex: o!say This is a test!```
        """)

# @client.command(aliases=['role'])
# async def addrole(ctx, role: discord.Role, user: discord.Member):
#     if ctx.message.author.guild_permissions.manage_roles or ctx.message.author.guild_permissions.administrator:
#         adEmbed = discord.Embed(title="Role Added", description=f"Added {role.mention} to {user.mention}.", color=0x1abc9c)

#         adEmbed.timestamp = datetime.datetime.now()
#         adEmbed.set_footer(text="Role Given", icon_url=client.user.avatar.url)
#         await user.add_roles(role)
#         await ctx.send(embed=adEmbed)
#     else:
#         await ctx.reply("You must have the `Manage Roles` permission.")
#     adEmbed = discord.Embed(title="Role Added", description=f"Added {role.mention} to {user.mention}.", color=0x1abc9c)

#     adEmbed.timestamp = datetime.datetime.now()
#     adEmbed.set_footer(text="Role Given", icon_url=client.user.avatar.url)

# @addrole.error
# async def addrole_error(ctx, error):
#     if isinstance(error, commands.RoleNotFound):
#         await ctx.reply(f"Role not found.")
#     elif isinstance(error, commands.CommandInvokeError):
#         await ctx.reply("An error occurred. Try again.")
#     elif isinstance(error, commands.MissingRequiredArgument):
#         await ctx.reply(f"""Syntax```
# m!addrole [roleName] [user/ID]
# Example: m!addrole @admin @brandon#4460```
#         """)


@client.command()
async def covid(ctx, loc):
    covid = Covid()
    cases = covid.get_status_by_country_name(loc)
    covidEmbed = discord.Embed(title=f"Covid stats in {loc}", color=0x80e619)
    covidEmbed.add_field(name="Country", value=f"`{loc}`", inline=False)
    covidEmbed.add_field(name="Active Cases", value=f"`{cases['active']}`", inline=False)
    covidEmbed.add_field(name="Confirmed Cases", value=f"`{cases['confirmed']}`", inline=False)
    covidEmbed.add_field(name="Deaths", value=f"`{cases['deaths']}`")
    covidEmbed.set_footer(text=f"{ctx.author.id}", icon_url=ctx.author.avatar.url)
    covidEmbed.timestamp = datetime.datetime.now()
    await ctx.send(embed=covidEmbed)

@client.tree.command(name="covidinfo", description="Sends the covid stats in country.")
async def covid(interaction: discord.Interaction, loc: str):
    covid = Covid()
    cases = covid.get_status_by_country_name(loc)
    covidEmbed = discord.Embed(title=f"Covid stats in {loc}", color=0x80e619)
    covidEmbed.add_field(name="Country", value=f"`{loc}`", inline=False)
    covidEmbed.add_field(name="Active Cases", value=f"`{cases['active']}`", inline=False)
    covidEmbed.add_field(name="Confirmed Cases", value=f"`{cases['confirmed']}`", inline=False)
    covidEmbed.add_field(name="Deaths", value=f"`{cases['deaths']}`", inline=False)
    covidEmbed.set_footer(text=f"{interaction.user.name}", icon_url=interaction.user.avatar.url)
    covidEmbed.timestamp = datetime.datetime.now()
    await interaction.response.send_message(embed=covidEmbed)


@client.command(aliases=['makerole', 'crole', 'mrole'])
async def create_role(ctx, *, name=None):
    guild = ctx.guild
    if ctx.message.author.guild_permissions.manage_roles:
        if guild.has_role(name=name):
            await ctx.send(f"Role with a name `{name}` already exist.")
        else:
            await guild.create_role(name=name)
            await ctx.send(f'Role `{name}` has been created!')
    elif ctx.message.author.guild_permissions.administrator:
       if guild.has_role(name=name):
            await ctx.send(f"Role with a name `{name}` already exist.")
       else:
            await guild.create_role(name=name)
            await ctx.send(f'Role `{name}` has been created!')
    elif name == None:
        await guild.create_role(name="None")
        await ctx.send(f'Role named `None` has been created!')
    else:
        await ctx.send("You must have the `manage roles` permission.")

@client.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def setnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

@client.tree.command(name="setnick", description="Sets a new nickname for member.")
@commands.has_permissions(manage_nicknames=True)
async def setnick(interaction: discord.Interaction, member: discord.Member, nick: str):
    await member.edit(nick=nick)
    await interaction.response.send_message(f'Nickname was changed for {member.mention} ', ephemeral=True)

@setnick.error
async def nick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You don't have permissions to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("""Syntax: ```
o!nick [user] [nickname]
Ex: o!nick @Brandon Jupiter```
        """)

@client.command()
async def nickme(ctx):
    nicknames = ['Boo', 'Chipmunk', 'Splendid', 'Error 404: Name Not Found', 'Mouse', 'Ward', ' Dr. Richard', 'Dolly', 'Bug', 'Bee', 'MunchKin', 'Senorita', 'Chica', 'Amigo', 'Nate', 'Rafe', 'Buck', 'Bud', 'Doc', 'Dude', 'Junior', 'ButterCup', 'Nugget', 'Oldie', 'Elegance', 'HoOmAn', 'Teacup', 'Smarty', 'Dottie', 'Ace', 'Rambo', 'Smiley', 'Punk', 'Rapunzel', 'Disaster', 'Giggles', 'Teeny', 'Squirt', 'Boomer', 'Ms. Congeniality', 'Wiggle', 'Chubby Cheeks', 'BooBoo', 'Bubbles', 'Bob', 'Sung-a-Bug', 'Tadpole', 'Panda', 'Penguin', 'Pup', 'Cupcake', 'Jelly Bean', 'Rockstar', 'Heat', 'Cold', 'Sparky', 'Dino', 'Dynamo', 'Sully', 'Double Trouble', 'Wild', 'Sundae', 'Cas', 'Zusa', 'Goku', 'Emerald', 'Fisk', 'Haven', 'Jasper', 'Jovie', 'Jupiter', 'Sublime', 'Atom', 'Electron', 'JakeFromStateFarm', 'Glizz', 'Heather', 'Hunter', 'Leo', 'Neptune', 'Mars', 'Fred', 'Flora', 'Shearer', 'Kane', 'Townsend', 'Predator', 'Topaz', 'Grizzi', 'Venus', 'Earth', 'Sunny']
    nicks = random.choice(nicknames)
    await ctx.author.edit(nick=nicks)

@client.command()
async def coinflip(ctx):
    flipOpt = ['heads', 'tails']
    flipOpts = random.choice(flipOpt)
    if flipOpts == 'tails':
        cointailsEmbed = discord.Embed(title="-Coin Flip-", description=f"Coin alight on **TAILS**", color=0xcd1818)
        cointailsEmbed.set_footer(text=f"Flipped by: {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=cointailsEmbed)
    else:
        coinheadsEmbed = discord.Embed(title="-Coin Flip-", description=f"Coin alight on **HEADS**", color=0x32fb35)
        coinheadsEmbed.set_footer(text=f"Flipped by: {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=coinheadsEmbed)

@client.tree.command(name="coinflip", description="Flips a coin for heads or tails.")
async def coinflip(interaction: discord.Interaction):
    flipOpt = ['heads', 'tails']
    flipOpts = random.choice(flipOpt)
    if flipOpts == 'tails':
        cointailsEmbed = discord.Embed(title="-Coin Flip-", description=f"Coin alight on **TAILS**", color=0xcd1818)
        cointailsEmbed.set_footer(text=f"Flipped by: {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=cointailsEmbed)
    else:
        coinheadsEmbed = discord.Embed(title="-Coin Flip-", description=f"Coin alight on **HEADS**", color=0x32fb35)
        coinheadsEmbed.set_footer(text=f"Flipped by: {interaction.user.name}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=coinheadsEmbed)

class Roll(discord.ui.View):
    def __init__(self, timeout=15):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Roll Again!", style=discord.ButtonStyle.blurple, emoji="🎲")
    async def roll_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        rollEmbed = discord.Embed(title="-Rolling Dice-", description=f"I rolled {random.randint(1, 390)}!", color=0xb87ee7)
        await interaction.response.edit_message(embed=rollEmbed)

    @discord.ui.button(label="End", style=discord.ButtonStyle.gray)
    async def end_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)

    async def on_timeout(self, interaction: discord.Interaction) -> None:
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)

@client.command()
async def roll(ctx):
    rollEmbed = discord.Embed(title="-Rolling Dice-", description=f"I rolled {random.randint(1, 100)}!", color=0xb87ee7)
    rollView = Roll()
    await ctx.send(embed=rollEmbed, view=rollView)

@client.tree.command(name="roll", description="Rolls a random number..")
async def roll(interaction: discord.Interaction):
    rollEmbed = discord.Embed(title="-Rolling Dice-", description=f"I rolled {random.randint(1, 390)}!", color=0xb87ee7)
    rollView = Roll()
    await interaction.response.send_message(embed=rollEmbed, view=rollView)

# class MyView(discord.ui.View):
#     def __init__(self, timeout=5):
#         super().__init__(timeout=timeout)

#     async def on_timeout(self) -> None:
#         # Step 2
#         for item in self.children:
#             item.disabled = True

#         # Step 3
#         await self.message.edit(view=self)

#     @discord.ui.button(label='Example')
#     async def example_button(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.send_message('Hello!', ephemeral=True)

# @client.command()
# async def tout(ctx):
#     """An example to showcase disabling buttons on timing out"""
#     view = MyView()
#     # Step 1
#     view.message = await ctx.send('Press me!', view=view)

# class avatarView(discord.ui.View):
#     def __init__(self):
#         super().__init__()

#         @discord.ui.button(label="🖼️ Avatar Link", style=discord.ButtonStyle.gray, url=)

@client.command()
async def avatar(ctx, member: discord.Member):
    avatarViewOne = discord.ui.View()
    avatarItem = discord.ui.Button(style=discord.ButtonStyle.link, label=" 🖼️ Avatar Link", url=ctx.member.avatar.url)
    avatarViewOne.add_item(item=avatarItem)
    avatarEmbedOne = discord.Embed(title=f"{ctx.member.name}\'s avatar", color=0xd8d5d5, timestamp=datetime.datetime.now())
    avatarEmbedOne.set_image(url=ctx.member.avatar.url)
    # avatarEmbedOne.timestamp = datetime.datetime.now()
    avatarEmbedOne.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar.url)
    print(ctx.member.avatar.url)
    await ctx.reply(embed=avatarEmbedOne, view=avatarViewOne)

@client.tree.command(name="avatar", description="Display a users avatar..")
async def avatar(interaction: discord.Interaction, member : discord.Member):
    avatarViewOne = discord.ui.View()
    avatarItem = discord.ui.Button(style=discord.ButtonStyle.link, label=" 🖼️ Avatar Link", url=interaction.member.avatar)
    avatarViewOne.add_item(item=avatarItem)
    avatarEmbedOne = discord.Embed(title=f"{interaction.member.name}\'s avatar", color=0xd8d5d5, timestamp=datetime.datetime.now())
    avatarEmbedOne.set_image(url=interaction.member.avatar.url)
    # avatarEmbedOne.timestamp = datetime.datetime.now()
    avatarEmbedOne.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar.url)
    await interaction.response.send_message(embed=avatarEmbedOne, view=avatarViewOne)

@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        avaUrl = ctx.author.avatar.url
        avatarView = discord.ui.View()
        avatarItem = discord.ui.Button(style=discord.ButtonStyle.link, label=" 🖼️ Avatar Link", url=ctx.author.avatar.url)
        avatarView.add_item(item=avatarItem)
        avatarEmbed = discord.Embed(title=f"{ctx.author.name}\'s avatar", color=0xd8d5d5, timestamp=datetime.datetime.now())
        avatarEmbed.set_image(url=avaUrl)
        # avatarEmbed.timestamp = datetime.datetime.now()
        avatarEmbed.set_footer(text=f"{client.user.name}", icon_url=client.user.avatar.url)
        await ctx.reply(embed=avatarEmbed, view=avatarView)

@client.command(aliases=['pong'])
@commands.cooldown(3, 10, commands.BucketType.user)
async def ping(ctx):
	await ctx.reply(f"Pong! \n Latency: {round(client.latency * 1000)}ms")

@client.tree.command(name="ping", description="Ping! pong! slash command and the latency of the bot.")
@commands.cooldown(3, 10, commands.BucketType.user)
async def ping(interaction: discord.Interaction):
	await interaction.response.send_message(f"Pong! \n Latency: {round(client.latency * 1000)}ms", ephemeral=True)

@client.tree.command(name='invite', description="Sends the bot invite link.")
@commands.cooldown(1, 10, commands.BucketType.user)
async def invite(interaction: discord.Interaction):
    inviteGifs = ["https://cdn.discordapp.com/attachments/826712558890516511/1010379856338505748/image_search_1660963553472.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379855575142400/image_search_1660963640794.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379855306690590/image_search_1660963646463.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379854723694643/image_search_1660963687301.gif"]

    inviteGifsChoice = random.choice(inviteGifs)
    inviteView = discord.ui.View()
    inviteItem = discord.ui.Button(style=discord.ButtonStyle.link, label="Invite", url="https://discord.com/oauth2/authorize?client_id=1003123662716674088&permissions=0&scope=applications.commands%20bot", emoji="🔗")

    inviteView.add_item(item=inviteItem)
    inviteEmbed = discord.Embed(title="Bot Invite", description="Invite [orenda](https://discord.com/oauth2/authorize?client_id=1003123662716674088&permissions=0&scope=applications.commands%20bot) using the button or link!", color=0x4585ed)
    # inviteEmbed.timestamp = datetime.datetime.now()
    # inviteEmbed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)
    inviteEmbed.set_thumbnail(url=inviteGifsChoice)
    await interaction.response.send_message(embed=inviteEmbed, view=inviteView)

@client.command(name='invite')
@commands.cooldown(2, 10, commands.BucketType.user)
async def invite(ctx):
    inviteGifs = ["https://cdn.discordapp.com/attachments/826712558890516511/1010379856338505748/image_search_1660963553472.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379855575142400/image_search_1660963640794.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379855306690590/image_search_1660963646463.gif",
    "https://cdn.discordapp.com/attachments/826712558890516511/1010379854723694643/image_search_1660963687301.gif"]

    inviteGifsChoice = random.choice(inviteGifs)
    inviteView = discord.ui.View()
    inviteItem = discord.ui.Button(style=discord.ButtonStyle.link, label="Invite", url="https://discord.com/oauth2/authorize?client_id=1003123662716674088&permissions=0&scope=applications.commands%20bot", emoji="🔗")

    inviteView.add_item(item=inviteItem)
    inviteEmbed = discord.Embed(title="Bot Invite", description="Invite [orenda](https://discord.com/oauth2/authorize?client_id=1003123662716674088&permissions=0&scope=applications.commands%20bot) using the button or link!", color=0x4585ed)
    # inviteEmbed.timestamp = datetime.datetime.now()
    # inviteEmbed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
    inviteEmbed.set_thumbnail(url=inviteGifsChoice)
    await ctx.send(embed=inviteEmbed, view=inviteView)

@client.tree.command(name="servers", description="Shows how many servers the bot's in. (owner only)")
async def servers(interaction: discord.Interaction):
    servers = discord.Embed(title="Active Servers", description=f"`{str(len(client.guilds))}` servers.", color=0x4f4f4f)
    if interaction.user.id == 736972265987637361:
        await interaction.response.send_message(embed=servers, ephemeral=True)
    else:
        await interaction.response.send_message("You can't use this command. (owner only)", ephemeral=True)

@client.command()
async def dm(ctx, *, message):
    dms = await ctx.author.create_dm()
    if ctx.message.author.id == 736972265987637361:
        try:
            await dms.send(message)
        except:
            await ctx.reply("Your `DM's` is closed.")
    else:
        await ctx.reply("You can't use this command.")

@client.command()
async def timer(ctx, timeInput, *, name):
    try:
        try:
            time = int(timeInput)
        except:
            convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
            time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
        if time > 86400:
            await ctx.send("I can't do timers over a day long.")
            return
        if time <= 0:
            await ctx.send("Timers don't go into negatives.")
            return
        if time >= 3600:
            hoursEmbed = discord.Embed(title=f"{name}", description=f"{time//3600} hours {time%3600//60} minutes {time%60} seconds", color=0x1a53ff)
            await ctx.message.channel.purge(limit=1)
            message = await ctx.send(embed=hoursEmbed)
            await message.add_reaction("⏱")
        elif time >= 60:
            minsecEmbed = discord.Embed(title=f"{name}", description=f"{time//60} minutes {time%60} seconds", color=0x1a53ff)
            await ctx.message.channel.purge(limit=1)
            message = await ctx.send(embed=minsecEmbed)
            await message.add_reaction("⏱")
        elif time < 60:
            secEmbed = discord.Embed(title=f"{name}", description=f"{time} seconds", color=0x1a53ff)
            await ctx.message.channel.purge(limit=1)
            message = await ctx.send(embed=secEmbed)
            await message.add_reaction("⏱")
        while True:
            try:
                await asyncio.sleep(1)
                time -= 1
                if time >= 3600:
                    hourEmbed = discord.Embed(title=f"{name}", description=f"{time//3600} hours {time %3600//60} minutes {time%60} seconds", color=0x1a53ff)
                    await message.edit(embed=hourEmbed)
                elif time >= 60:
                    minEmbed = discord.Embed(title=f"{name}", description=f"{time//60} minutes {time%60} seconds", color=0x1a53ff)
                    await message.edit(embed=minEmbed)
                elif time < 60:
                    secsEmbed = discord.Embed(title=f"{name}", description=f"{time} seconds", color=0x1a53ff)
                    await message.edit(embed=secsEmbed)
                if time <= 0:
                    enEmbed = discord.Embed(title=f"{name}", description=f"Ended!", color=0x1a53ff)
                    ended = await message.edit(embed=enEmbed)
                    await ctx.send(f"{ctx.author.mention}, your timer has ended.\n {ended.jump_url}")
                    break
            except:
                break
    except:
        await ctx.send(f"Retry with a valid time input.")
@timer.error
async def timer_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"""```
.timer 5m [name]
Example:
.timer 5m Test```""")

@client.command()
async def rps(ctx, message=None):
    choices = ['rock', 'paper', 'scissors']
    answer = message.lower()
    compAns = random.choice(choices)
    tie = ["Oh, wacky. We just tied. I call a rematch!!", "Oh well, we tied.", "Well, that was weird. It was a tie!"]
    ties = random.choice(tie)

    if message == None:
         await ctx.reply(f"""```
You have to input choice.
Syntax: .rps rock
Syntax: .rps paper
Syntax: .rps scissors```""")

    elif answer not in choices:
        await ctx.reply("Retry with a valid choice.")
    else:
        if compAns == answer:
            tieEmbed = discord.Embed(title=f"{ties}", url="https://brandon31.github.io/Rock-Paper-Scissors/", description=f"", color=0xc28024)
            tieEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
            tieEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
            tieEmbed.timestamp = datetime.datetime.now()
            await ctx.reply(embed=tieEmbed)
        if compAns == 'rock':
            if answer == 'paper':
                rpEmbed = discord.Embed(title="YOU WON!", url="https://brandon31.github.io/Rock-Paper-Scissors/", description=f"Aw man, you actually managed to beat me, i call a rematch.", color=0x2cdd2f)
                rpEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                rpEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                rpEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=rpEmbed)
                
        if compAns == 'paper':
            if answer == 'rock':
                prEmbed = discord.Embed(title="Hahaha.. You lose!", url="https://brandon31.github.io/Rock-Paper-Scissors/",, description=f"Nice try, but I won that time!!", color=0xd92417)
                prEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                prEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                prEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=prEmbed)
                
        if compAns == 'scissors':
            if answer == 'rock':
                srEmbed = discord.Embed(title="YOU WON!", url="https://brandon31.github.io/Rock-Paper-Scissors/",  description=f"The pen beats the sword? More like the paper beats the rock!!", color=0x2cdd2f)
                srEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                srEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                prEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=srEmbed)
            
        if compAns == 'rock':
            if answer == 'scissors':
                rsEmbed = discord.Embed(title="Hahaha I WON!", url="https://brandon31.github.io/Rock-Paper-Scissors/", description=f"HAHA!! I JUST CRUSHED YOU!! I ROCK!!", color=0xd92417)
                rsEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                rsEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                rsEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=rsEmbed)

        if compAns == 'paper':
            if answer == 'scissors':
                psEmbed = discord.Embed(title="You won!", url="https://brandon31.github.io/Rock-Paper-Scissors/",  description=f"Damn it! You won. It won't happen again!", color=0x2cdd2f)
                psEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                psEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                psEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=psEmbed)
                
        if compAns == 'scissors':
            if answer == 'paper':
                spEmbed = discord.Embed(title="You lose!", url="https://brandon31.github.io/Rock-Paper-Scissors/", description=f"Yay! I won! Try your luck again.", color=0xd92417)
                spEmbed.add_field(name="Choices", value=f"**Your choice**: {answer}\n**My choice**: {compAns}")
                spEmbed.set_footer(text="Rock | Paper | Scissors", icon_url=ctx.author.avatar.url)
                spEmbed.timestamp = datetime.datetime.now()
                await ctx.reply(embed=spEmbed)

class Guess(discord.ui.View):
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Lower", style=discord.ButtonStyle.blurple)
    async def lower_callback(interaction: discord.Interaction, button: discord.ui.Button):
        secret_number = random.randint(0, 100)
        hint_number = random.randint(0, 100)

        if hint_number > secret_number:
            successGuessEmbed = discord.Embed(title="You got it!!", description="...", color=0x3dff24)
            successGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            successGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            successGuessEmbed.set_footer(text="Winner Winner")
            await interaction.response.edit_message(embed=successGuessEmbed)
            await interaction.response.send_message("You got it!", ephemeral=True)
        else:
            failGuessEmbed = discord.Embed(title="You lost!", description="...", color=0xff2424)
            failGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            failGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            failGuessEmbed.set_footer(text="Loser Loser!")
            await interaction.response.edit_message(embed=failGuessEmbed)
            await interaction.response.send_message("You failed!", ephemeral=True)

    @discord.ui.button(label="JACKPOT!", style=discord.ButtonStyle.blurple)
    async def jackpot_callback(interaction: discord.Interaction, button: discord.ui.Button):
        secret_number = random.randint(0, 100)
        hint_number = random.randint(0, 100)
        
        if hint_number == secret_number:
            successGuessEmbed = discord.Embed(title="You got it!!", description="...", color=0x3dff24)
            successGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            successGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            successGuessEmbed.set_footer(text="Winner Winner")
            await interaction.response.edit_message(embed=successGuessEmbed)

        else:
            failGuessEmbed = discord.Embed(title="You lost!", description="...", color=0xff2424)
            failGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            failGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            failGuessEmbed.set_footer(text="Loser Loser!")
            await interaction.response.edit_message(embed=failGuessEmbed)

    @discord.ui.button(label="Higher", style=discord.ButtonStyle.blurple)
    async def higher_callback(interaction: discord.Interaction, button: discord.ui.Button):
        secret_number = random.randint(0, 100)
        hint_number = random.randint(0, 100)

        if hint_number < secret_number:
            successGuessEmbed = discord.Embed(title="You got it!!", description="...", color=0x3dff24)
            successGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            successGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            successGuessEmbed.set_footer(text="Winner Winner")
            await interaction.response.edit_message(embed=successGuessEmbed)
            await interaction.response.send_message("You got it!", ephemeral=True)
        else:
            failGuessEmbed = discord.Embed(title="You lost!", description="...", color=0xff2424)
            failGuessEmbed.set_author(name=f"{interaction.user.name}\'s high-low", icon_url=interaction.user.avatar.url)
            failGuessEmbed.add_field(name="", value=f"Your hint was {hint_number}. The hidden number was {secret_number}!", inline=False)
            failGuessEmbed.set_footer(text="Loser Loser!")
            await interaction.response.edit_message(embed=failGuessEmbed)
            await interaction.response.send_message("You failed!", ephemeral=True)

@client.command()
async def guess(ctx):
    guessView = Guess()
    hint_number = random.randint(0, 100)
    indexGuessEmbed = discord.Embed(title="", description="The secret number is between 1-100", color=0xb5b0b0)
    indexGuessEmbed.set_author(name=f"{ctx.author.name}\'s high-low", icon_url=ctx.author.avatar.url)
    indexGuessEmbed.add_field(name=f"Your hint is {hint_number}", value=f"Is the number *higher* or *lower*? ", inline=False)
    indexGuessEmbed.set_footer(text="Jackpot is if the number is the same.")
    await ctx.send(embed=indexGuessEmbed, view=guessView)
    # indexGuessEmbed.timestamp = datetime.datetime.now()

    # colors = ['0x49926c', '0x19e67c', '0x80e619', '0xf0f8e8', '0xebb624', '0x6924eb', '0x484252', '0x86848b', '0xe61961', '0xff0000', '0xb5b0b0', '0x360c0c']
    # gnumber = random.randint(0, 100)
    # guessEmbed = discord.Embed(title="Guess The Number", description="Guess a number (1-100)", color=0xb5b0b0)
    # guessEmbed.timestamp = datetime.datetime.now()
    # await ctx.reply(embed=guessEmbed)
    # while True:
    #     try:
    #         response = await client.wait_for('message', timeout=30)
    #         guess = response.content
    #         if guess > gnumber: 
    #             await ctx.send(f"Your number({guess}) is too high. Try again.")
    #         elif guess < gnumber:
    #             await ctx.send(f"Your number({guess}) is too low. Try again.")
    #         else:
    #             corEmbed = discord.Embed(title="You got it!", description=f"`{gnumber}` is correct!", color=0x17e81a)
    #             corEmbed.timestamp = datetime.datetime.now()
    #             await ctx.reply(embed=corEmbed)
    #             break
    #     except asyncio.TimeoutError:
    #         await ctx.reply("You didn't respond on time.")
    #         break

@client.tree.command(name="cat", description="Sends a random cat image.")
async def cat(interaction: discord.Interaction):
    response = requests.get('https://aws.random.cat/meow')
    data = response.json()
    catEmbed = discord.Embed(
        color=0xebb624
        )
    catEmbed.set_image(url=data['file'])      
    catEmbed.set_footer(text=interaction.user.name, icon_url=interaction.user.avatar.url)      
    catEmbed.timestamp = datetime.datetime.now()
    await interaction.response.send_message(embed=catEmbed)

@client.command()
async def cat(ctx: commands.Context):
    async with ctx.session.get('https://api.thecatapi.com/v1/images/search') as resp:
        if resp.status != 200:
            return await ctx.send('No cat found :(')
        js = await resp.json()
        await ctx.send(embed=discord.Embed(title='Random Cat').set_image(url=js[0]['url']))

@client.tree.command(name="dog", description="Sends a random dog image along with a fact in the footer.")
async def dog(interaction: discord.Interaction):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()

   dogEmbed = discord.Embed(color=0x19e67c)
   dogEmbed.set_image(url=dogjson['link'])
   dogEmbed.set_footer(text=factjson['fact'])
   await interaction.response.send_message(embed=dogEmbed)

@client.command()
async def dog(ctx: commands.Context):
        async with ctx.session.get('https://random.dog/woof') as resp:
            if resp.status != 200:
                return await ctx.send('No dog found :(')

            filename = await resp.text()
            url = f'https://random.dog/{filename}'
            filesize = ctx.guild.filesize_limit if ctx.guild else 8388608
            if filename.endswith(('.mp4', '.webm')):
                async with ctx.typing():
                    async with ctx.session.get(url) as other:
                        if other.status != 200:
                            return await ctx.send('Could not download dog video :(')

                        if int(other.headers['Content-Length']) >= filesize:
                            return await ctx.send(f'Video was too big to upload... See it here: {url} instead.')

                        fp = io.BytesIO(await other.read())
                        await ctx.send(file=discord.File(fp, filename=filename))
            else:
                await ctx.send(embed=discord.Embed(title='Random Dog').set_image(url=url))

@client.tree.command(name="meme", description="Sends a random meme.")
async def meme(interaction: discord.Interaction):
    likes = random.randint(212, 9032)
    comments = random.randint(63, 286)
    memeEmbed = discord.Embed(color=0xe61961)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            memeEmbed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            memeEmbed.set_footer(text=f"👍{likes} |  💬{comments}")
            await interaction.response.send_message(embed=memeEmbed)

@client.command(name="meme")
async def meme(ctx):
    likes = random.randint(212, 9032)
    comments = random.randint(63, 286)
    memeEmbed = discord.Embed(color=0xe61961)

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            memeEmbed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            memeEmbed.set_footer(text=f"👍{likes} |  💬{comments}")
            await ctx.send(embed=memeEmbed)

@client.tree.command(name='bless', description="Bless someone!")
async def bless(interaction: discord.Interaction, user: discord.Member=None):
    blessing = random.uniform(0.02, 2.10)
    blessings = round(blessing, 2)
    if user ==  None:
        await interaction.response.send_message("Next time. Mention someone you want to bless.")
    elif user == interaction.user:
        await interaction.response.send_message("You cannot bless yourself.")
    else:
        blessEmbed = discord.Embed(title="", description=f"You have blessed {user.mention} . . .\n {user} obtained {blessings} ❄️", color=0x47e6db)
        blessEmbed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)
        blessEmbed.set_footer(text="Just to be is a blessing...")
        blessEmbed.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=blessEmbed)

@client.command()
async def server_info(ctx):
    d_format = "%a, %d %b %Y %I:%M %p"

    serverInfoEmbed = discord.Embed(title="Server Information", color=0xcfa8ff)
    serverInfoEmbed.add_field(name="Server Name", value=f"`{ctx.guild.name}`", inline=False)
    serverInfoEmbed.add_field(name="Server ID", value=f"`{ctx.guild.id}`", inline=False)
    serverInfoEmbed.add_field(name="Text Channels", value=f"`{len(ctx.guild.text_channels)}`", inline=False)
    serverInfoEmbed.add_field(name="Voice Channels", value=f"`{len(ctx.guild.text_channels)}`", inline=False)
    # serverInfoEmbed.add_field(name="Categories", value=f"`{len(ctx.message.guild.categories)}`", inline=False)
    serverInfoEmbed.add_field(name="Roles", value=f"`{ctx.message.guild.roles}`", inline=False)
    serverInfoEmbed.add_field(name="Created At", value=f"`{ctx.guild.created_at.strftime(d_format)}`", inline=False)
    serverInfoEmbed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    serverInfoEmbed.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar.url)
    await ctx.send(embed=serverInfoEmbed)

# class Intro(discord.ui.Modal, title="Introducton"):
#     name = discord.ui.TextInput(label="Your Name")
#     age = discord.ui.TextInput(label="Your age")
#     hob = discord.ui.TextInput(label="Your Hobby", style=discord.TextStyle.paragraph)
#     async def on_submit(self, interaction: discord.Interaction):
#         global name
#         await interaction.response.send_message(f"Thanks for the info {name}", ephemeral=True)

class Help(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Main", emoji="👋", value="1", description="Main Help Page"),
            discord.SelectOption(label="Moderation", emoji="🛠️", value="2", description="Moderation commands"),
            discord.SelectOption(label="Utility", emoji="💡", value="3", description="Utility commands"),
            discord.SelectOption(label="Fun", emoji="🔮", value="4", description="Fun commands"),
            discord.SelectOption(label="Data Utils", emoji="📑", value="5", description="Data utils commands"),
            discord.SelectOption(label="Config", emoji="⚙️", value="6", description="Config commands"),
            discord.SelectOption(label="Other", emoji="➕", value="7", description="Other")
        ]

        super().__init__(placeholder="Select a category..", max_values=1, min_values=1, options=options)
    async def callback(self, interaction: discord.Interaction):

        if self.values[0] == "1":
            helpEmbed = discord.Embed(title="Bot Help", description=f"Hello {interaction.user.mention}! Welcome to the help page.\n Use the dropdown menu below to select a category for help.", color=0xc8ff75)
            helpEmbed.add_field(name="About me", value=">>> I am a **general-purpose bot** that is made to enhance your server with `moderation` and `auto bad word blocker`! On the other hand, I have other commands you can use or mess around with. \n You can get further information on my commands by using the dropdown below.", inline=False)
            await interaction.response.edit_message(embed=helpEmbed)

        if self.values[0] == "2":
            modHelpEmbed = discord.Embed(title="Moderation Commands", description="", color=0xe40c0c)
            modHelpEmbed.add_field(name="Kick", value=">>> Kicks a user from a server\n Syntax: `o!kick [member][reason]`", inline=False)
            modHelpEmbed.add_field(name="Ban", value=">>> Bans a user from a server\n Syntax: `o!ban [member][reason]`", inline=False)
            modHelpEmbed.add_field(name="Unban", value=">>> Unbans a user from a server\n Syntax: `o!unban [memberID]`", inline=False)
            modHelpEmbed.add_field(name="Purge", value=">>> Clear messages\n Syntax: `o!purge [No.Ofmessages]`", inline=False)
            modHelpEmbed.add_field(name="Nickname", value=">>> Set a members nickname\n Syntax: `o!setnick [member] [nickname]`", inline=False)
            modHelpEmbed.add_field(name="ID", value=">>> Check member's ID\n Syntax: `o!id [user]` (Available in slash commands).", inline=False)
            modHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            modHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786457679155312/image_search_1661293367611.jpg")
            modHelpEmbed.timestamp = datetime.datetime.now()
            await interaction.response.edit_message(embed=modHelpEmbed)

        if self.values[0] == "3":
            utilHelpEmbed = discord.Embed(title="Utility Commands", description="", color=0xffd1d1)
            utilHelpEmbed.add_field(name="Ping", value=">>> A basic ping pong command with latency\n Syntax: `o!ping or o!pong` (Available in slash commands).", inline=False)
            utilHelpEmbed.add_field(name="Bless", value=">>> Bless someone..\n Syntax: `o!bless [member]` (Available in slash commands).", inline=False)
            utilHelpEmbed.add_field(name="Roll", value=">>> Rolls a random number.\n Syntax: `o!roll` (Available in slash commands).", inline=False)
            utilHelpEmbed.add_field(name="Dictionary", value=">>> The dictionary command that searches a word on google\n Syntax: `o!google [word]` (Available in slash commands).", inline=False)
            utilHelpEmbed.add_field(name="Reminder", value=">>> A reminder command that reminds you about something\n Syntax: `o!remind [time] [about]`", inline=False)
            utilHelpEmbed.add_field(name="Timer", value=">>> A timer command\n Syntax: `o!timer [time] [timerName]`", inline=False)
            # utilHelpEmbed.add_field(name="Youtube", value=">>> Gets a video from youtube \n Syntax: `o!youtube [video]` (Available in slash commands)", inline=False)
            utilHelpEmbed.timestamp = datetime.datetime.now()
            utilHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            utilHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786454332096592/image_search_1661299026218.jpg")
            await interaction.response.edit_message(embed=utilHelpEmbed)
            
        if self.values[0] == "4":
            funHelpEmbed = discord.Embed(title="Fun Commands", description="", color=0xfff79e)
            funHelpEmbed.add_field(name="Cat", value=">>> Sends a random cat image\n Syntax: `o!cat` (Available in slash commands)", inline=False)
            funHelpEmbed.add_field(name="Dog", value=">>> Sends a random dog image along with a dog fact in the footer\n Syntax: `o!dog` (Available in slash commands)", inline=False)
            funHelpEmbed.add_field(name="Coinflip", value=">>> Flips a coin for either `heads` or `tails`\n Syntax: `o!coinflip` (Available in slash commands)", inline=False)
            funHelpEmbed.add_field(name="Meme", value=">>> Sends a random meme\n Syntax: `o!meme` (Available in slash commands)", inline=False)
            funHelpEmbed.add_field(name="Rock Paper Scissors", value=">>> Play rock paper scissors with the bot\n Syntax: `o!rps [choice]`", inline=False)
            funHelpEmbed.add_field(name="Scramble", value=">>> Play scamble with the bot\n Syntax: `o!scramble`", inline=False)
            funHelpEmbed.add_field(name="Guess", value=">>> Guess a random number between 0-100\n Syntax: `o!guess`", inline=False)
            funHelpEmbed.add_field(name="Tic Tac Toe", value=">>> Play tic tac toe! (can't play with another user and neither with cpu).\n Syntax: `o!ttt`", inline=False)
            funHelpEmbed.timestamp = datetime.datetime.now()
            funHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786454105591878/image_search_1661299048630.jpg")
            funHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            await interaction.response.edit_message(embed=funHelpEmbed)

        if self.values[0] == "5":
            dataHelpEmbed = discord.Embed(title="Data Utils Commands", color=0xffd599)
            dataHelpEmbed.add_field(name="User Infomation", value=">>> Displays a full info on a member\n Syntax: `o!userinfo` [Alias: `whois, ui, info`]", inline=False)
            dataHelpEmbed.add_field(name="Avatar", value=">>> Show a member's avatar with link\n Syntax: `o!avatar [member]`", inline=False)
            dataHelpEmbed.add_field(name="Covid", value=">>> Display full info of covid in a country\n Syntax: `o!covid [country]` (Available in slash commands).", inline=False)
            dataHelpEmbed.add_field(name="Server Information", value=">>> Displays full information on a server\n Syntax: `o!serverinfo` [Alias: `svinfo`]", inline=False)
            dataHelpEmbed.add_field(name="Server Icon", value=">>> Displays the server icon\n Syntax: `o!servericon` [Alias: `svicon, sicon`]", inline=False)
            dataHelpEmbed.add_field(name="Member Count", value=">>> Shows the current number of members in a server (mods only).\n Syntax: `o!membercount` [Alias: `mcount, mc`]\n (Available in slash commands)", inline=False)
            dataHelpEmbed.timestamp = datetime.datetime.now()
            dataHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786455032545351/image_search_1661293526563.jpg")
            dataHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            await interaction.response.edit_message(embed=dataHelpEmbed)

        if self.values[0] == "6":
            configHelpEmbed = discord.Embed(title="Configuration Help", color=0xb8b8b8)
            configHelpEmbed.add_field(name="Prefix", value=">>> To set a new prefix for the bot, use the following command:\n `o!setprefix [newprefix]`", inline=False)
            configHelpEmbed.timestamp = datetime.datetime.now()
            configHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786454810238986/image_search_1661298865576.jpg")
            configHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            await interaction.response.edit_message(embed=configHelpEmbed)

        if self.values[0] == "7":
            otherHelpEmbed = discord.Embed(title="Other Commands", color=0x5681c8)
            otherHelpEmbed.add_field(name="Eval", value=">>> A compiler (owner only command).", inline=False)
            otherHelpEmbed.add_field(name="Invite", value=">>> Send the bot's invite link (Available in slash commands).", inline=False)
            otherHelpEmbed.add_field(name="Say", value=">>> Make the bot say something\n Syntax: `o!say [content]` (only mods can use it).", inline=False)
            otherHelpEmbed.add_field(name="Servers", value=">>> Shows how many servers the server is currently in (owner only command) and (slash command only).", inline=False)
            otherHelpEmbed.add_field(name="Translate", value=">>> Translate a language to a language with Google Translate\n Syntax: `o!translate [language] [message]` (Available in slash commands).", inline=False)
            otherHelpEmbed.timestamp = datetime.datetime.now()
            otherHelpEmbed.set_thumbnail(url="https://cdn.discordapp.com/attachments/939661225602740224/1011786454562779226/image_search_1661298942750.jpg")
            otherHelpEmbed.set_footer(text="The `o!help [command]` is not available", icon_url=client.user.avatar.url)
            await interaction.response.edit_message(embed=otherHelpEmbed)

class HelpView(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.add_item(Help())

    @discord.ui.button(label="End Interaction", style=discord.ButtonStyle.gray)
    async def end_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        for item in self.children:
            item.disabled = True

        await interaction.response.edit_message(view=self)

@client.command()
async def help(ctx):
    helpSview = HelpView()
    helpEmbed = discord.Embed(title="Bot Help", description=f"Hello {ctx.author.mention}! Welcome to the help page.\n Use the dropdown menu below to select a category for help.", color=0xc8ff75)
    helpEmbed.add_field(name="About me", value=">>> I am a **general-purpose bot** that is made to enhance your server with `moderation` and `fun` commands! On the other hand, I have other commands you can use or mess around with. \n You can get further information on my commands by using the dropdown below.", inline=False)
    await ctx.send(embed=helpEmbed, view=helpSview)

# class ModView(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.add_item(Intro())
@client.command()
async def modal(interaction: discord.Interaction):
    # modalView = ModView()
    await interaction.response.send_modal(Intro())

@client.command()
async def setprefix(ctx):
    await ctx.reply("Development on progress. Sorry for the inconvinience.")

class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = f"It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: list[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

@client.command()
async def ttt(ctx: commands.Context):
    await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())

# @client.command()
# async def scramble(ctx):
#     words = ['mnoht', 'nemoy', 'egarc', 'mah', 'ehsvart', 'puiknmp', 'ncor', 'eip', 'gahsrni', 'shusaq', 'lnafhktu', 'aalds', 'ekytru', 'ispirlgm', 'laifmy', 'tuanmu', 'otetapso', 'dinesrf', 'dnbroan', 'ypmrgu', 'ngeam', 'ueingpn', 'tecaelebr', 'stpa', 'rfacs', 'cskos', 'ritnew', 'aterwes', 'oiedoh', 'iec', 'teminst', 'ldoc', 'baetknl', 'jetkac', 'fenzor', 'beraemc', 'inaboyc', 'eshou', 'ordo', 'rdya', 'tapryn', 'ndrega', 'lalh', 'hsde', 'artcree', 'omrdbeo', 'sgtceot']

#     wordR = random.choice(words)
#     correct = ["That's correct!", "Yes, that's right.", "You're quite right.", "Yes, that's correct.", "That's spot on!", "You've hit the nail on the head.", "You could say so.", "Accurate!", "Absolutely.", "Right, right!", "Perfect"]
#     wrong = ['You failed!', "That's wrong!", "Incorrect!", "Unpromising.", "Fruitless!", "Disappointing.", "Inadequate.", "That's unfortunate!", "Better luck next time.", "That's not the word."]

#     timeout = ["You didn't respond on time.", "You're out of time.", "Time's up!", "There's no more time.", "Clock has run out.", "Ancient time's up."]

#     correctRandom = random.choice(correct)
#     wrongRandom = random.choice(wrong)

#     await ctx.send(f"Your word is... `{wordR}`")

#     # def check(ctx, m: discord.Message):
#     #     return m.author.id == ctx.author.id and m.channel.id  == ctx.channel.id

#     try:
#         ans = await client.wait_for('message', timeout=40)
#     except asyncio.TimeoutError:
#         await ctx.reply(random.choice(timeout))
#         return

#     ansContent = False
#     async for pastMessage in ctx.channel.history(limit=None):
#         if not ansContent:
#             ansContent.lower() = (pastMessage.author.id == ctx.author.id)
#             break

#     # ansContent = ans.content

#     if wordR == 'mnoht':
#         if ansContent == 'month':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)
#     elif wordR == 'nemoy':
#         if ansContent == 'money':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)
#     elif wordR == 'egarc':
#         if ansContent == 'grace':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'eip':
#         if ansContent == 'pie':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'gahsrni':
#         if ansContent == 'sharing':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'aalds':
#         if ansContent == 'salad':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ncor':
#         if ansContent == 'corn':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ekytru':
#         if ansContent == 'turkey':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'puiknmp':
#         if ansContent == 'pumpkin':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'dinesrf':
#         if ansContent == 'friends':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'shusaq':
#         if ansContent == 'squash':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'otetapso':
#         if ansContent == 'potatoes':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)
    
#     elif wordR == 'laifmy':
#         if ansContent == 'family':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'venmerob':
#         if ansContent == 'november':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'tuanmu':
#         if ansContent == 'autumn':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ispirlgm':
#         if ansContent == 'pilgrims':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ehsvart':
#         if ansContent == 'harvest':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'mah':
#         if ansContent == 'ham':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'dnbroan':
#         if ansContent == 'brandon':
#             await ctx.reply("The name was so easy to guess, huh?")
#         else:
#             await ctx.reply("Ahh.. That's unfortunate! It's Brandon!")

#     elif wordR == 'ngeam':
#         if ansContent == 'megan':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ypmrgu':
#         if ansContent == 'grumpy':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ueingpn':
#         if ansContent == 'penguin':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'tecaelebr':
#         if ansContent == 'celebrate':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'stpa':
#         if ansContent == 'past':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ritnew':
#         if ansContent == 'winter':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'aterwes':
#         if ansContent == 'sweater':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'cskos':
#         if ansContent == 'socks':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'rfacs':
#         if ansContent == 'scarf':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ldoc':
#         if ansContent == 'cold':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'oiedoh':
#         if ansContent == 'hoodie':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'baetknl':
#         if ansContent == 'blanket':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'beraemc':
#         if ansContent == 'embrace':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'fenzor':
#         if ansContent == 'frozen':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'jetkac':
#         if ansContent == 'jacket':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'iec':
#         if ansContent == 'ice':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'teminst':
#         if ansContent == 'mittens':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'tapryn':
#         if ansContent == 'pantry':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'agtceot':
#         if ansContent == 'cottage':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'inaboyc':
#         if ansContent == 'balcony':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'rdya':
#         if ansContent == 'yard':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'artcree':
#         if ansContent == 'terrace':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'lalh':
#         if ansContent == 'hall':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'hsde':
#         if ansContent == 'shed':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'eshou':
#         if ansContent == 'house':
#             await ctx.reply("Got it!!")
#         elif ansContent != 'house':
#             await ctx.send("That")

#         elif ansContent == 'idk' or ansContent == 'what':
#             await ctx.reply("Alright!")

#     elif wordR == 'ordo':
#         if ansContent == 'door':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

#     elif wordR == 'ndrega':
#         if ansContent == 'garden':
#             await ctx.reply(correctRandom)
#         else:
#             await ctx.reply(wrongRandom)

class Scramble(discord.ui.Modal, title="Scramble"):


    words = ['mnoht', 'nemoy', 'egarc', 'mah', 'ehsvart', 'puiknmp', 'ncor', 'eip', 'gahsrni', 'shusaq', 'lnafhktu', 'aalds', 'ekytru', 'ispirlgm', 'laifmy', 'tuanmu', 'otetapso', 'dinesrf', 'dnbroan', 'ypmrgu', 'ngeam', 'ueingpn', 'tecaelebr', 'stpa', 'rfacs', 'cskos', 'ritnew', 'aterwes', 'oiedoh', 'iec', 'teminst', 'ldoc', 'baetknl', 'jetkac', 'fenzor', 'beraemc', 'inaboyc', 'eshou', 'ordo', 'rdya', 'tapryn', 'ndrega', 'lalh', 'hsde', 'artcree', 'omrdbeo', 'sgtceot']
    wordR = random.choice(words)
    answer = discord.ui.TextInput(label=f"Your word is... {wordR}", style=discord.TextStyle.short, placeholder=wordR, required=True)

    correct = ["That's correct!", "Yes, that's right.", "You're quite right.", "Yes, that's correct.", "That's spot on!", "You've hit the nail on the head.", "You could say so.", "Accurate!", "Absolutely.", "Right, right!", "Perfect"]
    wrong = ['You failed!', "That's wrong!", "Incorrect!", "Unpromising.", "Fruitless!", "Disappointing.", "Inadequate.", "That's unfortunate!", "Better luck next time.", "That's not the word."]

    # timeout = ["You didn't respond on time.", "You're out of time.", "Time's up!", "There's no more time.", "Clock has run out.", "Ancient time's up."]

    correctRandom = random.choice(correct)
    wrongRandom = random.choice(wrong)

    async def on_submit(self, interaction: discord.Interaction):

        if self.wordR == 'mnoht':
            if self.answer == 'month':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)
        elif self.wordR == 'nemoy':
            if self.answer == 'money':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)
        elif self.wordR == 'egarc':
            if self.answer == 'grace':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'eip':
            if self.answer == 'pie':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'gahsrni':
            if self.answer == 'sharing':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'aalds':
            if self.answer == 'salad':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ncor':
            if self.answer == 'corn':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ekytru':
            if self.answer == 'turkey':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'puiknmp':
            if self.answer == 'pumpkin':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'dinesrf':
            if self.answer == 'friends':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'shusaq':
            if self.answer == 'squash':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'otetapso':
            if self.answer == 'potatoes':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)
        
        elif self.wordR == 'laifmy':
            if self.answer == 'family':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'venmerob':
            if self.answer == 'november':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'tuanmu':
            if self.answer == 'autumn':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ispirlgm':
            if self.answer == 'pilgrims':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ehsvart':
            if self.answer == 'harvest':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'mah':
            if self.answer == 'ham':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'dnbroan':
            if self.answer == 'brandon':
                await interaction.response.send_message("The name was so easy to guess, huh?")
            else:
                await interaction.response.send_message("Ahh.. That's unfortunate! It's Brandon!")

        elif self.wordR == 'ngeam':
            if self.answer == 'megan':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ypmrgu':
            if self.answer == 'grumpy':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ueingpn':
            if self.answer == 'penguin':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'tecaelebr':
            if self.answer == 'celebrate':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'stpa':
            if self.answer == 'past':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ritnew':
            if self.answer == 'winter':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'aterwes':
            if self.answer == 'sweater':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'cskos':
            if self.answer == 'socks':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'rfacs':
            if self.answer == 'scarf':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ldoc':
            if self.answer == 'cold':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'oiedoh':
            if self.answer == 'hoodie':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'baetknl':
            if self.answer == 'blanket':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'beraemc':
            if self.answer == 'embrace':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'fenzor':
            if self.answer == 'frozen':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'jetkac':
            if self.answer == 'jacket':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'iec':
            if self.answer == 'ice':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'teminst':
            if self.answer == 'mittens':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'tapryn':
            if self.answer == 'pantry':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'agtceot':
            if self.answer == 'cottage':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'inaboyc':
            if self.answer == 'balcony':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'rdya':
            if self.answer == 'yard':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'artcree':
            if self.answer == 'terrace':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'lalh':
            if self.answer == 'hall':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'hsde':
            if self.answer == 'shed':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'eshou':
            if self.answer == 'house':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ordo':
            if self.answer == 'door':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

        elif self.wordR == 'ndrega':
            if self.answer == 'garden':
                await interaction.response.send_message(self.correctRandom)
            else:
                await interaction.response.send_message(self.wrongRandom)

@client.command()
async def scramble(interaction: discord.Interaction):
    await interaction.response.send_modal(Scramble())

# load_dotenv()

client.run(os.getenv('DISCORD_TOKEN'), log_handler=handler)



# client.run(token, log_handler=handler)
