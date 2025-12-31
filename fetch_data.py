import asyncio
from pathlib import Path

import aiofiles
import pandas as pd
from aiohttp import ClientSession


async def fetch_hero_id(session: ClientSession) -> list[str]:
    url = "https://www.dota2.com/datafeed/herolist?language=english"
    async with session.get(url) as response:
        data = await response.json()
        heroes = data["result"]["data"]["heroes"]
    hero_id = [i["id"] for i in heroes]
    return hero_id


async def fetch_hero_stats(id: int, hero_stats: dict, session: ClientSession, sem):
    url = f"https://www.dota2.com/datafeed/herodata?language=english&hero_id={id}"
    async with sem:
        async with session.get(url) as response:
            data = await response.json()
            heroes = data["result"]["data"]["heroes"][0]

    for k, v in hero_stats.items():
        v.append(heroes[k])


async def fetch_heroes_stats() -> pd.DataFrame:
    hero_stats = get_hero_stats_dict()
    sem = asyncio.Semaphore(4)
    async with ClientSession() as session:
        hero_id = await fetch_hero_id(session)
        tasks = [fetch_hero_stats(id, hero_stats, session, sem) for id in hero_id]

        await asyncio.gather(*tasks)

    df = pd.DataFrame(hero_stats)

    return df


def get_hero_stats_dict() -> dict:
    hero_stats = {
        k: []
        for k in [
            "id",
            "order_id",
            "name_loc",
            "bio_loc",
            "hype_loc",
            "npe_desc_loc",
            "str_base",
            "str_gain",
            "agi_base",
            "agi_gain",
            "int_base",
            "int_gain",
            "primary_attr",
            "complexity",
            "attack_capability",
            "damage_min",
            "damage_max",
            "attack_rate",
            "attack_range",
            "projectile_speed",
            "armor",
            "magic_resistance",
            "movement_speed",
            "turn_rate",
            "sight_range_day",
            "sight_range_night",
            "max_health",
            "health_regen",
            "max_mana",
            "mana_regen",
        ]
    }

    return hero_stats


def modify_name() -> dict:
    heroes = {
        1: "antimage",
        11: "nevermore",
        20: "vengefulspirit",
        21: "windrunner",
        22: "zuus",
        36: "necrolyte",
        39: "queenofpain",
        42: "skeleton_king",
        51: "rattletrap",
        53: "furion",
        54: "life_stealer",
        69: "doom_bringer",
        76: "obsidian_destroyer",
        83: "treant",
        91: "wisp",
        96: "centaur",
        97: "magnataur",
        98: "shredder",
        108: "abyssal_underlord",
    }

    return heroes


async def fetch_image(
    session: ClientSession, url: str, save_as: Path, sem: asyncio.Semaphore
) -> None:
    async with sem:
        async with session.get(url) as response:
            content = await response.read()

    async with aiofiles.open(save_as, "wb") as f:
        await f.write(content)


async def download_images(df: pd.DataFrame, *parts: str) -> None:
    base = Path() / "assets" / "images"
    # Construct full path
    fullpath = base.joinpath(*parts)
    # Create a directory
    fullpath.mkdir(parents=True, exist_ok=True)
    # Construct url parts
    url_part = "/".join(parts)
    base_url = "https://cdn.steamstatic.com/apps/dota2/images/dota_react"
    sem = asyncio.Semaphore(3)
    async with ClientSession() as session:
        tasks = []
        for name, name_temp in zip(df["name_loc"], df["name_temp"]):
            # Construct url
            url = f"{base_url}/{url_part}/{name_temp}.png"
            # Construct filename
            filename = name.lower().replace("'", "").replace(" ", "_")
            save_as = fullpath / f"{filename}.png"
            task = fetch_image(session, url, save_as, sem)

            tasks.append(task)

        await asyncio.gather(*tasks)


async def main():
    df = await fetch_heroes_stats()
    hero_name = modify_name()
    df["name_temp"] = df["name_loc"].str.lower().str.replace(" ", "_")
    df["name_temp"] = df["id"].map(hero_name).fillna(df["name_temp"])
    # Construct directory
    path = Path() / "assets" / "data"
    # Construct a filename
    filename = path / "raw_data.csv"
    df.to_csv(filename, index=False)

    await download_images(df, "heroes")
    await download_images(df, "heroes", "icons")


if __name__ == "__main__":
    asyncio.run(main())
