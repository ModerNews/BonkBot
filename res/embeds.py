import datetime

import discord
from discord import Member, User, Colour

from typing import Union, Optional, Literal

# region Violation Embeds

class BanEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Zbanowano {f'{member} (*{member.id}*)' if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Banned user {f'{member} (*{member.id}*)' if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.red())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)


class KickEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Wyrzucono {f'{member} (*{member.id}*)' if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Kicked user {f'{member} (*{member.id}*)' if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.red())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)


class UnbanEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Odbanowano {member.mention if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Unbaned user {member.mention if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.dark_green())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)


class WarnEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Ostrzeżono {member.mention if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Warned user {member.mention if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.orange())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)


class MuteEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Wyciszono {member.mention if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Muted user {member.mention if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.yellow())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)


class UnmuteEmbed(discord.Embed):
    def __init__(self, member: Union[Member, User, int], moderator: Union[Member, User, int], reason: Optional[str], case_id: int = None, lang: Literal["pl", "en"] = "en"):
        super().__init__(title=f"{'Sprawa' if lang == 'pl' else 'Case'} #{case_id if case_id >= 10 else f'0{case_id}'}",
                         description=f"Odciszono {member.mention if not isinstance(member, int) else f'o id {member}'}"
                                     if lang == 'pl' else
                                     f"Unmuted user {member.mention if not isinstance(member, int) else f'with id {member}'}",
                         colour=Colour.green())
        self.add_field(name='Moderator:', value=moderator.mention if not isinstance(moderator, int) else f"<@!{moderator}>")
        self.add_field(name="Powód:" if lang == "pl" else 'Reason:', value=reason if reason is not None and reason != "" else "Brak" if lang == "pl" else 'Unprovided')
        self.set_footer(text='Aby zobaczyć wszystkie wykroczenia użytkownika wpisz `*warns [member]'
                             if lang == "pl" else
                             'To see all user violations use `*warns [member]`')
        if isinstance(member, Member):
            if member.guild_avatar is not None:
                self.set_thumbnail(url=member.guild_avatar.url)
            else:
                self.set_thumbnail(url=member.avatar.url)
        elif isinstance(member, User):
            self.set_thumbnail(url=member.avatar.url)
#endregion


class WaifuEmbed(discord.Embed):
    def __init__(self, name: str, title: str, icon_url: str, *, trap: bool = False, hanime: bool = False):
        super().__init__(title=name, description=f"From **{title}**", colour=0xfc8cac)
        self.set_image(url=icon_url)
        self.add_field(name="Trap", value=trap)
        self.add_field(name="Hentai", value=hanime)
        now = datetime.datetime.utcnow()
        self.set_footer(text=f"Added at: {now.strftime('%d/%m/%y %H:%M')}")
