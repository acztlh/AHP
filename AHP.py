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
criteria_short = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]  # Kriterlerin kısaltmaları
solutions = [
    "Planting Trees", "Kağıt Geri Dönüşümü", "Workshop on Forest Education", 
    "Tree Distribution Events", "Wood as Building Material", 
    "Fire Reporting System", "Investment in Wood Market", "Forest Sprinkler System"
]

# Katılımcı verilerini saklamak için sözlük
if 'participants' not in st.session_state:
    st.session_state['participants'] = {}

# Açıklama
st.write("Aşağıda kriterlerin karşılaştırmalarını yaparak göreceli değerlerini belirleyebilirsiniz. "
         "Daha sonra çözüm önerilerini 10 üzerinden değerlendirerek puanlayacaksınız.")

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

# Boş DataFrame oluştur ve çözüm önerileri ile kriterleri ekle
solution_scores = pd.DataFrame(index=solutions, columns=criteria_short)
solution_scores = solution_scores.fillna(5).astype(float)  # Varsayılan değeri 5 olarak belirle ve float türüne çevir

# Çözüm önerileri puan tablosu başlığı
st.subheader("Çözüm Önerileri Puanlama Tablosu")

# Çözüm önerileri için puanlama tablosu
solution_scores = pd.DataFrame(index=solutions, columns=criteria)
solution_scores = solution_scores.fillna(5.0).astype(float)  # Varsayılan değeri 5.0 olarak belirle ve float türüne çevir

# Çözüm Önerilerini Değerlendir ve Toplam Puan Hesapla
solution_scores['Toplam Puan'] = solution_scores[criteria].dot(criteria_weights)


# Tabloyu kullanıcı girişi için oluştur
for i, solution in enumerate(solutions):
    for j, criterion in enumerate(criteria_short):
        score = st.number_input(f"{solution} için {criterion} puanı", 
                                min_value=0.0, max_value=10.0, value=solution_scores.iloc[i, j],
                                key=f"{solution}_{criterion}")
        solution_scores.loc[solution, criterion] = score

# Toplam puanları kriter ağırlıklarıyla çarp ve her çözüm için toplam puanı hesapla
solution_scores = solution_scores.astype(float)  # Puanları float'a dönüştür
solution_scores["Toplam Puan"] = solution_scores.dot(criteria_weights)

# Katılımcının En Yüksek Puanlı Çözüm Önerisini Kaydet
if user_name:
    max_solution = solution_scores['Toplam Puan'].idxmax()
    max_score = solution_scores['Toplam Puan'].max()
    st.session_state['participants'][user_name] = (solution_scores, max_solution, max_score)

# Katılımcıların Çözüm Önerilerine Verdiği Ortalama Puanlar
st.subheader("Katılımcıların Çözüm Önerilerine Verdiği Ortalama Puanlar")
all_scores = pd.DataFrame([data[0]['Toplam Puan'] for data in st.session_state['participants'].values()])
average_scores = all_scores.mean().sort_values(ascending=False)
st.write(average_scores)

# Katılımcıların En Yüksek Puan Verdiği Çözüm Önerileri
st.subheader("Katılımcıların En Yüksek Puan Verdiği Çözüm Önerileri")
results = pd.DataFrame([(name, data[1], data[2]) for name, data in st.session_state['participants'].items()],
                       columns=['Katılımcı', 'En İyi Çözüm Önerisi', 'Puan'])
st.write(results)

