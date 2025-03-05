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
        "min_attack",
        "max_attack",
        "avg_attack",
        "magic_resistance",
    ]
)

# Abaddon

df.loc[(df["name"] == "Abaddon"), ["base_mana_regeneration"]] = 0

# Ancient Apparition
df.loc[(df["name"] == "Ancient Apparition"), ["agility_gain"]] = 2.0

# Beastmaster
df.loc[
    (df["name"] == "Beastmaster"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 3

# Broodmother
df.loc[
    (df["name"] == "Broodmother"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 2

# Dark Seer
df.loc[(df["name"] == "Dark Seer"), ["base_armor"]] -= 1

# Ember Spirit
df.loc[(df["name"] == "Ember Spirit"), ["strength_gain"]] = 2.3

# Kez
df.loc[(df["name"] == "Kez"), ["strength_gain", "base_intelligence"]] = [2.8, 20]

# Lifestealer
df.loc[(df["name"] == "Lifestealer"), ["base_agility"]] -= 4

# Storm Spirit
df.loc[(df["name"] == "Storm Spirit"), ["intelligence_gain"]] = 3.7

# Windranger
df.loc[(df["name"] == "Windranger"), ["agility_gain"]] = 1.9

# Zeus
df.loc[
    (df["name"] == "Zeus"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] -= 4


df = df.assign(
    health=df.apply(calc_stats.calc_health, axis=1, lvl=1),
    health_regeneration=df.apply(calc_stats.calc_health_regeneration, axis=1, lvl=1),
    mana=df.apply(calc_stats.calc_mana, axis=1, lvl=1),
    mana_regeneration=df.apply(calc_stats.calc_mana_regeneration, axis=1, lvl=1),
    armor=df.apply(calc_stats.calc_armor, axis=1, lvl=1),
    magic_resistance=df.apply(calc_stats.calc_magic_resistance, axis=1, lvl=1),
    attack_speed=df.apply(calc_stats.calc_attack_speed, axis=1, lvl=1),
)

# Rename Movement Speed column
df = df.rename(columns={"movement_speed_daytime": "movement_speed"})

df.to_csv("../data/latest_data.csv", index=False)
