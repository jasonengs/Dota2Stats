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
df.loc[(df["name"] == "Batrider"), ["base_health_regeneration"]] = 1.25

# Death Prophet
df.loc[(df["name"] == "Death Prophet"), ["base_armor"]] = 0

# Doom
df.loc[(df["name"] == "Doom"), ["strength_gain"]] = 3.5

# Hoodwink
df.loc[(df["name"] == "Hoodwink"), ["movement_speed"]] = 315

# Muerta
df.loc[(df["name"] == "Muerta"), ["base_agility"]] = 21

# Naga Siren
df.loc[(df["name"] == "Naga Siren"), ["base_intelligence"]] = 20

# Pangolier
df.loc[
    (df["name"] == "Pangolier"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [26, 32, 29]

# Shadow Shaman
df.loc[(df["name"] == "Shadow Shaman"), ["base_armor", "base_intelligence"]] = [2, 23]

# Templar Assassin
df.loc[(df["name"] == "Templar Assassin"), ["base_strength"]] = 21

# Terrorblade
df.loc[
    (df["name"] == "Terrorblade"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [26, 32, 29]

# Tusk
df.loc[(df["name"] == "Tusk"), ["agility_gain"]] = 1.9

# Vengeful Spirit
df.loc[(df["name"] == "Vengeful Spirit"), ["base_attack_speed"]] = 100

# Winter Wyvern
df.loc[
    (df["name"] == "Winter Wyvern"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [15, 22, 18]

# Zeus
df.loc[(df["name"] == "Zeus"), ["base_intelligence"]] = 23


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
