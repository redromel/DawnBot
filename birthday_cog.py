from discord.ext import commands
import datetime

class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="setbirthday", description="Set your birthday.")
    async def birthday(self, ctx, month: int, day: int):

        if not self.validate_bday(month, day):
            await ctx.respond("Invalid date. Please enter a valid Date.")
            return
        await ctx.respond(f"Your birthday has been set to {month}-{day}.")


    @commands.slash_command(name="getbirthday", description="Get your birthday.")
    async def get_birthday(self, ctx):
        await ctx.respond("Make Later wtith SQL")
    def validate_bday(self, month: int, day: int):
        try:
            datetime.datetime(year=2023, month=month, day=day)
            return True
        except ValueError:
            return False
def setup(bot):
    bot.add_cog(BirthdayCog(bot))
    print("BirthdayCog loaded successfully.")