import streamlit as st
import pandas as pd
import numpy as np

# Başlık
st.title("AHP Karar Destek Sistemi")

# Kriterleri tanımla
criteria = ["Sustainability (A)", "Social Benefit (B)", "Less Carbon Emission (C)", "Efficiency (D)"]

# Açıklama
st.write("Aşağıdaki çapraz tabloda, iki kriteri karşılaştırarak göreceli değerlerini belirleyebilirsiniz. "
         "Çubuğun tam ortasında A=B bulunur, bu iki kriterin eşit değerliliğini ifade eder. "
         "Sağa veya sola kaydırarak değerleri artırabilirsiniz.")

# Karşılaştırma Matrisi
comparison_matrix = pd.DataFrame(np.ones((len(criteria), len(criteria))), 
                                 index=criteria, columns=criteria)

# AHP Çubuk Karşılaştırma
st.subheader("Kriter Karşılaştırma Tablosu")
for i, row_criterion in enumerate(criteria):
    for j, col_criterion in enumerate(criteria):
        if i < j:
            st.write(f"{row_criterion} ile {col_criterion} karşılaştırması:")

            # Karşılaştırma çubuğu
            value = st.slider(
                f"{row_criterion} ↔ {col_criterion}",
                min_value=-4, max_value=4, value=0,
                format="%d",
                help="Sağa kaydırarak soldaki kriteri daha değerli yapabilirsiniz. Sola kaydırarak sağdaki kriteri daha değerli yapabilirsiniz.",
                label_visibility="collapsed"
            )

            # Sol ve sağ tarafında kriter isimlerini göster
            col1, col2, col3 = st.columns([1, 6, 1])
            with col1:
                st.write(row_criterion)  # Sol tarafta ilk kriter
            with col3:
                st.write(col_criterion)  # Sağ tarafta ikinci kriter

            # Değerleri matrise dönüştür
            if value == 0:
                comparison_matrix.loc[row_criterion, col_criterion] = 1
                comparison_matrix.loc[col_criterion, row_criterion] = 1
            elif value > 0:
                comparison_matrix.loc[row_criterion, col_criterion] = value
                comparison_matrix.loc[col_criterion, row_criterion] = 1 / value
            else:
                comparison_matrix.loc[row_criterion, col_criterion] = 1 / abs(value)
                comparison_matrix.loc[col_criterion, row_criterion] = abs(value)

# Ağırlık Hesaplama Fonksiyonu
def calculate_ahp_weights(matrix):
    normalized_matrix = matrix / matrix.sum(axis=0)
    weights = normalized_matrix.mean(axis=1)
    return weights

# Ağırlıkları Hesapla ve Göster
criteria_weights = calculate_ahp_weights(comparison_matrix)
st.subheader("Kriter Ağırlıkları")
st.write(criteria_weights)

# Çözüm Önerileri
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

# Çözüm Önerilerini Değerlendir ve Toplam Puan Hesapla
st.subheader("Sonuçlar")
solution_df = pd.DataFrame(solution_scores, index=criteria)
solution_df = solution_df.T
solution_df['Toplam Puan'] = solution_df.dot(criteria_weights)

st.write("Çözüm Önerileri Puanları:")
st.dataframe(solution_df[['Toplam Puan']])

# En iyi çözüm önerisini göster
best_solution = solution_df['Toplam Puan'].idxmax()
st.write(f"En İyi Çözüm Önerisi: {best_solution}")
