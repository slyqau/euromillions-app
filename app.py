import pandas as pd
import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions Boost+ Advanced", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("euromillions_full_1000.csv")
        df["Date"] = pd.to_datetime(df["Date"])
        return df
    except:
        return pd.DataFrame()

def compute_scores(df):
    all_numbers = df[["N1", "N2", "N3", "N4", "N5"]].values.flatten()
    all_stars = df[["E1", "E2"]].values.flatten()
    freq_main = Counter(all_numbers)
    freq_star = Counter(all_stars)

    recent_df = df.sort_values("Date").tail(50)
    recent_main = recent_df[["N1", "N2", "N3", "N4", "N5"]].values.flatten()
    recent_star = recent_df[["E1", "E2"]].values.flatten()
    freq_recent_main = Counter(recent_main)
    freq_recent_star = Counter(recent_star)

    all_draws = df.sort_values("Date")

    def get_retard(n):
        for i, row in enumerate(all_draws.itertuples(index=False)):
            if n in [row.N1, row.N2, row.N3, row.N4, row.N5]:
                return len(all_draws) - i
        return len(all_draws)

    def get_retard_star(s):
        for i, row in enumerate(all_draws.itertuples(index=False)):
            if s in [row.E1, row.E2]:
                return len(all_draws) - i
        return len(all_draws)

    main_scores = {
        n: {
            "score": freq_main[n]*0.4 + freq_recent_main[n]*0.3 + get_retard(n)*0.3,
            "retard": get_retard(n),
            "freq_total": freq_main[n],
            "freq_50": freq_recent_main[n]
        }
        for n in range(1, 51)
    }

    star_scores = {
        s: {
            "score": freq_star[s]*0.4 + freq_recent_star[s]*0.3 + get_retard_star(s)*0.3,
            "retard": get_retard_star(s),
            "freq_total": freq_star[s],
            "freq_50": freq_recent_star[s]
        }
        for s in range(1, 13)
    }

    return main_scores, star_scores

def generate_grid_from_pool(pool, count):
    return sorted(random.sample(pool, count))

df = load_data()

st.title("💸 EuroMillions Boost+ Advanced")

if df.empty:
    st.warning("Aucune donnée chargée.")
else:
    st.success(f"{len(df)} tirages chargés – de {df['Date'].min().date()} à {df['Date'].max().date()}")

    main_scores, star_scores = compute_scores(df)

    st.header("📊 Scores des numéros principaux")
    st.dataframe(pd.DataFrame.from_dict(main_scores, orient='index').sort_values("score", ascending=False).head(15))

    st.header("📊 Scores des étoiles")
    st.dataframe(pd.DataFrame.from_dict(star_scores, orient='index').sort_values("score", ascending=False).head(10))

    st.header("🎰 Générateurs")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔥 Générer 3 grilles HOT"):
            top_main = sorted(main_scores, key=lambda x: main_scores[x]['score'], reverse=True)[:20]
            top_stars = sorted(star_scores, key=lambda x: star_scores[x]['score'], reverse=True)[:8]
            for i in range(3):
                nums = generate_grid_from_pool(top_main, 5)
                stars = generate_grid_from_pool(top_stars, 2)
                st.write(f"**HOT #{i+1}** → Numéros : {nums} | Étoiles : {stars}")

    with col2:
        if st.button("🕒 Générer 3 grilles RETARD"):
            top_main = sorted(main_scores, key=lambda x: main_scores[x]['retard'], reverse=True)[:20]
            top_stars = sorted(star_scores, key=lambda x: star_scores[x]['retard'], reverse=True)[:8]
            for i in range(3):
                nums = generate_grid_from_pool(top_main, 5)
                stars = generate_grid_from_pool(top_stars, 2)
                st.write(f"**RETARD #{i+1}** → Numéros : {nums} | Étoiles : {stars}")
