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
        with get_db_connection() as conn:
            self.conn = conn
            self.cursor = conn.cursor()
            self.cursor.execute(queries.CREATE_ANNOUNCEMENT_CHANNELS_TABLE)
            self.conn.commit()

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
            channel = self.bot.get_channel(
                int(os.getenv("BIRTHDY_CHANNEL_ID")))
            if channel and user:
                await channel.send(f"🎉🎉Happy Birthday {user.mention}!🎉🎉")

    @announce_birthday.before_loop
    async def before_announce_birthday(self):
        await self.bot.wait_until_ready()

    @commands.slash_command(name="setannouncement", description="Set current channel for birthday announcements.")
    async def set_announcement(self, ctx):
        
        channel = ctx.channel  
        guild = ctx.guild
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You do not have permission to set announcements.")
            return

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.INSERT_ANNOUNCEMENT_CHANNEL, (guild.id, channel.id))
            conn.commit()       
        
        # print(f"Setting announcement channel for guild {guild.id} ({guild}) to channel {channel.id} | {channel.name}")
        await ctx.respond(f"Announcement channel has been set successfully to {channel.mention} in {guild.name}.")

    @commands.slash_command(name="removeannouncement", description="Remove the announcement channel for birthdays.")
    async def remove_announcement(self, ctx):
        
        channel = ctx.channel  
        guild = ctx.guild
        
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You do not have permission to remove announcements.")
            return

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.DELETE_ANNOUNCEMENT_CHANNEL, (guild.id,))
            conn.commit()

        await ctx.respond(f"{channel.mention} has been removed as the announcement channel.")
        
    @commands.slash_command(name="getannouncement", description="Get the current announcement channel for birthdays.")
    async def get_announcement_channel(self, ctx):
        guild = ctx.guild
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(queries.CHECK_ANNOUNCEMENT_CHANNEL, (guild.id,))
            result = cursor.fetchone()
            
        if result:
            channel_id = result['channel_id']
            channel = self.bot.get_channel(channel_id)
            await ctx.respond(f"The current announcement channel is {channel.mention}.")
            return
        await ctx.respond("No announcement channel has been set for this server.")
        return

def setup(bot):
    bot.add_cog(BirthdayAnnouncer(bot))
    print("BirthdayAnnouncer cog loaded.")
