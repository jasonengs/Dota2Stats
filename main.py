import os
import calc_stats
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


df = pd.read_csv("./assets/data/hero_cleaned.csv")

# df.head()


def get_bar_chart_heroes_base_attribute(df, heroes_option):
    # Filter DataFrame based on dropdown or select box
    filtered_df = df.query("name in @heroes_option")
    index_position = df.index.get_loc(filtered_df.index[0])

    # Transpose the DataFrame
    source = (
        filtered_df[["base_strength", "base_agility", "base_intelligence"]]
        .transpose()
        .reset_index()
        .rename(
            columns={"index": "base_attributes", index_position: "attribute_points"}
        )
        .sort_index()
    )

    # Remove base_ and Set to Capital
    source["base_attributes"] = (
        source["base_attributes"].str.replace("base_", "").str.capitalize()
    )

    color_scale = alt.Scale(
        domain=source["base_attributes"].tolist(),
        range=["#ec3d06", "#26e030", "#00d9ec"],
    )

    chart = (
        alt.Chart(source)
        .mark_bar()
        .encode(
            alt.X("base_attributes", type="ordinal", sort=None)
            .axis(labelAngle=0)
            .title("Attributes"),
            alt.Y("attribute_points")
            .axis(tickCount=5)
            .scale(zero=False)
            .title("Attribute Points"),
            color=alt.Color(
                "base_attributes",
                scale=color_scale,
                legend=alt.Legend(title="Attributes"),
            ),
            tooltip=[
                alt.Tooltip("base_attributes", title="Attribute"),
                alt.Tooltip("attribute_points", title="Attribute Points"),
            ],
        )
        .configure_axis(
            labelFontSize=15,
            titleFontSize=15,
        )
        .configure_title(fontSize=30)
        .configure_legend(titleFontSize=20, labelFontSize=15)
        .properties(title="Base Attributes", width=800, height=400)
    )
    return chart


st.title("Dota 2 Heroes")


# form_values = {
#     "name": None,
#     "heroes": None
# }


# with st.form(key="user_inf")


heroes_option = st.selectbox("Choose Heroes:", df.loc[:, "name"].sort_values().tolist())

st.write("You Selected:", heroes_option)

primary_attribute = df.query("name in @heroes_option")["primary_attribute"].iloc[0]
st.write(primary_attribute)

image_path = df.query("name in @heroes_option")["image_path"].iloc[0]

st.image(f"./{image_path}", caption=heroes_option)

chart = get_bar_chart_heroes_base_attribute(df, heroes_option)

st.altair_chart(chart)

# Text Input (Search Function)
hero_input = st.text_input("Search Heroes")

# Filter by Attributes
attribute_option = st.selectbox(
    "Choose Attribute:", df.loc[:, "primary_attribute"].unique().tolist()
)


hero_output = df.query(
    f"name.str.contains('{hero_input.capitalize()}') and primary_attribute in @attribute_option"
)[["name", "primary_attribute"]]

# Output as Table
st.table(hero_output)

# Compare

st.header("Compare Heroes Stats")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Hero 1")
    hero_option1 = st.selectbox(
        "Choose Hero:",
        df.loc[:, "name"].sort_values().tolist(),
        key="hero_option1",
        index=0,
    )

with col2:
    st.subheader("Hero 2")
    hero_option2 = st.selectbox(
        "Choose Hero:",
        df.loc[:, "name"].sort_values().tolist(),
        key="hero_option2",
        index=1,
    )

# options = [
#     "Strength",
#     "Agility",
#     "Intelligence",
#     "Health",
#     "Health Regeneration",
#     "Mana",
#     "Mana Regeneration",
#     "Armor",
#     "Magic Resistance",
#     "Damage",
#     "Attack Speed",
# ]

options = [
    "Health",
    "Health Regeneration",
    "Mana",
    "Mana Regeneration",
    "Armor",
    "Magic Resistance",
    "Attack Speed",
]

stat_options = st.selectbox(
    "Choose Stats:", options=options, key="stat_options", index=0
)

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
        .properties(title=f"{stats} Comparison", width=800, height=400)
    )

    return chart


st.altair_chart(get_comparison_chart(filtered_df, stat_options))

# chart_comparison = (
#     alt.Chart(df_melt)
#     .mark_bar()
#     .encode(
#         alt.X("lvl", type="ordinal", sort=None).title("Level"),
#         alt.Y("stats", type="quantitative").axis(tickCount=5).title("Armor"),
#         alt.Color("name").title("Name"),
#         alt.XOffset("name"),
#         tooltip=[
#             alt.Tooltip("lvl", title="Level"),
#             alt.Tooltip("stats", title="Armor", format=".1f"),
#             alt.Tooltip("name", title="Name"),
#         ],
#     )
#     .configure_axis(
#         labelFontSize=15,
#         labelAngle=0,
#         titleFontSize=15,
#     )
#     .configure_title(fontSize=30)
#     .configure_legend(titleFontSize=15, labelFontSize=15)
#     .properties(title="Armor Comparison", width=800, height=400)
# )

# st.altair_chart(chart_comparison)
