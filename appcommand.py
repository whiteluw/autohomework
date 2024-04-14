import discord
from discord.ext import commands
from discord import app_commands

bot = commands.Bot(command_prefix="/")

@bot.tree.command(name='verify', description='创建一个认证')
@app_commands.describe(WkidotName='字符串类型')
async def verify(interaction: discord.Interaction, WkidotName: str):
    #添加代码

# 注册 '/code' 命令
@bot.tree.command(name='code', description='使用BRbot向你Wikidot收件箱发送的验证码')
@app_commands.describe(Code='整数，必须为6位数')
async def code(interaction: discord.Interaction, Code: int):
    #添加代码


# 运行Bot
bot.run('')
