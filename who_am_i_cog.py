from discord.ext import commands

class WhoAmICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="whoami", description="Get information about yourself")
    async def whoami(self, ctx):
        user = ctx.author
        await ctx.respond(f"You are {user.name}!")

def setup(bot):
    bot.add_cog(WhoAmICog(bot))
    print("WhoAmICog loaded successfully.")
        