import discord
from discord.ext import commands
import google.generativeai as genai
import os
import asyncio

BOT_TOKEN = "MTUzNjYwODE2NDk5MDk0NzQ0OA.GVve9g.ndbvvBc28n7IaYYoa5EtgikoQSoKJVQqFOmPIk"
GEMINI_API_KEY = "AQ.Ab8RN6KcM7UB0uTn9vxP_y1BSFPPRVW5ldehsNLprXHlJaCsyg"
BOT_PREFIX = "/"
CHANNEL_ID = 1506171439785447538
ROLE_ID = 1506170898854449163

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot Hidup: {bot.user}")
    print("Berjaya bersambung ke Discord!")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    role = discord.utils.get(member.guild.roles, id=ROLE_ID)
    if role:
        await member.add_roles(role)
    if channel:
        await channel.send(f"Selamat datang {member.mention} ke server! 🎉")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"Selamat tinggal {member.name}... 😢")

@bot.command()
async def tanya(ctx, *, soalan):
    await ctx.send("Saya sedang berfikir... 🤔")
    try:
        response = model.generate_content(soalan)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"Maaf, berlaku ralat: {e}")

@bot.command()
async def hai(ctx):
    await ctx.send(f"Hai {ctx.author.mention}! 👋 Apa khabar?")

@bot.command()
async def server(ctx):
    await ctx.send(f"Nama Server: {ctx.guild.name}\nJumlah Ahli: {ctx.guild.member_count}")

bot.run(BOT_TOKEN)
