import discord
from discord.ext import commands
import asyncio

# 設定機器人前綴與 Intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 儲存當前拍賣狀態
current_auction = {
    "active": False,
    "item": None,
    "highest_bid": 0,
    "highest_bidder": None,
    "channel_id": None
}

@bot.event
async def on_ready():
    print(f"機器人已成功上線：{bot.user.name}")

# 1. 發起拍賣指令：!start_auction <物品名稱> <起標價> <持續秒數>
@bot.command()
async def start_auction(ctx, item_name: str, starting_price: int, duration: int):
    if current_auction["active"]:
        await ctx.send("❌ 目前已經有一個拍賣正在進行中！")
        return

    # 初始化拍賣資料
    current_auction["active"] = True
    current_auction["item"] = item_name
    current_auction["highest_bid"] = starting_price
    current_auction["highest_bidder"] = None
    current_auction["channel_id"] = ctx.channel.id

    embed = discord.Embed(
        title="📢 拍賣正式開始！",
        description=f"**拍賣物品：** {item_name}\n"
                    f"**起標金額：** ${starting_price}\n"
                    f"**競標時間：** {duration} 秒\n\n"
                    f"請使用 `!bid <金額>` 參與競標！",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

    # 倒數計時
    await asyncio.sleep(duration)

    # 結算拍賣
    if current_auction["highest_bidder"] is None:
        await ctx.send(f"⏰ 拍賣結束！物品 **{item_name}** 流標（無人出價）。")
    else:
        winner = current_auction["highest_bidder"]
        price = current_auction["highest_bid"]
        await ctx.send(f"🎉 **拍賣結束！**\n恭喜 {winner.mention} 以 **${price}** 贏得 **{item_name}**！")

    # 重置拍賣狀態
    current_auction["active"] = False

# 2. 出價指令：!bid <金額>
@bot.command()
async def bid(ctx, amount: int):
    if not current_auction["active"]:
        await ctx.send("❌ 目前沒有正在進行的拍賣。")
        return

    if ctx.channel.id != current_auction["channel_id"]:
        await ctx.send("❌ 請在發起拍賣的頻道中喊價！")
        return

    # 檢查出價是否高於當前最高價
    if amount <= current_auction["highest_bid"]:
        await ctx.send(f"⚠️ 出價失敗！您的出價必須高於當前金額 **${current_auction['highest_bid']}**。")
        return

    # 更新最高出價者資訊
    current_auction["highest_bid"] = amount
    current_auction["highest_bidder"] = ctx.author

    await ctx.send(f"✅ {ctx.author.mention} 出價 **${amount}**！成為目前的最高出價者！")

# 填入你的 Bot Token
bot.run("L6Z2OCMvrcYFFTW5Oj9zhvtoVm8zRPEY")
