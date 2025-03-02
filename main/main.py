from dotenv import load_dotenv
from discord import app_commands
import discord
import os
import random
import json

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
print(token)

# init intents
intents = discord.Intents.default()
intents.guild_messages = True
intents.members = True

bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Load role IDs from config file
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Save role IDs to config file
def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f)

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('Donut Machine is working!', ephemeral=True)

@tree.command(name="setrole", description="Set the role for matching members")
@app_commands.describe(role="The role to match members with")
async def setrole(interaction: discord.Interaction, role: discord.Role):
    config = load_config()
    server_id = str(interaction.guild.id)
    if "servers" not in config:
        config["servers"] = {}
    if server_id not in config["servers"]:
        config["servers"][server_id] = {}
    config["servers"][server_id]["role_id"] = role.id
    save_config(config)
    await interaction.response.send_message(f"Role {role.name} has been set for matching in this server.")

@tree.command(name="setsize", description="Set a group size")
@app_commands.describe(value="The integer value to set")
async def setszie(interaction: discord.Interaction, value: int):
    config = load_config()
    server_id = str(interaction.guild.id)
    if "servers" not in config:
        config["servers"] = {}
    if server_id not in config["servers"]:
        config["servers"][server_id] = {}
    config["servers"][server_id]["value"] = value
    save_config(config)
    await interaction.response.send_message(f"Value {value} has been set for this server.")

@tree.command(name="roll", description="Makes the groups")
async def roll(interaction: discord.Interaction):
    config = load_config()
    server_id = str(interaction.guild.id)
    server_config = config.get("servers", {}).get(server_id, {})
    role_id = server_config.get("role_id")
    size = server_config.get("value")

    if not role_id:
        await interaction.response.send_message("No role has been set for matching in this server. Use /setrole to set a role.")
        return

    role = interaction.guild.get_role(role_id)
    if not role:
        await interaction.response.send_message("The role set for matching no longer exists. Use /setrole to set a new role.")
        return
    
    if not size:
        await interaction.response.send_message("No group size has been set. Please use /setvalue to set the group sizes")
    
    to_match = [m for m in interaction.guild.members if role in m.roles]

    random.shuffle(to_match)

    counter = 0
    message = ""
    leftovers = len(to_match) % size
    while len(to_match) > leftovers + size: #works through the main groups
        m=to_match[0]
        message += m.mention + " "
        counter += 1
        if counter == size:
            counter = 0
            message += '\n\n'
        to_match.pop(0)
    for m in (to_match): #deals with leftovers making a group smaller than 2*size
        message += m.mention + " "
    await interaction.response.send_message(message)


# event: when the bot is ready
@bot.event
async def on_ready():
    await tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)