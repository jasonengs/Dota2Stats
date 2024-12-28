import numpy as np


def get_bonus_attributes(row, lvl):
    additional_bonus = 1 if row != "Morphling" else 2
    if lvl >= 1 and lvl <= 16:
        bonus = 0 * additional_bonus
    elif lvl >= 17 and lvl <= 18:
        bonus = 2 * additional_bonus
    elif lvl >= 19 and lvl <= 20:
        bonus = 4 * additional_bonus
    elif lvl == 21:
        bonus = 6 * additional_bonus
    elif lvl == 22:
        bonus = 8 * additional_bonus
    elif lvl == 23:
        bonus = 10 * additional_bonus
    elif lvl >= 24 and lvl <= 25:
        bonus = 12 * additional_bonus
    elif lvl >= 26:
        bonus = 14 * additional_bonus
    return bonus


def get_total_attributes(row_base, row_gain, lvl, bonus):
    result = row_base + (row_gain * (lvl - 1)) + bonus
    return result


# Dragon Knight for Health Regeneration and Armor
def get_dragon_knight_dragon_blood(lvl):
    result = 2 + lvl * 0.5
    return result


def get_luna_lunar_blessing(lvl, stats):
    if stats.lower() == "attack damage":
        result = 2 * lvl
    elif stats.lower() == "vision range nighttime":
        result = 250 + (25 * lvl)
    return result


def get_sven_wrath_of_god(lvl):
    if lvl >= 1 and lvl <= 5:
        bonus_per_strength = 0.4
    elif lvl >= 6 and lvl <= 11:
        bonus_per_strength = 0.5
    elif lvl >= 12 and lvl <= 17:
        bonus_per_strength = 0.6
    elif lvl >= 18:
        bonus_per_strength = 0.7
    else:
        bonus_per_strength = 0.0
    return bonus_per_strength


def get_ursa_maul(lvl):
    if lvl >= 1 and lvl <= 5:
        health_as_damage = round(1.2 / 100, 3)
    elif lvl >= 6 and lvl <= 11:
        health_as_damage = round(1.3 / 100, 3)
    elif lvl >= 12 and lvl <= 17:
        health_as_damage = round(1.4 / 100, 3)
    elif lvl >= 18:
        health_as_damage = round(1.5 / 100, 3)
    else:
        health_as_damage = 0.0
    return health_as_damage


def get_sniper_keen_scope(lvl):
    if lvl >= 1 and lvl <= 5:
        result = 160
    elif lvl >= 6 and lvl <= 11:
        result = 260
    elif lvl >= 12 and lvl <= 17:
        result = 360
    elif lvl >= 18:
        result = 460
    return result


def get_razor_unstable_current(lvl):
    result = 1 + (lvl / 100)
    return result


def get_death_prophet_witchcraft(lvl):
    result = 1 + (lvl * 0.75 / 100)
    return result


def get_void_spirit_intrinsic_edge():
    result = 1.25
    return result


def get_outworld_destroyer_ominous_discernment():
    result = 2.5
    return result


def get_crystal_maiden_blueheart_floe():
    result = 1.5
    return result


def get_drow_ranger_precision_aura(lvl):
    result = 1 + (lvl * 0.02)
    return result


def calc_health(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)

    total_strength = np.floor(
        get_total_attributes(row["base_strength"], row["strength_gain"], lvl, bonus)
    )
    result = 120 + total_strength * 22
    return result


def calc_health_regeneration(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_strength = get_total_attributes(
        row["base_strength"], row["strength_gain"], lvl, bonus
    )
    health_regeneration_per_strength = 0.1
    if row["name"] == "Dragon Knight":
        health_regeneration_bonus = get_dragon_knight_dragon_blood(lvl)
        health_regeneration_per_strength_bonus = 1
    elif row["name"] == "Void Spirit":
        health_regeneration_bonus = 0
        health_regeneration_per_strength_bonus = get_void_spirit_intrinsic_edge()
    else:
        health_regeneration_bonus = 0
        health_regeneration_per_strength_bonus = 1
    result = round(
        row["base_health_regeneration"]
        + total_strength
        * (health_regeneration_per_strength * health_regeneration_per_strength_bonus)
        + health_regeneration_bonus,
        2,
    )
    return result


def calc_mana(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_intelligence = np.floor(
        get_total_attributes(
            row["base_intelligence"], row["intelligence_gain"], lvl, bonus
        )
    )
    if row["name"] == "Huskar":
        result = np.nan
    elif row["name"] == "Ogre Magi":
        total_strength = get_total_attributes(
            row["base_strength"], row["strength_gain"], lvl, bonus
        )
        result = 120 + np.floor(total_strength * 6)
    elif row["name"] == "Outworld Destroyer":
        mana_per_intelligence_bonus = get_outworld_destroyer_ominous_discernment()
        result = round(75 + total_intelligence * (12 + mana_per_intelligence_bonus))
    else:
        result = 75 + total_intelligence * 12
    return result


def calc_mana_regeneration(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_intelligence = get_total_attributes(
        row["base_intelligence"], row["intelligence_gain"], lvl, bonus
    )
    mana_regeneration_per_intelligence = 0.05
    if row["name"] == "Huskar":
        result = np.nan
    if row["name"] == "Lich":
        result = np.float32(0)
    elif row["name"] == "Crystal Maiden":
        mana_regeneration_amplification = get_crystal_maiden_blueheart_floe()
        result = round(
            (
                row["base_mana_regeneration"]
                + total_intelligence * mana_regeneration_per_intelligence
            )
            * mana_regeneration_amplification,
            2,
        )
    elif row["name"] == "Ogre Magi":
        total_strength = get_total_attributes(
            row["base_strength"], row["strength_gain"], lvl, bonus
        )
        result = round(row["base_mana_regeneration"] + total_strength * 0.02, 2)
    elif row["name"] == "Void Spirit":
        mana_regeneration_per_intelligence_bonus = get_void_spirit_intrinsic_edge()
        result = round(
            row["base_mana_regeneration"]
            + total_intelligence
            * (
                mana_regeneration_per_intelligence
                * mana_regeneration_per_intelligence_bonus
            ),
            2,
        )
    else:
        result = round(
            row["base_mana_regeneration"]
            + total_intelligence * mana_regeneration_per_intelligence,
            2,
        )
    return result


def calc_attack_speed(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_agility = get_total_attributes(
        row["base_agility"], row["agility_gain"], lvl, bonus
    )
    if row["name"] == "Drow Ranger":
        agility_bonus = get_drow_ranger_precision_aura(lvl)
    else:
        agility_bonus = 1
    result = round(row["base_attack_speed"] + total_agility * (1 * agility_bonus))
    return result


def calc_armor(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_agility = get_total_attributes(
        row["base_agility"], row["agility_gain"], lvl, bonus
    )
    armor_per_agility = 1 / 6
    if row["name"] == "Dragon Knight":
        armor_bonus = get_dragon_knight_dragon_blood(lvl)
        armor_per_agility_bonus = 1
    elif row["name"] == "Drow Ranger":
        armor_bonus = 0
        armor_per_agility_bonus = get_drow_ranger_precision_aura(lvl)
    elif row["name"] == "Void Spirit":
        armor_bonus = 0
        armor_per_agility_bonus = get_void_spirit_intrinsic_edge()
    else:
        armor_bonus = 0
        armor_per_agility_bonus = 1

    result = round(
        row["base_armor"]
        + total_agility * (armor_per_agility * armor_per_agility_bonus)
        + armor_bonus,
        1,
    )
    return result


def calc_magic_resistance(row, lvl):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    magic_resistance_per_intelligence = 0.1
    total_intelligence = get_total_attributes(
        row["base_intelligence"], row["intelligence_gain"], lvl, bonus
    )
    if row["name"] == "Void Spirit":
        magic_resistance_per_intelligence_bonus = get_void_spirit_intrinsic_edge()
    elif row["name"] == "Ogre Magi":
        # Ogre Magi Max Intelligence is 0 It means it cannot be added by attribute bonus
        magic_resistance_per_intelligence_bonus = 1
        total_intelligence = 0
    else:
        magic_resistance_per_intelligence_bonus = 1
    result = round(
        25
        + total_intelligence
        * (magic_resistance_per_intelligence * magic_resistance_per_intelligence_bonus)
    )
    return result


def calc_attack_damage(row, lvl, stats):
    # Invoker has no bonus attributes
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_strength = get_total_attributes(
        row["base_strength"], row["strength_gain"], lvl, bonus
    )
    total_agility = get_total_attributes(
        row["base_agility"], row["agility_gain"], lvl, bonus
    )
    total_intelligence = get_total_attributes(
        row["base_intelligence"], row["intelligence_gain"], lvl, bonus
    )
    if row["primary_attribute"] == "Strength":
        if row["name"] == "Sven":
            attack_damage_bonus = get_sven_wrath_of_god(lvl)
            attack_damage_reduction = 20
        else:
            attack_damage_bonus = 0
            attack_damage_reduction = 0

        result = np.floor(
            (row[f"base_{stats}_attack"] - attack_damage_reduction)
            + total_strength
            + np.floor(total_strength * attack_damage_bonus)
        )
    elif row["primary_attribute"] == "Agility":
        if row["name"] == "Drow Ranger":
            attack_damage_bonus = get_drow_ranger_precision_aura(lvl)
            result = np.floor(
                row[f"base_{stats}_attack"] + total_agility * (attack_damage_bonus)
            )
        elif row["name"] == "Luna":
            attack_damage_bonus = get_luna_lunar_blessing(lvl, "attack damage")
            result = np.floor(
                row[f"base_{stats}_attack"] + total_agility + attack_damage_bonus
            )
        elif row["name"] == "Ursa":
            total_health = 120 + np.floor(total_strength) * 22
            attack_damage_bonus = get_ursa_maul(lvl)
            result = np.floor(
                row[f"base_{stats}_attack"]
                + np.floor(total_agility)
                + (total_health * attack_damage_bonus)
            )
        else:
            result = np.floor(row[f"base_{stats}_attack"] + total_agility)
    elif row["primary_attribute"] == "Intelligence":
        if row["name"] == "Jakiro":
            attack_damage_reduction = 50 / 100
            total_attack_damage_reduction = (
                row["base_avg_attack"] + total_intelligence
            ) * attack_damage_reduction
            result = np.floor(
                row[f"base_{stats}_attack"]
                + total_intelligence
                - np.floor(total_attack_damage_reduction)
            )
        else:
            result = np.floor((row[f"base_{stats}_attack"] + total_intelligence))

    elif row["primary_attribute"] == "Universal":
        point_per_attribute = 0.7
        result = np.floor(
            row[f"base_{stats}_attack"]
            + np.floor(total_strength + total_agility + total_intelligence)
            * point_per_attribute
        )
    return result


def calc_attack_range(row, lvl):
    if row["name"] == "Sniper":
        attack_range_bonus = get_sniper_keen_scope(lvl)
    else:
        attack_range_bonus = 0
    result = row["attack_range"] + attack_range_bonus
    return result


def calc_movement_speed_daytime(row, lvl):
    if row["name"] == "Death Prophet":
        movement_speed_bonus = get_death_prophet_witchcraft(lvl)
    elif row["name"] == "Razor":
        movement_speed_bonus = get_razor_unstable_current(lvl)
    else:
        movement_speed_bonus = 1
    result = int(row["movement_speed_daytime"] * movement_speed_bonus)
    return result


def calc_movement_speed_nighttime(row, lvl):
    if row["name"] == "Death Prophet":
        movement_speed_bonus = get_death_prophet_witchcraft(lvl)
    elif row["name"] == "Razor":
        movement_speed_bonus = get_razor_unstable_current(lvl)
    else:
        movement_speed_bonus = 1
    result = int((row["movement_speed_daytime"] + 30) * movement_speed_bonus)
    return result


def calc_vision_range_nighttime(row, lvl):
    if row["name"] == "Luna":
        vision_range_nighttime_bonus = get_luna_lunar_blessing(
            lvl, "vision range nighttime"
        )
    else:
        vision_range_nighttime_bonus = 0
    result = row["vision_range_nighttime"] + vision_range_nighttime_bonus
    return result
