import math
from enum import IntEnum

import numpy as np
from pandas import Series


class Attr(IntEnum):
    STR = 0
    AGI = 1
    INT = 2


def get_bonus_attributes(name: str, lvl: int, attr: int) -> int:
    additional_bonus = 3 if (name == "Morphling" and attr == Attr.AGI) else 0
    if lvl < 15:
        base = 0
        multiplier = 0
    elif lvl == 15:
        base, multiplier = 2, 1
    elif lvl == 16:
        base, multiplier = 4, 2
    elif lvl <= 18:
        base, multiplier = 6, 3
    elif lvl == 19:
        base, multiplier = 8, 4
    elif lvl == 20:
        base, multiplier = 10, 5
    elif lvl == 21:
        base, multiplier = 12, 6
    else:
        base, multiplier = 14, 7

    total_bonus = 0 if name == "Invoker" else base + additional_bonus * multiplier

    return total_bonus


def get_total_attributes(
    att_base: int, attr_gain: float, lvl: int, bonus: int
) -> float:
    total_attributes = att_base + (attr_gain * (lvl - 1)) + bonus
    return total_attributes


# Dragon Knight for Health Regen and Armor
def get_dragon_knight_dragon_blood(lvl: int) -> float:
    bonus = 2 + lvl * 0.5
    return bonus


# Luna Innate
def get_luna_lunar_blessing(lvl: int, stats: str) -> int:
    if stats.lower() == "attack damage":
        bonus = 2 * lvl
    elif stats.lower() == "sight_range_night":
        bonus = 250 + (25 * lvl)
    return bonus


# Sven Facet
def get_sven_wrath_of_god(lvl: int) -> float:
    if lvl >= 1 and lvl <= 5:
        bonus_per_str = 0.0
    elif lvl >= 6 and lvl <= 11:
        bonus_per_str = 0.2
    elif lvl >= 12 and lvl <= 17:
        bonus_per_str = 0.3
    elif lvl >= 18:
        bonus_per_str = 0.4
    else:
        bonus_per_str = 0.0
    return bonus_per_str


# Ursa Innate
def get_ursa_maul(lvl: int) -> float:
    bonus_health_as_damage = round(1.25 / 100, 3)
    return bonus_health_as_damage


# Sniper Innate
def get_sniper_keen_scope(lvl: int) -> int:
    if lvl >= 1 and lvl <= 5:
        bonus_attack_range = 160
    elif lvl >= 6 and lvl <= 11:
        bonus_attack_range = 260
    elif lvl >= 12 and lvl <= 17:
        bonus_attack_range = 360
    elif lvl >= 18:
        bonus_attack_range = 460
    return bonus_attack_range


# Razor Innate
def get_razor_unstable_current(lvl: int) -> float:
    bonus_movement_speed = 1 + (lvl / 100)
    return bonus_movement_speed


# Death Prophet Innate
def get_death_prophet_witchcraft(lvl: int) -> float:
    bonus_movement_speed = 1 + (lvl * 0.75 / 100)
    return bonus_movement_speed


# Void Spirit Innate
def get_void_spirit_intrinsic_edge() -> float:
    bonus_on_secondary = 1.25
    return bonus_on_secondary


# Outwolrd Destroyer Innate
def get_outworld_destroyer_ominous_discernment() -> float:
    bonus_mana = 2.5
    return bonus_mana


# Crystal Maiden Innate
def get_crystal_maiden_blueheart_floe(lvl: int) -> float:
    if lvl >= 1 and lvl <= 5:
        bonus_mana_regen_amplification = 1.25
    elif lvl >= 6 and lvl <= 11:
        bonus_mana_regen_amplification = 1.50
    elif lvl >= 12 and lvl <= 17:
        bonus_mana_regen_amplification = 1.75
    elif lvl >= 18:
        bonus_mana_regen_amplification = 2.0
    else:
        bonus_mana_regen_amplification = 0.0
    return bonus_mana_regen_amplification


# Drow Ranger Innate
def get_drow_ranger_precision_aura(lvl: int) -> float:
    if lvl >= 1 and lvl <= 5:
        bonus_agi = 1.04 + (lvl * 0.01)
    elif lvl >= 6 and lvl <= 11:
        bonus_agi = 1.08 + (lvl * 0.01)
    elif lvl >= 12 and lvl <= 17:
        bonus_agi = 1.12 + (lvl * 0.01)
    elif lvl >= 18:
        bonus_agi = 1.16 + (lvl * 0.01)
    else:
        bonus_agi = 0.0
    return bonus_agi


# Slardar Innate only applies when on puddles, trail, river
def get_slardar_seaborn_sentinel(lvl: int, bonus_type: str) -> int | float:
    movement_speed_bonus = 1 + (18 / 100)
    if lvl >= 1 and lvl <= 5:
        bonuses = {"health_regeneration": 2.5, "armor": 3, "attack_damage": 8}
    elif lvl >= 6 and lvl <= 11:
        bonuses = {"health_regeneration": 5, "armor": 4, "attack_damage": 16}
    elif lvl >= 12 and lvl <= 17:
        bonuses = {"health_regeneration": 7.5, "armor": 5, "attack_damage": 24}
    elif lvl >= 18:
        bonuses = {"health_regeneration": 10, "armor": 6, "attack_damage": 32}
    else:
        bonuses = {"health_regeneration": 0.0, "armor": 0, "attack_damage": 0}
    bonuses["movement_speed"] = movement_speed_bonus
    result = bonuses[bonus_type.lower().replace(" ", "_")]
    return result


def calc_total_str(row: Series, lvl: int) -> float:
    bonus = get_bonus_attributes(row["name"], lvl, Attr.STR)
    total_str = get_total_attributes(row["str_base"], row["str_gain"], lvl, bonus)
    return total_str


def calc_total_agi(row: Series, lvl: int) -> float:
    bonus = get_bonus_attributes(row["name"], lvl, Attr.AGI)
    total_agi = get_total_attributes(row["agi_base"], row["agi_gain"], lvl, bonus)

    if row["name"] == "Drow Ranger":
        agi_bonus = get_drow_ranger_precision_aura(lvl)
        total_agi *= agi_bonus
    return total_agi


def calc_total_int(row: Series, lvl: int) -> float:
    bonus = get_bonus_attributes(row["name"], lvl, Attr.INT)
    total_int = get_total_attributes(row["int_base"], row["int_gain"], lvl, bonus)
    return total_int


def calc_health(row: Series, lvl: int) -> int:
    base_health = 120
    health_point = 22
    total_str = math.floor(calc_total_str(row, lvl))
    total_health = base_health + total_str * health_point
    return total_health


def calc_health_regen(row: Series, lvl: int) -> float:
    total_str = calc_total_str(row, lvl)
    health_regen_per_str = 0.1
    if row["name"] == "Dragon Knight":
        health_regen_bonus = get_dragon_knight_dragon_blood(lvl)
        health_regen_per_str_bonus = 1
        # elif row["name"] == "Slardar":
        #     health_regen_bonus = get_slardar_seaborn_sentinel(
        #         lvl, "health regen"
        #     )
        health_regen_per_str_bonus = 1
    elif row["name"] == "Void Spirit":
        health_regen_bonus = 0
        health_regen_per_str_bonus = get_void_spirit_intrinsic_edge()
    else:
        health_regen_bonus = 0
        health_regen_per_str_bonus = 1
    total_health_regen = round(
        row["base_health_regen"]
        + total_str * (health_regen_per_str * health_regen_per_str_bonus)
        + health_regen_bonus,
        2,
    )
    return total_health_regen


def calc_mana(row: Series, lvl: int) -> int:
    base_mana = 75 if row["name"] != "Ogre Magi" else 120
    total_attribute = (
        math.floor(calc_total_int(row, lvl))
        if row["name"] != "Ogre Magi"
        else calc_total_str(row, lvl)
    )
    mana_point = 12 if row["name"] != "Ogre Magi" else 6
    if row["name"] == "Huskar":
        total_mana = np.nan
    elif row["name"] == "Ogre Magi":
        total_mana = base_mana + math.floor(total_attribute * mana_point)
    elif row["name"] == "Outworld Destroyer":
        mana_per_int_bonus = get_outworld_destroyer_ominous_discernment()
        total_mana = round(
            base_mana + total_attribute * (mana_point + mana_per_int_bonus)
        )
    else:
        total_mana = base_mana + total_attribute * mana_point
    return total_mana


def calc_mana_regen(row: Series, lvl: int) -> float:
    total_attribute = (
        calc_total_int(row, lvl)
        if row["name"] != "Ogre Magi"
        else calc_total_str(row, lvl)
    )
    # total_int = calc_total_int(row, lvl)
    mana_regen_per_attribute = 0.05 if row["name"] != "Ogre Magi" else 0.02
    if row["name"] == "Huskar":
        total_mana_regen = np.nan
    elif row["name"] == "Lich":
        total_mana_regen = 0.0
    elif row["name"] == "Crystal Maiden":
        mana_regen_amplification = get_crystal_maiden_blueheart_floe(lvl)
        total_mana_regen = round(
            (row["base_mana_regen"] + total_attribute * mana_regen_per_attribute)
            * mana_regen_amplification,
            2,
        )
    elif row["name"] == "Ogre Magi":
        total_mana_regen = round(
            row["base_mana_regen"] + total_attribute * mana_regen_per_attribute,
            2,
        )
    elif row["name"] == "Void Spirit":
        mana_regen_per_int_bonus = get_void_spirit_intrinsic_edge()
        total_mana_regen = round(
            row["base_mana_regen"]
            + total_attribute * (mana_regen_per_attribute * mana_regen_per_int_bonus),
            2,
        )
    else:
        total_mana_regen = round(
            row["base_mana_regen"] + total_attribute * mana_regen_per_attribute,
            2,
        )
    return total_mana_regen


def calc_attack_speed(row: Series, lvl: int) -> int:
    total_agi = calc_total_agi(row, lvl)
    total_attack_speed = round(row["base_attack_speed"] + total_agi)
    return total_attack_speed


def calc_armor(row: Series, lvl: int) -> float:
    total_agi = calc_total_agi(row, lvl)
    armor_per_agi = 1 / 6
    if row["name"] == "Dragon Knight":
        armor_bonus = get_dragon_knight_dragon_blood(lvl)
        armor_per_agi_bonus = 1
        # elif row["name"] == "Slardar":
        #     armor_bonus = get_slardar_seaborn_sentinel(lvl, "armor")
        armor_per_agi_bonus = 1
    elif row["name"] == "Void Spirit":
        armor_bonus = 0
        armor_per_agi_bonus = get_void_spirit_intrinsic_edge()
    else:
        armor_bonus = 0
        armor_per_agi_bonus = 1

    total_armor = round(
        row["base_armor"]
        + total_agi * (armor_per_agi * armor_per_agi_bonus)
        + armor_bonus,
        1,
    )
    return total_armor


def calc_magic_resistance(row: Series, lvl: int) -> int:
    base_magic_resistance = 25
    magic_resistance_per_int = 0.1
    total_int = calc_total_int(row, lvl)
    if row["name"] == "Void Spirit":
        magic_resistance_per_int_bonus = get_void_spirit_intrinsic_edge()
    elif row["name"] == "Ogre Magi":
        # Ogre Magi Max Int is 0 It means it cannot be added by attribute bonus
        magic_resistance_per_int_bonus = 1
        total_int = 0
    else:
        magic_resistance_per_int_bonus = 1
    total_magic_resistance = round(
        base_magic_resistance
        + total_int * (magic_resistance_per_int * magic_resistance_per_int_bonus)
    )
    return total_magic_resistance


def calc_attack_damage(row: Series, lvl: int, stats: str) -> int:
    if row["primary_attr"] == 0:
        total_str = calc_total_str(row, lvl)
        if row["name"] == "Sven":
            attack_damage_bonus = get_sven_wrath_of_god(lvl)
        # elif row["name"] == "Slardar":
        #     attack_damage_bonus = get_slardar_seaborn_sentinel(lvl, "attack damage")
        else:
            attack_damage_bonus = 0

        total_attack_damage = math.floor(
            (row[f"base_damage_{stats}"])
            + total_str
            + math.floor(total_str * attack_damage_bonus)
        )
    elif row["primary_attr"] == 1:
        total_agi = calc_total_agi(row, lvl)
        if row["name"] == "Luna":
            attack_damage_bonus = get_luna_lunar_blessing(lvl, "attack damage")
            total_attack_damage = math.floor(
                row[f"base_damage_{stats}"] + total_agi + attack_damage_bonus
            )
        elif row["name"] == "Ursa":
            total_health = calc_health(row, lvl)
            attack_damage_bonus = get_ursa_maul(lvl)
            total_attack_damage = math.floor(
                row[f"base_damage_{stats}"]
                + math.floor(total_agi)
                + (total_health * attack_damage_bonus)
            )
        else:
            total_attack_damage = math.floor(row[f"base_damage_{stats}"] + total_agi)
    elif row["primary_attr"] == 2:
        total_int = calc_total_int(row, lvl)
        if row["name"] == "Jakiro":
            attack_damage_reduction = 50 / 100
            total_attack_damage_reduction = (
                row["base_damage_avg"] + total_int
            ) * attack_damage_reduction
            total_attack_damage = math.floor(
                row[f"base_damage_{stats}"]
                + total_int
                - math.floor(total_attack_damage_reduction)
            )
        else:
            total_attack_damage = math.floor((row[f"base_damage_{stats}"] + total_int))

    elif row["primary_attr"] == 3:
        total_str = calc_total_str(row, lvl)
        total_agi = calc_total_agi(row, lvl)
        total_int = calc_total_int(row, lvl)
        total_attributes = math.floor(total_str + total_agi + total_int)
        point_per_attribute = 0.45
        total_attack_damage = math.floor(
            row[f"base_damage_{stats}"] + total_attributes * point_per_attribute
        )
    return total_attack_damage


def calc_attack_damage_min(row: Series, lvl: int) -> int:
    total_attack_damage = calc_attack_damage(row, lvl, "min")
    return total_attack_damage


def calc_attack_damage_max(row: Series, lvl: int) -> int:
    total_attack_damage = calc_attack_damage(row, lvl, "max")
    return total_attack_damage


def calc_attack_damage_avg(row: Series, lvl: int) -> int:
    total_attack_damage = calc_attack_damage(row, lvl, "avg")
    return total_attack_damage


def calc_attack_range(row: Series, lvl: int) -> int:
    if row["name"] == "Sniper":
        attack_range_bonus = get_sniper_keen_scope(lvl)
    else:
        attack_range_bonus = 0
    total_attack_range = row["attack_range"] + attack_range_bonus
    return total_attack_range


def calc_movement_speed(row: Series, lvl: int) -> int:
    if row["name"] == "Death Prophet":
        movement_speed_bonus = get_death_prophet_witchcraft(lvl)
    elif row["name"] == "Razor":
        movement_speed_bonus = get_razor_unstable_current(lvl)
    # elif row["name"] == "Slardar":
    #     movement_speed_bonus = get_slardar_seaborn_sentinel(lvl, "movement speed")
    else:
        movement_speed_bonus = 1
    total_movement_speed_bonus = int(row["movement_speed"] * movement_speed_bonus)
    return total_movement_speed_bonus


def calc_vision_range_nighttime(row: Series, lvl: int) -> int:
    if row["name"] == "Luna":
        vision_range_nighttime_bonus = get_luna_lunar_blessing(lvl, "sight_range_night")
    else:
        vision_range_nighttime_bonus = 0
    total_vision_range_nighttime = (
        row["sight_range_night"] + vision_range_nighttime_bonus
    )
    return total_vision_range_nighttime
