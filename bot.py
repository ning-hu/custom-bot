import os
import re
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
ROLE = os.getenv('ROLE')

# Needed to get all members in the server.
intents = discord.Intents.default()
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

bot.run(TOKEN)