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

# Abaddon

df.loc[(df["name"] == "Abaddon"), ["base_armor"]] -= 1

# Dark Seer
df.loc[
    (df["name"] == "Dark Seer"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 2

# Enchantress
df.loc[(df["name"] == "Enchantress"), ["intelligence_gain"]] = 4.0

# Lycan
df.loc[(df["name"] == "Lycan"), ["base_strength"]] = 28

# Magnus
df.loc[(df["name"] == "Magnus"), ["base_strength"]] = 23

# Windranger
df.loc[
    (df["name"] == "Windranger"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 3


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
