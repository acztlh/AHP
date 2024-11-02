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
criteria_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
solutions = [
    "Planting Trees", "Kağıt Geri Dönüşümü", "Workshop on Forest Education", 
    "Tree Distribution Events", "Wood as Building Material", 
    "Fire Reporting System", "Investment in Wood Market", "Forest Sprinkler System"
]

# Katılımcı verilerini saklamak için session_state içinde bir sözlük
if 'participants' not in st.session_state:
    st.session_state['participants'] = {}

# Uyarı mesajı
st.write("Değerlendirme 10 puan üzerinden yapılmaktadır.")

# Çözüm Önerileri için Puanlama Tablosu
st.subheader("Çözüm Önerileri Puanlama")
solution_scores = {solution: [5.0] * len(criteria) for solution in solutions}  # Varsayılan değerler 5.0

# Puanlama tablosu
scoring_df = pd.DataFrame(solution_scores, index=criteria_labels)

for criterion_label, criterion_name in zip(criteria_labels, criteria):
    for solution in solutions:
        scoring_df.loc[criterion_label, solution] = st.number_input(
            f"{solution} için {criterion_name} ({criterion_label}) puanı", 
            min_value=0.0, max_value=10.0, value=5.0
        )

# Ağırlık Hesaplama Fonksiyonu
def calculate_ahp_weights(matrix):
    normalized_matrix = matrix / matrix.sum(axis=0)
    weights = normalized_matrix.mean(axis=1)
    return weights

# Karşılaştırma Matrisi ile kriter ağırlıklarını hesaplayın
comparison_matrix = pd.DataFrame(np.ones((len(criteria), len(criteria))), index=criteria, columns=criteria)
criteria_weights = calculate_ahp_weights(comparison_matrix)

# Çözüm Önerileri Puanlamasını ve Toplam Puanları Hesapla
solution_df = scoring_df.T
solution_df['Toplam Puan'] = solution_df.dot(criteria_weights)

# Katılımcının En Yüksek Puanlı Çözüm Önerisini Bul
if user_name:
    max_solution = solution_df['Toplam Puan'].idxmax()
    max_score = solution_df['Toplam Puan'].max()
    st.session_state['participants'][user_name] = (max_solution, max_score, solution_df)

# Katılımcıların Tüm Çözüm Önerilerini Göster
st.subheader("Katılımcıların Tüm Çözüm Önerileri Puanları")
for participant, data in st.session_state['participants'].items():
    solution_table = data[2]
    st.write(f"{participant} için Çözüm Önerileri Puanları:")
    st.write(solution_table)

# Katılımcıların En Yüksek Puanlı Çözüm Önerilerini Göster
st.subheader("Katılımcıların En Yüksek Puanlı Çözüm Önerileri")
results = pd.DataFrame(
    [(participant, data[0], data[1]) for participant, data in st.session_state['participants'].items()],
    columns=['Katılımcı', 'En Yüksek Çözüm Önerisi', 'Puan']
)
st.write(results)

# Tüm Katılımcıların Ortalama En Yüksek Puanını Hesapla ve Göster
if not results.empty:
    average_score = results['Puan'].mean()
    st.subheader("Tüm Katılımcıların Ortalama En Yüksek Puanı")
    st.write(f"Ortalama Puan: {average_score:.2f}")
