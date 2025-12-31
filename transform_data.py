from pathlib import Path

import numpy as np
import pandas as pd


def calc_base_attack_damage(row: pd.Series, stats: str) -> int:
    if row["primary_attr"] == 0:
        result = row[f"damage_{stats}"] - row["str_base"]
    elif row["primary_attr"] == 1:
        result = row[f"damage_{stats}"] - row["agi_base"]
    elif row["primary_attr"] == 2:
        result = row[f"damage_{stats}"] - row["int_base"]
    elif row["primary_attr"] == 3:
        result = row[f"damage_{stats}"]
    return result


def calc_universal_attack_damage(row: pd.Series, stats: str) -> int:
    if row["primary_attr"] == 3:
        result = np.floor(
            (row["str_base"] + row["agi_base"] + row["int_base"]) * 0.45
            + row[f"damage_{stats}"]
        )
    else:
        result = row[f"damage_{stats}"]
    return result


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df["base_health_regen"] = df["health_regen"] - (0.1 * df["str_base"])
    df["base_mana_regen"] = df["mana_regen"] - (0.05 * df["int_base"])
    df["base_armor"] = df["armor"] - (df["agi_base"] / 6)
    df["base_damage_min"] = df.apply(calc_base_attack_damage, axis=1, stats="min")
    df["base_damage_max"] = df.apply(calc_base_attack_damage, axis=1, stats="max")
    df["base_damage_max"] = df.apply(calc_base_attack_damage, axis=1, stats="max")
    df["base_damage_max"] = df.apply(calc_base_attack_damage, axis=1, stats="max")
    # Calculate damage_min for hero with primary attribute = 3
    df["damage_min"] = df.apply(calc_universal_attack_damage, axis=1, stats="min")
    # Calculate damage_max for hero with primary attribute = 3
    df["damage_max"] = df.apply(calc_universal_attack_damage, axis=1, stats="max")
    df["damage_avg"] = np.floor((df["damage_min"] + df["damage_max"]) / 2)
    df["base_damage_avg"] = np.floor(
        (df["base_damage_min"] + df["base_damage_max"]) / 2
    )
    df["hype_loc"] = df["hype_loc"].str.replace("</?b>", "", regex=True)
    df["bio_loc"] = df["bio_loc"].str.replace("\s*<br\s*/?>\s*", "", regex=True)
    df["heroes_path"] = df["name_loc"].apply(
        lambda name: get_images_path(name, "heroes")
    )

    df["icons_path"] = df["name_loc"].apply(
        lambda name: get_images_path(name, "heroes", "icons")
    )

    final_df = df.drop(
        columns=[
            "order_id",
            "damage_min",
            "damage_max",
            "armor",
            "magic_resistance",
            "max_health",
            "health_regen",
            "max_mana",
            "mana_regen",
            "name_temp",
            "damage_avg",
        ]
    )

    final_df = final_df.rename(columns={"name_loc": "name"})

    return final_df


def get_images_path(name: str, *directories: str):
    # Construct path
    base = Path() / "assets" / "images"
    # Construct fullpath
    fullpath = base.joinpath(*directories)
    result = fullpath / (name.lower().replace(" ", "_").replace("'", "") + ".png")
    return result


def main():
    df = pd.read_csv("./assets/data/raw_data.csv").sort_values(
        by="name_loc", ignore_index=True
    )

    final_df = transform_data(df)

    final_df.to_csv("./assets/data/latest_data.csv", index=False)


if __name__ == "__main__":
    main()
