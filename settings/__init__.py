import os, discord
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("bot_token")

PREFIX = "b!"
INTENTS = discord.Intents.all()

