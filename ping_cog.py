from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="ping", description="Responds with Pong and latency.")
    async def ping(self, ctx):
        await ctx.respond(f"Pong'd in {round(self.bot.latency * 1000)} ms")

def setup(bot):
    bot.add_cog(PingCog(bot))
    print("PingCog loaded successfully.")