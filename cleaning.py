# This file can be ignored as the data already exists in assets/data directory

import numpy as np
import pandas as pd
from datetime import datetime


def save_df_csv(df, file_name):
    today = datetime.today().strftime("%Y_%m_%d")
    # today = f"{datetime.today(): %Y_%m_%d}"
    df.to_csv(f"assets/data/{today}_{file_name}.csv", index=False)


def move_columns(df, start, end, at):
    col = df.columns.tolist()

    cols_to_move = col[start:end]
    cols_to_keep = [c for c in col if c not in cols_to_move]

    insert_col_at = at

    new_col_order = (
        cols_to_keep[:insert_col_at] + cols_to_move + cols_to_keep[insert_col_at:]
    )

    return new_col_order


# This function calculate the base stats at 1 and without innate or facets
def calc_health(row):
    result = 120 + row["base_strength"] * 22
    return result


def calc_health_regeneration(row):
    result = row["base_health_regeneration"] + row["base_strength"] * 0.1
    return result


def calc_mana(row):
    result = 75 + row["base_intelligence"] * 12 if row["name"] != "Ogre Magi" else 120
    return result


def calc_mana_regeneration(row):
    result = row["base_mana_regeneration"] + row["base_intelligence"] * 0.05
    return result


def calc_magic_resistance(row):
    result = 25 + row["base_intelligence"] * 0.1
    return result


def calc_attack_speed(row):
    result = row["base_attack_speed"] + row["base_agility"] * 1
    return result


def calc_armor(row):
    result = np.round(row["base_armor"] + (row["base_agility"] / 6), 1)
    return result


def calc_nighttime_movement_speed(row):
    result = row["movement_speed_daytime"] + 30
    return result


def calc_damage(row, base_attack):
    if row["primary_attribute"] == "Strength":
        result = row[f"{base_attack}"] + row["base_strength"] * 1
    elif row["primary_attribute"] == "Agility":
        result = row[f"{base_attack}"] + row["base_agility"] * 1
    elif row["primary_attribute"] == "Intelligence":
        result = row[f"{base_attack}"] + row["base_intelligence"] * 1
    elif row["primary_attribute"] == "Universal":
        result = (
            row[f"{base_attack}"]
            + (row["base_strength"] + row["base_agility"] + row["base_intelligence"])
            * 0.7
        )
    return result


df = pd.read_csv("./assets/data/2024_12_16_hero_raw.csv")


# Replace the "_" with " "
df["name"] = df["name"].str.replace("_", " ")

# Replace "str" with "strength", "agi" with "agility", "int" with "intelligence" and "all" with "universal"
df["primary_attribute"] = df["primary_attribute"].replace(
    {"str": "strength", "agi": "agility", "int": "intelligence", "all": "universal"}
)

# Set to Title case
df["primary_attribute"] = df["primary_attribute"].str.title()


# Split Base Attribute Gain Per LvL to two columns
df[["base_strength", "strength_gain"]] = df["base_strength_gain_per_lvl"].str.split(
    "+", expand=True
)

df[["base_agility", "agility_gain"]] = df["base_agility_gain_per_lvl"].str.split(
    "+", expand=True
)

df[["base_intelligence", "intelligence_gain"]] = df[
    "base_intelligence_gain_per_lvl"
].str.split("+", expand=True)

# Replace Instant with 0 projectile_speed column
df["projectile_speed"] = df["projectile_speed"].replace("Instant", 0)

# Split Animation into attack_point and attack_backswing column
df[["attack_point", "attack_backswing"]] = df["animation"].str.split("+", expand=True)

# Replace "\n" with " " in lore column
df["lore"] = df["lore"].str.replace("\n", " ", regex=True)

# Drop unnecessary columns
df.drop(
    columns=[
        "roles",
        "base_strength_gain_per_lvl",
        "base_agility_gain_per_lvl",
        "base_intelligence_gain_per_lvl",
        "animation",
        "image",
        "map_icon",
        "name_as_key",
    ],
    inplace=True,
)

# Casting Data Type
df = df.astype(
    {
        "id": "int16",
        "primary_attribute": "category",
        "attack_type": "category",
        "legs": "int8",
        "projectile_speed": "int16",
        "attack_range": "int16",
        "bat": "float32",
        "movement_speed_daytime": "int16",
        "turn_rate": "float32",
        "vision_range_daytime": "int16",
        "vision_range_nighttime": "int16",
        "gib_type": "category",
        "complexity": "int8",
        "base_health_regeneration": "float32",
        "base_mana_regeneration": "float32",
        "base_armor": "int8",
        "base_attack_speed": "int16",
        "base_min_attack": "int16",
        "base_max_attack": "int16",
        "base_avg_attack": "int16",
        "base_strength": "int8",
        "strength_gain": "float32",
        "base_agility": "int8",
        "agility_gain": "float32",
        "base_intelligence": "int8",
        "intelligence_gain": "float32",
        "attack_point": "float32",
        "attack_backswing": "float32",
    }
)

# Cast to Datetime
df["released"] = pd.to_datetime(df["released"])


# Shadow Shaman Base Strength 23 -> 20
df.loc[(df["name"] == "Shadow Shaman"), ["base_strength"]] = 20

# Warlock Base Strength 24 -> 22
df.loc[(df["name"] == "Warlock"), ["base_strength"]] = 22

# Clockwerk Strength Gain Per LvL 2.8 -> 3.1
df.loc[(df["name"] == "Clockwerk"), ["strength_gain"]] = np.float32(3.1)

# Nyx Strength Gain Per LvL 2.1 -> 2.5
df.loc[(df["name"] == "Nyx Assassin"), ["strength_gain"]] = np.float32(2.5)

# Tidehunter Strength Gain Per LvL 3.5 -> 3.6
df.loc[(df["name"] == "Tidehunter"), ["strength_gain"]] = np.float32(3.6)

# NP Base Intelligence 23 -> 22
df.loc[(df["name"] == "Nature's Prophet"), ["base_intelligence"]] = 22

# Mirana Intelligence Gain Per LvL 1.2 -> 1.4
df.loc[(df["name"] == "Mirana"), ["intelligence_gain"]] = np.float32(1.4)

# Primal Beast Intelligence Gain Per LvL 1.4 -> 1.7
df.loc[(df["name"] == "Primal Beast"), ["intelligence_gain"]] = np.float32(1.7)

# Ringmaster Base Health Regeneration 0.2 to 0.25
df.loc[(df["name"] == "Ringmaster"), ["base_health_regeneration"]] = np.float32(0.25)

# Ursa Base Health Regeneration 0.5 to 1.0
df.loc[(df["name"] == "Ursa"), ["base_health_regeneration"]] = np.float32(1.0)

# Winter Wyvern Base Mana Regeneration 0.25 to 0.5
df.loc[(df["name"] == "Winter Wyvern"), ["base_mana_regeneration"]] = np.float32(0.5)

# Axe Base Armor -1 to 0
df.loc[(df["name"] == "Axe"), ["base_armor"]] = 0

# Huskar Base Armor 0 to 1
df.loc[(df["name"] == "Huskar"), ["base_armor"]] = 1

# Mirana Movement Speed Daytime 290 -> 285
df.loc[(df["name"] == "Mirana"), ["movement_speed_daytime"]] = 285

# Beastmaster Base Max Attack 7 to 9, Base Avg Attack 6 to 7
df.loc[(df["name"] == "Beastmaster"), ["base_max_attack", "base_avg_attack"]] = [9, 7]

# Brewmaster Base Max Attack 15 to 16
df.loc[(df["name"] == "Brewmaster"), ["base_max_attack"]] = 16

# Broodmother Base Min Attack 8 to 9, Base Max Attack 14 to 15, Base Avg Attack 11 to 12
df.loc[
    df["name"] == "Broodmother",
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [9, 15, 12]

# Morphling  Base Min Attack 9 to 12, Base Max Attack 18 to 21, Base Avg Attack 13 to 16
df.loc[
    df["name"] == "Morphling", ["base_min_attack", "base_max_attack", "base_avg_attack"]
] = [12, 21, 16]

# Techies Base Min Attack 5 to 3, Base Max Attack 7 to 5, Base Avg Attack 4
df.loc[
    df["name"] == "Techies", ["base_min_attack", "base_max_attack", "base_avg_attack"]
] = [3, 5, 4]

# Winter Wyvern Base Min Attack 0 to - 1, Base Max Attack 5 to 4
df.loc[
    df["name"] == "Winter Wyvern",
    ["base_min_attack", "base_max_attack", "base_avg_attack"],
] = [-1, 4, 1]


# Vengeful Spirit BAT 1.7 to 1.5 (Soul Strike Facet)
df.loc[df["name"] == "Vengeful Spirit", ["bat"]] = [1.5]


df = df.assign(
    health=df.apply(calc_health, axis=1),
    health_regeneration=df.apply(calc_health_regeneration, axis=1),
    mana=df.apply(calc_mana, axis=1),
    mana_regeneration=df.apply(calc_mana_regeneration, axis=1),
    magic_resistance=df.apply(calc_magic_resistance, axis=1),
    attack_speed=df.apply(calc_attack_speed, axis=1),
    armor=df.apply(calc_armor, axis=1),
    movement_speed_nighttime=df.apply(calc_nighttime_movement_speed, axis=1),
    main_min_damage=df.apply(calc_damage, axis=1, base_attack="base_min_attack"),
    main_max_damage=df.apply(calc_damage, axis=1, base_attack="base_max_attack"),
    main_avg_damage=df.apply(calc_damage, axis=1, base_attack="base_avg_attack"),
)

df.head()

df.info()

# Re Order Column Complexity to index 6
df = df[move_columns(df, 14, 15, 6)]

# Re Order Column Base Attribute and Attribute Gain to index 7
df = df[move_columns(df, 27, 33, 7)]

# Re Order Column Health, Health Regeneration, Mana, Mana Regeneration and Magic Resistance to index 13
df = df[move_columns(df, 35, 40, 13)]

# Re Order Column Armor to index 17
df = df[move_columns(df, 41, 42, 17)]

# Re Order Column Damage to index 18
df = df[move_columns(df, 43, 46, 18)]

# Re Order Column Attack Speed to index 24
df = df[move_columns(df, 44, 45, 24)]

# Re Order Column Attack Point and Backswing to index 26
df = df[move_columns(df, 43, 45, 26)]

# Re Order Movement Speed Nighttime to index 29
df = df[move_columns(df, 45, 46, 29)]

# Casting

df = df.astype(
    {
        "health": "int16",
        "health_regeneration": "float32",
        "mana": "int16",
        "mana_regeneration": "float32",
        "armor": "float32",
        "attack_speed": "int16",
        "movement_speed_nighttime": "int16",
        "main_min_damage": "int16",
        "main_max_damage": "int16",
        "main_avg_damage": "int16",
    }
)

df.head()

df.info()

save_df_csv(df, "hero_cleaned")
