import os
import sys
import discord
from discord.ext.commands.core import guild_only
from discord.ext import commands
from core import defs

#bot = commands.Bot(command_prefix="$")
token = 'NzY5MTc0MzUzNjgxMTg2ODQ3.X5LLcA.wS1kqWBrwxiChZPYxTpmG73oozM'

class Bot(discord.Client):
    players = {}
    COR = 0xF7FE2E

    async def on_ready(self):
        await bot.change_presence(activity=discord.Game(name="Coding Python!"))
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

    async def on_message(self, message):

        if message.content.startswith('$ola'):
            await message.channel.send("Olá tudo bem!")
        
        if message.content.startswith('$help'):
            await message.author.create_dm()
            await message.author.dm_channel.send(
                f'Olá, vc pediu ajuda, segue ai uma lista de comando, para te ajudar'
            )
            await message.channel.send(
                f'Te mandei no privado {message.author}, da uma olhadinha lá'
            )
        if message.content.startswith('$entrar'):
            try:
                channel = message.author.voice.voice_channel
                await self.join_voice_channel(channel)
            except discord.errors.InvalidArgument:
                await message.channel.send("Já estou em um canal de voz.")
            except Exception as error:
                await message.channel.send("Ein Error: ```{error}```".format(error=error))

        if message.content.startswith('$sair'):
            try:
                mscleave = discord.Embed(
                    title="\n",
                    color=COR,
                    description="Sai do canal de voz e a musica parou!"
                )
                voice_client = client.voice_client_in(message.server)
                await client.send_message(message.channel, embed=mscleave)
                await voice_client.disconnect()
            except AttributeError:
                await message.channel.send("Não estou em nenhum canal de voz")
            except Exception as Hugo:
                await message.channel.send("Ein Error: ```{error}```".format(error=error))
        if message.content.startswith('$play'):
            try:
                yt_url = message.content[6:]
                if client.is_voice_connected(message.server):
                    try:
                        voice = client.voice_client_in(message.server)
                        players[message.server.id].stop()
                        player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                        players[message.server.id] = player
                        player.start()
                        mscemb = discord.Embed(
                            title="Música para tocar:",
                            color=COR
                        )
                        mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                        mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                        mscemb.add_field(name="Enviado em:", value="`{}`".format(player.uploaded_date))
                        mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploadeder))
                        mscemb.add_field(name="Duraçao:", value="`{}`".format(player.uploadeder))
                        mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                        mscemb.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                        await client.send_message(message.channel, embed=mscemb)
                    except Exception as e:
                        await client.send_message(message.server, "Error: [{error}]".format(error=e))

                if not client.is_voice_connected(message.server):
                    try:
                        channel = message.author.voice.voice_channel
                        voice = await client.join_voice_channel(channel)
                        player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                        players[message.server.id] = player
                        player.start()
                        mscemb2 = discord.Embed(
                            title="Música para tocar:",
                            color=COR
                        )
                        mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                        mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                        mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                        mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                        mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                        mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                        mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                        await client.send_message(message.channel, embed=mscemb2)
                    except Exception as error:
                        await message.channel.send("Error: [{error}]".format(error=error))
            except Exception as e:
                await client.send_message(message.channel, "Error: [{error}]".format(error=e))




    if message.content.startswith('$pause'):
        try:
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
            players[message.server.id].pause()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))
    if message.content.startswith('!resume'):
        try:
            mscresume = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscresume)
            players[message.server.id].resume()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))

bot = Bot()
bot.run(token)