import numpy as np


def get_bonus_attributes(row, lvl):
    additional_bonus = 0 if row != "Morphling" else 3
    if lvl >= 1 and lvl <= 16:
        bonus = 0 * (additional_bonus * 0)
    elif lvl >= 17 and lvl <= 18:
        bonus = 2 + (additional_bonus * 1)
    elif lvl >= 19 and lvl <= 20:
        bonus = 4 + (additional_bonus * 2)
    elif lvl == 21:
        bonus = 6 + (additional_bonus * 3)
    elif lvl == 22:
        bonus = 8 + (additional_bonus * 4)
    elif lvl == 23:
        bonus = 10 + (additional_bonus * 5)
    elif lvl >= 24 and lvl <= 25:
        bonus = 12 + (additional_bonus * 6)
    elif lvl >= 26:
        bonus = 14 + (additional_bonus * 7)
    return bonus


def get_total_attributes(row_base, row_gain, lvl, bonus):
    result = row_base + (row_gain * (lvl - 1)) + bonus
    return result


# Dragon Knight for Health Regeneration and Armor
def get_dragon_knight_dragon_blood(lvl):
    result = 2 + lvl * 0.5
    return result


# Luna Innate
def get_luna_lunar_blessing(lvl, stats):
    if stats.lower() == "attack damage":
        result = 2 * lvl
    elif stats.lower() == "vision range nighttime":
        result = 250 + (25 * lvl)
    return result


# Sven Facet
def get_sven_wrath_of_god(lvl):
    if lvl >= 1 and lvl <= 5:
        bonus_per_strength = 0.0
    elif lvl >= 6 and lvl <= 11:
        bonus_per_strength = 0.3
    elif lvl >= 12 and lvl <= 17:
        bonus_per_strength = 0.4
    elif lvl >= 18:
        bonus_per_strength = 0.5
    else:
        bonus_per_strength = 0.0
    return bonus_per_strength


# Ursa Innate
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


# Sniper Innate
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


# Razor Innate
def get_razor_unstable_current(lvl):
    result = 1 + (lvl / 100)
    return result


# Death Prophet Innate
def get_death_prophet_witchcraft(lvl):
    result = 1 + (lvl * 0.5 / 100)
    return result


# Void Spirit Innate
def get_void_spirit_intrinsic_edge():
    result = 1.25
    return result


# Outwolrd Destroyer Innate
def get_outworld_destroyer_ominous_discernment():
    result = 2.5
    return result


# Crystal Maiden Innate
def get_crystal_maiden_blueheart_floe(lvl):
    if lvl >= 1 and lvl <= 5:
        mana_regeneration_amplification = 1.25
    elif lvl >= 6 and lvl <= 11:
        mana_regeneration_amplification = 1.50
    elif lvl >= 12 and lvl <= 17:
        mana_regeneration_amplification = 1.75
    elif lvl >= 18:
        mana_regeneration_amplification = 2.0
    else:
        mana_regeneration_amplification = 0.0
    return mana_regeneration_amplification


# Drow Ranger Innate
def get_drow_ranger_precision_aura(lvl):
    if lvl >= 1 and lvl <= 5:
        result = 1.04 + (lvl * 0.01)
    elif lvl >= 6 and lvl <= 11:
        result = 1.08 + (lvl * 0.01)
    elif lvl >= 12 and lvl <= 17:
        result = 1.12 + (lvl * 0.01)
    elif lvl >= 18:
        result = 1.16 + (lvl * 0.01)
    else:
        result = 0.0
    return result


def calc_total_strength(row, lvl):
    # Invoker has no bonus attribute
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    result = get_total_attributes(
        row["base_strength"], row["strength_gain"], lvl, bonus
    )
    return result


def calc_total_agility(row, lvl):
    # Invoker has no bonus attribute
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    total_agility = get_total_attributes(
        row["base_agility"], row["agility_gain"], lvl, bonus
    )

    if row["name"] == "Drow Ranger":
        agility_bonus = get_drow_ranger_precision_aura(lvl)
        result = np.round(total_agility * agility_bonus)
    else:
        result = total_agility
    return result


def calc_total_intelligence(row, lvl):
    # Invoker has no bonus attribute
    bonus = 0 if row["name"] == "Invoker" else get_bonus_attributes(row["name"], lvl)
    result = get_total_attributes(
        row["base_intelligence"], row["intelligence_gain"], lvl, bonus
    )
    return result


def calc_health(row, lvl):
    total_strength = np.floor(calc_total_strength(row, lvl))
    result = 120 + total_strength * 22
    return result


def calc_health_regeneration(row, lvl):
    total_strength = calc_total_strength(row, lvl)
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
    total_intelligence = np.floor(calc_total_intelligence(row, lvl))
    if row["name"] == "Huskar":
        result = np.nan
    elif row["name"] == "Ogre Magi":
        total_strength = calc_total_strength(row, lvl)
        result = 120 + np.floor(total_strength * 6)
    elif row["name"] == "Outworld Destroyer":
        mana_per_intelligence_bonus = get_outworld_destroyer_ominous_discernment()
        result = round(75 + total_intelligence * (12 + mana_per_intelligence_bonus))
    else:
        result = 75 + total_intelligence * 12
    return result


def calc_mana_regeneration(row, lvl):
    total_intelligence = calc_total_intelligence(row, lvl)
    mana_regeneration_per_intelligence = 0.05
    if row["name"] == "Huskar":
        result = np.nan
    elif row["name"] == "Lich":
        result = np.float32(0)
    elif row["name"] == "Crystal Maiden":
        mana_regeneration_amplification = get_crystal_maiden_blueheart_floe(lvl)
        result = round(
            (
                row["base_mana_regeneration"]
                + total_intelligence * mana_regeneration_per_intelligence
            )
            * mana_regeneration_amplification,
            2,
        )
    elif row["name"] == "Ogre Magi":
        total_strength = calc_total_strength(row, lvl)
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
    total_agility = calc_total_agility(row, lvl)
    result = round(row["base_attack_speed"] + total_agility)
    return result


def calc_armor(row, lvl):
    total_agility = calc_total_agility(row, lvl)
    armor_per_agility = 1 / 6
    if row["name"] == "Dragon Knight":
        armor_bonus = get_dragon_knight_dragon_blood(lvl)
        armor_per_agility_bonus = 1
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
    magic_resistance_per_intelligence = 0.1
    total_intelligence = calc_total_intelligence(row, lvl)
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
    if row["primary_attribute"] == "Strength":
        total_strength = calc_total_strength(row, lvl)
        if row["name"] == "Sven":
            attack_damage_bonus = get_sven_wrath_of_god(lvl)
        else:
            attack_damage_bonus = 0

        result = np.floor(
            (row[f"base_{stats}_attack"])
            + total_strength
            + np.floor(total_strength * attack_damage_bonus)
        )
    elif row["primary_attribute"] == "Agility":
        total_agility = calc_total_agility(row, lvl)
        if row["name"] == "Luna":
            attack_damage_bonus = get_luna_lunar_blessing(lvl, "attack damage")
            result = np.floor(
                row[f"base_{stats}_attack"] + total_agility + attack_damage_bonus
            )
        elif row["name"] == "Ursa":
            total_health = calc_health(row, lvl)
            attack_damage_bonus = get_ursa_maul(lvl)
            result = np.floor(
                row[f"base_{stats}_attack"]
                + np.floor(total_agility)
                + (total_health * attack_damage_bonus)
            )
        else:
            result = np.floor(row[f"base_{stats}_attack"] + total_agility)
    elif row["primary_attribute"] == "Intelligence":
        total_intelligence = calc_total_intelligence(row, lvl)
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
        total_strength = calc_total_strength(row, lvl)
        total_agility = calc_total_agility(row, lvl)
        total_intelligence = calc_total_intelligence(row, lvl)

        point_per_attribute = 0.45
        result = np.floor(
            row[f"base_{stats}_attack"]
            + np.floor(total_strength + total_agility + total_intelligence)
            * point_per_attribute
        )
    return result


def calc_min_attack_damage(row, lvl):
    result = calc_attack_damage(row, lvl, "min")
    return result


def calc_max_attack_damage(row, lvl):
    result = calc_attack_damage(row, lvl, "max")
    return result


def calc_avg_attack_damage(row, lvl):
    result = calc_attack_damage(row, lvl, "avg")
    return result


def calc_attack_range(row, lvl):
    if row["name"] == "Sniper":
        attack_range_bonus = get_sniper_keen_scope(lvl)
    else:
        attack_range_bonus = 0
    result = row["attack_range"] + attack_range_bonus
    return result


def calc_movement_speed(row, lvl):
    if row["name"] == "Death Prophet":
        movement_speed_bonus = get_death_prophet_witchcraft(lvl)
    elif row["name"] == "Razor":
        movement_speed_bonus = get_razor_unstable_current(lvl)
    else:
        movement_speed_bonus = 1
    result = int(row["movement_speed"] * movement_speed_bonus)
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
