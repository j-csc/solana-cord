import discord
from discord.ext import commands,tasks

class EpochTrackerCog(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.name_str = "Est: 0d 0h 0m ⇝ 0.00%"
        self.update_stake_status_presence.start()

    '''
    COMMANDS
    '''
    @commands.command(name='ooga')
    async def ooga(self, ctx):
        await ctx.send('OOGA OOGA OOGA!')
            
    '''
    TASKS
    '''
    @tasks.loop(seconds=30)
    async def update_stake_status_presence(self):
        epr = await self.bot.rpcClient.getEpochProgress()
        curr_progress = epr[0]
        est_time_remaining = epr[1]
        self.name_str = "{} ⇝ {}".format(est_time_remaining, curr_progress)
        desired_activity = discord.Activity(type=discord.ActivityType.playing, name=self.name_str)
        await self.bot.change_presence(activity=desired_activity)

def setup(bot):
    bot.add_cog(EpochTrackerCog(bot))