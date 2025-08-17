---
layout: default
title: Yazılım Tasarım Dokümanı
nav_order: 4
---

# Yazılım Tasarım Dokümanı: Clonify Labs

**Proje Adı**: Medikal Sektörde 3 Boyutlu Tarama ile Kişiye Özel Hızlı Kalıp Üretimi
**Ürün Adı**: Clonify Labs Modelleme Yazılımı
**Versiyon**: 0.2
**Tarih**: 15.08.2025

## İçindekiler

1. [Yönetici Özeti](#1-yönetici-özeti)
2. [Giriş](#2-giriş)
    *   [2.1. Dokümanın Amacı](#21-dokümanın-amacı)
    *   [2.2. Projenin Kapsamı](#22-projenin-kapsamı)
    *   [2.3. Tanımlar ve Kısaltmalar](#23-tanımlar-ve-kısaltmalar)
3. [Hedefler ve Amaçlar](#3-hedefler-ve-amaçlar)
4. [Paydaşlar](#4-paydaşlar)
5. [Üst Düzey Mimari](#5-üst-düzey-mimari)
    *   [5.1. Katmanlı Mimari Yaklaşımı](#51-katmanlı-mimari-yaklaşımı)
    *   [5.2. Katmanların Detaylı Analizi](#52-katmanların-detaylı-analizi)
6. [Modül Envanteri](#6-modül-envanteri-seçilmiş)
7. [Kullanılan Teknolojiler ve Kütüphaneler](#7-kullanılan-teknolojiler-ve-kütüphaneler)
8. [Çekirdek Fonksiyonların Mantıksal Akışı](#8-çekirdek-fonksiyonların-mantıksal-akışı)
    *   [8.1. Fonksiyon: Mesh Yükleme](#81-fonksiyon-mesh-yükleme)
    *   [8.2. Fonksiyon: Basınç Boyama](#82-fonksiyon-basınç-boyama)
    *   [8.3. Fonksiyon: Isı Haritası Oluşturma (Asenkron)](#83-fonksiyon-ısı-haritası-oluşturma-asenkron)
    *   [8.4. Fonksiyon: Kalıp Oluşturma](#84-fonksiyon-kalıp-oluşturma)
    *   [8.5. Fonksiyon: Tarama Temizleme](#85-fonksiyon-tarama-temizleme)
    *   [8.6. Fonksiyon: Anatomik Hizalama](#86-fonksiyon-anatomik-hizalama)
    *   [8.7. Fonksiyon: Hacimsel Deformasyon](#87-fonksiyon-hacimsel-deformasyon)
9. [Kullanıcı Etkileşim Tasarımı](#9-kullanıcı-etkileşim-tasarımı)
    *   [9.1. Modüler Etkileşim Stilleri](#91-modüler-etkileşim-stilleri)
    *   [9.2. İletişim Desenleri](#92-iletişim-desenleri)
10. [Çekirdek Alan Modelleri](#10-çekirdek-alan-modelleri)
11. [Hizmet Katmanı: VTKProcessor](#11-hizmet-katmanı-vtkprocessor)
12. [Arka Uç Araçları (Backend Tooling)](#12-arka-uç-araçları-backend-tooling)
13. [Asenkron İşleme](#13-asenkron-işleme)
14. [Render (Görselleştirme) Hattı](#14-render-görselleştirme-hattı)
15. [Mesh İşlemleri (Temsili)](#15-mesh-işlemleri-temsili)
16. [Performans Stratejileri](#16-performans-stratejileri)
17. [Loglama ve Hata Yönetimi](#17-loglama-ve-hata-yönetimi)
18. [Konfigürasyon ve Ortam](#18-konfigürasyon-ve-ortam)
19. [Derleme ve Bağımlılık Yönetimi](#19-derleme-ve-bağımlılık-yönetimi)
20. [Kodlama Standartları](#20-kodlama-standartları)
21. [Test Stratejisi](#21-test-stratejisi)
22. [Kalite Kontrolleri](#22-kalite-kontrolleri)
23. [Güvenlik ve Gizlilik](#23-güvenlik-ve-gizlilik)
24. [Riskler ve Azaltma Yöntemleri](#24-riskler-ve-azaltma-yöntemleri)
25. [Gelecek Geliştirmeler ve Genişletme Noktaları](#25-gelecek-geliştirmeler-ve-genişletme-noktaları)
26. [Sözlük](#26-sözlük)
---



# 1. Giriş

**ClonifyCad**, medikal sektörde, özellikle ortopedi ve protez alanında, 3 boyutlu tarama verileri kullanarak kişiye özel protez ve uzuv kalıpları hazırlama, basınca dayalı modifikasyonlar yapma ve kalıp üretimi için tasarlanmış bir masaüstü CAD (Bilgisayar Destekli Tasarım) yazılımıdır. Kullanıcı arayüzü için PyQt5 ve 3D mesh işlemleri için VTK'yı birleştirerek, etkileşimli şekillendirme, yüksek performans ve genişletilebilirlik üzerine odaklanmıştır. Yazılım, 3D tarayıcıdan gelen STL, OBJ, PLY gibi veri dosyalarını manipüle edip kişiye özel kalıplar hazırlayarak bu kalıpların STL formatında 3B baskı alınmasını sağlar. Protez kalıp rektifikasyonu (düzeltme/şekillendirme) süreci, adım adım ilerleyen rehberli bir iş akışı (workflow) ile kullanıcıya sunulur.

## 1.1. Dokümanın Amacı

Bu dokümanın temel amacı, **ClonifyCad** yazılımının teknik mimarisini, tasarım kararlarını, temel bileşenlerini ve bu bileşenler arasındaki etkileşimi detaylı bir şekilde açıklamaktır. Bu belge, projenin mevcut ve gelecekteki geliştiricileri için bir referans kaynağı olarak hizmet edecek, kodun sürdürülebilirliğini ve genişletilebilirliğini sağlamak için bir yol haritası sunacaktır.

## 1.2. Projenin Kapsamı

Bu doküman, yazılımın aşağıdaki çekirdek işlevselliklerini ve planlanan modüllerini kapsar:

**Planlanan Özellikler:**
-   STL, PLY, OBJ formatlarında 3D model yükleme ve görselleştirme.
-   2D seçimle 3D gürültü temizleme.
-   Model yüzeyindeki deliklerin otomatik doldurulması.
-   Etkileşimli kesit bantları ile radyal deformasyon.
-   "Bulge/Smooth" fırçaları ile serbest form modelleme.
-   Geri Al/İleri Al (Undo/Redo) yeteneği.
-   Çoklu pencerede (multi-view) anatomik hizalama.
-   Otomatik ölçüm ve analiz araçları.
-   Baskı için 3D çıktı alma seçenekleri.

**Yazılımın temel hedefleri:**
-   Hastanın taranmış uzuv verilerini dijital ortamda hassas bir şekilde modellemek.
-   Protez kalıplarını dijital ortamda hassas bir şekilde modellemek.
-   Ortopedi uzmanlarının klinik bilgi ve deneyimlerini dijital sürece entegre etmelerini sağlamak.
-   Kişiye özel, konforlu ve performanslı protezlerin üretimini hızlandırmak ve kolaylaştırmak.
-   Geleneksel kalıplama yöntemlerinin zorluklarını (yüksek kilolu hasta, çift taraflı amputasyon, tekrarlanan düzeltmeler vb.) dijital çözümlerle aşmak.

## 1.3. Tanımlar ve Kısaltmalar

-   **GUI**: Grafiksel Kullanıcı Arayüzü (Graphical User Interface)
-   **VTK**: The Visualization Toolkit
-   **STL**: Stereolithography (3D dosya formatı)
-   **PolyData**: VTK'da poligon ağını (noktalar, hücreler) temsil eden temel veri yapısı.
-   **Pipeline**: Veri akış hattı. VTK'da verinin bir dizi filtreden geçerek işlenmesi.
-   **Frustum**: Kesik piramit. 3D'de bir kamera görüş alanını tanımlayan geometrik hacim.
-   **PHI**: (Personal Health Information) Kişisel Sağlık Bilgileri
-   **CAD**: Bilgisayar Destekli Tasarım (Computer-Aided Design)
-   **CAM**: Bilgisayar Destekli Üretim (Computer-Aided Manufacturing)
-   **3D**: Üç Boyutlu (Three-Dimensional)
-   **Dimension Sheet**: Boyut Tablosu


## 1.4. Uygulama İş Akışı Adımları (Workflow Steps)

Clonify Labs Modelleme Yazılımı, planlanan özellikler doğrultusunda, kullanıcıyı adım adım yönlendiren mantıksal bir iş akışı sunar. Bu akış, ham tarama verisinden baskıya hazır 3D modele kadar olan süreci kapsar ve her adımda `Geri Al/İleri Al (Undo/Redo)` yeteneği ile desteklenir.

### Adım 1: Veri Yükleme ve Görselleştirme (Data Loading & Visualization)

*   **Amacı:** Hastadan alınan ham 3D tarama verisinin sisteme aktarılması ve incelenmesi.
*   **İşlevselliği:**
    *   **Model İçe Aktarma:** Kullanıcı, `STL`, `PLY`, veya `OBJ` formatlarındaki 3D modelleri yazılıma yükler.
    *   **3D Görüntüleme:** Yüklenen model, 3D görüntüleme penceresinde serbestçe döndürülebilir, kaydırılabilir ve yakınlaştırılabilir bir şekilde sunulur. Bu, modelin ilk genel değerlendirmesi için temel oluşturur.

### Adım 2: Çoklu Tarama Birleştirme (Multi-Scan Registration)(Not Priority)

*   **Amacı:** Hastanın farklı açılardan veya zamanlarda yapılmış birden fazla 3D taramasını tek, bütünsel bir modelde birleştirmek. Bu, eksik verileri tamamlamak ve daha eksiksiz bir anatomi oluşturmak için gereklidir.
*   **İşlevselliği:**
    *   **Otomatik Hizalama (Automated Registration):** Yazılım, ortak geometrik özellikleri veya kullanıcı tarafından belirlenen referans noktalarını kullanarak birden fazla taramayı otomatik olarak hizalar.
    *   **Manuel İnce Ayar:** Otomatik hizalamanın ardından, kullanıcıya hizalamayı manuel olarak hassas bir şekilde ayarlama imkanı sunulu, gerekirse.
    *   **Model Birleştirme (Merging):** Hizalanan taramalar, tek ve tutarlı bir 3D model oluşturmak için birleştirilir. Bu birleşik model, sonraki adımlarda kullanılacak olan ana model haline gelir.

### Adım 3: Tarama Temizleme ve Onarım (Scan Cleaning & Repair)

*   **Amacı:** Tarama sürecinden kaynaklanan gürültü, artefakt ve geometrik kusurların giderilmesi.
*   **İşlevselliği:**
    *   **2D Seçimle Gürültü Temizleme:** Kullanıcı, 2D görüntüleme düzleminde istenmeyen alanları (örneğin, tarama masası, destek yapıları, ilgisiz uzuvlar) seçerek 3D modelden kolayca kaldırır.
    *   **Otomatik Delik Doldurma:** Yazılım, model yüzeyindeki istenmeyen delikleri ve boşlukları akıllı algoritmalarla tespit eder ve otomatik olarak kapatarak su geçirmez (manifold) bir model oluşturur.

### Adım 4: Anatomik Hizalama (Anatomical Alignment)

*   **Amacı:** Modelin, standart bir anatomik referans sistemine göre doğru bir şekilde konumlandırılması ve yönlendirilmesi.
*   **İşlevselliği:**
    *   **Çoklu Pencerede Hizalama:** Kullanıcı, farklı açılardan (ön, yan, üst) gösterilen model üzerinde anatomik referans noktaları belirler.
    *   **Otomatik Yönlendirme:** Belirlenen noktalara göre yazılım, modeli otomatik olarak standart anatomik düzleme (örneğin, uzun ekseni Z eksenine paralel olacak şekilde) hizalar.

### Adım 5: Serbest Form Modelleme ve Deformasyon (Free-form Modeling & Deformation)

*   **Amacı:** Protez kalıbının hasta için en uygun ve konforlu hale getirilmesi amacıyla model üzerinde hassas geometrik değişiklikler yapılması.
*   **İşlevselliği:**
    *   **"Bulge/Smooth" Fırçaları:** Kullanıcı, fırça benzeri araçlarla model yüzeyinde sezgisel olarak hacim ekleme (şişirme), çıkarma (aşındırma) ve pürüzsüzleştirme işlemleri yapar. Bu, özellikle basınç noktalarını rahatlatmak veya destek alanları oluşturmak için kullanılır.
    *   **Etkileşimli Kesit Bantları ile Radyal Deformasyon:** Model üzerine yerleştirilen kesit bantları aracılığıyla, belirli bölgelerde dairesel (radyal) olarak hassas boyutlandırma (genişletme/daraltma) yapılır. Bu, uzvun çevresel ölçülerine tam uyum sağlamak için kritiktir.

### Adım 6: Ölçüm ve Analiz (Measurement & Analysis)

*   **Amacı:** Yapılan modifikasyonların doğruluğunu teyit etmek ve klinik gereksinimlere uygunluğunu kontrol etmek.
*   **İşlevselliği:**
    *   **Otomatik Ölçüm Araçları:** Yazılım, model üzerinde uzunluk, çevre, açı ve hacim gibi kritik ölçümleri otomatik olarak yapabilir. Bu, tasarımın sayısal verilerle doğrulanmasını sağlar.
    *   **Analiz:** İki model arasındaki farkları veya belirli bölgelerdeki değişiklikleri görsel ve sayısal olarak analiz etme imkanı sunar.

### Adım 7: Baskıya Hazırlık ve Çıktı (Print Preparation & Export)

*   **Amacı:** Tamamlanan modelin 3D yazıcıda basılmak üzere hazırlanması.
*   **İşlevselliği:**
    *   **Model Sonlandırma:** Modelin baskıya uygunluğu (örneğin, duvar kalınlığı kontrolü) son kez denetlenir.
    *   **3D Çıktı Alma:** Nihai model, 3D baskı için yaygın olarak kullanılan `STL` veya diğer formatlarda dışa aktarılır.

# 3. Hedefler ve Amaçlar

-   Klinisyenlere/teknisyenlere anatomik mesh'leri hassas bir şekilde düzeltmek için araçlar sağlamak.
-   Görsel geri bildirim (ısı haritası) ile basınca dayalı ayarlamaları desteklemek.
-   Tekrarlanabilir bir şekilde deplasman tabanlı kalıplar üretmek (örn. aynı basınç haritası ve parametrelerle, deterministik test mesh'leri ve prosedürel kaynaklar kullanılarak her seferinde aynı sonuçların elde edilmesi; örnek için bkz. "Test Stratejisi" ve "Çekirdek Alan Modelleri" bölümleri).
-   Yoğun geometri operasyonları sırasında duyarlı bir kullanıcı arayüzü sürdürmek.
-   Gelecekteki araçlar (kesme desenleri, şekillendirme, işaretleme, GPU hızlandırma) için modüler bir arka uç sunmak.
-   Tekrarlanabilirliği sağlamak (deterministik test mesh'leri, prosedürel kaynaklar).

# 4. Paydaşlar

-   Klinik protez teknisyenleri (birincil kullanıcılar).
-   Hastane merkezleri.
-   Dahili geliştiriciler (araç zinciri genişletme).
-   QA/test personeli (doğrulama senaryoları).  

# 5. Üst Düzey Mimari

Yazılım, katmanlı mimari yaklaşımını benimseyerek modüler, sürdürülebilir ve genişletilebilir bir yapı sunmaktadır. Bu mimari, görevleri net bir şekilde ayırarak kodun karmaşıklığını azaltır.

## 5.1. Katmanlı Mimari Yaklaşımı

Yazılım, kodun yönetilebilirliğini ve modülerliğini sağlamak amacıyla, görevleri net bir şekilde ayrıştıran üç katmanlı bir mimari üzerine inşa edilmiştir. Bu yapı, Model-View-Controller (MVC) tasarım deseninden güçlü bir şekilde ilham almıştır.

## 5.2. Katmanların Detaylı Analizi

| Katman | Sorumluluk | Teknolojiler / Bileşenler |
| :--- | :--- | :--- |
| **Sunum (Presentation)** | Kullanıcı etkileşimini yönetir, görsel bileşenleri sunar ve kullanıcı girdilerini alır. | PyQt (Widget'lar, Sinyaller/Slotlar), VTK (3D Render Penceresi) |
| **Uygulama (Application)** | Arayüzden gelen istekleri işler, iş mantığını koordine eder ve servisleri çağırır. | Ana uygulama sınıfı, olay yöneticileri, UI ve servisler arası köprü. |
| **Servisler (Services)** | Belirli işlevleri (örn: dosya I/O, mesh işleme) kapsülleyen senkron veya asenkron operasyonları yürütür. | `VTKProcessor`, `AsyncMeshProcessor`, API istemcileri. |
| **Arka Uç (Backend)** | Yoğun hesaplama gerektiren özel alan operasyonlarını ve algoritmaları içerir. | Basınç haritalama, kalıp oluşturma, hizalama algoritmaları. |
| **Alan Modelleri (Domain)** | Uygulamanın durumunu ve temel veri yapılarını (örn: mesh, oturum bilgileri, geri alma yığını) temsil eder. | `AnatomySession`, `vtkPolyData`, `PressureDict`. |
| **Altyapı (Infrastructure)** | Veri depolama, loglama, konfigürasyon ve harici sistemlerle iletişimi yönetir. | Dosya sistemi, veritabanı bağlantıları, loglama kütüphanesi. |


# 7. Kullanılan Teknolojiler ve Kütüphaneler

Projenin geliştirilmesinde, açık kaynak kodlu, endüstri standardı, yüksek performanslı ve geniş topluluk desteğine sahip teknolojiler tercih edilecektir.

## 7.1. Ana Programlama Dili: Python 3.10

**Python**, hızlı prototipleme, temiz sözdizimi ve zengin kütüphane desteği sayesinde projenin ana dili olarak seçilmiştir. Özellikle bilimsel hesaplama ve veri analizi alanlarındaki gücü, medikal veri işleme doğasıyla örtüşmektedir. Python'un "yapıştırıcı dil" özelliği, **VTK** gibi C++ kütüphanelerinin kolayca entegre edilmesini sağlamıştır.

## 7.2. Grafiksel Kullanıcı Arayüzü (GUI): PyQt5

**PyQt5**, platformdan bağımsız masaüstü uygulamaları geliştirmek için kullanılan, Qt C++ kütüphanesinin Python versiyonudur.
-   **Olgunluk ve Kararlılık:** Kararlı ve güvenilir bir arayüz çatısıdır.
-   **Sinyal ve Slot Mekanizması:** Arayüz elemanları ile program mantığı arasında esnek ve ayrıştırılmış iletişim sağlar.
-   **Geniş Widget Seti:** Karmaşık ve profesyonel bir kullanıcı arayüzünün hızlıca oluşturulmasına olanak tanır.
-   **VTK Entegrasyonu:** `QVTKRenderWindowInteractor` widget'ı sayesinde, **VTK**'nın 3D render pencerelerinin bir Qt uygulaması içine sorunsuz entegrasyonu sağlar.

## 7.3. 3D Görselleştirme ve İşleme Motoru: VTK (The Visualization Toolkit)

**VTK**, bilimsel ve medikal verilerin 3 boyutlu olarak işlenmesi, görselleştirilmesi ve analizi için tasarlanmış, C++ tabanlı, yüksek performanslı bir kütüphanedir. Projenin 3D ile ilgili tüm ağır işlerini **VTK** üstlenir.
-   **Veri Akış Hattı Mimarisi (Pipeline Architecture):** `Source -> Filter -> Mapper -> Actor` şeklindeki veri akış modeli, karmaşık 3D veri işleme zincirlerinin modüler ve verimli bir şekilde oluşturulmasını sağlar.
-   **Zengin Filtre Kütüphanesi:** `vtkClipPolyData`, `vtkTransformPolyDataFilter` ve `vtkSTLReader` gibi yüzlerce hazır algoritma içerir. Gelecekte `vtkFillHolesFilter`, `vtkSmoothPolyDataFilter` gibi filtreler de kullanılacaktır.
-   **Gelişmiş Etkileşim Mekanizmaları:** `vtkRenderWindowInteractor` ve `vtkInteractorStyle` alt sınıfları, fare ve klavye ile karmaşık 3D sahne etkileşimleri oluşturmak için güçlü bir altyapı sunar.

## 7.4. Matematiksel ve Bilimsel Hesaplama: NumPy

**NumPy**, Python'da bilimsel hesaplamalar için temel pakettir. Çok boyutlu diziler üzerinde yüksek performanslı matematiksel işlemler için kullanılır.
-   **Performans:** Büyük veri kümeleri üzerinde hızlı hesaplamalar sağlar.
-   **Vektör Matematiği:** Anatomik hizalama ve deformasyon algoritmalarında vektör ve matris işlemleri için kullanılır.
-   **VTK Uyumluluğu:** `vtk.util.numpy_support` modülü, NumPy dizileri ile VTK veri dizileri arasında verimli veri alışverişi sağlar.

# 8. Çekirdek Fonksiyonların Mantıksal Akışı

## 8.1. Fonksiyon: Mesh Yükleme

**Amaç:** Harici bir dosyadan (örn: .stl, .ply) 3D mesh verilerini uygulamaya yüklemek ve görselleştirmek.

**Mantıksal Akış:**
1.  **UI Talebi:** Kullanıcı, UI sayfasından bir mesh yükleme isteği başlatır (dosya yolu ile).
2.  **İşlem Başlangıcı Sinyali:** Kontrol Katmanı, UI'a bir "processingStarted" sinyali gönderir.
3.  **Dosya Okuma:** **VTKProcessor** (Hizmet Katmanı), dosya uzantısına göre uygun VTK okuyucusunu (`vtkSTLReader`, `vtkPLYReader`) seçer.
4.  **Mesh Yükleme:** Okuyucu, 3D mesh verilerini (**vtkPolyData**) belleğe yükler.
5.  **Orijinal Veri Kopyası:** Yüklenen mesh'in derin bir kopyası `original_poly_data` olarak saklanır.
6.  **Aktif Veri Ayarı:** Yüklenen mesh, `active_poly_data` olarak ayarlanır.
7.  **Geçmiş Yığınına Ekleme:** Uygulamanın başlangıç durumu, `HistoryStack`'e ilk "işlem" olarak eklenir.
8.  **Mesh Yüklendi Sinyali:** **VTKProcessor**, yüklendiğini ve `active_poly_data`'yı referans alarak "meshLoaded" sinyali gönderir.
9.  **İşlem Tamamlandı Sinyali:** Son olarak, "processingFinished" sinyali gönderilir.
10. **UI Güncelleme:** UI, `update_renderer` metoduyla yeni `active_poly_data`'yı görselleştirmek üzere güncellenir.
11. **MESH kalitesi arttırma**: Yüklenen mesh verileri, `VTKProcessor` tarafından çeşitli iyileştirme teknikleri (örn: yüzey pürüzsüzleştirme, kenar keskinleştirme) ile işlenir.

## 8.2. Fonksiyon: Basınç Boyama

**Amaç:** Kullanıcının 3D mesh üzerinde fare ile çizim yaparak her bir noktaya (vertex) bir basınç değeri atamasını sağlamak ve bunu görselleştirmek (ısı haritası).

**Mantıksal Akış:**
1.  **Fırça Seçimi:** Kullanıcı UI'dan bir fırça (boyut, sertlik, güç) seçer.
2.  **Uzamsal Sorgu Başlatma:** `vtkStaticPointLocator` nesnesi (hızlı uzamsal sorgular için önceden oluşturulmuş/önbelleğe alınmış) başlatılır.
3.  **Çizim Başlangıcı:** Kullanıcı fareyi mesh üzerinde sürüklemeye başladığında, geçerli fırça vuruşu için bir tampon (buffer) temizlenir.
4.  **Fırça Hareketi:** Kullanıcı farenin basılı tutarak mesh üzerinde hareket etmesiyle (`mouse_moved` olayı), `PressureTool` şu adımları izler:
    -   Fırça merkezi çevresindeki noktalar (radius) bir uzamsal sorgu ile bulunur.
    -   Her etkilenen nokta için, fırça merkezine olan uzaklığa göre bir "ağırlık" (weight) veya etki düşüşü (falloff) hesaplanır.
    -   Yeni basınç değeri (örn: `yeni_basinc = mevcut_basinc + guc * agirlik`) hesaplanır ve -100 ile 100 arasında bir değere clamped edilir.
    -   Noktanın ID'si, eski değeri ve yeni değeri bir vuruş tamponuna (`stroke buffer`) kaydedilir (bu nokta ilk kez değiştiriliyorsa).
    -   Basınç değerleri, hafızadaki `pressure_dict`'te güncellenir.
    -   Bu değişiklikler, `vtkFloatArray` olan `PressureValues` skaler dizisine yansıtılır ve render isteği, UI'da gerçek zamanlı görsel geri bildirim sağlamak için gruplanır (throttled).
5.  **Çizim Sonu:** Kullanıcı fareyi bıraktığında (`mouse_released` olayı), tüm vuruş tamponu, geri alma/ileri alma yığınına (`HistoryStack`) bir "işlem" olarak eklenir.

## 8.3. Fonksiyon: Isı Haritası Oluşturma (Asenkron)

**Amaç:** `pressure_dict`'teki basınç değerlerini mesh üzerinde görsel olarak bir ısı haritası olarak göstermek. Performans için asenkron (arka planda) olarak çalışır.

**Mantıksal Akış:**
1.  **UI İsteği:** Kullanıcı, UI'dan ısı haritası oluşturma talebini tetikler.
2.  **Asenkron Kuyruk:** Kontrol Katmanı, bu operasyonu `AsyncMeshProcessor`'a (ayrı bir thread) sıraya alır.
3.  **Thread Başlatma:** Ayrı bir thread'de (işlemciyi dondurmamak için) `AsyncMeshProcessor` çalışmaya başlar.
4.  **Skaler Dizi Oluşturma/Güncelleme:** Thread, `pressure_dict`'teki değerleri kullanarak veya güncelleyerek `vtkFloatArray` tipinde bir `PressureValues` skaler dizisi oluşturur/günceller.
5.  **Tamamlanma Sinyali:** İşlem tamamlandığında, thread, sonuç meta verileriyle (örn: değer aralığı) bir `processing_complete` sinyali gönderir.
6.  **UI Güncelleme:** Kontrol Katmanı, bu sinyali ana thread'de yakalar. Isı haritasının renk dönüşümü için `vtkLookupTable` (LUT) yapılandırılır ve bu LUT'ye göre renderer güncellenir.

## 8.4. Fonksiyon: Kalıp Oluşturma

**Amaç:** Mesh'in `PressureValues`'ına dayalı olarak protez kalıbını (deforme edilmiş mesh) oluşturmak.

**Mantıksal Akış:**
1.  **Isı Haritası Garantisi:** İşlem başlamadan önce `PressureValues`'ın doğru bir şekilde hesaplanmış ve meshe atanmış olduğundan emin olunur.
2.  **Deplasman Skaleri Hesaplama:** Her bir nokta için bir deplasman skaleri (`displacement_scalar`) hesaplanır. Bu genellikle atanmış basınç değerinin (`pressure_value`) bir `warp_scale` faktörü ile çarpılmasıyla elde edilir (örn: `displacement_scalar = -pressure_value * warp_scale`). Negatif değerler, materyalin dışarı doğru itilmesi anlamına gelir.
3.  **Geometri Deformasyonu:**
    -   Modeldeki her bir noktanın normal vektörü alınır.
    -   Noktanın yeni konumu, `yeni_konum = mevcut_konum + deplasman_skaleri * normal_vektör` formülüyle hesaplanır.
    -   Bu, `vtkWarpVector` filtresi veya manuel nokta deplasmanı algoritmaları kullanılarak gerçekleştirilebilir.
4.  **MoldDisplacement Kaydı:** Hesaplanan deplasman değerleri, daha sonra tekrarlanabilirlik ve analiz için `MoldDisplacement` adında yeni bir skaler dizi olarak meshe atanabilir.
5.  **Güncelleme:** Deforme olmuş **PolyData**, `active_poly_data` olarak ayarlanır ve `HistoryStack`'e eklenir. Render güncellenir.
6.  **Meta Veri:** Oluşturulan kalıbın ölçeği, minimum/maksimum deplasman gibi meta veriler, daha sonra raporlama veya analiz için kaydedilir.

## 8.5. Fonksiyon: Tarama Temizleme

**Amaç:** Kullanıcının 2D bir seçimle 3D modelin istenmeyen kısımlarını (örn: tarama gürültüsü, gereksiz arka plan) silmesi.

**Mantıksal Akış:**
1.  **Giriş:** Kullanıcı, 3D görüntüleme penceresinde 2D bir dikdörtgen veya serbest form bir alan çizer (fare sürüklemesi ile).
2.  **2D -> 3D Dönüşüm:** Sistem (VTK Picker ve Frustum sınıfları), bu 2D seçim alanını, 3D uzayda bir seçim hacmine (frustum veya bounding box) dönüştürür. Bu hacim, kameranın bakış açısı ve derinliği dikkate alınarak oluşturulur.
3.  **Kesme İşlemi:** Seçilen 3D hacmin içinde veya dışında kalan (kullanıcının seçimine bağlı olarak) tüm 3D geometri (**PolyData**'nın noktaları ve hücreleri), `vtkClipPolyData` veya benzeri bir filtre kullanılarak modelden çıkarılır.
4.  **Güncelleme:** Temizlenmiş **PolyData** nesnesi, yeni "Aktif Veri" olarak ayarlanır ve `HistoryStack`'e yeni bir işlem olarak eklenir. Arayüz güncellenir.

## 8.6. Fonksiyon: Anatomik Hizalama

**Amaç:** 3D modeli (örneğin, ampute uzuv taraması), standart bir anatomik koordinat sistemine göre yeniden yönlendirmek (örn: uzvun uzun eksenini Z eksenine, ön-arka yönünü Y eksenine hizalamak).

**Mantıksal Akış:**
1.  **Giriş:** Kullanıcı, model üzerinde stratejik anatomik referans noktalarını işaretler (örn: büyük trokanter, lateral/medial epikondil, distal uç). Bu noktalar, 3D uzayda `vtkPointPicker` gibi araçlarla seçilir ve koordinatları saklanır.
2.  **Koordinat Sistemi Hesaplama:** Sistem (**NumPy** ve lineer cebir fonksiyonları kullanarak), işaretlenen bu noktalardan yola çıkarak yeni bir anatomik koordinat sistemi (yeni X, Y, Z eksenleri) hesaplar. Örneğin, uzvun uzun ekseni iki nokta arasındaki vektörden, ön-arka ekseni ise diğer noktaların konumlarına göre belirlenir.
3.  **Dönüşüm Matrisi Oluşturma:** Modelin mevcut koordinat sistemi ile yeni hesaplanan anatomik koordinat sistemi arasında geçişi sağlayacak bir dönüşüm (rotasyon ve translasyon) matrisi (`vtkTransform`) oluşturulur.
4.  **Model Hizalama:** `vtkTransformPolyDataFilter` kullanılarak, tüm **PolyData** bu matris ile döndürülür ve hizalanmış olur.
5.  **Güncelleme:** Hizalanmış **PolyData** nesnesi "Aktif Veri" olarak kaydedilir ve `HistoryStack` güncellenir.

## 8.7. Fonksiyon: Hacimsel Deformasyon

**Amaç:** Protez soketinin belirli bölgelerinde (örn: yük taşıyan alanlar, hassas kemik bölgeleri) ölçüleri hassas bir şekilde artırmak (hacim ekleme) veya azaltmak (hacim çıkarma/sıkıştırma).

**Mantıksal Akış:**
1.  **Giriş:** Kullanıcı, model üzerinde deforme etmek istediği bir bölgeyi (örn: kesit bantları ile, veya manuel fırça ile) ve uygulanacak deformasyon miktarını (+/- mm) tanımlar.
2.  **Nokta Seçimi ve Etki Alanı:** Sistem, tanımlanan bölge içindeki tüm 3D noktaları belirler. Bir fırça kullanılıyorsa, fırça merkezine olan uzaklığa göre bir "etki düşüşü" (falloff) fonksiyonu hesaplanır.
3.  **Deformasyon Uygulama:**
    -   Her bir seçili nokta için, noktanın yüzey normal vektörü hesaplanır.
    -   Nokta, belirlenen deformasyon miktarı ve falloff fonksiyonuna göre (yüzey normali boyunca) içe (azaltma) veya dışa (artırma) doğru hareket ettirilir.
    -   Bu işlem, **PolyData**'nın nokta koordinatlarını doğrudan değiştirerek gerçekleştirilir.
4.  **Güncelleme:** Deforme olmuş **PolyData** nesnesi "Aktif Veri" olarak ayarlanır ve `HistoryStack`'e eklenir.

# 9. Kullanıcı Etkileşim Tasarımı

## 9.1. Modüler Etkileşim Stilleri

Uygulama, farklı görevler için farklı fare ve klavye davranışları gerektirir. Bu, **VTK**'nın `vtkInteractorStyle` sınıfından türetilen "Etkileşim Stilleri" adı verilen değiştirilebilir modüllerle yönetilir. `MainWindow` (Controller), kullanıcının seçtiği araca göre bu stiller arasında dinamik olarak geçiş yapar.

-   **Kamera Stili (Varsayılan):** Varsayılan mod. Kullanıcının 3D sahneyi serbestçe döndürme, kaydırma ve yakınlaştırma işlemlerini (fare tekerleği, sol/orta/sağ tıklama ve sürükleme ile) sağlar. (Örn: `vtkInteractorStyleTrackballCamera`).
-   **Seçim Stili:** Tarama Temizleme aracı aktifken, kullanıcının 2D bir dikdörtgen veya serbest form seçim alanı çizmesini sağlar. Bu 2D seçim, 3D uzayda geometriyi kesmek veya filtrelemek için kullanılır. (Örn: `vtkInteractorStyleRubberBand2D` veya özel bir interaktör stili).
-   **İşaretleme Stili:** Anatomik Hizalama aracı aktifken, kullanıcının model üzerinde belirli 3D noktaları (örn: kemik işaretleri) tıklayarak seçmesini sağlar. Seçilen noktalar, daha sonra dönüşüm matrisleri hesaplamak için kullanılır. (Örn: `vtkInteractorStyleTrackballCamera` ile birlikte `vtkPointPicker` kullanılarak özelleştirilmiş bir stil).
-   **Fırça/Heykel Stili:** Oyma/Ekleme veya Yumuşatma araçları aktifken, kullanıcının fareyi model üzerinde sürükleyerek lokal deformasyonlar veya yumuşatmalar yapmasını sağlar. Fırça imleci ve etki alanı görselleştirilir. (Özel bir `vtkInteractorStyle` alt sınıfı).

# 15. Mesh İşlemleri (Temsili)

**Clonify Labs**, protez kalıplarını hazırlamak ve düzeltmek için çeşitli temel mesh işleme operasyonlarını kullanır. Bu operasyonlar **VTK** kütüphanesinin gücünü kullanır.

| Operasyon | Tekniği / VTK Filtresi | Açıklama |
|---|---|---|
| Temizleme (Clean) | `vtkCleanPolyData` | Mesh'teki fazladan (duplicate) noktaları birleştirmek, küçük açıklıkları kapatmak ve genel topolojik temizlik yapmak için kullanılır. Tarama verilerindeki hataları gidermede önemlidir. |
| Yumuşatma (Smooth) (Taubin/Laplacian) | `vtkSmoothPolyDataFilter` veya özelleşmiş filtreler | Mesh yüzeyindeki pürüzlülüğü azaltır, köşeleri yumuşatır ve daha organik bir görünüm sağlar. Konfor açısından kritik bir adımdır. |
| Basitleştirme (Decimate) | `vtkDecimatePro` ile hedef azaltma oranı | Mesh'in poligon sayısını azaltır. Dosya boyutunu küçültür ve işlem performansını artırır, ancak modelin detay seviyesini düşürebilir. |
| Alt Bölümlere Ayırma (Subdivide) | `vtkLoopSubdivisionFilter` (ayarlanabilir iterasyonlar) | Mesh'in poligon sayısını artırır, yüzeylere daha fazla detay ekler ve daha pürüzsüz kıvrımlar sağlar. Özellikle manuel şekillendirme için daha fazla kontrol sağlar. |
| Normallerin Yeniden Hesaplanması | `vtkPolyDataNormals` (modifikasyon sonrası) | Mesh üzerinde yapılan deformasyonlar sonrası noktaların ve yüzeylerin normal vektörlerini yeniden hesaplar. Doğru görselleştirme ve sonraki işlemler (örn: kalınlık verme) için esastır. |
| Çarpıtma (Warp) (Kalıp için) | `vtkWarpVector` veya manuel nokta deplasmanı | Kalıp oluşturma sürecinde, belirli bir yönde (genellikle yüzey normali boyunca) ve belirli bir miktar kadar noktaları kaydırarak mesh'i deforme eder. Basınç değerleri bu deplasman miktarını belirleyebilir. |

# 16. Performans Stratejileri

Yazılımın yoğun 3D işlemler sırasında bile kullanıcı arayüzünün (UI) duyarlı kalmasını sağlamak için çeşitli performans optimizasyon stratejileri uygulanmıştır.

| Endişe | Teknik |
|---|---|
| UI Donması | İşlem maliyeti yüksek fonksiyonlar için ayrı iş parçacıkları (**QThread**) ve sinyaller (**PyQt Signal/Slot**) kullanarak arka planda işlem yürütme. |
| Aşırı Render Çağrıları | Hızlı ardışık güncelIemeleri (`mouseMoveEvent` gibi) tek bir render çağrısında birleştiren gruplama (`BatchRenderer`) ve kısıtlama (throttling) mekanizmaları. |
| Uzamsal Sorgular | `vtkStaticPointLocator` gibi **VTK**'nın optimize edilmiş uzamsal indeksleme yapılarının yeniden kullanımı. Bu, büyük meshlerdeki noktalara hızlı erişim sağlar (örn: fırça etki alanı sorguları). |
| Skaler Dizi Güncellemeleri | Skaler dizilerin (`vtkFloatArray`) her değişiklikte yeniden oluşturulması yerine, mevcut dizi verilerinin doğrudan bellekte güncellenmesi (in-place modification). |
| Geri Alma Yığını Boyutu | Tam **PolyData** kopyaları yerine, yalnızca değiştirilen nokta ID'leri ve eski/yeni değerler gibi delta değişikliklerini depolayarak yığın boyutunu optimize etme. |
| Büyük Mesh Yumuşatma | Yumuşatma iterasyonlarının sınırlanması, yoğun mesh'ler için işlem öncesi basitleştirme (decimation) uygulama. |
| GPU Kullanımı (isteğe bağlı) | Mümkün olduğunda **VTK**'nın GPU destekli mapper'larını veya filtrelerini kullanma. GPU mevcut değilse sorunsuz bir şekilde CPU tabanlı yöntemlere geri düşme. |

**İzleme:**
-   Maliyetli operasyonların (örn: mesh işleme) sürelerini kaydetmek için loglama kullanılır.
-   Önemli performans noktaları için basit zamanlama dekoratörlerinin entegrasyonu potansiyel bir iyileştirmedir.

# 17. Loglama ve Hata Yönetimi

Uygulamanın çalışma zamanı davranışını izlemek, sorunları teşhis etmek ve kullanıcıya geri bildirim sağlamak için kapsamlı bir loglama ve hata yönetimi stratejisi benimsenmiştir.

-   **Modül Başına Logger:** `print` ifadeleri yerine, her Python modülü için ayrı bir `logging` nesnesi kullanılır. Bu, günlüklerin düzenli olmasını ve filtrelenmesini kolaylaştırır.
-   **Kullanıcıya Yönelik Durum Sinyalleri:** Kullanıcı arayüzünde görünen durum mesajları için özel sinyaller (`logMessage`) kullanılır. Bu sinyaller, işlemin başladığını, ilerlemesini, tamamlandığını veya bir hata oluştuğunu kullanıcıya bildirir.
-   **Desteklenmeyen Dosya Tipleri:** Desteklenmeyen dosya uzantıları veya bozuk mesh dosyaları için yükleme aşamasında erken ret mekanizmaları bulunur. Bu durumlar günlüğe kaydedilir ve kullanıcıya açık bir hata mesajı sunulur.
-   **Asenkron Hata Yakalama:** Asenkron iş parçacıklarında (örn: `AsyncMeshProcessor`) meydana gelen istisnalar `try`/`catch` blokları içinde yakalanır. Hata detayları günlüğe kaydedilir ve ana thread'e bir hata sinyali gönderilerek UI'ın duyarlı kalması sağlanır.
-   **Günlük Dosyaları:** Çalışma zamanı günlükleri, `logs/` dizini altında zaman damgalı dosyalar halinde saklanır. Bu günlükler, sorun giderme ve uygulama denetimleri için kullanılabilir.
-   **Bağlam İçeriği:** Hata mesajlarına, ilgili mesh dosyasının adı gibi bağlam bilgileri eklenerek sorunların tespiti kolaylaştırılır.

# 18. Konfigürasyon ve Ortam

Yazılımın kurulumu ve farklı ortamlarda çalıştırılması için konfigürasyon ve bağımlılık yönetimi stratejileri belirlenmiştir.

-   **Python 3.11 Hedefi:** Proje, Python 3.11 veya daha yeni versiyonlarını hedef alarak en güncel dil özelliklerinden ve performans iyileştirmelerinden faydalanır.
-   **Bağımlılık Yönetimi:** Tüm Python bağımlılıkları (**PyQt5**, **VTK**, **NumPy** vb.) `pyproject.toml` veya `requirements.txt` dosyaları aracılığıyla yönetilir. Bu, projenin farklı geliştirme veya dağıtım ortamlarında bağımlılıkların kolayca kurulmasını sağlar.
-   **Çalışma Zamanı Dizini Yapısı:**
    -   `logs/`: Çalışma zamanı günlüklerinin depolandığı yazılabilir bir dizindir. Uygulama ilk çalıştığında otomatik olarak oluşturulur.
    -   `data/`: Test mesh'leri ve prosedürel örnek mesh'ler gibi statik verilerin saklandığı dizindir.
-   **İsteğe Bağlı Ortam Değişkenleri:** Gelecekte, uygulamanın davranışını etkileyebilecek (örn: debug modu, varsayılan dosya yolları) ortam değişkenleri için merkezi bir konfigürasyon (`app/core/config.py`) veya dışarıdan yüklenen bir `.env` dosyası kullanılabilir ve bu dokümanda belgelenmelidir.

# 19. Derleme ve Bağımlılık Yönetimi

Yazılımın geliştirme ve dağıtım süreçlerinde bağımlılıkların yönetimi ve derleme (build) adımları belirlenmiştir.

-   **Kurulum Yöntemi:** Geliştirme ortamında, proje `pip install -e .` komutuyla kurulabilir (eğer `pyproject.toml` projenin tanımını içeriyorsa). Bu, projenin kaynak koduna doğrudan bağlı olarak düzenlenebilir bir kurulum sağlar.
-   **Sürüm Sabitleme:** Özellikle **VTK** gibi kritik kütüphanelerin belirli sürümleri sabitlenir (`requirements.txt` dosyasında `vtk==X.Y.Z` gibi). Bu, farklı **VTK** versiyonlarının yol açabileceği uyumluluk sorunlarını veya çalışma zamanı davranış farklılıklarını önler.
-   **Sürekli Entegrasyon (CI - Gelecek):** Gelecekte bir CI/CD boru hattı kurulması planlanmaktadır. Bu hat, kod kalitesini ve kararlılığını sağlamak için şu adımları otomatik olarak çalıştıracaktır:
    -   Linting ve Stil Kontrolleri: Kodun PEP8 gibi stil rehberlerine uygunluğunu kontrol eder.
    -   Çekirdek Testler: Temel işlevselliğin doğru çalıştığından emin olmak için birim ve entegrasyon testlerini çalıştırır.
    -   Performans Smoke Testleri: Kritik operasyonlarda performans düşüşleri olup olmadığını kontrol etmek için seçilmiş performans testlerini çalıştırır.
-   **Paketleme (Dağıtım için):** Son kullanıcı dağıtımları için, PyInstaller gibi araçlar kullanılarak Python uygulaması tek bir yürütülebilir dosyaya (executable) paketlenebilir. Bu, bağımlılıkları yönetme yükünü son kullanıcıdan alır.
-   **Başlatma Betikleri:** Platformlar arası uyumluluk sağlamak için isteğe bağlı başlatma betikleri (launcher scripts) sağlanabilir.

# 20. Kodlama Standartları

Kodun okunabilirliğini, sürdürülebilirliğini ve ekip içinde tutarlılığı sağlamak için belirli kodlama standartları benimsenmiştir.

-   **PEP8 Uyumluluğu:** Python kodunun büyük ölçüde PEP8 stil rehberine uygun olması hedeflenir. Ancak, özellikle **VTK** boru hatlarının okunabilirliğini artırmak amacıyla, bazı durumlarda daha uzun ve birleşik fonksiyonlara pratik tolerans gösterilebilir.
-   **Tip İpuçları (Type Hints):** Tüm genel (public) arayüzlerde ve mümkün olduğunca diğer yerlerde tip ipuçları (type hints) kullanılır. Bu, kodun anlaşılırlığını artırır ve statik analiz araçlarıyla potansiyel hataların erken tespitine yardımcı olur.
-   **Doküman Dizileri (Docstrings):** Her fonksiyon, sınıf ve önemli metot için kısa bir özet satırı içeren docstring'ler yazılır. Parametreler ve dönüş değerleri hakkında detaylı bilgi sağlanır.
-   **Skaler Dizi Adlandırması:** `PressureValues`, `MoldDisplacement` gibi skaler diziler için tutarlı ve açıklayıcı adlandırma standartları kullanılır.
-   **Harici Kütüphanelerden Kaçınma:** Zorunlu olmadıkça yeni harici Python kütüphaneleri eklemekten kaçınılır. Yeni bir bağımlılık eklenmeden önce dikkatlice değerlendirilir.
-   **Loglama Kullanımı:** Kod içinde `print()` ifadeleri yerine, hata ayıklama ve izleme için merkezi loglama (`logging` modülü) tercih edilir. İstisnalar sessizce yutulmaz; uygun hata logları kaydedilir.

# 21. Test Stratejisi

Yazılımın doğruluğunu, güvenilirliğini ve performansını sağlamak için kapsamlı bir test stratejisi uygulanmaktadır.

**Mevcut Test Betikleri:** Projenin test klasöründe (`tests/`) bulunan mevcut test betikleri, uygulamanın çeşitli özelliklerini doğrulamak için kullanılır:
-   `test_pressure_mapping.py`: Basınç boyama, ısı haritası oluşturma ve UI entegrasyonunun temel işlevselliğini doğrular.
-   `test_enhanced_pressure_mapping.py`: Gelişmiş basınç boyama özelliklerini test eder.
-   `test_split_view_pressure_mapping.py`: Çoklu görünümdeki basınç boyama ve görselleştirme davranışını test eder.
-   `test_mesh_subdivision.py`: Mesh alt bölümlere ayırma (subdivision) doğruluğunu test eder.
-   `test_page3_performance.py`: UI'ın belirli sayfalardaki performansını ve tepki süresini test eder.
-   `test_gpu_performance.py`: GPU hızlandırma yollarının performansını test eder.
-   `test_landmarks.py`: İşaret noktası yerleştirme mantığını doğrular.
-   `test_orientation_definition.py`: Anatomik yönelim hesaplama boru hattını test eder.
-   `test_page4_cutting_patterns.py`: Kesme deseni oluşturma davranışını test eder.
-   `MOLD_GENERATION_SUCCESS.py` gibi betikler, kalıp oluşturma iş akışlarının başarıyla tamamlandığını gösterir.

**Test Desenleri:**
-   **Prosedürel Geometri:** Testlerde, dış dosyalar yerine genellikle küp, küre gibi basit prosedürel geometriler veya programatik olarak oluşturulmuş mesh'ler kullanılır. Bu, testlerin bağımsızlığını ve tekrarlanabilirliğini artırır.
-   **Onaylamalar (Assertions):** Nokta sayıları, skaler değer aralıkları, fonksiyonların çökmeden çalışması gibi konular üzerinde net onaylamalar (`assert`) kullanılır.
-   **Geri Al/İleri Al Doğrulaması:** Modifikasyonlar sonrası `HistoryStack`'in doğru çalıştığından ve geri alma/ileri alma işlemlerinin veriyi tutarlı bir şekilde önceki/sonraki durumlara döndürdüğünden emin olmak için özel testler bulunur.
-   **Kalıp Deplasmanı Tutarlılığı:** Kalıp oluşturma işleminde minimum/maksimum deplasman değerlerinin ve genel geometri tutarlılığının korunup korunmadığı test edilir.
-   **Performans Eşiği Kontrolü:** Belirli operasyonların belirtilen performans eşiklerini aşmadığını doğrulamak için zamanlama testleri kullanılır.

**Test Kategorileri:**
-   **Birim Testleri:** Her bir fonksiyon veya küçük sınıfın izole edilmiş bir şekilde doğru çalıştığını doğrular.
-   **Entegrasyon Testleri:** Farklı modüllerin veya katmanların birbiriyle doğru etkileşim kurduğunu doğrular.
-   **Sistem Testleri:** Tüm uygulamanın uçtan uca senaryolarda beklendiği gibi çalıştığını doğrular.
-   **Performans Testleri:** Belirli operasyonların ve genel uygulamanın tepki süresi ve kaynak kullanımı hedeflerini karşıladığını doğrular.
-   **Regresyon Testleri:** Yeni kod eklendikten veya mevcut kod değiştirildikten sonra, daha önce çalışan özelliklerin hala doğru çalıştığını garanti eder.

# 22. Kalite Kontrolleri

Yazılımın yüksek kalitesini sürekli olarak sağlamak için çeşitli kalite kontrol mekanizmaları belirlenmiştir.

| Kontrol Noktası | Amaç |
|---|---|
| Linting/Stil Kontrolü | Kodun okunabilirliğini ve stil standartlarına (örn. PEP8) uygunluğunu sürdürmek. |
| Tip Kontrolü (isteğe bağlı) | Arayüz tutarsızlıklarını ve tip hatalarını tespit etmek için Python'ın tip ipuçları ile statik analiz araçları kullanmak. |
| Birim Testleri | Her bir küçük kod biriminin (fonksiyon, metod) doğru çalıştığından emin olmak. |
| Performans Smoke Testleri | Boyama ve kalıp oluşturma boru hatları gibi kritik işlevlerde performans gerilemelerinin olmadığını doğrulamak. |
| Loglama Varlığı | Temel operasyonların izlenebilirlik için doğru günlük mesajları ürettiğini ve bu günlüklerin yeterli izleme bilgisi içerdiğini doğrulamak. |

# 23. Güvenlik ve Gizlilik

Medikal bir yazılım olarak, güvenlik ve gizlilik **Clonify Labs** için kritik öneme sahiptir. Kişisel Sağlık Bilgilerinin (**PHI**) korunması en üst düzeyde önceliklidir.

-   **PHI Saklama:** Yazılım, hasta tanımlayıcı bilgilerini veya kişisel sağlık bilgilerini (**PHI**) doğrudan kalıcı olarak saklamaz. Mesh dosya adları anonimleştirilir veya jenerik bir formatta tutulur.
-   **Günlük Dosyaları:** Günlük dosyaları, hasta tanımlayıcılarını içermez. Yalnızca teknik sorun giderme için gerekli olan uygulama davranışları ve hata bilgileri kaydedilir.
-   **Ağ İletişimi:** Mevcut durumda, yazılımın herhangi bir ağ üzerinden doğrudan geometri veya hasta verisi iletimi yapmadığı varsayılır (çevrimdışı masaüstü uygulaması olarak çalışır).
-   **Gelecek Genişletmeleri:** Eğer gelecekte bulut senkronizasyonu veya çok kullanıcılı işbirliği gibi ağ bağlantılı özellikler eklenirse:
    -   **Veri Şifreleme:** Saklanan oturum durumları veya iletilen veriler için endüstri standardı şifreleme yöntemleri (örn: AES-256) kullanılacaktır.
    -   **Kimlik Doğrulama ve Yetkilendirme:** Kullanıcı kimlik doğrulaması (örneğin, OAuth, API anahtarları) ve yetkilendirme (rol tabanlı erişim kontrolü) mekanizmaları uygulanacaktır.
    -   **Güvenli Protokoller:** HTTPS/TLS gibi güvenli iletişim protokolleri zorunlu tutulacaktır.
    -   **Gizlilik Politikaları:** **PHI**'nin nasıl işlendiğini, saklandığını ve korunduğunu açıklayan net gizlilik politikaları belirlenecek ve kullanıcılara sunulacaktır.

# 24. Riskler ve Azaltma Yöntemleri

Proje boyunca karşılaşılabilecek potansiyel riskler ve bunları azaltmaya yönelik stratejiler belirlenmiştir.

| Risk | Etki | Azaltma Yöntemi |
|---|---|---|
| VTK Sürüm Uyumsuzluğu | Çalışma zamanı hataları, beklenmeyen davranışlar. | Bağımlılıkları belirli sürümlere sabitlemek (`pip freeze` veya `requirements.txt` ile) ve farklı VTK versiyonlarıyla düzenli test matrisi çalıştırmak. |
| Büyük Mesh Bellek Kullanımı | Uygulama yavaşlaması/donması veya çökmesi. | Büyük mesh'ler için ön işlemde basitleştirme (decimation) uygulama, gelecekte veri akışını optimize eden "streaming" teknikleri araştırmak. |
| UI Donması (Yanıt Vermemesi) | Kullanıcı deneyiminin kötüleşmesi, üretkenlik kaybı. | Tüm maliyetli operasyonları (dosya yükleme, karmaşık hesaplamalar) ayrı iş parçacıklarında (**QThread**) yürütme ve sinyallerle iletişim kurma. |
| Geri Alma Yığını Büyümesi | Aşırı bellek tüketimi, performans düşüşü. | Geçmiş yığınını belirli bir boyutta sınırlama veya tam mesh kopyaları yerine sadece değişiklikleri (delta) sıkıştırarak depolama. |
| Skaler Dizi Tutarsızlığı | Görsel hatalar, hatalı ısı haritaları veya kalıp deformasyonları. | Skaler dizi güncellemeleri için merkezi ve güvenli bir işlev kullanma, güncellemeleri yalnızca ana iş parçacığında yapma. |
| GPU Yolu Ayrışması | Farklı donanımlarda tekrarlanamayan veya zor teşhis edilen hatalar. | GPU destekli özellikler için isteğe bağlı kod yolları sağlama ve GPU mevcut olmadığında sorunsuz bir şekilde CPU tabanlı yöntemlere geri dönme. Hem GPU hem de CPU yollarını test etme. |
| Kişisel Sağlık Bilgileri (PHI) Sızıntısı | Yasal sorunlar, hasta güveninin kaybı. | Hasta verilerini anonimleştirme, günlüklerde PHI bulundurmama, ağ iletimi için şifreleme (gelecekte) ve erişim kontrolleri. |
| Aşırı Kullanıcı Geribildirimi/Fırça Darbeleri | Performans düşüşü, gereksiz işlem yükü. | Fırça darbelerini veya hızlı olayları gruplandıran ve belirli bir oranda işleyen kısıtlama (throttling) mekanizmaları kullanma. |
| Yeni Geliştirici Onboarding Süresi | Ekip büyümesinde verimlilik kaybı. | Minimum geliştirici onboarding adımları sağlama, kapsamlı dokümantasyon ve örnekler sunma. |

# 25. Gelecek Geliştirmeler ve Genişletme Noktaları

**APPClonify**'ın mevcut mimarisi, gelecekteki fonksiyonel ve teknolojik genişletmeler için güçlü bir temel sağlamaktadır. Aşağıdaki alanlar, potansiyel gelecek geliştirmeler ve genişletme noktaları olarak tanımlanmıştır:

-   **Oturum Serileştirme:**
    -   **Strateji:** Mevcut oturum durumunu (basınç verileri, işaret noktaları, modifiye edilmiş mesh ve tüm geçmiş yığını) tek bir dosyada kaydetme ve yükleme yeteneği ekleme. Bu, kullanıcıların projelerine daha sonra devam etmelerini sağlar.
    -   **Teknoloji:** JSON veya XML tabanlı özel bir dosya formatı kullanarak tüm Python ve VTK nesnelerini serileştirme (`pickle` veya özel serileştirme mantığı gerekebilir).
-   **Parametrik Kalıp Tasarımı:**
    -   **Strateji:** Tek tip kalınlık uygulamanın ötesinde, kullanıcının farklı anatomik bölgeler için katmanlı veya değişken kalınlık profilleri tanımlamasına olanak tanıyan parametrik bir sistem geliştirme.
    -   **Teknoloji:** Özel UI widget'ları ve arka uçta geometriyi katmanlara ayırıp her katmanı ayrı ayrı deforme eden VTK filtreleri.
-   **Kesme Desenleri İçin Gelişmiş Düzleştirme (Unwrapping):**
    -   **Strateji:** Kesilmiş 3D mesh yüzeylerini, fiziksel şablon üretimi veya kumaş kesimi için 2D düzleme doğru bir şekilde açma (unwrapping) yeteneği ekleme.
    -   **Teknoloji:** `vtkUnwrapPolyData` gibi VTK filtreleri veya özel düzleştirme algoritmaları.
-   **Sonlu Elemanlar Analizi (FEM) Entegrasyonu:**
    -   **Strateji:** Protez soketinin biyomekanik davranışını (örn: basınç noktaları, gerilme) simüle etmek için harici bir FEM çözücüsünü entegre etme.
    -   **Teknoloji:** Harici bir FEM kütüphanesi (örn: FEniCS, PyVista ile entegre), mesh'i FEM için uygun formata dönüştürme ve sonuçları geri **PolyData**'ya map etme.
-   **Çoklu Fırça Ayarları ve Basınç AI Önerileri:**
    -   **Strateji:** Farklı fırça tipleri, boyutları, sertlikleri için önceden tanımlanmış ayarlar sunma. Hasta verilerine (tarama, yaş, cinsiyet) dayanarak belirli bölgeler için yapay zeka tabanlı basınç ayarlama önerileri sunma.
    -   **Teknoloji:** Makine öğrenimi modelleri (örn: `scikit-learn`, `TensorFlow`/`PyTorch`) "Model Katmanı"nda, UI'da önerileri görüntülemek için yeni arayüz elemanları.
-   **Özel Filtreler İçin Eklenti Mekanizması:**
    -   **Strateji:** Geliştiricilerin, yazılıma kolayca yeni 3D işleme filtreleri eklemesine olanak tanıyan bir eklenti (plugin) mimarisi oluşturma.
    -   **Teknoloji:** Belirli bir arayüze (interface) uyan Python sınıflarını dinamik olarak yükleyebilen bir modül yükleyici.
-   **Web Assembly (Uzun Vadeli Taşınabilirlik):**
    -   **Strateji:** Yazılımın bir web tarayıcısı üzerinden çalışabilmesi için (uzun vadeli hedef) Web Assembly (Wasm) teknolojilerini araştırma.
    -   **Teknoloji:** Pyodide, Emscripten gibi araçlar ve VTK.js gibi web tabanlı VTK portları.
-   **Gerçek Zamanlı Biyomekanik Sezgisel Katmanlar:**
    -   **Strateji:** Modelleme sırasında, protezin potansiyel biyomekanik etkilerini (örn: kalça abduksiyon açısı, diz eklemi ekseni) gerçek zamanlı olarak gösteren görsel katmanlar (overlays) sunma.
    -   **Teknoloji:** `vtkActor`, `vtkLineSource`, `vtkTextActor` gibi VTK elemanları ve dinamik hesaplamalar.

# 26. Sözlük

| Terim | Tanım |
|---|---|
| Skaler Dizi | Renklendirme veya deplasman için kullanılan, nokta başına veri dizisi. |
| Isı Haritası | `PressureValues`'ın renkli görselleştirmesi. |
| Çarpıtma (Warp) | Skaler deplasmana dayalı geometri dönüşümü. |
| Bulucu (Locator) | En yakın/belirli yarıçap içindeki sorgular için uzamsal indeks. |
| Vuruş (Stroke) | Tek bir sürekli boyama etkileşimi. |
| Kalıp (Mold) | Fiziksel bir negatif oluşturmak için kullanılan ayarlanmış geometri. |
