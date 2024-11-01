import streamlit as st
import numpy as np
import pandas as pd

# Başlık
st.title("Value Engineering Workshop Değerlendirme Formu")

# Kriter isimleri
criteria_names = ["Sustainability", "Social Benefit", "Less Carbon Emission", "Efficiency"]

# 1. Kriter Karşılaştırma Matrisi (AHP Ağırlıkları için)
st.header("Kriter Önemi Karşılaştırması")
criteria_comparison = np.ones((len(criteria_names), len(criteria_names)))

# Kriterlerin birbirine göre önemini almak için bir döngüyle giriş oluşturuyoruz
for i in range(len(criteria_names)):
    for j in range(i + 1, len(criteria_names)):
        criteria_comparison[i, j] = st.slider(f"{criteria_names[i]} / {criteria_names[j]} karşılaştırması:", 1, 9, 1)
        criteria_comparison[j, i] = 1 / criteria_comparison[i, j]

# Kriter önem ağırlıkları hesaplama
column_sums = criteria_comparison.sum(axis=0)
normalized_matrix = criteria_comparison / column_sums
criteria_weights = normalized_matrix.mean(axis=1)
criteria_weights_df = pd.DataFrame(criteria_weights, index=criteria_names, columns=["Weight"])
st.write("Kriter Ağırlıkları:\n", criteria_weights_df)

# 2. Çözüm Önerileri ve Puanlamaları
st.header("Çözüm Önerisi Değerlendirmesi")
solution_names = [
    "Planting Trees", "Paper Recycling", "Forest Education Workshop", 
    "Tree Distribution Event", "Promote Wood Use"
]

# Çözüm önerilerinin her kriter için puanlamalarını almak için bir DataFrame oluşturuyoruz
solution_ratings = pd.DataFrame(index=criteria_names, columns=solution_names)

# Çözüm önerileri puanlamalarını kullanıcıdan alıyoruz
for solution in solution_names:
    st.subheader(f"{solution} Puanlama")
    for criterion in criteria_names:
        solution_ratings.loc[criterion, solution] = st.slider(
            f"{solution} için {criterion} puanı:", 1, 5, 3
        )

# Çözüm önerileri tablosunu göster
st.write("Çözüm Önerileri Kriter Puanlaması:\n", solution_ratings)

# 3. Ağırlıklı Puanların Hesaplanması
# Her çözüm önerisinin puanını kriter ağırlıklarıyla çarpıp toplam puanı hesaplıyoruz
solution_ratings = solution_ratings.astype(float)  # Verileri sayısal formata dönüştürüyoruz
weighted_scores = solution_ratings.T.dot(criteria_weights)
weighted_scores = pd.DataFrame(weighted_scores, columns=["Total Score"])

# Çözüm önerilerini en yüksek puandan düşük puana sıralıyoruz
ranked_solutions = weighted_scores.sort_values(by="Total Score", ascending=False)
st.write("Sıralı Çözüm Önerileri ve Toplam Puanları:\n", ranked_solutions)
