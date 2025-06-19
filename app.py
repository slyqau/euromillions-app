import pandas as pd
import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions Boost+", layout="wide")

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

    main_scores = {n: freq_main[n]*0.4 + freq_recent_main[n]*0.3 + get_retard(n)*0.3 for n in range(1, 51)}
    star_scores = {s: freq_star[s]*0.4 + freq_recent_star[s]*0.3 + get_retard_star(s)*0.3 for s in range(1, 13)}

    return main_scores, star_scores

def generate_weighted_grid(scores_main, scores_star):
    main_pool = list(scores_main.keys())
    star_pool = list(scores_star.keys())
    main_weights = [scores_main[n] for n in main_pool]
    star_weights = [scores_star[s] for s in star_pool]

    main_selected = sorted(random.choices(main_pool, weights=main_weights, k=5))
    star_selected = sorted(random.choices(star_pool, weights=star_weights, k=2))
    return main_selected, star_selected

df = load_data()

st.title("💸 EuroMillions Boost+ – Générateur Pondéré")

if df.empty:
    st.warning("Aucune donnée chargée.")
else:
    st.success(f"{len(df)} tirages chargés – de {df['Date'].min().date()} à {df['Date'].max().date()}")
    scores_main, scores_star = compute_scores(df)

    if st.button("🎰 Générer 8 grilles pondérées"):
        for i in range(8):
            grid = generate_weighted_grid(scores_main, scores_star)
            st.write(f"**Grille #{i+1}** : Numéros → {[int(x) for x in grid[0]]} | Étoiles → {[int(x) for x in grid[1]]}")
