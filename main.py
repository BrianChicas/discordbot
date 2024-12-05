import discord
import os
import random
from discord.ext import commands
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata

# Load environment variables
load_dotenv("token.env")

# Bot setup
token = os.getenv('TOKEN')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True


client = commands.Bot(command_prefix="!", intents=intents)


# Command example
@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Event: Bot ready
@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

# Event: Message handling
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return

    if channel == "random":
        if user_message.lower() in ["hello", "hi"]:
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
            return
        elif user_message.lower() == "tell me a joke":
            jokes = [
                "Your R6 Aim",
                "What has a head but no Brain? Derry.",
                "Yo mama is like an arcade game—give her a quarter and she’ll play with your joystick."
            ]
            await message.channel.send(random.choice(jokes))
            return
        elif user_message.lower() == "region":
            await message.channel.send(f'Your EC2 region is {ec2_metadata.region}')
            return
        elif user_message.lower() == "ip":
            await message.channel.send(f'Your public IP is {ec2_metadata.public_ipv4}')
            return
        elif user_message.lower() == "zone":
            await message.channel.send(f'Your availability zone is {ec2_metadata.availability_zone}')
            return
        elif user_message.lower() == "tell me about my server":
            await message.channel.send(
                f'Your EC2 region is {ec2_metadata.region}, Your public IP is {ec2_metadata.public_ipv4}, '
                f'Your availability zone is {ec2_metadata.availability_zone}')
            return

    # Allow commands to work
    await client.process_commands(message)