import discord
from discord.ext import commands,tasks

class EpochTrackerCog(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.name_str = "Est: 0d 0h 0m ⇝ 0.00%"
        self.est_remaining = "0d 0h 0m"
        self.update_stake_status_presence.start()
        self.broadcastTimeRemaining.start()
        
    '''
    HELPER
    '''
    def cog_unload(self):
        self.update_stake_status_presence.cancel()

    '''
    COMMANDS
    '''
    @commands.command(name='ooga')
    async def ooga(self, ctx):
        await ctx.send('OOGA OOGA OOGA!')
            
    '''
    TASKS
    '''
    @tasks.loop(minutes=15)
    async def broadcastTimeRemaining(self):
        # send message in channel
        time_disect = self.est_remaining.split(" ")
        if int(time_disect[0][:-1]) == 0 and (int(time_disect[1][:-1]) == 1 and (int(time_disect[2][:-1]) < 5 or int(time_disect[2][:-1]) > 1)) or (int(time_disect[1][:-1] == 0) and int(time_disect[2][-1] == 59)):
            embed = discord.Embed(title=f'1 hour remaining!', 
            description=self.name_str, colour=discord.Colour.gold())
        
            for channel in self.bot.config.bound_channels:
                chn = self.bot.get_channel(int(channel))
                await chn.send("@community The epoch is estimated to end in about an hour. Please complete any staking actions before the start of the next epoch.")
            
    @broadcastTimeRemaining.before_loop
    async def before_broadcast_update(self):
        # logger.info("Waiting for bot to initialize before loop...")
        await self.bot.wait_until_ready()
    
    @tasks.loop(minutes=15)
    async def update_stake_status_presence(self):
        epr = await self.bot.rpcClient.getEpochProgress()
        curr_progress = epr[0]
        est_time_remaining = epr[1]

        # Update instance vars
        self.est_remaining = est_time_remaining
        self.name_str = "{} ⇝ {}".format(est_time_remaining, curr_progress)

        desired_activity = discord.Activity(type=discord.ActivityType.playing, name=self.name_str)
        await self.bot.change_presence(activity=desired_activity)
    
    @update_stake_status_presence.before_loop
    async def before_status_update(self):
        # logger.info("Waiting for bot to initialize before loop...")
        await self.bot.wait_until_ready()
        

def setup(bot):
    bot.add_cog(EpochTrackerCog(bot))