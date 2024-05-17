import datetime
import io
import os
import random
import logging
import asyncio

import requests
import discord
import psycopg2
from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop
from discord import app_commands as commands

from crud import BotConnector
# from games import Waifu_Cog, Game_Cog

logging.basicConfig(level=logging.INFO)


class BonkBot(Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="*",
                         intents=intents)
        self.bonks: list[str] = self._fetch_bonks()
        self.database: None | BotConnector = None
        self.base_color = discord.Color(0xfc8cac)

    async def setup_hook(self) -> None:
        await self.add_cog(BonkCog(self))

        await self.tree.sync()
        self._connect_database()
        print(self.tree.get_commands())

    def _connect_database(self) -> None:
        self.database = BotConnector(os.getenv("DB_HOST"),
                                     os.getenv("DB_USER"),
                                     os.getenv("DB_PASS"),
                                     os.getenv("DB_NAME"), use_ssh=False)

    @staticmethod
    def _fetch_bonks() -> list[str]:
        with open("bonks.txt", "r") as f:
            return f.read().split('\n')[:-1]

    def write_bonks(self) -> None:
        with open("bonks.txt", "w") as f:
            f.write('\n'.join(self.bonks))

    def append_bonk(self, bonk: str) -> None:
        with open("bonks.txt", "a") as f:
            f.write(bonk + '\n')
        self.bonks.append(bonk)

    async def on_ready(self):
        print(f"{self.user.name} is ready to engage!")


class BonkCog(Cog):
    def __init__(self, bot):
        self.bot: BonkBot = bot
        self.resync_tree.start()
        self.truncate_bonk_cache.start()
        self.log_channel: discord.TextChannel = None

    async def cog_load(self) -> None:
        self.log_channel = await self.bot.fetch_channel(785892784359079936)
    
    @loop(seconds=60)
    async def truncate_bonk_cache(self):
        count = self.bot.database.delete_all_bonks_before_date(datetime.datetime.now() - datetime.timedelta(minutes=10))
        logging.info("Truncated bonk cache, affected rows: %s", count)

    @loop(hours=1)
    async def resync_tree(self):
        logging.info(f"Resyncing tree, with {len(self.bot.tree.get_commands())} commands")
        await self.bot.tree.sync()
        print(self.bot.tree.get_commands())

    @resync_tree.before_loop
    async def before_resync_tree(self):
        await self.bot.wait_until_ready()

    @truncate_bonk_cache.before_loop
    async def before_truncate_bonk_cache(self):
        await self.bot.wait_until_ready()

    def _generate_embed(self, bonker: discord.Member, bonked: discord.Member):
        embed = discord.Embed(title=f"**{bonker.display_name}** bonks **{bonked.display_name}**! "
                                    f"{random.choice(['Ouch!', 'Ow!', 'That must have hurt!'])}",
                              color=discord.Color(0xfc8cac))
        embed.set_image(url=random.choice(self.bot.bonks))
        return embed

    @commands.command(name="add", description="Add new image to collection!")
    async def suggest(self, ctx: discord.Interaction, attachment: discord.Attachment):
        await ctx.response.defer()

        embed = discord.Embed(title=f"New image added, by {ctx.user.mention}!", color=self.bot.base_color)
        embed.set_image(url=attachment.url)

        view = discord.ui.View()
        view.add_item(BonkDenyButton(attachment.url, self.bot))

        await self.log_channel.send(embed=embed, view=view)

        self.bot.append_bonk(attachment.url)
        await ctx.followup.send("Image added to collection!")

    @commands.command(name="bonk", description="Bonk your friends!")
    async def ping(self, ctx: discord.Interaction, usr: discord.Member = None):
        await ctx.response.defer()  # This often takes a while, so response is deferred and followup webhook will be used instead

        if not usr:
            usr = ctx.message.mentions[0]
            print(usr.id)

        try:
            self.bot.database.insert_new_bonk(ctx.user.id, usr.id)
            await ctx.followup.send(embed=self._generate_embed(ctx.user, usr))
        except psycopg2.Error as e:
            await ctx.followup.send("Something went wrong, report sent, please try again later!", ephemeral=True)
            logging.exception("Something went wrong with bonk command, passing full error track to stdout")
            print(e.pgcode, e.pgerror, e.diag.message_detail, sep='\n')

        if len(self.bot.database.get_all_bonks_by_user_bonked(usr.id)) >= 4:
            try:
                await usr.timeout(datetime.timedelta(minutes=10), reason="Horny")
                await ctx.followup.send(f"💬 Horny timeout for {usr.mention}! 10 minutes")
            except discord.Forbidden:
                await ctx.followup.send(f"💬 Error: Missing permissions")
                logging.exception("Couldn't timeout user, missing permissions")
            finally:
                self.bot.database.delete_all_bonks_by_user_bonked(usr.id)


class BonkDenyButton(discord.ui.Button):
    def __init__(self, target_img: str, bot: BonkBot):
        super().__init__(style=discord.ButtonStyle.red, label="Delete")
        self.target_img = target_img
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        try:
            self.bot.bonks.remove(self.target_img)
            await interaction.response.send_message("Image removed from stack!", ephemeral=True)
        except ValueError:
            logging.error("Image not found in stack, ignoring")
            await interaction.followup.send("Image was already removed", ephemeral=True)
        self.bot.write_bonks()
        self.disabled = True
        view = discord.ui.View()
        view.add_item(self)
        await interaction.message.edit(view=view)

bot = BonkBot()
bot.run(os.getenv("TOKEN"))

