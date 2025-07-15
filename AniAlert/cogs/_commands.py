from AniAlert.db.database import cursor, conn

from AniAlert.cogs.cogs.seasonal import SeasonalAnimeLookUpCog
from AniAlert.cogs.cogs.search import AllAnimeSearchCog
from AniAlert.cogs.cogs.remove import RemoveAnimeCog
from AniAlert.cogs.cogs.notify_list import CheckNotifyListCog
from AniAlert.cogs.cogs.notify_airing import NotifyAnimeAiredCog
from AniAlert.cogs.cogs.clear_notify_list import ClearNotifyListCog
from AniAlert.cogs.cogs.random import RandomAnimeCog
from AniAlert.cogs.cogs.guess import GuessAnimeCog
from AniAlert.cogs.cogs.schedule import ScheduleCog


async def setup(bot):
  await bot.add_cog(SeasonalAnimeLookUpCog(bot))
  await bot.add_cog(AllAnimeSearchCog(bot))
  await bot.add_cog(CheckNotifyListCog(bot, cursor))
  await bot.add_cog(NotifyAnimeAiredCog(bot, cursor, conn))
  await bot.add_cog(RemoveAnimeCog(bot, cursor, conn))
  await bot.add_cog(ClearNotifyListCog(bot, cursor, conn))
  await bot.add_cog(RandomAnimeCog(bot))
  await bot.add_cog(GuessAnimeCog(bot))
  await bot.add_cog(ScheduleCog(bot))
