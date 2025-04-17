# The project
The goal is to make a wrapper around the various oldschool runescape api's.

## osrs hiscores
```py
import asyncio

from aiohttp import ClientSession

from osrs.asyncio import Hiscore, HSMode
from osrs.utils import RateLimiter
from osrs.exceptions import PlayerDoesNotExist


async def main():
    # 100 calls per minute
    limiter = RateLimiter(calls_per_interval=100, interval=60)
    hiscore_instance = Hiscore(proxy="", rate_limiter=limiter)
    
    async with ClientSession() as session:
        player_stats = await hiscore_instance.get(
            mode=HSMode.OLDSCHOOL,
            player="extreme4all",
            session=session,
        )
        print(player_stats)

    # if you do not provide a session we'll make one for you, this session will not be reused
    # for multiple requests we advice doing that within one session like the example above
    player_stats = await hiscore_instance.get(
        mode=HSMode.OLDSCHOOL,
        player="extreme4all",
    )
    print(player_stats)
# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
```
## osrs itemdb (Catalogue & Grand Exchange)
```py
import asyncio

from aiohttp import ClientSession

from osrs.asyncio import ItemDBMode, Catalogue, Graph
from osrs.utils import RateLimiter

async def main():
    # Initialize the Catalogue with optional proxy and rate limiter
    limiter = RateLimiter(calls_per_interval=100, interval=60)
    catalogue_instance = Catalogue(proxy="", rate_limiter=limiter)
    graph_instance = Graph(proxy="", rate_limiter=limiter)

    async with ClientSession() as session:
        # Example 1: Fetching items by alphabetical filter
        alpha = "A"  # Items starting with "A"
        page = 1     # First page of results
        category = 1 # Category identifier, for OSRS there is only 1 category
        items = await catalogue_instance.get_items(
            session, 
            alpha=alpha, 
            page=page, 
            mode=ItemDBMode.OLDSCHOOL, 
            category=category
        )
        print("Fetched Items:", items)

        # Example 2: Fetching detailed information for a specific item
        item_id = 4151  # Example item ID (Abyssal whip in OSRS)
        item_detail = await catalogue_instance.get_detail(
            session, 
            item_id=item_id, 
            mode=ItemDBMode.OLDSCHOOL
        )
        print("Item Detail:", item_detail)

        # Example 3: Fetching historical trade data (price graph) for a specific item
        item_id = 4151  # Example item ID (Abyssal whip in OSRS)
        trade_history = await graph_instance.get_graph(
            session, 
            item_id=item_id, 
            mode=ItemDBMode.OLDSCHOOL
        )
        print("Trade History:", trade_history)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
```
## wiki prices
the wiki via runelite collects item price, which they expose via an api.
```py
import asyncio

from aiohttp import ClientSession

from osrs.asyncio import WikiPrices, Interval
from osrs.utils import RateLimiter

async def main():
    limiter = RateLimiter(calls_per_interval=100, interval=60)
    prices_instance = WikiPrices(user_agent="Your User Agent", rate_limiter=limiter)

    async with ClientSession() as session:
        # Fetch item mappings
        mappings = await prices_instance.get_mapping(
            session=session
        )
        print("Item Mappings:", mappings)

        # Fetch latest prices
        latest_prices = await prices_instance.get_latest_prices(
            session=session
        )
        print("Latest Prices:", latest_prices)

        # Fetch average prices
        average_prices = await prices_instance.get_average_prices(
            session=session, 
            interval=Interval.FIVE_MIN
        )

        print("Average Prices:", average_prices)

        # Fetch time series data
        item_id = 4151  # Example item ID (Abyssal whip in OSRS)
        time_series = await prices_instance.get_time_series(
            session=session, 
            item_id=item_id, 
            timestep=Interval.ONE_HOUR
        )
        print("Time Series Data:", time_series)

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
```