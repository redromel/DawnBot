
from discord.ext import commands
from discord import Embed

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

        json_response = response.json()
        deck = json_response["deck"]

        if response.status_code >= 400:
            await ctx.followup.send(
                f'There was an error with the request: "{json_response["error"]}" ', ephemeral=True)
            return

        formatted_deck = f"```{deck}```"
        await ctx.followup.send(f"Decklist for https://sveclient.vercel.app/ Created:\n{formatted_deck}")
        return

    @commands.slash_command(name="comparedecks", description="Compare 2 Decks to see what cards were removed, added, or changed")
    async def compare_decks(self, ctx, old_deck_url: str, new_deck_url: str):
        await ctx.defer()
        body = {'urlA': old_deck_url, 'urlB': new_deck_url}

        response = requests.post(f"{API_BASE_URL}/decks/compare", json=body)

        json_response = response.json()

        if response.status_code >= 400:
            await ctx.followup.send(
                f'There was an error with the request: "{json_response["error"]}" ', ephemeral=True)
            return

        take_out, same_card, slot_in = embed_builder(json_response)

        embed = Embed(
            title="Deck Comparison",
            color= 200
        )
        
        embed.add_field(name="Keep Cards", value="\n".join(same_card), inline=False)
        embed.add_field(name="Take Out", value="\n".join(take_out), inline=False)
        embed.add_field(name="Slot In", value="\n".join(slot_in), inline=False)
        embed.set_footer(text="Powered by BushiScraper")
        
        
        await ctx.followup.send(embed=embed)
        return


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
