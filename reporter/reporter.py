import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import asyncio


class Reports(commands.Cog):
    """
    Easy report system right here!
    """
    def __init__(self, bot):
        self.bot = bot
        self.coll = bot.plugin_db.get_partition(self)

    @commands.command()
    @checks.has_permissions(PermissionLevel.REGULAR)
    async def report(self, ctx):
        """
        Report a player.
        """

        staffChannel = self.bot.get_channel(742712457084272651)
        guestChannel = self.bot.get_channel(742712346312573020)
        texta = """**React with the type of your report:**
1️⃣ | Staff Report
2️⃣ | User Report
"""
        
        
        embed1 = discord.Embed(description=texta, color=self.bot.main_color)
        embed1.set_footer(text="React with ❌ to cancel")
        reactionmsg = await ctx.send(embed = embed1)
        for emoji in ('1️⃣', '2️⃣', '❌'):
          await reactionmsg.add_reaction(emoji)
        
        def checkmsg(msg: discord.Message):
          return msg.channel == ctx.channel and msg.author == ctx.author

        def check(r, u):
          return u == ctx.author
        
        reaction, user = await self.bot.wait_for("reaction_add", check=check)

        if str(reaction.emoji) == '1️⃣':
          await ctx.send("ok 1")
          await reactionmsg.clear_reactions()

          text = "Alright, we'll do a staff report. What is the username of the user you're reporting?\n1/5"
          await reactionmsg.edit(embed = discord.Embed(description=text, color=self.bot.main_color))
          username = await self.bot.wait_for('message', check=checkmsg)
          #await ctx.send(username.content)
          await username.delete()

          text = "What is the rank of the suspect?\n2/5"
          await reactionmsg.edit(embed = discord.Embed(description=text, color=self.bot.main_color))
          rank = await self.bot.wait_for('message', check=checkmsg)
          #await ctx.send(rank.content)
          await rank.delete()
          
          text = "What is the reason for this report?\n3/5"
          await reactionmsg.edit(embed = discord.Embed(description=text, color=self.bot.main_color))
          reason = await self.bot.wait_for('message', check=checkmsg)
          #await ctx.send(reason.content)
          await reason.delete()

          text = "Please provide proof of this happening. You can upload a video/image or use a link to an image or video.\n4/5"
          await reactionmsg.edit(embed = discord.Embed(description=text, color=self.bot.main_color))
          proof = await self.bot.wait_for('message', check=checkmsg)
          #await ctx.send(proof.content)
          my_files = [await x.to_file() for x in proof.attachments]
          await ctx.send(str(my_files))
          await proof.delete()

          reportEmbed = discord.Embed(description=f"Username: {username.content}\nRank: {rank.content}\nReason: {reason.content}\nProof: {proof.content}", color=self.bot.main_color)

          await staffChannel.send(embed = reportEmbed, files = my_files)
          text = "The report has successfully been sent!\n5/5"
          await reactionmsg.edit(embed = discord.Embed(description=text, color=self.bot.main_color))

        if str(reaction.emoji) == '2️⃣':
          #editmsg("Alright, we'll do a normal user report. What is the username of the user you're reporting?")
          return await ctx.send("coming soon")

        if str(reaction.emoji) == '❌':
          cancelEmbed = discord.Embed(description="❌ | Cancelled report", color=15158332)
          await reactionmsg.edit(embed=cancelEmbed)
          return await reactionmsg.clear_reactions() 

def setup(bot):
    bot.add_cog(Reports(bot))
