from discord.ext import commands
import datetime
import sqlite3
import discord


class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.conn = sqlite3.connect('birthdays.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS birthdays (
                user_id INTEGER PRIMARY KEY,
                month INTEGER NOT NULL,
                day INTEGER NOT NULL
            )
        ''')
        self.conn.commit()

    @commands.slash_command(name="setbirthday", description="Set your birthday.")
    async def birthday(self, ctx, month: int, day: int):

        if not self.validate_bday(month, day):
            await ctx.respond("Invalid date. Please enter a valid Date.")
            return

        self.cursor.execute('''
            INSERT OR REPLACE INTO birthdays (user_id, month, day)
            VALUES (?, ?, ?)
        ''', (ctx.author.id, month, day))
        self.conn.commit()

        month_name = self.month_convert(month)
        await ctx.respond(f"Your birthday has been set to {month_name} {day}.")

    @commands.slash_command(name="getbirthday", description="Get Member's birthday.")
    async def get_birthday(self, ctx, member: discord.Member):
        user_id = member.id if member else ctx.author.id

        self.cursor.execute('''
            SELECT month, day FROM birthdays WHERE user_id = ?
        ''', (user_id,))

        result = self.cursor.fetchone()

        if result:
            month, day = result
            month_name = self.month_convert(month)

            if user_id == ctx.author.id:
                await ctx.respond(f"Your birthday is {month_name} {day}.")
                return
            await ctx.respond(f"{member}'s birthday is {month_name} {day}.")
        else:
            if user_id == ctx.author.id:
                await ctx.respond("You have not set your birthday yet.")
                return
            await ctx.respond(f"{member} have not set your birthday yet.")

    def validate_bday(self, month: int, day: int):
        try:
            datetime.datetime(year=2023, month=month, day=day)
            return True
        except ValueError:
            return False

    def month_convert(self, month: int):
        months = {
            1: "January", 2: "February", 3: "March",
            4: "April", 5: "May", 6: "June",
            7: "July", 8: "August", 9: "September",
            10: "October", 11: "November", 12: "December"
        }
        return months.get(month, None)


def setup(bot):
    bot.add_cog(BirthdayCog(bot))
    print("BirthdayCog loaded successfully.")
