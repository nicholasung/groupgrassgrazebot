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
    config["servers"][server_id] = role.id
    save_config(config)
    await interaction.response.send_message(f"Role {role.name} has been set for matching in this server.", ephemeral=True)

@tree.command(name="setvalue", description="Set an integer value for the server")
@app_commands.describe(value="The integer value to set")
async def setvalue(interaction: discord.Interaction, value: int):
    config = load_config()
    server_id = str(interaction.guild.id)
    if "servers" not in config:
        config["servers"] = {}
    if server_id not in config["servers"]:
        config["servers"][server_id] = {}
    config["servers"][server_id]["value"] = value
    save_config(config)
    await interaction.response.send_message(f"Value {value} has been set for this server.", ephemeral=True)

async def match(interaction: discord.Interaction):
    config = load_config()
    server_id = str(interaction.guild.id)
    server_config = config.get("servers", {}).get(server_id, {})
    role_id = server_config.get("role_id")

    if not role_id:
        await interaction.response.send_message("No role has been set for matching in this server. Use /setrole to set a role.", ephemeral=True)
        return

    role = interaction.guild.get_role(role_id)
    if not role:
        await interaction.response.send_message("The role set for matching no longer exists. Use /setrole to set a new role.", ephemeral=True)
        return
    
    to_match = [m for m in interaction.guild.members if role in m.roles]

    random.shuffle(to_match)
    
    # iterate through the list at given size while the list is divisibile by that given size. when it isnt anymore. the list should be of given size + remainder. give that as the last group

# event: when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in bot.tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)