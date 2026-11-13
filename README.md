# B2B Book Distribution Intelligence

**İstanbul Teknik Üniversitesi · ISL 533 Veri Madenciliği · Ödev I**  
**Proje:** Python Streamlit ile Akıllı Gösterge Paneli Tasarımı

[**Canlı Gösterge Paneli**](https://isl533-b2b-intelligence.streamlit.app) · [**GitHub Kaynak Kodu**](https://github.com/jacobhunter17/ISL533-B2B-Intelligence)

## Proje Hakkında

Bu çalışma, B2B kitap dağıtım işlemlerinden elde edilen verileri satış, pazarlama ve ürün portföyü kararlarında kullanılabilecek etkileşimli göstergelere dönüştürür. Python ve Streamlit ile geliştirilen uygulama; tarih, şehir ve kategori filtreleriyle farklı iş kesitlerini incelemeyi, müşteri ve ürünleri sınıflandırmayı ve kısa dönemli satış/adet öngörüleri üretmeyi sağlar.

## Uygulama Bölümleri

| Bölüm | İçerik |
|---|---|
| **Genel Bakış** | Net satış, fatura, satılan adet ve müşteri KPI'ları; aylık satış eğilimi, en yüksek satışlı kategoriler, şehir dağılımı ve aylık fatura/adet grafikleri |
| **Müşteri & RFM** | Recency–Frequency–Monetary analizi, müşteri segmentleri, segmentlerin satış payı, müşteri detayları ve CSV çıktısı |
| **Ürün & ABC** | Ürünlerin satış değerine göre ABC sınıflandırılması, ürün/satış dağılımı, ayrıntılı ürün listesi ve CSV çıktısı |
| **Talep Tahmini** | Aylık satış tutarı veya adet için 1–6 aylık öngörü; seçilen model, geçmişe dönük MAE ve tahmin CSV çıktısı |

## Veri Seti ve Hazırlık

- **Kaynak:** `B2B_Transaction_Data_.xlsx` — 2020 yılına ait **664.154** işlem satırı.
- **Uygulamanın okuduğu veri:** Depo kök dizinindeki `b2b_transactions.csv.gz`. Kaynak Excel'in sıkıştırılmış CSV biçimi, bulutta daha hızlı yükleme için kullanılır.
- Tarihler tarih tipine, miktar ve fiyat alanları sayısal tipe dönüştürülür.
- Eksik müşteri/ürün/tarih, geçersiz miktar ve fiyat taşıyan kayıtlar analizden çıkarılır. Geçerli kayıt sayısı **664.143**'tür.
- Eksik şehir/kategori alanları `Bilinmiyor` etiketiyle korunur.
- Birbirinin aynı görünen satırlar otomatik silinmez: Veride her fatura kalemini benzersiz belirleyen bir satır kimliği bulunmamaktadır.
- Filtreler değiştirildiğinde KPI, RFM ve ABC analizleri seçilen veri üzerinden yeniden hesaplanır.

**Ölçüm varsayımı:** Net satış `Quantity × NetPrice` olarak hesaplanır; `NetPrice` birim net fiyat varsayılmıştır. Panelin TL gösterimi veri kaynağında doğrulanmış bir para birimi bilgisine dayanmamaktadır.

## Kullanılan Analitik Yöntemler

### RFM müşteri segmentasyonu

- **Recency (R):** Müşterinin son işleminin referans tarihe uzaklığı.
- **Frequency (F):** Farklı fatura sayısı.
- **Monetary (M):** Toplam hesaplanan net satış.

R, F ve M değişkenleri 1–5 arasında sıralama-temelli dilimlerle puanlanır. Kurallara göre müşteriler *Şampiyonlar*, *Sadık müşteriler*, *Risk altındakiler*, *Uyuyan müşteriler* ve *Gelişim potansiyeli* gruplarına ayrılır.

### ABC ürün analizi

Ürünler hesaplanan net satış değerine göre büyükten küçüğe sıralanır. Kümülatif satış payı yaklaşık **%80 / %15 / %5** eşiklerine göre A, B ve C sınıfları oluşturulur.

### Aylık tahmin ve değerlendirme

Aylık seride iki yöntem karşılaştırılır:

1. **Son dönem (naive):** Son gözlenen ayın değerini ileri taşır.
2. **Doğrusal trend:** Geçmiş aylara doğrusal eğilim uydurur.

Son en fazla dört dönem için ileriye dönük, zaman sıralı testler yapılarak **ortalama mutlak hata (MAE)** hesaplanır. Daha düşük MAE'ye sahip yöntem, seçilen 1–6 aylık ufuk için kullanılır. Negatif öngörüler sıfıra sınırlandırılır.

**Sınırlar:** Veri yalnızca 2020'yi kapsar. Tahminler keşifsel ve kısa dönemlidir; güncel koşulları doğrudan temsil etmez. Stok miktarı, teslim/tedarik süresi ve maliyet verisi bulunmadığından stok optimizasyonu veya gerçek kârlılık ölçümü yapılmaz.

## Kullanılan Teknolojiler

- **Python** — veri işleme ve analitik hesaplama
- **Streamlit** — etkileşimli web uygulaması
- **Pandas / NumPy** — veri hazırlama, gruplama ve hesaplamalar
- **Plotly** — etkileşimli görselleştirme

Gerekli sürümler `requirements.txt` dosyasında listelenmiştir.

## Proje Dosya Yapısı

```text
ISL533-B2B-Intelligence/
├── README.md
├── requirements.txt
├── streamlit_app.py
└── b2b_transactions.csv.gz
```

## Yerel Kurulum ve Çalıştırma

Python 3.10 veya üzeri önerilir.

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Uygulama varsayılan olarak `http://localhost:8501` adresinde açılır. Veri dosyası `streamlit_app.py` ile **aynı klasörde** bulunmalıdır.

## Dağıtım

Uygulama **Streamlit Community Cloud** üzerinde, bu GitHub deposundaki `main` dalı ve `streamlit_app.py` giriş noktası kullanılarak yayımlanmıştır.

- [Canlı uygulama](https://isl533-b2b-intelligence.streamlit.app)
- [Kaynak kod deposu](https://github.com/jacobhunter17/ISL533-B2B-Intelligence)

## Notlar

Bu proje akademik amaçla hazırlanmıştır. Depoda yayımlanan müşteri/işlem verilerinin paylaşım izni, veri sahibi tarafından ayrıca doğrulanmalıdır. Gösterge panelindeki metrikler belirtilen veri ve hesaplama varsayımlarına bağlıdır.
