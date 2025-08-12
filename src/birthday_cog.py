from discord.ext import commands
import datetime
from db import get_db_connection
import discord
from discord import Option  # type: ignore
import queries
import datetime


class BirthdayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with get_db_connection() as conn:
            self.conn = conn
            self.cursor = conn.cursor()
            self.cursor.execute(queries.CREATE_BIRTHDAYS_TABLE)
            self.conn.commit()

    @commands.slash_command(name="setbirthday",
                            description="Set your birthday.")
    async def birthday(self,
                       ctx,
                
                       month: Option(int, "Month Number (1-12)"), # type: ignore
                       day: Option(int, "Day Number (1-31)")):  # type: ignore
        # print(ctx.author.id)
        if not self.validate_bday(month, day):
            await ctx.respond("Invalid date. Please enter a valid Date.")
            return

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.INSERT_BIRTHDAY,
                           (ctx.author.id, month, day))
            conn.commit()

        month_name = self.month_convert(month)
        await ctx.respond(f"Your birthday has been set to {month_name} {day}.")

    @commands.slash_command(name="getbirthday", description="Get Member's birthday.")
    async def get_birthday(self, ctx, member: discord.Member):
        user_id = member.id
        # print(user_id)
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(queries.SELECT_BIRTHDAY, (user_id,))
                result = cursor.fetchone()

        if result:

            month, day = result['month'], result['day']
            month_name = self.month_convert(month)

            if user_id == ctx.author.id:
                await ctx.respond(f"Your birthday is {month_name} {day}.")
                return
            await ctx.respond(f"{member}'s birthday is {month_name} {day}.")
        else:
            if user_id == ctx.author.id:
                await ctx.respond("You have not set your birthday yet.")
                return
            await ctx.respond(f"{member} has not set their birthday yet.")

    @commands.slash_command(name="testbirthday", description="Test birthday.")
    async def test_birthday(self, ctx):
        now = datetime.datetime.now()
        today = now.date()

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                queries.CHECK_BIRTHDAY, (today.month, today.day))
            birthdays_today = cursor.fetchall()
        if not birthdays_today:
            await ctx.respond("No birthdays today.")
            return

        for birthday in birthdays_today:
            # print(birthday)
            user_id = birthday["user_id"]
            month = birthday["month"]
            day = birthday["day"]

            # print(f"User ID: {user_id}, Month: {month}, Day: {day}")
            # print(f"User ID type: {type(user_id)}, Month type: {type(month)}, Day type: {type(day)}")

            user = await self.bot.fetch_user(user_id)

            if user:
                month_name = self.month_convert(month)
                await ctx.respond(f"Happy Birthday {user.mention}! 🎉 Your birthday is today: {month_name} {day}.")



    @commands.slash_command(name="serverbirthdays", description="Get upcoming birthdays for the server.")
    async def server_birthdays(self, ctx):
        now = datetime.datetime.now()
        today = now.date()
        next

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.ALL_BIRTHDAYS)
            upcoming_birthdays = cursor.fetchall()
        if not upcoming_birthdays:
            await ctx.respond("No one in the server has set birthdays.")
            return
        lines = []
        for birthday in upcoming_birthdays:
            user_id = birthday["user_id"]
            month = birthday["month"]
            day = birthday["day"]

            member = ctx.guild.get_member(user_id)
            if member:
                month_name = self.month_convert(month)
                lines.append(f"{member.display_name} - {month_name} {day}")

        if not lines:
            await ctx.respond("No one in the server has set birthdays.")
        else:
            response = "Members Birthdays:\n" + "\n".join(lines)
            await ctx.respond(response)

    @commands.slash_command(name="upcomingbirthday", description="Get upcoming birthdays for the server (up to the end of the next month).")
    async def upcoming_birthday(self, ctx):
        now = datetime.datetime.now()
        today = now.date()
        next_month = (today.month % 12) + 1

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.UPCOMING_BIRTHDAYS,
                           (today.month, today.day, next_month))
            upcoming_birthdays = cursor.fetchall()

        if not upcoming_birthdays:
            await ctx.respond("No upcoming birthdays in the server.")
            return
        
        lines = []
        for birthday in upcoming_birthdays:
            user_id = birthday["user_id"]
            month = birthday["month"]
            day = birthday["day"]

            member = ctx.guild.get_member(user_id)
            if member:
                month_name = self.month_convert(month)
                lines.append(f"{member.display_name} - {month_name} {day}")

        if not lines:
            await ctx.respond("No upcoming birthdays in the server.")
            return
        response = "Upcoming Birthdays:\n" + "\n".join(lines)
        await ctx.respond(response)
        return
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
