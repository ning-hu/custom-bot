import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')

# Needed to get all members in the server.
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Adds a role to a specified list of users. If role does not exist, create it.
@bot.command(pass_context=True, name='addrole', help=f'Adds role to the list of following users. If the role does not exist, the bot will create the role')
@commands.has_permissions(administrator=True)
async def addrole(ctx, role, *users):
    message = f'Finished adding role {role} to the specified users.\n'

    # Create role if it doesn't exist.
    if not discord.utils.get(ctx.guild.roles, name=role):
        await ctx.guild.create_role(name=role)

    for member in ctx.message.mentions:
        try:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name=role))
        except Exception as e:
            message += f'\nFailed to add role {role} to {member.mention} with error {e}'

    await ctx.message.channel.send(message)    

# Deletes a role from all users and the actual role itself.
@bot.command(pass_context=True, name='removerole', help='Removes role from all users')
@commands.has_permissions(administrator=True)
async def removerole(ctx, role):
    message = f'Finished removing role {role} from all users\n'

    role = discord.utils.get(ctx.guild.roles, name=role)
    members = role.members
    for member in members:
        try:
            await member.remove_roles(role)
        except Exception as e:
            message += f'\nFailed to remove role {role} to {member.mention} with error {e}'

    await ctx.message.channel.send(message)

bot.run(TOKEN)