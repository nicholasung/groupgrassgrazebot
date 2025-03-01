from dotenv import load_dotenv
from discord import app_commands
import io
import discord
import os

# Load environment variables from .env file
load_dotenv()
token = os.getenv('TOKEN')
print(token)

# init intents
intents = discord.Intents.default()

global most_recent
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

@tree.command(name="status", description="Check the bot's status")
async def status(interaction: discord.Interaction):
     await interaction.response.send_message('Donut Machine is working!', ephemeral=True)

# event: when the bot is ready
@bot.event
async def on_ready():
    await bot.tree.sync()
    print('We have logged in and synced')
    print('Synced commands:')
    for command in bot.tree.walk_commands():
        print(f"- {command.name}: {command.description}")

bot.run(token)