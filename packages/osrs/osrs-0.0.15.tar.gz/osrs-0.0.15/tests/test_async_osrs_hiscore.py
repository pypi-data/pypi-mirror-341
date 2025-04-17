import pytest
from aiohttp import ClientSession

from osrs.asyncio import Hiscore, HSMode
from osrs.asyncio.osrs.hiscores import PlayerStats
from osrs.exceptions import PlayerDoesNotExist


@pytest.mark.asyncio
async def test_get_valid():
    hiscore_instance = Hiscore()
    async with ClientSession() as session:
        player_stats = await hiscore_instance.get(
            mode=HSMode.OLDSCHOOL,
            player="extreme4all",
            session=session,
        )

        # Assertions to confirm the response is correct
        assert isinstance(player_stats, PlayerStats), (
            "The returned object is not of type PlayerStats"
        )
        assert player_stats.skills, "Skills data should not be empty"
        assert player_stats.activities, "Activities data should not be empty"


@pytest.mark.asyncio
async def test_get_invalid():
    hiscore_instance = Hiscore()
    async with ClientSession() as session:
        with pytest.raises(PlayerDoesNotExist):
            _ = await hiscore_instance.get(
                mode=HSMode.OLDSCHOOL,
                player="This_is_not_a_valid_name",
                session=session,
            )


@pytest.mark.asyncio
async def test_get_default_no_session():
    hiscore_instance = Hiscore()
    player_stats = await hiscore_instance.get(player="extreme4all")
    # Assertions to confirm the response is correct
    assert isinstance(player_stats, PlayerStats), (
        "The returned object is not of type PlayerStats"
    )
    assert player_stats.skills, "Skills data should not be empty"
    assert player_stats.activities, "Activities data should not be empty"
