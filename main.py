import calc_stats
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

df = pd.read_csv("./assets/data/latest_data.csv")

st.title("Dota2Stats")
st.header("Heroes Stats Comparison")
st.subheader("Version: 7.38")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Hero 1")
    hero_option1 = st.selectbox(
        "Choose Hero:",
        df.loc[:, "name"].sort_values().tolist(),
        key="hero_option1",
        index=0,
    )
    image_path1 = df.query("name in @hero_option1")["image_path"].iloc[0]
    st.image(f"./{image_path1}")


with col2:
    st.subheader("Hero 2")
    hero_option2 = st.selectbox(
        "Choose Hero:",
        df.loc[:, "name"].sort_values().tolist(),
        key="hero_option2",
        index=1,
    )
    image_path2 = df.query("name in @hero_option2")["image_path"].iloc[0]
    st.image(f"./{image_path2}")

# Dropdown Options
options = [
    "Health",
    "Health Regeneration",
    "Mana",
    "Mana Regeneration",
    "Armor",
    "Magic Resistance",
    "Attack Speed",
    "Attack Damage",
    "Strength",
    "Agility",
    "Intelligence",
]
# Sort the Dropdown Options
options.sort()

# Create a Dropdown
stat_options = st.selectbox(
    "Choose Stats:", options=options, key="stat_options", index=0
)

# Filter DataFrame from hero selected in Dropdown
filtered_df = df.query("name in @hero_option1 or name in @hero_option2")


def get_comparison_chart(df, stats):
    if stats == "Health":
        chart = get_bar_chart(reshape_df(df, calc_stats.calc_health, stats), stats)
    elif stats == "Health Regeneration":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_health_regeneration, stats), stats
        )
    elif stats == "Mana":
        chart = get_bar_chart(reshape_df(df, calc_stats.calc_mana, stats), stats)
    elif stats == "Mana Regeneration":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_mana_regeneration, stats), stats
        )
    elif stats == "Armor":
        chart = get_bar_chart(reshape_df(df, calc_stats.calc_armor, stats), stats)
    elif stats == "Magic Resistance":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_magic_resistance, stats), stats
        )
    elif stats == "Attack Speed":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_attack_speed, stats), stats
        )
    elif stats == "Attack Damage":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_avg_attack_damage, stats), stats
        )
    elif stats == "Strength":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_total_strength, stats), stats
        )
    elif stats == "Agility":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_total_agility, stats), stats
        )
    elif stats == "Intelligence":
        chart = get_bar_chart(
            reshape_df(df, calc_stats.calc_total_intelligence, stats), stats
        )

    return chart


def reshape_df(df, calc_function, stats):
    df_stats = df.assign(
        lvl_1=df.apply(calc_function, axis=1, lvl=1),
        lvl_5=df.apply(calc_function, axis=1, lvl=5),
        lvl_10=df.apply(calc_function, axis=1, lvl=10),
        lvl_15=df.apply(calc_function, axis=1, lvl=15),
        lvl_20=df.apply(calc_function, axis=1, lvl=20),
        lvl_25=df.apply(calc_function, axis=1, lvl=25),
        lvl_30=df.apply(calc_function, axis=1, lvl=30),
    )[["name", "lvl_1", "lvl_5", "lvl_10", "lvl_15", "lvl_20", "lvl_25", "lvl_30"]]
    df_reshape = df_stats.melt(id_vars=["name"], var_name="lvl", value_name=stats)

    df_reshape["lvl"] = df_reshape["lvl"].str.replace("lvl_", "")

    return df_reshape


def get_bar_chart(df, stats):
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("lvl", type="ordinal", sort=None).title("Level"),
            alt.Y(stats, type="quantitative").axis(tickCount=5).title(stats),
            alt.Color("name").title("Name"),
            alt.XOffset("name"),
            tooltip=[
                alt.Tooltip("lvl", title="Level"),
                alt.Tooltip(stats, title=stats, format=".1f"),
                alt.Tooltip("name", title="Name"),
            ],
        )
        .configure_axis(
            labelFontSize=15,
            labelAngle=0,
            titleFontSize=15,
        )
        .configure_title(fontSize=30)
        .configure_legend(titleFontSize=15, labelFontSize=15)
        .properties(title=stats, width=800, height=450)
    )

    return chart


# Display Altair Chart
st.altair_chart(get_comparison_chart(filtered_df, stat_options))
