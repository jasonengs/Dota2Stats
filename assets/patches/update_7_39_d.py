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
df.loc[(df["name"] == "Batrider"), ["base_agility"]] = 13
# Earth Spirit
df.loc[
    df["name"] == "Earth Spirit",
    ["base_min_attack", "base_avg_attack"],
] = [31, 33]
# Nature's Prophet
df.loc[(df["name"] == "Nature's Prophet"), ["agility_gain"]] = 3.0
# Puck
df.loc[(df["name"] == "Puck"), ["agility_gain"]] = 2.3
# Sand King
df.loc[(df["name"] == "Sand King"), ["base_strength"]] = 23
# Shadow Fiend
df.loc[(df["name"] == "Shadow Fiend"), ["base_armor"]] = 0
# Silencer
df.loc[(df["name"] == "Silencer"), ["base_strength"]] = 18
# Spirit Breaker
df.loc[
    df["name"] == "Spirit Breaker",
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [34, 44, 39]
# Techies
df.loc[(df["name"] == "Techies"), ["intelligence_gain"]] = 3.0
# Templar Assassin
df.loc[
    (df["name"] == "Templar Assassin"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [28, 33, 31]
# Vengeful Spirit
df.loc[
    (df["name"] == "Vengeful Spirit"),
    ["agility_gain", "base_min_attack", "base_max_attack", "base_avg_attack"],
] = [3.0, 28, 34, 31]

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
