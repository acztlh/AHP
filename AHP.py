import streamlit as st
import pandas as pd
import numpy as np

# Başlık
st.title("AHP Karar Destek Sistemi")

# Kriterleri ve Çözüm Önerilerini tanımla
criteria = ["Sustainability", "Social Benefit", "Less Carbon Emission", "Social Sustainability", 
            "Efficiency", "Beeing Local", "Scaleability", "Nationally Aggrable", "Having Legislation in Law"]
solutions = ["Planting Trees", "Kağıt Geri Dönüşümü", "Workshop on Forest Education", 
             "Tree Distribution Events", "Wood as Building Material", "Fire Reporting System", 
             "Investment in Wood Market", "Forest Sprinkler System"]

# Kriter karşılaştırma matrisi için çapraz tablo
st.subheader("Kriter Karşılaştırma Matrisi")
comparison_matrix = pd.DataFrame(np.ones((len(criteria), len(criteria))), 
                                 index=criteria, columns=criteria)

# Kullanıcıdan kriterleri karşılaştırmasını iste
for i, row in enumerate(criteria):
    for j, col in enumerate(criteria):
        if i < j:
            comparison_matrix.loc[row, col] = st.number_input(f"{row} ile {col} karşılaştırması", 
                                                              min_value=0.0, value=1.0)
            comparison_matrix.loc[col, row] = 1 / comparison_matrix.loc[row, col]

# Ağırlıkları hesaplama
st.write("Kriter Karşılaştırma Matrisi:")
st.dataframe(comparison_matrix)

def calculate_ahp_weights(matrix):
    # Normalize matrisi
    normalized_matrix = matrix / matrix.sum(axis=0)
    # Her bir kriterin ağırlığını bul
    weights = normalized_matrix.mean(axis=1)
    return weights

criteria_weights = calculate_ahp_weights(comparison_matrix)
st.write("Kriter Ağırlıkları:", criteria_weights)

# Çözüm önerileri için kriter puanları
st.subheader("Çözüm Önerileri Puanlama")

# Her çözüm önerisi için kriter puanlarını girme
solution_scores = {}
for solution in solutions:
    scores = []
    st.write(f"Çözüm: {solution}")
    for criterion in criteria:
        score = st.number_input(f"{solution} için {criterion} puanı", min_value=0.0, max_value=10.0, value=5.0)
        scores.append(score)
    solution_scores[solution] = scores

# Çözüm önerilerini değerlendirme
st.subheader("Sonuçlar")

# Çözüm önerilerini değerlendir ve toplam puanlarını hesapla
solution_df = pd.DataFrame(solution_scores, index=criteria)
solution_df = solution_df.T
solution_df['Toplam Puan'] = solution_df.dot(criteria_weights)

st.write("Çözüm Önerileri Puanları:")
st.dataframe(solution_df[['Toplam Puan']])

# En iyi çözüm önerisini göster
best_solution = solution_df['Toplam Puan'].idxmax()
st.write(f"En İyi Çözüm Önerisi: {best_solution}")
