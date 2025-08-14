from discord.ext import commands, tasks
import datetime
from db import get_db_connection
import zoneinfo
import queries


class BirthdayAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezone = zoneinfo.ZoneInfo("America/New_York")
        self.announce_birthday.start()
        try:
            with get_db_connection() as conn:
                self.conn = conn
                self.cursor = conn.cursor()
                self.cursor.execute(queries.CREATE_ANNOUNCEMENT_CHANNELS_TABLE)
                self.conn.commit()
        except Exception as e:
            print(f"Error initializing DB in BirthdayAnnouncer: {e}")

    def cog_unload(self):
        self.announce_birthday.stop()

    @tasks.loop(hours=1)
    async def announce_birthday(self):
        now = datetime.datetime.now(tz=self.timezone)
        today = now.date()

        if now.hour != 7:
            return  # Only run at 7 AM

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    queries.CHECK_BIRTHDAY, (today.month, today.day))
                birthdays_today = cursor.fetchall()
                cursor.execute(queries.GET_ALL_ANNOUNCEMENT_CHANNELS)
                announcement_channels = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching birthdays or announcement channels: {e}")
            return

        if not birthdays_today or not announcement_channels:
            return

        for birthday in birthdays_today:
            user_id = birthday['user_id']

            for channel_info in announcement_channels:
                guild_id = channel_info['guild_id']
                channel_id = channel_info['channel_id']

                try:
                    guild = self.bot.get_guild(guild_id)
                    channel = guild.get_channel(channel_id) if guild else None
                    member = guild.get_member(user_id) if guild else None

                    if channel and member:
                        await channel.send(
                            f"🎉 Happy Birthday {member.mention}!!!"
                        )
                except Exception as e:
                    print(f"Error sending birthday announcement: {e}")

    @announce_birthday.before_loop
    async def before_announce_birthday(self):
        await self.bot.wait_until_ready()

    @commands.slash_command(name="setannouncement", description="Set current channel for birthday announcements.")
    async def set_announcement(self, ctx):

        channel = ctx.channel
        guild = ctx.guild

        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You do not have permission to set announcements.", ephemeral=True)
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.INSERT_ANNOUNCEMENT_CHANNEL,
                               (guild.id, channel.id))
                conn.commit()
        except Exception as e:
            await ctx.respond(f"Failed to set announcement channel: {e}", ephemeral=True)
            return

        await ctx.respond(f"Announcement channel has been set successfully to {channel.mention} in {guild.name}.", delete_after=30)

    @commands.slash_command(name="removeannouncement", description="Remove the announcement channel for birthdays.")
    async def remove_announcement(self, ctx):

        channel = ctx.channel
        guild = ctx.guild

        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You do not have permission to remove announcements.", ephemeral=True)
            return

        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.DELETE_ANNOUNCEMENT_CHANNEL, (guild.id,))
                conn.commit()
        except Exception as e:
            await ctx.respond(f"Failed to remove announcement channel: {e}", ephemeral=True)
            return

        await ctx.respond(f"{channel.mention} has been removed as the announcement channel.", delete_after=30)

    @commands.slash_command(name="getannouncement", description="Get the current announcement channel for birthdays.")
    async def get_announcement_channel(self, ctx):
        guild = ctx.guild
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.CHECK_ANNOUNCEMENT_CHANNEL, (guild.id,))
                result = cursor.fetchone()
        except Exception as e:
            await ctx.respond(f"Failed to get announcement channel: {e}", ephemeral=True)
            return

        if result:
            channel_id = result['channel_id']
            try:
                channel = self.bot.get_channel(channel_id)
                await ctx.respond(f"The current announcement channel is {channel.mention}.", delete_after=30)
            except Exception as e:
                await ctx.respond(f"Error fetching channel: {e}", ephemeral=True)
            return
        await ctx.respond("No announcement channel has been set for this server.", delete_after=30)
        return

    @commands.slash_command(name="getallannouncementchannels", description="Get all announcement channels for birthdays (ADMIN ONLY).")
    async def get_all_announcement_channels(self, ctx):

        if not ctx.author.guild_permissions.administrator:
            await ctx.respond("You do not have permission to view all announcement channels.", ephemeral=True)
            return
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(queries.GET_ALL_ANNOUNCEMENT_CHANNELS)
                announcement_channels = cursor.fetchall()
        except Exception as e:
            await ctx.respond(f"Failed to get all announcement channels: {e}", ephemeral=True)
            return

        list_of_channels = []
        for channel_info in announcement_channels:
            guild_id = channel_info['guild_id']
            channel_id = channel_info['channel_id']
            try:
                guild = self.bot.get_guild(guild_id)
                channel = guild.get_channel(channel_id) if guild else None
                if channel:
                    list_of_channels.append(f"{guild.name}: {channel.mention}")
            except Exception as e:
                print(f"Error fetching guild/channel: {e}")
        if list_of_channels:
            await ctx.respond("Announcement channels:\n" + "\n".join(list_of_channels), ephemeral=True)
            return
        await ctx.respond("No announcement channels have been set for any servers.", ephemeral=True)


def setup(bot):
    bot.add_cog(BirthdayAnnouncer(bot))
    print("BirthdayAnnouncer cog loaded.")
