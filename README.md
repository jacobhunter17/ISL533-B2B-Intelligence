# B2B Book Distribution Intelligence

**İTÜ · ISL 533 Veri Madenciliği · Ödev I**

Streamlit tabanlı, B2B kitap dağıtım şirketi için satış, pazarlama ve tedarik planlama karar destek paneli.

## Özellikler

1. **Yönetici görünümü:** net satış, fatura sayısı, satılan adet, aktif müşteri, ortalama fatura tutarı; aylık kategori ve şehir bazlı grafikler.
2. **Pazarlama / RFM:** müşteri bazlı recency, frequency, monetary skorları; segmentler, müşteri öncelik listesi, CSV aktarımı.
3. **Ürün portföyü / ABC:** satış katkısı bakımından ürün bazlı A/B/C sınıfları, adet ve fatura göstergeleri, CSV aktarımı.
4. **Öngörü:** aylık satış veya adet serisi için naive ve doğrusal trend modelleri; zaman sıralı rolling-origin MAE doğrulaması; 1–6 aylık tahmin.
5. **Veri denetimi:** eksikler, geçersiz satırlar, birebir tekrarların raporlanması; veri seti ve hesaplama varsayımları.

## Veri

- Excel kaynağı: `B2B_Transaction_Data_.xlsx` (664.154 işlem satırı). Kaynağın sıkıştırılmış CSV sürümü `data/b2b_transactions.csv.gz` ile birlikte gelir.
- Uygulama CSV.gz dosyasını doğrudan kullanır; sıkıştırılmış CSV, büyük Excel dosyasının bulutta yüklenmesini hızlandırır.
- **Satış tanımı:** `Revenue = Quantity × NetPrice`. NetPrice satır başına *birim net satış fiyatı* kabul edilmiştir. Kaynakta para birimi açıkça belirtilmediği için TL gösterimi doğrulanması gereken bir varsayımdır.
- Yinelenen satırlar **otomatik silinmez**, çünkü fatura satırlarına ait güvenilir benzersiz satır kimliği yoktur.
- Filtreler uygulanınca RFM sınıfları ve ABC eşikleri o alt kümeye göre değişir.
- Stok, sevkiyat, teslim süresi, maliyet ve iadeye dair güvenilir işaretleyici bulunmadığı için stok optimizasyonu veya gerçek kâr ölçülmez.
- Veri yalnızca **2020** yılını kapsar; tahminler keşifseldir ve 2026 güncel taleplerine doğrudan genellenmemelidir.

## Yerel çalıştırma

Python 3.10+ ile:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Streamlit Community Cloud ile yayımlama

1. GitHub'da örneğin `isl533-b2b-intelligence` isimli **public** repo oluşturun.
2. Bu dizinin **içeriğini** repo kök dizinine yükleyin (`streamlit_app.py`, `requirements.txt`, `data/` ve `README.md`).
3. [share.streamlit.io](https://share.streamlit.io) sitesine GitHub ile girin.
4. **Create app** → ilgili repo ve branch → entrypoint `streamlit_app.py` → Deploy.
5. İlk yükleme sonrasında KPI, RFM, ABC ve tahmin sekmelerinin düzgün açıldığını ayrı tarayıcı penceresinde test edin.
6. Ödev tesliminde **canlı uygulama URL'si** ve **GitHub repo URL'sini** Ninova'ya yükleyin.

> Cloud üzerinde herkese açık yayımlanan veriler de indirilebilir hâle gelebilir. Veri paylaşım iznini ders bağlamında kontrol edin. Bu proje içinde gerçek müşteri kodları ve işlem verileri bulunmaktadır.

## Kod yapısı

```text
ISL533_B2B_Intelligence/
├── streamlit_app.py
├── requirements.txt
├── README.md
└── data/
    └── b2b_transactions.csv.gz
```

## Model doğrulama

Model doğrulaması için son en çok dört gözlenen ay ileri kaydırmalı test seti olarak kullanılır. Her dönemde yalnızca öncesindeki aylarla eğitim yapılır; naive ve doğrusal trend yöntemlerinin bir sonraki ay için mutlak hatası ölçülür. MAE küçük olan yöntem tüm tarihçe üzerinde yeniden kurulur ve seçilen ufuk için tahmin üretir. Bu bir nedensel tahmin veya güven aralığı değildir.

## Ödev değerlendirme eşleştirmesi

| Kriter | Uygulama |
|---|---|
| Veri ön işleme %15 | Tür kontrolü, veri denetimi, bozuk değerlerin ele alınması |
| Analitik özellikler %25 | RFM, ABC, zaman serisi modeli / doğrulama |
| Raporlama yapısı %15 | İş fonksiyonlarına göre 5 sekme |
| Görsel tasarım %15 | Koyu tema, KPI kartları, duyarlı Plotly grafikler |
| Etkileşim %15 | Tarih, şehir, kategori, segment, model ufku, CSV |
| Kod kalitesi %15 | Fonksiyonlar, cache, dökümantasyon, bağımlılık dosyası |
