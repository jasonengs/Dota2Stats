# This file can be ignored as the data already exists in assets/data directory

import os
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup


def create_directory(directory_name):
    try:
        os.mkdir(directory_name)
        print(f"Directory: {directory_name} Created Successfully")
    except FileExistsError:
        print(f"Directory: {directory_name} Already Exists")
    except PermissionError:
        print(f"Permission Denied: Unable to Create {directory_name}")
    except Exception as e:
        print(f"An Error Occurred: {e}")


def get_response(url, path=""):
    response = requests.get(f"{url}{path}")
    return response


def get_soup(response):
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def get_bat(soup, hero):
    data = soup.find(
        "table",
        style="width:300px; border-collapse:collapse; text-align:center; border-top:2px solid;",
    )
    index = 6 if hero != "Huskar" else 5
    pattern = r"\(([\d.]+) BAT\)"
    result = float(
        re.search(
            pattern,
            data.find_all(
                "div", style="position:absolute; bottom:3px; right:5px; font-size:80%;"
            )[index].getText(),
        ).group(1)
    )

    return result


def get_complexity(soup):
    result = int(
        len(
            soup.find("table", style="max-width:61.875rem").find_all(
                attrs={"title": "Hero Complexity"}
            )
        )
        // 2
    )
    return result


def get_quote(soup):
    result = soup.find("div", class_="quote-text").getText()
    return result


def get_full_name(soup):
    result = soup.find("div", class_="quote-source").getText().split(" ", 1)[-1].strip()
    return result


def get_lore(soup):
    result = (
        soup.find("div", style="display:table; max-width:61.875rem;")
        .find("div", style="display:table-cell;max-width:850px")
        .getText()
    )
    return result


def get_map_icon(soup, hero_name):
    updated_hero_name = hero_name.replace("_", " ")
    result = (
        soup.find("div", class_="quote-source")
        .find(attrs={"title": f"{updated_hero_name}"})
        .find("img")
        .get("srcset")
        .split(" ")[0]
    )
    return result


def get_image(soup):
    result = (
        soup.find(
            "div",
            style="float:right; clear:right; margin:.5em 0 1em .5em; padding:2px; width:306px; border:1px solid grey;",
        )
        .find("img")
        .get("src")
    )
    return result


def get_hero_attribute_stats(soup, index):
    hero_attribute_stats = soup.find(
        "div",
        style="float:right; clear:right; margin:.5em 0 1em .5em; padding:2px; width:306px; border:1px solid grey;",
    ).find_all("div", style="color:#FFF; text-shadow:1px 1px 2px #000;")
    result = hero_attribute_stats[index].getText()
    return result


def get_stats(soup, stats, index=0):
    data = soup.find(
        "table",
        style="width:300px; border-collapse:collapse; text-align:center; border-top:2px solid;",
    )
    try:
        if index == 0:
            result = data.find(attrs={"title": f"{stats.title()}"}).getText()
            return result
        else:
            result = (
                data.find_all(
                    "div", style="position:relative; text-align:center; font-size:85%;"
                )[index]
                .getText()
                .split(f"{stats.title()}")[0]
                .strip()
            )
            return result
    except AttributeError:
        result = pd.NA
        return result


def get_vision(soup, vision):
    vision_stats = (
        soup.find(
            "table",
            style="width:300px; border-collapse:collapse; text-align:center; border-top:2px solid;",
        )
        .find_all("div", style="position:relative; text-align:center; font-size:85%;")[
            11
        ]
        .getText()
    )
    split_vision_stats = vision_stats.split("/")
    if len(split_vision_stats) == 2:
        if vision.lower() == "day":
            result = int(split_vision_stats[0].strip())
        elif vision.lower() == "night":
            result = get_number_from_text(split_vision_stats[1])
            # result = int(re.split(r"[^\d]+", split_vision_stats[1].strip())[0])
    else:
        result = get_number_from_text(split_vision_stats[0])
        # int(re.split(r"[^\d]+", split_vision_stats[0].strip())[0])
    return result


# Helper Function for get_vision
def get_number_from_text(text):
    result = int(re.split(r"[^\d]+", text.strip())[0])
    return result


# Get Data From API
def get_data_from_api(url):
    # Declaring Variable
    id = []
    name = []
    primary_attribute = []
    attack_type = []
    roles = []
    legs = []

    # Request to API
    response = get_response(url)

    data = response.json()
    for i in data:
        id.append(i["id"])
        # Replace " " with "_" for example
        name.append(i["localized_name"].replace(" ", "_"))
        primary_attribute.append(i["primary_attr"])
        attack_type.append(i["attack_type"])
        roles.append(i["roles"])
        legs.append(i["legs"])

    # Create a DataFrame
    df = pd.DataFrame(
        data={
            "id": id,
            "name": name,
            "primary_attribute": primary_attribute,
            "attack_type": attack_type,
            "roles": roles,
            "legs": legs,
        }
    )

    return df


# Get Data From Website
def get_hero(df_api):
    base_url = "https://liquipedia.net/dota2/"
    base_strength_gain_per_lvl = []
    base_agility_gain_per_lvl = []
    base_intelligence_gain_per_lvl = []
    bat = []
    projectile_speed = []
    attack_range = []
    animation = []
    movement_speed_daytime = []
    turn_rate = []
    vision_range_daytime = []
    vision_range_nighttime = []
    gib_type = []
    complexity = []
    quote = []
    full_name = []
    image = []
    map_icon = []
    lore = []
    released = []

    modified_name = [hero for hero in df_api["name"].tolist()]

    for i in modified_name:
        response = get_response(f"{base_url}{i}")
        soup = get_soup(response)
        full_name.append(get_full_name(soup))
        base_strength_gain_per_lvl.append(get_hero_attribute_stats(soup, 0))
        base_agility_gain_per_lvl.append(get_hero_attribute_stats(soup, 1))
        base_intelligence_gain_per_lvl.append(get_hero_attribute_stats(soup, 2))
        projectile_speed.append(get_stats(soup, "projectile speed"))
        attack_range.append(get_stats(soup, "attack range", 4))
        bat.append(get_bat(soup, i))
        animation.append(get_stats(soup, "animation", 6))
        movement_speed_daytime.append(get_stats(soup, "move speed"))
        turn_rate.append(get_stats(soup, "turn rate", 8))
        vision_range_daytime.append(get_vision(soup, "day"))
        vision_range_nighttime.append(get_vision(soup, "night"))
        gib_type.append(get_stats(soup, "gib type"))
        complexity.append(get_complexity(soup))
        quote.append(get_quote(soup))
        lore.append(get_lore(soup))
        image.append(f"https://liquipedia.net{get_image(soup)}")
        map_icon.append(f"https://liquipedia.net{get_map_icon(soup, i)}")
        released.append(get_stats(soup, "released", 13))
        # Delay 1 Second for next iterate
        # print(i)
        time.sleep(1)

    df = pd.DataFrame(
        data={
            "id": df_api["id"],
            "name": df_api["name"],
            "full_name": full_name,
            "primary_attribute": df_api["primary_attribute"],
            "attack_type": df_api["attack_type"],
            "roles": df_api["roles"],
            "legs": df_api["legs"],
            "base_strength_gain_per_lvl": base_strength_gain_per_lvl,
            "base_agility_gain_per_lvl": base_agility_gain_per_lvl,
            "base_intelligence_gain_per_lvl": base_intelligence_gain_per_lvl,
            "projectile_speed": projectile_speed,
            "attack_range": attack_range,
            "bat": bat,
            "animation": animation,
            "movement_speed_daytime": movement_speed_daytime,
            "turn_rate": turn_rate,
            "vision_range_daytime": vision_range_daytime,
            "vision_range_nighttime": vision_range_nighttime,
            "gib_type": gib_type,
            "complexity": complexity,
            "quote": quote,
            "image": image,
            "map_icon": map_icon,
            "lore": lore,
            "released": released,
        }
    )

    return df


# Get Base Health Regeneration, Mana Regeneration, Armor, and Attack Speed
def get_base_stats(url, path, table_number):
    response = get_response(url, path)
    soup = get_soup(response)
    stats_keys = path.replace("/", "").lower()

    key_name = ["name", f"base_{stats_keys}"]

    stats_dict = {k: [] for k in key_name}

    for i in soup.find_all("table", class_="wikitable")[table_number].find_all("tr"):
        if not i.find("th"):
            base_value = i.getText()
            heroes = i.find_all("a")

            for h in heroes:
                stats_dict["name"].append(h.get("title").replace(" ", "_"))
                stats_dict[f"base_{stats_keys}"].append(base_value)

    df = pd.DataFrame(data=stats_dict)
    return df


# Get Base Attack Damage
def get_base_attack_damage():
    response = get_response("https://liquipedia.net/dota2/Attack_Damage/Heroes")

    soup = get_soup(response)

    key_name = [
        "name",
        "range",
        "base_min_attack",
        "base_max_attack",
        "base_avg_attack",
        # "main_min_attack",
        # "main_max_attack",
        # "main_avg_attack",
    ]

    attack_damage_dict = {k: [] for k in key_name}
    for table in soup.find_all("table", class_="wikitable sortable"):
        for idx, row in enumerate(table.find_all("tr")):
            # Skip Table Headers
            if idx > 1:
                data = row.find_all("td")
                for i, keys in enumerate(key_name):
                    if i != 1:
                        attack_damage_dict[keys].append(
                            data[i]
                            .getText()
                            .replace("\n", "")
                            .strip()
                            .replace(" ", "_")
                        )
    # Remove the range
    attack_damage_dict.pop("range")

    df = pd.DataFrame(data=attack_damage_dict)

    return df


def create_df_roles(df):
    df_roles = df.loc[:, ["id", "roles"]].explode("roles", ignore_index=True)

    df_roles = (
        df_roles.drop(columns="id")
        .drop_duplicates()
        .sort_values("roles")
        .reset_index(drop=True)
        .reset_index(names="id")
    )

    # Add 1 to id column as id start from 0
    df_roles["id"] = df_roles["id"] + 1

    # Cast datatype for the columns
    df_roles = df_roles.astype({"id": "int8", "roles": "category"})

    # Return df_roles
    return df_roles


def create_df_hero_roles(df, df_roles):
    df_hero_roles = df.loc[:, ["id", "roles"]].explode("roles", ignore_index=True)

    # Rename column for id to hero_id
    df_hero_roles = df_hero_roles.rename(columns={"id": "hero_id"})

    # Join df and df_roles
    df_hero_roles = df_hero_roles.merge(df_roles, how="inner", on="roles").drop(
        columns="roles"
    )
    # Cast datatype for hero_id columns
    df_hero_roles = df_hero_roles.astype({"hero_id": "int16"})

    # Return df_hero_roles
    return df_hero_roles


# Download Image from the website
def download_image(url, pattern, directory_name):
    # Get Current Directory
    cd = os.getcwd()
    # Get New Directory Path
    new_directory = os.path.join(cd, "assets/images", directory_name)
    # Create another directory
    os.makedirs(new_directory, exist_ok=True)

    for i in url:
        response = get_response(i)
        match = re.search(pattern, i)
        result = match.group().replace("%27", "").lower()
        save_as = os.path.join(new_directory, f"{result}.png")
        with open(save_as, "wb") as file:
            file.write(response.content)
        # Delay 1 Second for next iterate
        time.sleep(1)


# Download Map Icon from the website
def download_hero_icon(url):
    # Get Current Directory
    cd = os.getcwd()
    # Get Map Icon Path
    map_icon_path = os.path.join(cd, "assets/images", "hero_icons")
    # Create another directory
    os.makedirs(map_icon_path, exist_ok=True)
    # Regex Pattern
    pattern = r"/([^/]+(?:_[^/]+)?)_(?:mapicon|icon)|/([^/]+)icon"

    for i in url:
        response = get_response(i)
        match = re.search(pattern, i)
        if match.group(1):
            if match.group(1) != "Anti_Mage":
                if match.group(1) != "Outworld_Devourer":
                    result = match.group(1).replace("%27", "")
                else:
                    result = "Outworld_Destroyer"
            else:
                result = "Anti-Mage"
        else:
            result = match.group(2) if not match.group(2) else "Lone_Druid"
        save_as = os.path.join(map_icon_path, f"{result.lower()}.png")
        with open(save_as, "wb") as file:
            file.write(response.content)
        # Delay 1 Second for next iterate
        time.sleep(1)


# Get png files from directory
def get_png_from_directory(directory_name):
    # Get Current Directory
    cd = os.getcwd()
    # Get Path
    full_path = os.path.join(cd, "assets/images", directory_name)
    # List all the files in directory
    if os.path.exists(full_path):
        results = [
            os.path.join("assets/images", directory_name, file)
            for file in os.listdir(full_path)
        ]
    # Return the results
    return results


def create_df_for_img(directory_name):
    # Replace \\ with /
    img_path = [i.replace("\\", "/") for i in get_png_from_directory(directory_name)]

    # Remove the png use regex
    name = [
        re.search(rf"assets/images/{directory_name}/(.+?)\.png", i).group(1)
        for i in img_path
    ]
    df = pd.DataFrame(
        data={
            # Split the directory name by removing "_" and get the first index
            # for example attribute_icons to attribute
            "name_as_key": name,
            f"{directory_name}_path": img_path,
        }
    )

    return df


# Get Attribute Icon from website
def get_attribute_icon():
    url = "https://liquipedia.net/dota2/Portal:Heroes"
    response = get_response(url)
    soup = get_soup(response)
    attribute_icons = soup.find_all("div", class_="heroes-panel__category-title")
    # index 0: 36 x 36
    # index 2: 45 x 45
    results = [
        "https://liquipedia.net" + a.find("img").get("srcset").split(" ")[2]
        for a in attribute_icons
    ]
    return results


# Save DF to csv
def save_df_csv(df, file_name):
    # today = datetime.today().strftime("%Y_%m_%d")
    # today = f"{datetime.today(): %Y_%m_%d}"
    df.to_csv(f"assets/data/{file_name}.csv", index=False)


# --------------------------------------------------------------------
# Create Assets Directory to store data
create_directory("assets")

data_directory = os.path.join(os.getcwd(), "assets", "data")

# Create Data Directory inside thg Assets Directory
create_directory(data_directory)

image_directory = os.path.join(os.getcwd(), "assets", "images")
# Create Image Directory for storing png file
create_directory(image_directory)

url = "https://api.opendota.com/api/heroes"
df_data_from_api = get_data_from_api(url)


df = get_hero(df_data_from_api)

# Get Base Health Regeneration DataFrame
df_base_health_regen = get_base_stats(
    "https://liquipedia.net/dota2", "/Health_Regeneration", 1
)


# Get Base Mana Regeneration DataFrame
df_base_mana_regen = get_base_stats(
    "https://liquipedia.net/dota2", "/Mana_Regeneration", 1
)


# Get Base Armor DataFrame
df_base_armor = get_base_stats("https://liquipedia.net/dota2", "/Armor", 0)


# Get Base Attack Speed DataFrame
df_base_attack_speed = get_base_stats(
    "https://liquipedia.net/dota2", "/Attack_Speed", 4
)

# Get Base Attack Damage DataFrame
df_base_attack_damage = get_base_attack_damage()

# Get Roles DataFrame
df_roles = create_df_roles(df)

# Get Hero Roles DataFrame
df_hero_roles = create_df_hero_roles(df, df_roles)

# Download Image
download_image(df["image"], r"(?<=\/)([^/]+)(?=_Large)", "hero_images")
df_image = create_df_for_img("hero_images")

# Download Map Icon
download_hero_icon(df["map_icon"])
df_map_icon = create_df_for_img("hero_icons")


df = (
    df.merge(df_base_health_regen, how="inner", on="name")
    .merge(df_base_mana_regen, how="inner", on="name")
    .merge(df_base_armor, how="inner", on="name")
    .merge(df_base_attack_speed, how="inner", on="name")
    .merge(df_base_attack_damage, how="inner", on="name")
)

df["name_as_key"] = df["name"].apply(
    lambda x: x.lower() if "'" not in x else x.replace("'", "").lower()
)

df = df.merge(df_image, how="inner", on="name_as_key").merge(
    df_map_icon, how="inner", on="name_as_key"
)

# Save the raw file without cleaning
save_df_csv(df, "hero_raw")


# Attributes
attribute_icons = get_attribute_icon()

# Download Attribute Icons From Website
download_image(attribute_icons, r"(?<=Dota2_)[^_]+(?=_icon)", "attribute_icons")

# Create DataFrame for Attribute Icons
df_attribute_icons = create_df_for_img("attribute_icons")

# Save Attribute Icons as csv file
save_df_csv(df_attribute_icons, "attribute_icons")
save_df_csv(df_attribute_icons, "attribute_icons")
