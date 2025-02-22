# Hero Changes

import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import calc_stats

df = pd.read_csv("../data/hero_cleaned.csv")


df = df.drop(
    columns=[
        "health",
        "health_regeneration",
        "mana",
        "mana_regeneration",
        "armor",
        "main_min_damage",
        "main_max_damage",
        "main_avg_damage",
        "magic_resistance",
        "attack_speed",
        "movement_speed_nighttime",
    ]
)

# Abaddon
df.loc[
    (df["name"] == "Abaddon"),
    ["strength_gain", "agility_gain", "base_intelligence", "intelligence_gain"],
] = [2.6, 1.5, 18, 2]

df.loc[
    (df["name"] == "Abaddon"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 26

# Arc Warden
df.loc[(df["name"] == "Arc Warden"), ["primary_attribute"]] = ["Universal"]

df.loc[
    (df["name"] == "Arc Warden"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 10

# Axe
df.loc[
    (df["name"] == "Axe"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 1

# Bane
df.loc[
    (df["name"] == "Bane"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 25

# Batrider
df.loc[
    (df["name"] == "Batrider"),
    ["base_strength", "strength_gain", "agility_gain", "intelligence_gain"],
] = [23, 2.9, 1.8, 2.9]

df.loc[
    (df["name"] == "Batrider"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 16

# Beastmaster
df.loc[(df["name"] == "Beastmaster"), ["agility_gain", "intelligence_gain"]] = [
    1.9,
    1.9,
]

df.loc[
    (df["name"] == "Beastmaster"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 23

# Brewmaster
df.loc[
    (df["name"] == "Brewmaster"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 17

# Broodmother
df.loc[
    (df["name"] == "Broodmother"),
    [
        "primary_attribute",
        "base_strength",
        "strength_gain",
        "agility_gain",
        "intelligence_gain",
    ],
] = ["Agility", 18, 2.9, 3.4, 2.0]

df.loc[
    (df["name"] == "Broodmother"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 20

# Chaos Knight
df.loc[(df["name"] == "Chaos Knight"), ["agility_gain"]] = 1.8

# Chen
df.loc[
    (df["name"] == "Chen"),
    ["primary_attribute", "base_min_attack", "base_max_attack", "base_avg_attack"],
] = ["Intelligence", 27, 37, 32]

# Clockwerk
df.loc[
    (df["name"] == "Clockwerk"),
    ["primary_attribute", "base_strength", "strength_gain", "agility_gain"],
] = ["Strength", 26, 3.2, 2.3]

df.loc[
    (df["name"] == "Clockwerk"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 16

# Dark Seer
df.loc[(df["name"] == "Dark Seer"), ["primary_attribute"]] = ["Intelligence"]

df.loc[
    (df["name"] == "Dark Seer"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 26

# Dark Willow
df.loc[
    (df["name"] == "Dark Willow"),
    ["primary_attribute", "agility_gain", "intelligence_gain"],
] = ["Intelligence", 1.6, 3.5]

df.loc[
    (df["name"] == "Dark Willow"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 22

# Dazzle
df.loc[
    (df["name"] == "Dazzle"), ["strength_gain", "agility_gain", "intelligence_gain"]
] = [2.3, 1.7, 3.7]

df.loc[
    (df["name"] == "Dazzle"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 16

# Death Prophet
df.loc[(df["name"] == "Death Prophet"), ["primary_attribute", "base_agility"]] = [
    "Universal",
    17,
]

df.loc[
    (df["name"] == "Death Prophet"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 3

# Enigma
df.loc[
    (df["name"] == "Enigma"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 12

# Faceless Void
df.loc[(df["name"] == "Faceless Void"), ["base_agility"]] = 21

# Gyrocopter
df.loc[(df["name"] == "Gyrocopter"), ["base_agility", "agility_gain"]] = [25, 3.2]

# Hoodwink
df.loc[(df["name"] == "Hoodwink"), ["base_agility"]] = [25]

# Invoker
df.loc[
    (df["name"] == "Invoker"),
    [
        "primary_attribute",
        "strength_gain",
        "agility_gain",
        "base_intelligence",
        "intelligence_gain",
        "base_health_regeneration",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
    ],
] = ["Intelligence", 2.5, 2, 20, 4.7, 0.25, 15, 21, 18]

# Io
df.loc[(df["name"] == "Io"), ["strength_gain"]] = [3.0]

df.loc[
    (df["name"] == "Io"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 17

# Keeper of the Light
df.loc[(df["name"] == "Keeper of the Light"), ["intelligence_gain"]] = [3.3]

# Kez
df.loc[(df["name"] == "Kez"), ["base_agility", "movement_speed_daytime"]] = [27, 315]

df.loc[(df["name"] == "Kez"), ["base_armor"]] -= 1

# Legion Commander
df.loc[(df["name"] == "Legion Commander"), ["base_strength"]] = [24]

# Lifestealer
df.loc[(df["name"] == "Lifestealer"), ["movement_speed_daytime"]] = [315]

# Lone Druid
df.loc[
    (df["name"] == "Lone Druid"),
    [
        "primary_attribute",
        "base_strength",
        "strength_gain",
        "agility_gain",
        "intelligence_gain",
    ],
] = ["Agility", 18, 2.5, 2.8, 1.4]

df.loc[
    (df["name"] == "Lone Druid"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 17

# Lycan
df.loc[
    (df["name"] == "Lycan"),
    ["primary_attribute", "strength_gain", "agility_gain", "intelligence_gain"],
] = ["Strength", 3.4, 1.7, 1.7]

df.loc[
    (df["name"] == "Lycan"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 20

# Magnus
df.loc[(df["name"] == "Magnus"), ["intelligence_gain"]] = [2.1]

df.loc[
    (df["name"] == "Magnus"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 21

# Marci
df.loc[
    (df["name"] == "Marci"),
    ["intelligence_gain", "base_min_attack", "base_max_attack", "base_avg_attack"],
] = [1.9, 29, 33, 31]


# Mirana
df.loc[
    (df["name"] == "Mirana"),
    [
        "primary_attribute",
        "base_strength",
        "strength_gain",
        "agility_gain",
        "intelligence_gain",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
    ],
] = ["Agility", 20, 2.2, 3.1, 1.9, 22, 28, 25]

# Muerta
df.loc[(df["name"] == "Muerta"), ["base_intelligence", "intelligence_gain"]] = [23, 3.4]

# Nature's Prophet
df.loc[(df["name"] == "Nature's Prophet"), ["primary_attribute"]] = ["Universal"]

df.loc[
    (df["name"] == "Nature's Prophet"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] -= 2

# Nyx Assassin
df.loc[
    (df["name"] == "Nyx Assassin"),
    ["strength_gain", "agility_gain", "intelligence_gain"],
] = [2.7, 2.9, 2.6]

df.loc[
    (df["name"] == "Nyx Assassin"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 14

# Oracle
df.loc[(df["name"] == "Oracle"), ["intelligence_gain"]] = [3.6]

# Pangolier
df.loc[(df["name"] == "Pangolier"), ["agility_gain"]] = [3.2]

df.loc[
    (df["name"] == "Pangolier"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 20

# Phantom Lancer
df.loc[(df["name"] == "Phantom Lancer"), ["base_strength"]] = [21]

# Phoenix
df.loc[(df["name"] == "Phoenix"), ["primary_attribute"]] = ["Strength"]

df.loc[
    (df["name"] == "Phoenix"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 12

# Sand King
df.loc[
    (df["name"] == "Sand King"),
    [
        "base_strength",
        "agility_gain",
        "intelligence_gain",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
    ],
] = [22, 2.0, 2.0, 19, 29, 24]

# Snapfire
df.loc[
    (df["name"] == "Snapfire"), ["strength_gain", "agility_gain", "intelligence_gain"]
] = [3.5, 1.9, 2.2]

df.loc[
    (df["name"] == "Snapfire"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 14

# Spectre
df.loc[(df["name"] == "Spectre"), ["primary_attribute"]] = ["Universal"]

df.loc[
    (df["name"] == "Spectre"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] -= 2

# Sven
df.loc[(df["name"] == "Sven"), ["base_strength", "strength_gain", "base_agility"]] = [
    23,
    3.5,
    18,
]

df.loc[
    (df["name"] == "Sven"),
    ["base_armor"],
] += 1

# Techies
df.loc[
    (df["name"] == "Techies"), ["strength_gain", "agility_gain", "intelligence_gain"]
] = [2.6, 1.8, 2.8]

df.loc[
    (df["name"] == "Techies"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 17

# Templar Assassin
df.loc[(df["name"] == "Templar Assassin"), ["agility_gain"]] = [3.4]

# Vengeful Spirit
df.loc[
    (df["name"] == "Vengeful Spirit"),
    ["primary_attribute", "strength_gain", "agility_gain", "intelligence_gain", "bat"],
] = ["Agility", 2.6, 3.2, 1.5, 1.7]

df.loc[
    (df["name"] == "Vengeful Spirit"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 17

# Venomancer
df.loc[
    (df["name"] == "Venomancer"), ["strength_gain", "agility_gain", "intelligence_gain"]
] = [2.1, 2.8, 1.8]

df.loc[
    (df["name"] == "Venomancer"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 21

# Visage
df.loc[
    (df["name"] == "Visage"), ["strength_gain", "agility_gain", "intelligence_gain"]
] = [2.8, 1.3, 2.9]

df.loc[
    (df["name"] == "Visage"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 17

# Void Spirit
df.loc[
    (df["name"] == "Void Spirit"),
    ["base_strength", "strength_gain", "intelligence_gain"],
] = [22, 2.6, 3.1]

df.loc[
    (df["name"] == "Void Spirit"),
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] += 18

# Warlock
df.loc[
    (df["name"] == "Warlock"), ["base_min_attack", "base_max_attack", "base_avg_attack"]
] += 3

# Windranger
df.loc[
    (df["name"] == "Windranger"),
    [
        "strength_gain",
        "agility_gain",
        "base_intelligence",
        "intelligence_gain",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
    ],
] = [2.6, 1.7, 18, 3.2, 21, 33, 27]

# Winter Wyvern
df.loc[
    (df["name"] == "Winter Wyvern"),
    [
        "primary_attribute",
        "base_strength",
        "strength_gain",
        "agility_gain",
        "intelligence_gain",
        "base_attack_speed",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
    ],
] = ["Intelligence", 22, 2.5, 1.7, 3.6, 100, 14, 21, 17]


df = df.assign(
    health=df.apply(calc_stats.calc_health, axis=1, lvl=1),
    health_regeneration=df.apply(calc_stats.calc_health_regeneration, axis=1, lvl=1),
    mana=df.apply(calc_stats.calc_mana, axis=1, lvl=1),
    mana_regeneration=df.apply(calc_stats.calc_mana_regeneration, axis=1, lvl=1),
    armor=df.apply(calc_stats.calc_armor, axis=1, lvl=1),
    magic_resistance=df.apply(calc_stats.calc_magic_resistance, axis=1, lvl=1),
    attack_speed=df.apply(calc_stats.calc_attack_speed, axis=1, lvl=1),
    min_attack=df.apply(calc_stats.calc_attack_damage, axis=1, lvl=1, stats="min"),
    max_attack=df.apply(calc_stats.calc_attack_damage, axis=1, lvl=1, stats="max"),
    avg_attack=df.apply(calc_stats.calc_attack_damage, axis=1, lvl=1, stats="avg"),
)


df.to_csv("../data/latest_data.csv", index=False)
