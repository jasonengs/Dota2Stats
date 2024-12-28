import os
import calc_stats
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt


df = pd.read_csv("./assets/data/2024_12_17_hero_cleaned.csv")

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
