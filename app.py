import pandas as pd
import streamlit as st
import random
from collections import Counter

st.set_page_config(page_title="EuroMillions Boost", layout="wide")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("euromillions_full_1000.csv")
    except:
        df = pd.DataFrame()
    return df

def generate_optimized_grid(top_main, top_stars):
    return sorted(random.sample(top_main, 5)), sorted(random.sample(top_stars, 2))

df = load_data()

st.title("💸 EuroMillions Boost – Analyse et Générateur")
st.markdown("Application locale avec statistiques tirages et générateur de grilles optimisées.")

if df.empty:
    st.warning("Données non chargées.")
else:
    st.success(f"{len(df)} tirages chargés depuis {df['Date'].min()}")

    # Statistiques
    st.header("📊 Statistiques")
    main_numbers = df[["N1", "N2", "N3", "N4", "N5"]].values.flatten()
    star_numbers = df[["E1", "E2"]].values.flatten()
    main_freq = Counter(main_numbers)
    star_freq = Counter(star_numbers)

    st.subheader("Top 10 des numéros principaux")
    top_main_display = pd.DataFrame(main_freq.most_common(10), columns=["Numéro", "Fréquence"])
    st.dataframe(top_main_display)

    st.subheader("Top 5 des étoiles")
    top_star_display = pd.DataFrame(star_freq.most_common(5), columns=["Étoile", "Fréquence"])
    st.dataframe(top_star_display)

    # Générateur
    st.header("🎰 Générateur de Grilles Optimisées")
    top_main = [num for num, _ in main_freq.most_common(13)]
    top_stars = [num for num, _ in star_freq.most_common(6)]

    if st.button("Générer 8 grilles"):
        grids = [generate_optimized_grid(top_main, top_stars) for _ in range(8)]
        for i, grid in enumerate(grids):
          st.write(f"Grille #{i+1} : Numéros → {[int(n) for n in grid[0]]} | Étoiles → {[int(e) for e in grid[1]]}")

