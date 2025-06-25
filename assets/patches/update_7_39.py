import os
import sys

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import calc_stats

df = pd.read_csv("../data/latest_data.csv")

df = df.drop(
    columns=[
        "health",
        "health_regeneration",
        "mana",
        "mana_regeneration",
        "armor",
        "magic_resistance",
    ]
)

# Batrider

df.loc[(df["name"] == "Batrider"), ["movement_speed"]] = 320

# Beastmaster
df.loc[(df["name"] == "Beastmaster"), ["base_agility"]] = 19

# Chen
df.loc[
    (df["name"] == "Chen"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 2

# Dark Seer
df.loc[(df["name"] == "Dark Seer"), ["agility_gain"]] = 1.5

# Dawnbreaker
df.loc[
    (df["name"] == "Dawnbreaker"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 5

# Gyrocopter
df.loc[(df["name"] == "Gyrocopter"), ["base_armor"]] -= 1

# Invoker
df.loc[
    (df["name"] == "Invoker"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 4

df.loc[(df["name"] == "Invoker"), ["intelligence_gain"]] = 4

# Kez
df.loc[(df["name"] == "Kez"), ["base_health_regeneration", "base_attack_speed"]] = [
    1.5,
    110,
]


# Lifestealer
df.loc[(df["name"] == "Lifestealer"), ["base_strength"]] = 23

# Marci
df.loc[(df["name"] == "Marci"), ["agility_gain"]] = 2.2

# Meepo
df.loc[(df["name"] == "Meepo"), ["base_armor"]] -= 1

# Morphling
df.loc[(df["name"] == "Morphling"), ["strength_gain", "base_mana_regeneration"]] = [
    2.6,
    0,
]

# Naga Siren
df.loc[(df["name"] == "Naga Siren"), ["base_agility"]] = 22

# Nature's Prophet
df.loc[(df["name"] == "Nature's Prophet"), ["attack_range"]] = 600

# Ogre Magi
df.loc[(df["name"] == "Ogre Magi"), ["base_strength"]] = 25

# Oracle
df.loc[(df["name"] == "Oracle"), ["attack_range"]] = 625

# Phantom Lancer
df.loc[(df["name"] == "Phantom Lancer"), ["base_health_regeneration"]] += 0.5

# Skywrath Mage
df.loc[(df["name"] == "Skywrath Mage"), ["base_intelligence"]] = 25

# Slardar
df.loc[(df["name"] == "Slardar"), ["base_armor"]] -= 1

# Techies
df.loc[(df["name"] == "Techies"), ["movement_speed"]] = 310

# Terrorblade
df.loc[(df["name"] == "Terrorblade"), ["base_health_regeneration"]] -= 1

# Tinker
df.loc[(df["name"] == "Tinker"), ["base_armor"]] -= 2

# Undying
df.loc[
    (df["name"] == "Undying"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 2

# Vengeful Spirit
df.loc[(df["name"] == "Vengeful Spirit"), ["base_agility"]] = 23

# Void Spirit
df.loc[(df["name"] == "Void Spirit"), ["base_agility"]] = 21
# Wraith king
df.loc[(df["name"] == "Wraith king"), ["movement_speed", "base_intelligence"]] = [
    310,
    16,
]


df = df.assign(
    health=df.apply(calc_stats.calc_health, axis=1, lvl=1),
    health_regeneration=df.apply(calc_stats.calc_health_regeneration, axis=1, lvl=1),
    mana=df.apply(calc_stats.calc_mana, axis=1, lvl=1),
    mana_regeneration=df.apply(calc_stats.calc_mana_regeneration, axis=1, lvl=1),
    armor=df.apply(calc_stats.calc_armor, axis=1, lvl=1),
    magic_resistance=df.apply(calc_stats.calc_magic_resistance, axis=1, lvl=1),
    attack_speed=df.apply(calc_stats.calc_attack_speed, axis=1, lvl=1),
)


df.to_csv("../data/latest_data.csv", index=False)
