import os
import re
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
ROLE = os.getenv('ROLE')
CHANNEL = None
CATEGORY = None

# Needed to get all members in the server.
intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Adds role to a specified list of users. If role does not exist, create it.
@bot.command(pass_context=True, name='addrole', help=f'Adds role to the list of following users. If the role does not exist, the bot will create the role')
async def add_role(ctx, role, *users):
    if not can_call(ctx):
        await ctx.message.channel.send(f'{ctx.author.mention} You need the role {ROLE} to add roles.') 
        return

    if not is_valid_role(role):
        await ctx.message.channel.send(f'{ctx.author.mention} Role must match ^pay[0-9]+.') 
        return

    message = f'{ctx.author.mention} Finished adding role {role} to the specified users.\n'

    # Create role if it doesn't exist.
    if not discord.utils.get(ctx.guild.roles, name=role):
        await ctx.guild.create_role(name=role)

    for member in ctx.message.mentions:
        try:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name=role))
        except Exception as e:
            message += f'\nFailed to add role {role} to {member.mention} with error {e}'

    await ctx.message.channel.send(message)    

# Deletes role from all users.
@bot.command(pass_context=True, name='removerole', help='Removes role from all users')
async def remove_role(ctx, role):
    if not can_call(ctx):
        await ctx.message.channel.send(f'{ctx.author.mention} You need the role {ROLE} to remove roles.') 
        return

    if not is_valid_role(role):
        await ctx.message.channel.send(f'{ctx.author.mention} Role must match ^pay[0-9]+.') 
        return

    if not discord.utils.get(ctx.guild.roles, name=role):
        await ctx.message.channel.send(f'{ctx.author.mention} Role must exist.') 
        return

    message = f'{ctx.author.mention} Finished removing role {role} from all users\n'

    role = discord.utils.get(ctx.guild.roles, name=role)
    members = role.members
    for member in members:
        try:
            await member.remove_roles(role)
        except Exception as e:
            message += f'\nFailed to remove role {role} to {member.mention} with error {e}'

    await ctx.message.channel.send(message)

# Whether the author can use the bot
def can_call(ctx):
    role = discord.utils.get(ctx.guild.roles, name=ROLE)
    if role is None or role not in ctx.author.roles:
        return False
    return True

# Whether the role is valid
def is_valid_role(role):
    return re.match('^pay[0-9]+', role)

# Registers the bot to log voice channel (under a category if specified or all categories if not specified) changes to a text channel.
@bot.command(pass_context=True, name='registervc', help='Logs voice channel changes to a text channel given a category id. If category id is omitted, then all voice channels will logged.')
async def register_vc(ctx, id:int=None):
    category = bot.get_channel(id)
    if id and not category:
        await ctx.message.channel.send("Failed to register this channel for logging vc changes because the category id is present but invalid")
        return

    global CHANNEL, CATEGORY
    
    message = ""
    if not CHANNEL:
        message += 'Registered this channel for logging vc changes'
        if id:
            message += f' for category {category.name}'
        
        CATEGORY = id
        CHANNEL = ctx.channel.id
    else:
        message += 'This channel will no longer be logging vc changes'
        if CATEGORY:
            message += f' for category {category.name}'

        CATEGORY = None
        CHANNEL = None
    
    await ctx.message.channel.send(message)

@bot.event
async def on_voice_state_update(member, before, after):
    if not CHANNEL or member.bot or before.channel.id == after.channel.id:
        return

    message = ""
    if before.channel is not None and in_category(before.channel.category_id):
        message += f'{member.mention} left {before.channel.name}\n'
    if after.channel is not None and in_category(after.channel.category_id):
        message += f'{member.mention} joined {after.channel.name}'

    embed = discord.Embed(description=message)
    channel = bot.get_channel(CHANNEL)
    await channel.send(embed=embed)

# Whether the category is correct
def in_category(category_id):
    return True if CATEGORY == None else category_id == CATEGORY

bot.run(TOKEN)