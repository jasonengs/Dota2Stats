import json

import pandas as pd


def rename_columns(df):
    columns = df.columns.to_list()
    results = []
    for i in columns:
        split_column_name = i.split("_")

        if len(split_column_name) > 1:
            results.append(
                split_column_name[0]
                + "".join(word.capitalize() for word in split_column_name[1:])
            )

        else:
            results.append(split_column_name[0])
    return results


def move_columns(df, start, end, at):
    col = df.columns.tolist()

    cols_to_move = col[start:end]
    cols_to_keep = [c for c in col if c not in cols_to_move]

    insert_col_at = at

    new_col_order = (
        cols_to_keep[:insert_col_at] + cols_to_move + cols_to_keep[insert_col_at:]
    )

    return new_col_order


df = pd.read_csv("./assets/data/latest_data.csv")

# Drop some columns
df = df.drop(
    columns=[
        "health",
        "health_regeneration",
        "mana",
        "mana_regeneration",
        "armor",
        "magic_resistance",
        "attack_speed",
    ]
)

df_attribute = pd.read_csv("./assets/data/attribute_icons.csv")

df_merge = df.merge(
    df_attribute, how="left", left_on="primary_attribute", right_on="name_as_key"
)

df_merge = df_merge.drop(columns=["name_as_key"])

# Merging Roles
df_roles = pd.read_csv("./assets/data/roles.csv")
df_hero_roles = pd.read_csv("./assets/data/hero_roles.csv")

df_roles_merge = df_hero_roles.merge(df_roles, how="inner", on="id")

# Dropping a column
df_roles_merge = df_roles_merge.drop(columns=["id"])

# Aggregating into List for the roles
df_roles_merge = (
    df_roles_merge.groupby("hero_id")["roles"].agg(lambda x: list(set(x))).reset_index()
)

# Merging df_merge with df_roles_merge
df_final = df_merge.merge(df_roles_merge, how="inner", left_on="id", right_on="hero_id")

# Remove hero id column from df_roles_merge
df_final = df_final.drop(columns=["hero_id"])

# Rename columns
renamed_column = rename_columns(df_final)

for i, col in enumerate(df_final.columns):
    df_final.columns.values[i] = renamed_column[i]

# Move columns
# df = df[move_columns(df, 14, 15, 6)]

# Move Base Agility
df_final = df_final[move_columns(df_final, 9, 10, 8)]

# Move Base Intelligence
df_final = df_final[move_columns(df_final, 11, 12, 9)]

df_final = df_final[move_columns(df_final, 26, 33, 13)]

df_final = df_final[move_columns(df_final, 21, 23, 20)]

# Save to JSON
df_final.to_json("./assets/data/latest_data.json", orient="records")

stats_key = df_final.columns.to_list()[7:29]

images_key = df_final.columns.to_list()[33:36]

with open("./assets/data/latest_data.json", "r") as f:
    data = json.load(f)

for hero in data:
    hero["stats"] = {key: hero.pop(key) for key in stats_key if key in hero}
    hero["images"] = {key: hero.pop(key) for key in images_key if key in hero}

with open("./assets/data/latest_data.json", "w") as f:
    json.dump(data, f, indent=4)
