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

# Doom
df.loc[(df["name"] == "Doom"), ["base_health_regeneration"]] = 0.66

# Elder Titan
df.loc[(df["name"] == "Elder Titan"), ["movement_speed"]] = 305

# Oracle
df.loc[(df["name"] == "Oracle"), ["strength_gain"]] = 2.2

# Sniper
df.loc[(df["name"] == "Sniper"), ["base_armor"]] += 1


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
