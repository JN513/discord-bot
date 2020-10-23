import os
import sys
import discord
from discord.ext.commands.core import guild_only
from discord.ext import commands
from core import defs

#bot = commands.Bot(command_prefix="$")
token = 'NzY5MTc0MzUzNjgxMTg2ODQ3.X5LLcA.wS1kqWBrwxiChZPYxTpmG73oozM'

class Bot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, Bem vindo ao meu servidor!'
        )
    
    async def on_member_remove(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Olá {member.name}, Voce foi removido do servidor por ter cometido alguma inflação.'
        )

    async def on_message(self, message, member):

        if message.content.startswith('$ola'):
            await message.channel.send("Olá tudo bem!")
        
        elif message.content.startswith('$help'):
            await member.create_dm()
            await member.dm_channel.send(
                f'Olá, vc pediu ajuda, segue ai uma lista de comando, para te ajudar'
            )
            await message.channel.send(
                f'Te mandei no privado @{member.name}, da uma olhadinha lá'
            )

bot = Bot()
bot.run(token)