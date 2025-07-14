import discord
import os
from dotenv import load_dotenv


load_dotenv()


intents = discord.Intents.default()
bot = discord.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.sync_commands()


async def hello(ctx):
    await ctx.respond("Whats up, Rokyuu!!!")


@bot.slash_command(name="goodbye", description="Say goodbye")
async def bye(ctx):
    await ctx.respond("BYE, Rokyuu!")


bot.load_extension("ping_cog")
bot.load_extension("who_am_i_cog")
bot.load_extension("birthday_cog")
bot.load_extension("birthday_announcer")

bot.run(os.getenv('DISCORD_TOKEN'))

