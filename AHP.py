import streamlit as st
import pandas as pd
import numpy as np

# Başlık
st.title("AHP Karar Destek Sistemi")

# Kriterleri tanımla
criteria = ["Sustainability (A)", "Social Benefit (B)", "Less Carbon Emission (C)", "Efficiency (D)"]

# Karşılaştırma Tablosu Açıklaması
st.write("Aşağıdaki çapraz tabloda, her iki kriterin göreli değerini belirleyebilirsiniz. "
         "Örneğin, '4A' girişi, ilk kriterin (A) diğerine göre dört kat daha değerli olduğunu gösterir.")

# Karşılaştırma Matrisi Oluştur
comparison_matrix = pd.DataFrame(np.ones((len(criteria), len(criteria))), 
                                 index=criteria, columns=criteria)

# Kriter Karşılaştırma Tablosu Girdisi
st.subheader("Kriter Karşılaştırma Tablosu")
for i, row_criterion in enumerate(criteria):
    for j, col_criterion in enumerate(criteria):
        if i < j:
            st.write(f"{row_criterion} ile {col_criterion} karşılaştırması:")
            value = st.radio(f"{row_criterion} mi {col_criterion} mi daha değerli?",
                             ["Eşit (A=B)", f"{row_criterion}", f"2{row_criterion}", f"3{row_criterion}", f"4{row_criterion}",
                              f"{col_criterion}", f"2{col_criterion}", f"3{col_criterion}", f"4{col_criterion}"],
                             horizontal=True, index=0)
            
            # Kullanıcının seçimini matris değerine dönüştürme
            if value == "Eşit (A=B)":
                comparison_matrix.loc[row_criterion, col_criterion] = 1
                comparison_matrix.loc[col_criterion, row_criterion] = 1
            elif value.endswith("A") or value.endswith("B") or value.endswith("C") or value.endswith("D"):
                comparison_matrix.loc[row_criterion, col_criterion] = int(value[0])
                comparison_matrix.loc[col_criterion, row_criterion] = 1 / int(value[0])
            else:
                comparison_matrix.loc[row_criterion, col_criterion] = 1
                comparison_matrix.loc[col_criterion, row_criterion] = 1

# Ağırlıkları hesaplama fonksiyonu
def calculate_ahp_weights(matrix):
    # Normalize matrisi
    normalized_matrix = matrix / matrix.sum(axis=0)
    # Her bir kriterin ağırlığını bul
    weights = normalized_matrix.mean(axis=1)
    return weights

# Ağırlık Hesaplama ve Gösterme
criteria_weights = calculate_ahp_weights(comparison_matrix)
st.subheader("Kriter Ağırlıkları")
st.write(criteria_weights)

# Örnek çözümler ve çözüm puanlamaları
solutions = ["Planting Trees", "Kağıt Geri Dönüşümü", "Workshop on Forest Education", 
             "Tree Distribution Events", "Wood as Building Material", "Fire Reporting System", 
             "Investment in Wood Market", "Forest Sprinkler System"]

# Çözüm Önerileri için Puanlama Girdisi
st.subheader("Çözüm Önerileri Puanlama")
solution_scores = {}
for solution in solutions:
    scores = []
    st.write(f"Çözüm: {solution}")
    for criterion in criteria:
        score = st.number_input(f"{solution} için {criterion} puanı", min_value=0.0, max_value=10.0, value=5.0)
        scores.append(score)
    solution_scores[solution] = scores

# Çözüm önerilerini değerlendir ve toplam puanlarını hesapla
st.subheader("Sonuçlar")
solution_df = pd.DataFrame(solution_scores, index=criteria)
solution_df = solution_df.T
solution_df['Toplam Puan'] = solution_df.dot(criteria_weights)

st.write("Çözüm Önerileri Puanları:")
st.dataframe(solution_df[['Toplam Puan']])

# En iyi çözüm önerisini göster
best_solution = solution_df['Toplam Puan'].idxmax()
st.write(f"En İyi Çözüm Önerisi: {best_solution}")
