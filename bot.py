import discord
from discord.ext import commands
import datetime
from datetime import date
import time
import asyncio
import json
from .config1 import TOKEN, CATEGORYID, LOGCHANNELID, SETCOMMENTRANKS, HELPCHANNELID, PREFIX

bot = commands.Bot(command_prefix=str(PREFIX))

client = bot

today = date.today()

datev2 = time.strftime("%m-%d-%Y")

print('Loading...')

@client.event
async def on_ready():
    print('Bot is ready')
    activity = discord.Activity(name='for tickets', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)


rank = 0


@client.command()
async def getid(ctx):
    print(ctx.author.guild.id)



@bot.event
async def on_message(message):
    me = client.get_user(670375106006089728)
    guild = client.get_guild(588548216644042753)
    tmod = discord.utils.get(guild.roles, name='Trial Moderator')
    mod = discord.utils.get(guild.roles, name='Moderator')
    supmod = discord.utils.get(guild.roles, name='Supervisor Moderator')
    admin = discord.utils.get(guild.roles, name='Admin')
    founder = discord.utils.get(guild.roles, name='Founder')
    category = discord.utils.get(guild.categories, id=int(CATEGORYID))
    await bot.process_commands(message)
    if message.guild is None and message.author != bot.user:
        membersname1 = message.author.name
        membersname = membersname1.replace(" ", "")
        tchannel2 = discord.utils.get(guild.text_channels, name=f'ticket-{membersname.lower()}')
        tchannel = discord.utils.get(guild.text_channels, name=f'ticket-{membersname.lower()}')
        if tchannel2 == None:
            if tchannel == None:
                channel2 = await guild.create_text_channel(f'ticket-{membersname.lower()}', category=category)
                embed = discord.Embed(title=f"New ticket from {membersname.lower()}",
                                    description=f"Hello {message.author.mention}, a staff member will be with you shortly. In the meantime please take some time to further explain your problem.",
                                    color=0x0080ff)
                embed.add_field(name="Problem", value=message.content, inline=False)
                embed.set_footer(text=f"uID: {message.author.id}")
                await message.author.send(embed=embed)
                await channel2.send(message.author.id)
                await channel2.send(embed=embed)
                await bot.process_commands(message)
                return
        else:
            print('3')
            await bot.process_commands(message)
            await message.add_reaction(emoji=u"\u2705")
            embed = discord.Embed(title=f"{message.author.name} says", description=message.content,
                                  color=0x00c600)
            await tchannel2.send(embed=embed)
            pic_ext = ['.jpg', '.png', '.jpeg']
            for ext in pic_ext:
                print('1')
                if message.attachments[0].url.endswith(ext):
                    print('2')
                    embed = discord.Embed(title=f"{message.author.name} sent", color=0x0080ff)
                    embed.set_image(url=message.attachments[0].url)
                    await tchannel2.send(embed=embed)
                    await message.add_reaction(emoji=u"\u2705")
    else:
        if message.content.startswith('%%'):
            await message.delete()
            user1 = message.author
            await bot.process_commands(message)
            global rank
            if tmod in user1.roles:
                rank = 'Trial Moderator'
            if admin in user1.roles:
                rank = 'Admin'
            if supmod in user1.roles:
                rank = 'Supervisor Moderator'
            if mod in user1.roles:
                rank = 'Moderator'
            if founder in user1.roles:
                rank = 'Founder'
            comment = message.content
            cutcomment = comment[2:]
            if SETCOMMENTRANKS.lower() == 'true':
                embed = discord.Embed(title=f"Comment from {user1} - {rank}", description=cutcomment, color=0x202225)
                embed.set_footer(text=f"uID: a{message.author.id}")
            else:
                embed = discord.Embed(title=f"Comment from {user1} - Support", description=cutcomment, color=0x202225)
                embed.set_footer(text=f"uID: a{message.author.id}")
            await message.channel.send(embed=embed)
            await bot.process_commands(message)
        else:
            if message.channel.name.startswith('ticket'):
                if message.author == me or message.content.startswith(f'{PREFIX}close') or message.content.startswith(f'{PREFIX}solve'):
                    return
                else:
                    async for message2 in message.channel.history(oldest_first=True, limit=1):
                        membersid = message2.content
                    member = guild.get_member(int(membersid))
                    if member == None:
                        await message.channel.send('ERROR1: Cannot find member to message. Please contact peeeeeta')
                    embed = discord.Embed(title=f"{message.author.name} says", description=message.content,
                                            color=0x00c600)
                    async with member.typing():
                        await member.send(embed=embed)
                    await message.add_reaction(emoji=u"\u2705")
                    pic_ext = ['.jpg', '.png', '.jpeg']
                    for ext in pic_ext:
                        if message.attachments[0].url.endswith(ext):
                            embed = discord.Embed(title=f"{message.author.name} sent", color=0x0080ff)
                            embed.set_image(url=message.attachments[0].url)
                            await member.send(embed=embed)
                            await message.add_reaction(emoji=u"\u2705")
                            await bot.process_commands(message)
                    await bot.process_commands(message)
            else:
                return
    await bot.process_commands(message)


@client.command(aliases=['solve'])
async def close(ctx):
    if ctx.channel.name.startswith('ticket'):
        opendate = f'{ctx.channel.created_at.month}-{ctx.channel.created_at.day}-{ctx.channel.created_at.year}'
        async for message2 in ctx.message.channel.history(oldest_first=True, limit=1):
            membersid = message2.content
        member = ctx.message.guild.get_member(int(membersid))
        embed = discord.Embed(title=f"{ctx.author.name} has closed your ticket",
                              description=f"Hello {member.mention}, your ticket was closed. PM me again to create a new one",
                              color=0x0080ff)
        embed.add_field(name="Ticket Creation Date", value=opendate, inline=False)
        embed.add_field(name="Ticket Close Date", value=datev2, inline=False)
        await member.send(embed=embed)
        channel2 = client.get_channel(int(LOGCHANNELID))
        embed = discord.Embed(title=f"Ticket closed by {ctx.author.name}", color=0x008080)
        embed.add_field(name="Ticket Open Date", value=opendate, inline=False)
        embed.add_field(name="Ticket Close Date", value=datev2, inline=True)
        embed.add_field(name="Ticket Creator", value=member.name)
        await ctx.channel.delete(reason=None)
        await channel2.send(embed=embed)
    else:
        await ctx.send(f'{ctx.author.mention} this can only be used in ticket channels!')

#For FSATC to create the information channel
@client.command()
async def createhelpchannel(ctx):
    channel = client.get_channel(int(HELPCHANNELID))
    embed = discord.Embed(title=":ticket:Tickets Help")
    embed.add_field(name="", value="Command Prefix: `$`", inline=False)
    embed.add_field(name="", value="Close Ticket: `.close/solve`", inline=False)
    embed.add_field(name="How to open a ticket:", value="When a user DMs the bot it will create a ticket", inline=False)
    await channel.send(embed=embed)

def getJSON(filePathAndName):
    with open(filePathAndName, 'r') as fp:
        return json.load(fp)

@client.command()
async def docs(ctx, arg1):
    myObj = getJSON('./reference.json')
    await ctx.send('Showing Results for: ' + arg1)
    await ctx.send(myObj.get(f"{arg1}", ""))

#V1.2 - 11:06 PM EST 4/8/2020

client.run(str(TOKEN))

