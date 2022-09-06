# custom-bot

Custom Discord bot for personal use. Hosted on Raspberry Pi.

## Requirements
- Python 3.9
- Discord
  - Privileged Gateway Intents
    - Presence intent
    - Server members intent
    - Message content intent
  - Permissions
    - Manage roles

## Environment Variables
- `DISCORD_TOKEN`: Token from Discord developer portal
- `PREFIX`: Prefix for commands
- `ROLE`: Role that is allowed to call the bot 

## Commands
> `!addrole rolename @user @user ...`

Adds role `rolename` to all users listed

> `!remove rolename`

Removes role `rolename` from all users
