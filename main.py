import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
intents = discord.Intents.default()
intents.message_content = True # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(os.getenv('DISCORD_TOKEN'))