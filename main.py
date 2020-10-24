import os
import sys
import discord
from discord.ext.commands.core import guild_only
from discord.ext import commands
from core import defs
import requests

#bot = commands.Bot(command_prefix="$")
token = 'NzY5MTc0MzUzNjgxMTg2ODQ3.X5LLcA.wS1kqWBrwxiChZPYxTpmG73oozM'

class Bot(discord.Client):
    players = {}
    COR = 0xF7FE2E
    msg_id = None
    msg_user = None

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

        if message.content.lower().startswith('$ola'):
            await message.channel.send("Olá tudo bem!")
        
        if message.content.lower().startswith('$help'):
            await message.author.create_dm()
            await message.author.dm_channel.send(
                f'Olá, vc pediu ajuda, segue ai uma lista de comando, para te ajudar'
            )
            await message.channel.send(
                f'Te mandei uma menssagem no privado {message.author.name}, da uma olhadinha lá'
            )
        if message.content.lower().startswith('$entrar'):
            try:
                channel = message.author.voice.channel
                await channel.connect()
            except discord.errors.InvalidArgument:
                await message.channel.send("Já estou em um canal de voz.")
            except Exception as error:
                await message.channel.send("Ein Error: ```{error}```".format(error=error))

        if message.content.lower().startswith('$sair'):
            try:
                mscleave = discord.Embed(
                    title="\n",
                    color=self.COR,
                    description="Sai do canal de voz e a musica parou!"
                )
                server = message.guild.voice_client
                await server.disconnect()
                await message.channel.send(embed=mscleave)

            except AttributeError:
                await message.channel.send("Não estou em nenhum canal de voz")
            except Exception as Hugo:
                await message.channel.send("Ein Error: ```{error}```".format(error=Hugo))
        if message.content.lower().startswith('$play'):
            try:
                yt_url = message.content[6:]
                try:

                    channel = message.author.voice.channel
                    await channel.connect()
                except:
                    await message.channel.send("Conecte-se a um canal de voz")
                
                server = message.guild.voice_client
                try:
                    player = await server.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()

                    mscemb2 = discord.Embed(
                        title="Música para tocar:",
                        color=self.COR
                    )

                    mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await message.channel.send(embed=mscemb2)

                except Exception as error:
                    await message.channel.send("Error: [{error}]".format(error=error))

            except Exception as e:
                await message.channel.send("Error: [{error}]".format(error=e))

        if message.content.lower().startswith('$pause'):
            try:
                mscpause = discord.Embed(
                    title="\n",
                    color=self.COR,
                    description="Musica pausada com sucesso!"
                )
                await message.channel.send(embed=mscpause)
                players[message.server.id].pause()
            except Exception as error:
                await message.channel.send("Error: [{error}]".format(error=error))
        if message.content.lower().startswith('$resume'):
            try:
                mscresume = discord.Embed(
                    title="\n",
                    color=self.COR,
                    description="Musica pausada com sucesso!"
                )
                await message.channel.send(embed=mscresume)
                players[message.server.id].resume()
            except Exception as error:
                await message.channel.send("Error: [{error}]".format(error=error))

        if message.content.lower().startswith("$lol"):
            embed1 =discord.Embed(
                title="Escolha sua area!",
                color=self.COR,
                description="- Dev Web = 🐤\n"
                            "- Dev Mobile  =  📘 \n"
                            "- Cientista de dados  = 📙\n"
                            "- Hacker = 💻\n",
                            )

            botmsg = await message.channel.send(embed=embed1)

            await botmsg.add_reaction("🐤")
            await botmsg.add_reaction("📘")
            await botmsg.add_reaction("📙")
            await botmsg.add_reaction("💻")


            self.msg_id = botmsg.id

            self.msg_user = message.author
    
        if message.content.lower().startswith("$gitstats"):
            menssagem = message.content.split(" ")
            if len(menssagem) > 2:
                await message.channel.send("Mais parametros que o esperado. Digite '$help' para receber ajuda.")
            elif len(menssagem) == 1:
                await message.channel.send("Menos parametros que o esperado. Digite '$help' para receber ajuda.")
            else:
                user = str(menssagem[1])
                e = discord.Embed(
                    title=f"Status de {user} no Git-Hub",
                    color=self.COR,
                    description=f"https://github-readme-stats.vercel.app/api?username={user}&show_icons=true&hide_border=true&count_private=true"
                )
                await message.channel.send(embed=e)

    async def on_reaction_add(self, reaction, user):
        msg = reaction.message

        if reaction.emoji == "🐤" and msg.id == self.msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Dev Web", msg.guild.roles)
            await user.add_roles(role)
            print("add")

        if reaction.emoji == "📘" and msg.id == self.msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Dev Mobile", msg.guild.roles)
            await user.add_roles(role)
            print("add")

        if reaction.emoji == "📙" and msg.id == self.msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Cientista de dados", msg.guild.roles)
            await user.add_roles(role)
            print("add")

        if reaction.emoji == "💻" and msg.id == self.msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Hacker", msg.guild.roles)
            await user.add_roles(role)
            print("add")

    async def on_reaction_remove(self, reaction, user):
        msg = reaction.message

        if reaction.emoji == "🐤" and msg.id == msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Dev Web", msg.guild.roles)
            await user.remove_roles(role)
            print("remove")

        if reaction.emoji == "📘" and msg.id == msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Dev Mobile", msg.guild.roles)
            await user.remove_roles(role)
            print("remove")

        if reaction.emoji == "📙" and msg.id == msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Cientista de dados", msg.guild.roles)
            await user.remove_roles(role)
            print("remove")
        if reaction.emoji == "💻" and msg.id == self.msg_id: #and user == msg_user:
            role = discord.utils.find(lambda r: r.name == "Hacker", msg.guild.roles)
            await user.remove_roles(role)
            print("remove")

bot = Bot()
bot.run(token)