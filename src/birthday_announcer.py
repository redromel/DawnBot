from discord.ext import commands, tasks
import datetime
from db import get_db_connection
import zoneinfo
import os
import queries

class BirthdayAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = zoneinfo.ZoneInfo("America/New_York")
        self.announce_birthday.start()

    def cog_unload(self):
        self.announce_birthday.stop()

    @tasks.loop(hours=24)
    async def announce_birthday(self):
        now = datetime.datetime.now(tz=self.timezone)
        today = now.date()
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                queries.CHECK_BIRTHDAY, (today.month, today.day))
            birthdays_today = cursor.fetchall()

        for birthday in birthdays_today:
            user_id = birthday["user_id"]

            
            user = await self.bot.fetch_user(user_id)
            channel = self.bot.get_channel(int(os.getenv("BIRTHDY_CHANNEL_ID")))
            if channel and user:
                await channel.send(f"🎉🎉Happy Birthday {user.mention}!🎉🎉")

    @announce_birthday.before_loop
    async def before_announce_birthday(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(BirthdayAnnouncer(bot))
    print("BirthdayAnnouncer cog loaded.")
