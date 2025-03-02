import json
import pandas as pd

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
        "min_attack",
        "max_attack",
        "avg_attack",
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

# Save to JSON
df_final.to_json("./assets/data/latest_data.json", orient="records")

stats_key = [
    "base_strength",
    "base_agility",
    "base_intelligence",
    "strength_gain",
    "agility_gain",
    "intelligence_gain",
    "base_health",
    "base_mana",
    "base_health_regeneration",
    "base_mana_regeneration",
    "base_armor",
    "base_attack_speed",
    "base_min_attack",
    "base_max_attack",
    "base_avg_attack",
    "attack_range",
    "bat",
    "projectile_speed",
    "attack_point",
    "attack_backswing",
    "movement_speed_daytime",
    "turn_rate",
    "vision_range_daytime",
    "vision_range_nighttime",
]

images_key = ["hero_images_path", "hero_icons_path", "attribute_icons_path"]


with open("./assets/data/latest_data.json", "r") as f:
    data = json.load(f)

for hero in data:
    hero["stats"] = {key: hero.pop(key) for key in stats_key if key in hero}
    hero["images"] = {key: hero.pop(key) for key in images_key if key in hero}

with open("./assets/data/latest_data.json", "w") as f:
    json.dump(data, f, indent=4)
