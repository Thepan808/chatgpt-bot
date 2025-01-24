# ©️biisal jai shree krishna 😎
from os import environ
from dotenv import load_dotenv

load_dotenv()

API_ID = environ.get("API_ID" , "4954361")
API_HASH = environ.get("API_HASH" , "43a786a8548a30f9d6887e36d53c0e64")
BOT_TOKEN = environ.get("BOT_TOKEN" , "6390154239:AAG1raMRKyIyeZNh8q0BIb8FJVn1t5HiExU")
ADMIN = int(environ.get("ADMIN" , "737737727"))
CHAT_GROUP = int(environ.get("CHAT_GROUP", "-1001745424158"))
LOG_CHANNEL = environ.get("LOG_CHANNEL", "-1001509201180")
MONGO_URL = environ.get("MONGO_URL" , "mongodb+srv://thepanda:thepanda@cluster0.tumon.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
AUTH_CHANNEL = int(
    environ.get("AUTH_CHANNEL", "-1001509201180")
)
FSUB = environ.get("FSUB", False)
STICKERS_IDS = (
    "CAACAgQAAxkBAAEK99dlfC7LDqnuwtGRkIoacot_dGC4zQACbg8AAuHqsVDaMQeY6CcRojME"
).split()
COOL_TIMER = 20  # keep this atleast 20
ONLY_SCAN_IN_GRP = environ.get(
    "ONLY_SCAN_IN_GRP", True
)  # If IMG_SCAN_IN_GRP is set to True, image scanning is restricted to your support group only. If it's False, the image scanning feature can be used anywhere.
REACTIONS = ["❤️‍🔥", "⚡", "🔥"]
