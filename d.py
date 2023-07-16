# Made by zyqs
# V1.3.5
import subprocess
import discord
from discord.ext import commands, tasks
import sys
import json
import os
import asyncio

def execute_main_py():
    subprocess.call(["python", "main.py"])

def update_scan_speed_watcher(value):
    config_file = "config.json"

    if os.path.exists(config_file):
        with open(config_file, "r+") as file:
            config = json.load(file)
            config["scan_speed_watcher1"] = value
            config["scan_speed_watcher2"] = value
            file.seek(0)
            json.dump(config, file, indent=4)
            file.truncate()
    else:
        print("Config file not found.")

# Bot config
bot_token = "TOKEN"
command_prefix = "!"
owner_id = "OWNER ID"
auto_restart_interval = 60  # You can change with !autorestart <minutes>

intents = discord.Intents.default()

# Restart command
bot = commands.Bot(command_prefix=command_prefix, intents=intents)


@bot.command()
async def restart(ctx):
    if ctx.author.id == int(owner_id):
        await ctx.send('Restarting...')

        command = [sys.executable, __file__]

        subprocess.Popen(command)
        await bot.close()
    else:
        await ctx.send('You can\'t use this command.')


# Auto restart command
@bot.command()
async def autorestart(ctx, status: str = None):
    if ctx.author.id == int(owner_id):
        if status == 'on':
            autorestart_task.start()
            await ctx.send('Auto restart is now on.')
        elif status == 'off':
            autorestart_task.stop()
            await ctx.send('Auto restart is now off.')
        else:
            try:
                new_interval = int(status)
                if new_interval > 0:
                    global auto_restart_interval
                    auto_restart_interval = new_interval
                    await ctx.send(f'Auto restart interval set to {new_interval} minutes.')
                else:
                    await ctx.send('Please provide a number for the new interval.')
            except ValueError:
                await ctx.send('Invalid input. Please provide either "on", "off", or a number for the new interval.')
    else:
        await ctx.send('You can\'t use this command.')


@bot.command()
async def fastsnipe(ctx):
    if ctx.author.id == int(owner_id):
        update_scan_speed_watcher("1.1")
        await ctx.send('Scan speed watcher values updated: 1.1')
        command = [sys.executable, "main.py"]
        subprocess.Popen(command)
        await asyncio.sleep(15)
        update_scan_speed_watcher("0.2")
        await ctx.send('Scan speed watcher values updated: 0.2')
    else:
        await ctx.send('You can\'t use this command.')
        
@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user.name}')
    execute_main_py()
    
# Auto restart task
@tasks.loop(minutes=auto_restart_interval)
async def autorestart_task():
    command = [sys.executable, __file__]
    subprocess.Popen(command)
    await bot.close()
    
bot.run(bot_token)
