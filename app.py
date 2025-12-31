from typing import Callable

import altair as alt
import pandas as pd
import streamlit as st

import calc_stats


def get_stats_fn() -> dict[str, Callable]:
    stats = {
        "Health": calc_stats.calc_health,
        "Health Regen": calc_stats.calc_health_regen,
        "Mana": calc_stats.calc_mana,
        "Mana Regen": calc_stats.calc_mana_regen,
        "Armor": calc_stats.calc_armor,
        "Magic Resistance": calc_stats.calc_magic_resistance,
        "Attack Damage": calc_stats.calc_attack_damage_avg,
        "Strength": calc_stats.calc_total_str,
        "Agility": calc_stats.calc_total_agi,
        "Intelligence": calc_stats.calc_total_int,
    }
    return stats


def load_data() -> pd.DataFrame:
    df = pd.read_csv("./assets/data/latest_data.csv")

    return df


def show_hero_img(col: int, df: pd.DataFrame, selected_hero: str) -> None:
    st.subheader(f"Hero : {col}")
    img = df.loc[df["name"] == selected_hero, "heroes_path"].iloc[0]
    st.image(img, caption=selected_hero)


def select_hero_options(col: int, df: pd.DataFrame) -> str:
    selected_hero = st.selectbox(
        "Choose a Hero:",
        df.loc[:, "name"].sort_values().tolist(),
        key=f"hero_option-{col}",
        index=col - 1,
    )
    return selected_hero


def melt_df(df: pd.DataFrame, stats: str, stats_fn: Callable) -> pd.DataFrame:
    levels = [1, 5, 10, 15, 20, 25, 30]

    stats_df = df.copy()

    for i in levels:
        stats_df.loc[:, f"lvl_{i}"] = stats_df.apply(stats_fn, lvl=i, axis=1)

    selected_columns_df = stats_df.iloc[:, [1] + list(range(29, stats_df.shape[1]))]

    final_df = selected_columns_df.melt(
        id_vars=["name"], var_name="lvl", value_name=stats
    )

    final_df["lvl"] = final_df["lvl"].str.replace("lvl_", "")

    return final_df


def get_bar_chart(df: pd.DataFrame, stats: str) -> alt.Chart:
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
            grid=False,
            labelFontSize=15,
            labelAngle=0,
            titleFontSize=15,
        )
        .configure_title(fontSize=30)
        .configure_legend(titleFontSize=15, labelFontSize=15)
        .properties(title=stats, width=800, height=450)
    )

    return chart


st.title("Dota2Stats")
st.header("Heroes Stats Comparison")
st.subheader("Patch: 7.40b")

df = load_data()

col1, col2 = st.columns(2)

with col1:
    selected_hero_1 = select_hero_options(1, df)
    show_hero_img(1, df, selected_hero_1)
with col2:
    selected_hero_2 = select_hero_options(2, df)
    show_hero_img(2, df, selected_hero_2)

stats = get_stats_fn()

sorted_stats = sorted(list(stats.keys()))

selected_stat = st.selectbox(
    "Choose Stats:", options=sorted_stats, key="selected_stat", index=0
)

stats_fn = stats.get(selected_stat)

filtered_df = df.loc[(df["name"].isin([selected_hero_1, selected_hero_2]))]

st.altair_chart(
    get_bar_chart(melt_df(filtered_df, selected_stat, stats_fn), selected_stat)
)
