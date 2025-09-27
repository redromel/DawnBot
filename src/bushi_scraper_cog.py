
from discord.ext import commands
from discord import Embed

import requests
import json
import os
import asyncio

API_BASE_URL = os.getenv("API_BASE_URL", "http://host.docker.internal:3000")


class BushiScraperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="getendeck", description="Given a JP Decklog, It will give an EN Bushiroad Decklog")
    async def get_en_deck(self, ctx, url: str, deck_name: str = None):
        # This is a long command
        await ctx.respond("Creating EN Deckilst...")

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

    # @commands.slash_command(name="getdecklist", description="Get Decklist for Deck to use for the https://sveclient.vercel.app/ sim")
    # async def get_decklist(self, ctx, url: str):
    #     await ctx.defer()
    #     body = {'url': url}
    #     response = requests.post(
    #         f"{API_BASE_URL}/decks/simDecklist", json=body)

    #     json_response = response.json()
    #     deck = json_response["deck"]

    #     if response.status_code >= 400:
    #         await ctx.followup.send(
    #             f'There was an error with the request: "{json_response["error"]}" ', ephemeral=True)
    #         return

    #     formatted_deck = f"```{deck}```"
    #     await ctx.followup.send(f"Decklist for https://sveclient.vercel.app/ Created:\n{formatted_deck}")
    #     return

    @commands.slash_command(
        name="getendeck",
        description="Given a JP Decklog, it will give an EN Bushiroad Decklog"
    )
    async def get_en_deck(self, ctx, url: str, deck_name: str = None):

        await ctx.respond(
            f"Working on your decklist, {ctx.author.mention}...", ephemeral=True
        )

        async def do_work():
            body = {"url": url, "deck_name": deck_name}
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(
                        f"{API_BASE_URL}/decks/bushiDecklist", json=body, timeout=120
                    )
                )
                json_response = response.json()

                if response.status_code >= 400:
                    await ctx.channel.send(
                        f"Error for {ctx.author.mention}: {json_response.get('error', 'Unknown error')}", ephemeral=True
                    )
                    return

                await ctx.channel.send(
                    f"EN Decklink for {ctx.author.mention}: {json_response['url']}"
                )

            except Exception as e:
                await ctx.channel.send(
                    f"Failed for {ctx.author.mention}: {e}", ephemeral=True
                )

        self.bot.loop.create_task(do_work())

    @commands.slash_command(
        name="comparedecks",
        description="Compare 2 Decks to see what cards were removed, added, or changed"
    )
    async def compare_decks(self, ctx, old_deck_url: str, new_deck_url: str):

        await ctx.respond(f"Comparing decks for {ctx.author.mention}...")

        async def do_work():
            body = {"urlA": old_deck_url, "urlB": new_deck_url}
            try:
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: requests.post(f"{API_BASE_URL}/decks/compare", json=body, timeout=120)
                )
                json_response = response.json()

                if response.status_code >= 400:
                    await ctx.channel.send(
                        f"Error for {ctx.author.mention}: {json_response.get('error', 'Unknown error')}"
                    )
                    return


                take_out, same_card, slot_in = embed_builder(json_response)
                title_a = json_response["details"]["titleA"]
                title_b = json_response["details"]["titleB"]
                embed = Embed(
                    title=f'Comparing {title_a} to {title_b}',
                    color=0xC8A2C8  
                )
                embed.add_field(
                    name="Keep Cards",
                    value="\n".join(same_card) if same_card else "None",
                    inline=False
                )
                embed.add_field(
                    name="Take Out",
                    value="\n".join(take_out) if take_out else "None",
                    inline=False
                )
                embed.add_field(
                    name="Slot In",
                    value="\n".join(slot_in) if slot_in else "None",
                    inline=False
                )
                embed.set_footer(text="Powered by BushiScraper")

                await ctx.channel.send(embed=embed)

            except Exception as e:
                await ctx.channel.send(
                    f"Failed to compare decks for {ctx.author.mention}: {e}"
                )

        # Run in background
        self.bot.loop.create_task(do_work())

def embed_builder(response):

    decks = response["details"]
    take_out = []
    same_card = []
    slot_in = []

    for card in decks["sameCard"]:
        same_card.append(f"{card['quantity']} {card['card_name']}")
    for card in decks["removedCards"]:
        take_out.append(f"{card['quantity']} {card['card_name']}")
    for card in decks["addedCards"]:
        slot_in.append(f"{card['quantity']} {card['card_name']}")

    return take_out, same_card, slot_in


def setup(bot):
    bot.add_cog(BushiScraperCog(bot))
    print("BushiScraperCog loaded successfully")
