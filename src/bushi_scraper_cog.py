
from discord.ext import commands


import requests
import json
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://host.docker.internal:3000")


class BushiScraperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="getendeck", description="Given a JP Decklog, It will give an EN Bushiroad Decklog")
    async def get_en_deck(self, ctx, url: str, deck_name: str = None):
        # This is a long command
        await ctx.defer()
        body = {'url': url, 'deck_name': deck_name}
        response = requests.post(
            f"{API_BASE_URL}/decks/bushiDecklist", json=body)
        json_response = response.json()

        if response.status_code >= 400:
            await ctx.followup.send(
                f'There was an error with the request: "{json_response["error"]}" ', ephemeral=True)
            return
        await ctx.followup.send(
            f'EN Decklink successfully created:  {json_response["url"]}')
        return

    @commands.slash_command(name="getdecklist", description="Get Decklist for Deck to use for the https://sveclient.vercel.app/ sim")
    async def get_decklist(self, ctx, url: str):
        await ctx.defer()
        body = {'url': url}
        response = requests.post(
            f"{API_BASE_URL}/decks/simDecklist", json=body)

        if response.status_code >= 400:
            await ctx.followup.send(
                f'There was an error with the request: "{json_response["error"]}" ', ephemeral=True)
            return

        json_response = response.json()
        deck = json_response["deck"]
        formatted_deck = f"```{deck}```"
        await ctx.followup.send(f"Decklist for https://sveclient.vercel.app/ Created:\n{formatted_deck}")
        return


def setup(bot):
    bot.add_cog(BushiScraperCog(bot))
    print("BushiScraperCog loaded successfully")
