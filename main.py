import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

# Get the token from the .env file
token = os.getenv('DISCORD_TOKEN')
if not token:
    raise ValueError("No DISCORD_TOKEN found in .env file")
casual_server_id = os.getenv('CASUAL_SERVER_ID')
if not casual_server_id:
    raise ValueError("No CASUAL_SERVER_ID found in .env file")

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

        try:
            GUILD_ID = discord.Object(id=casual_server_id)
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} commands to ({GUILD_ID.id})')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('~hello'):
            await message.channel.send(f'world!!!')
        if message.content.startswith('~bye'):
            await message.channel.send(f'bye bsdk!!!')

    async def on_reaction(self, reaction, user):
        if reaction.emoji == '🖕':
            await reaction.message.channel.send(f'{user} lund dikhana hai kya?')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.presences = True
intents.voice_states = True
intents.guild_messages = True
intents.dm_messages = True
intents.dm_reactions = True
intents.dm_typing = True



client = Client(command_prefix='~', intents=intents)

GUILD_ID = discord.Object(id=casual_server_id)

@client.tree.command(name="hello", description="replies world!!!", guild=GUILD_ID)
async def reply_world(interaction: discord.Interaction):
    await interaction.response.send_message('world!!!')

@client.tree.command(name="add", description="adds two numbers", guild=GUILD_ID)
async def reply_world(interaction: discord.Interaction, num1: int, num2: int):
    await interaction.response.send_message(f'{num1} + {num2} = {num1 + num2}')


client.run(token)