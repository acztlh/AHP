import streamlit as st
import pandas as pd
import numpy as np

# Başlık
st.title("AHP Karar Destek Sistemi - Katılımcı Bazlı")

# Kullanıcı adı girişi
user_name = st.text_input("Katılımcı Adınızı Girin:")

# Kriterleri ve Çözüm Önerilerini Tanımla
criteria = [
    "Sustainability", "Social Benefit", "Less Carbon Emission", 
    "Social Sustainability", "Efficiency", "Being Local", 
    "Scalability", "Nationally Agreeable", "Having Legislation in the Law"
]
solutions = [
    "Planting Trees", "Kağıt Geri Dönüşümü", "Workshop on Forest Education", 
    "Tree Distribution Events", "Wood as Building Material", 
    "Fire Reporting System", "Investment in Wood Market", "Forest Sprinkler System"
]

# Katılımcı verilerini saklamak için sözlük
if 'participants' not in st.session_state:
    st.session_state['participants'] = {}

# Açıklama
st.write("Aşağıdaki çapraz tabloda, iki kriteri karşılaştırarak göreceli değerlerini belirleyebilirsiniz. "
         "Çubuğun tam ortasında A=B bulunur, bu iki kriterin eşit değerliliğini ifade eder. "
         "Sağa veya sola kaydırarak değerleri artırabilirsiniz.")

# Karşılaştırma Matrisi
comparison_matrix = pd.DataFrame(np.ones((len(criteria), len(criteria))), index=criteria, columns=criteria)

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
                st.write(row_criterion)
            with col3:
                st.write(col_criterion)
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

# Kriter Ağırlıkları Hesapla
criteria_weights = calculate_ahp_weights(comparison_matrix)

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
solution_df = pd.DataFrame(solution_scores, index=criteria)
solution_df = solution_df.T
solution_df['Toplam Puan'] = solution_df.dot(criteria_weights)

# Katılımcı Sonuçlarını Kaydet ve Görüntüle
if user_name:
    st.session_state['participants'][user_name] = solution_df['Toplam Puan']

# Katılımcı Sonuçları Tablosu
st.subheader("Katılımcı Sonuçları")
for participant, results in st.session_state['participants'].items():
    st.write(f"{participant} Sonuçları:")
    st.write(results)

# Ortalama Sonuçları Hesapla ve Göster
if len(st.session_state['participants']) > 0:
    all_scores = pd.DataFrame(st.session_state['participants']).T
    all_scores['Ortalama Sonuç'] = all_scores.mean(axis=1)
    st.subheader("Tüm Katılımcıların Ortalama Sonuçları")
    st.write(all_scores[['Ortalama Sonuç']])
