import streamlit as st
import pandas as pd

# Uygulama başlığı
st.title("AHP Değerlendirme Uygulaması")

# Katılımcıların sonuçlarını saklamak için session_state içinde bir sözlük oluşturuyoruz
if 'participants' not in st.session_state:
    st.session_state['participants'] = {}

# Katılımcı adı
participant_name = st.text_input("Katılımcı Adı")

# Kriterler ve çözüm önerileri
criteria = [
    "Sustainability", "Social Benefit", "Less Carbon emission",
    "Social Sustainability", "Efficiency", "Being Local",
    "Scalability", "Nationally agreeable", "Having legislation in the law"
]
solutions = [
    "Planting trees", "Kağıt geri dönüşümü", "Workshop about forest to educate people",
    "İnsanlara ağaç dağıtma etkinliği.", "Encourage use of wood as building materials (advertisement)",
    "Create community reporting mechanism system on fire incidents",
    "Investment opportunities on Wood market", "Forest sprinkler system"
]

# Her bir çözüm için AHP değerlendirme matrisleri ekleyin
solution_scores = {}

st.subheader("Çözüm Önerisi Değerlendirme")
for solution in solutions:
    st.write(f"Çözüm Önerisi: {solution}")
    score = 0
    for criterion in criteria:
        st.write(f"Kriter: {criterion}")
        
        # Karşılaştırma değerlendirme çubuğu
        evaluation = st.select_slider(
            f"{criterion} ile karşılaştırma (1-9 arası)",
            options=[1, 2, 3, 4, 5, 6, 7, 8, 9],
            value=5
        )
        score += evaluation  # Her kriter için puanı topla
    
    # Çözüm önerisi için toplam puanı kaydet
    solution_scores[solution] = score

# En yüksek puanlı çözüm önerisini bul
best_solution = max(solution_scores, key=solution_scores.get)
best_score = solution_scores[best_solution]

# Katılımcı sonucu kaydet
if participant_name:
    st.session_state['participants'][participant_name] = (best_solution, best_score)
    st.success(f"{participant_name} için en yüksek puanlı çözüm önerisi kaydedildi.")

# Katılımcıların En Yüksek Puanlı Çözüm Önerilerini Göster
st.subheader("Katılımcı Sonuçları")

# 'participants' sözlüğünü DataFrame'e dönüştürerek her katılımcının sonucunu göster
results = pd.DataFrame(st.session_state['participants'].items(), columns=['Katılımcı', 'Sonuç'])

# 'Sonuç' sütunundaki her kaydın iki elemanlı (çözüm önerisi, puan) olduğundan emin ol
sonuc_listesi = []
for sonuc in results['Sonuç']:
    if isinstance(sonuc, (list, tuple)) and len(sonuc) == 2:
        sonuc_listesi.append(sonuc)
    else:
        sonuc_listesi.append((None, None))  # Eksik ya da hatalı veriler için boş değer ekle

# Sonuçları iki sütuna ayır ve tabloyu güncelle
results[['Çözüm Önerisi', 'Puan']] = pd.DataFrame(sonuc_listesi, index=results.index)
results = results.drop(columns=['Sonuç'])  # Artık 'Sonuç' sütununu kaldırabiliriz

# Tüm katılımcı sonuçlarını tablo olarak göster
st.write(results)

# En yüksek ortalama puana sahip çözüm önerisini bul
average_scores = results.groupby("Çözüm Önerisi")["Puan"].mean()
top_solution = average_scores.idxmax()
top_score = average_scores.max()

st.subheader("En Yüksek Ortalama Puanlı Çözüm Önerisi")
st.write(f"Çözüm Önerisi: {top_solution}")
st.write(f"Ortalama Puan: {top_score:.2f}")
