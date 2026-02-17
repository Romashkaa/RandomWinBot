import telekit
import handlers

with open("token.txt") as token:
    TOKEN: str = token.read().strip()

telekit.Server(TOKEN).polling()
