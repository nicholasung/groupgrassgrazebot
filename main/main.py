from dotenv import load_dotenv
from discord import app_commands
import discord
import os
import random

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
print(token)

# init intents
intents = discord.Intents.default()
intents.guild_messages = True
intents.members = True

global most_recent
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('Donut Machine is working!', ephemeral=True)

# need to add way to specify a role and a size

async def match(interaction: discord.Interaction):
    to_match = [] #list of members to match

    for m in interaction.guild.members:
        to_match.append(m) #change this to only grab members with a role
    
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