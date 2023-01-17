import datetime
import os
import random
import logging
import asyncio

import discord
import psycopg2
from discord.ext.commands import Bot, Cog
from discord.ext.tasks import loop
from discord import app_commands as commands

from crud import BotConnector

logging.basicConfig(level=logging.INFO)

class BonkBot(Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="*",
                         intents=intents)
        self.bonks: list[str] = self._fetch_bonks()
        self.database: None | BotConnector = None
        self.mute_role: None | discord.Role = None

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

    async def on_ready(self):
        print(f"{self.user.name} is ready to engage!")


@commands.context_menu(name="Bonker")
async def bonk_context(ctx: discord.Interaction, usr: discord.User):
    await ctx.response.send_message(f'All bonk {usr.mention}!', ephemeral=True)


class BonkCog(Cog):
    def __init__(self, bot):
        self.bot: BonkBot = bot
        self.resync_tree.start()
        self.truncate_bonk_cache.start()

    @loop(seconds=60)
    async def truncate_bonk_cache(self):
        self.bot.database.delete_all_bonks_before_date(datetime.datetime.now() - datetime.timedelta(minutes=10))
        logging.info("Truncated bonk cache, affected rows: %s", self.bot.database.cursor.rowcount)

    @loop(hours=1)
    async def resync_tree(self):
        logging.info(f"Resyncing tree, with {len(self.bot.tree.get_commands())} commands")
        await self.bot.tree.sync()

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

    @commands.command(name="bonk", description="Bonk your friends!")
    async def ping(self, ctx: discord.Interaction, usr: discord.Member):
        await ctx.response.defer()  # This often takes a while, so response is deferred and followup webhook will be used instead
        if not self.bot.mute_role:
            self.bot.mute_role = ctx.guild.get_role(876940414500872242)
        try:
            self.bot.database.insert_new_bonk(ctx.user.id, usr.id)
            await ctx.followup.send(embed=self._generate_embed(ctx.user, usr))
        except psycopg2.Error as e:
            await ctx.followup.send("Something went wrong, report sent, please try again later!", ephemeral=True)
            logging.exception("Something went wrong with bonk command, passing full error track to stdout")
            print(e.pgcode, e.pgerror, e.diag.message_detail, sep='\n')

        if len(self.bot.database.get_all_bonks_by_user_bonked(usr.id)) >= 4:
            await usr.add_roles(self.bot.mute_role)
            await ctx.followup.send(f"💬 Horny timeout for {usr.mention}! 10 minutes")

            # TODO migrate to database
            await asyncio.sleep(600)

            await usr.remove_roles(self.bot.mute_role)
            await ctx.followup.send(f"💬 Horny timeout for {usr.mention} is over!")

    @commands.command(name="bonklist", description="List all bonks!")
    async def bl(self, ctx: discord.Interaction):
        await ctx.response.defer()
        for bonk in self.bot.bonks:
            # TODO fetch image with requests and send as file instead of sending url
            await ctx.followup.send(bonk)


bot = BonkBot()
bot.run(os.getenv("TOKEN"))

