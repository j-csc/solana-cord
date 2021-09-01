from epochbot.bot import EpochBot

def main():
    bot = EpochBot()
    cogs = ['epochbot.cogs.epochTracker']
    for cog in cogs:
        bot.load_extension(cog)
    bot.run()
        
if __name__ == "__main__":
    main()