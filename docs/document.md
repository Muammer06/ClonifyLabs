---
layout: default
title: Yazılım Tasarım Dokümanı
nav_order: 4
---
# Yazılım Tasarım Dokümanı: Clonify Labs

| Proje Adı | Medikal Sektörde 3 Boyutlu Tarama ile Kişiye Özel Hızlı Kalıp Üretimi |
| :--- | :--- |
| **Ürün Adı** | **Clonify Labs Modelleme Yazılımı** |
| **Versiyon** | 2.0 (Planlanan) |
| **Tarih** | 08.08.2025 |
| **Şirket** | Clonify Labs  |


---

## İçindekiler

1.  [**Giriş**](#bölüm-1-giriş)
    1.1. [Dokümanın Amacı](#11-dokümanın-amacı)
    1.2. [Projenin Kapsamı](#12-projenin-kapsamı)
    1.3. [Tanımlar ve Kısaltmalar](#13-tanımlar-ve-kısaltmalar)
2.  [**Sistem Mimarisi**](#bölüm-2-sistem-mimarisi)
    2.1. [Mimari Yaklaşım: Katmanlı Mimari](#21-mimari-yaklaşım-katmanlı-mimari)
    2.2. [Katmanların Detaylı Analizi](#22-katmanların-detaylı-analizi)
    2.3. [Mimari Şeması ve Veri Akışı](#23-mimari-şeması-ve-veri-akışı)
3.  [**Kullanılan Teknolojiler ve Kütüphaneler**](#bölüm-3-kullanılan-teknolojiler-ve-kütüphaneler)
4.  [**Ana Bileşenlerin Tasarımı ve Sorumlulukları**](#bölüm-4-ana-bileşenlerin-tasarımı-ve-sorumlulukları)
    4.1. [Kontrol Katmanı: `MainWindow`](#41-kontrol-katmanı-mainwindow)
    4.2. [Arayüz Katmanı: `ui` Modülleri](#42-arayüz-katmanı-ui-modülleri)
    4.3. [Araç Katmanı: `tools` Modülleri](#43-araç-katmanı-tools-modülleri)


---

## Bölüm 1: Giriş

### 1.1. Dokümanın Amacı
Bu dokümanın temel amacı, QClonifyCad yazılımının teknik mimarisini, tasarım kararlarını, temel bileşenlerini ve bu bileşenler arasındaki etkileşimi detaylı bir şekilde açıklamaktır. Bu belge, projenin mevcut ve gelecekteki geliştiricileri için bir referans kaynağı olarak hizmet edecek, kodun sürdürülebilirliğini ve genişletilebilirliğini sağlamak için bir yol haritası sunacaktır.

### 1.2. Projenin Kapsamı
Bu doküman, yazılımın aşağıdaki çekirdek işlevselliklerini ve planlanan modüllerini kapsar:
-   **Mevcut Özellikler:**
    -   STL formatında 3D model yükleme ve görselleştirme.
    -   Çoklu pencerede (multi-view) anatomik hizalama.
    -   2D seçimle 3D gürültü temizleme.
-   **Planlanan Özellikler:**
    -   Model yüzeyindeki deliklerin otomatik doldurulması.
    -   Etkileşimli kesit bantları ile radyal deformasyon.
    -   "Bulge/Smooth" fırçaları ile serbest form modelleme.
    -   Geri Al/İleri Al (Undo/Redo) yeteneği.

### 1.3. Tanımlar ve Kısaltmalar
-   **GUI:** Grafiksel Kullanıcı Arayüzü (Graphical User Interface)
-   **VTK:** The Visualization Toolkit
-   **STL:** Stereolithography (3D dosya formatı)
-   **PolyData:** VTK'da poligon ağını (noktalar, hücreler) temsil eden temel veri yapısı.
-   **Pipeline:** Veri akış hattı. VTK'da verinin bir dizi filtreden geçerek işlenmesi.
-   **Frustum:** Kesik piramit. 3D'de bir kamera görüş alanını tanımlayan geometrik hacim.

---

## Bölüm 2: Sistem Mimarisi

### 2.1. Mimari Yaklaşım: Katmanlı Mimari
Yazılım, kodun yönetilebilirliğini ve modülerliğini sağlamak amacıyla, görevleri net bir şekilde ayrıştıran **üç katmanlı bir mimari** üzerine inşa edilmiştir. Bu yapı, Model-View-Controller (MVC) tasarım deseninden güçlü bir şekilde ilham almıştır.

### 2.2. Katmanların Detaylı Analizi
-   **Arayüz Katmanı (View):** `PyQt5` ile oluşturulmuştur. Sadece görsel elemanları barındırır ve kullanıcı etkileşimlerini sinyallere dönüştürür. `main.py`'deki veriyi görselleştirir ancak kendi içinde mantık veya durum barındırmaz.
-   **Kontrol/Mantık Katmanı (Controller):** `main.py` dosyasındaki `MainWindow` sınıfıdır. Uygulamanın beyni olarak çalışır. Arayüzden gelen sinyalleri işler, uygulama durumunu (`state`) yönetir ve 3D Araçlar katmanına komutlar gönderir.
-   **3D Çekirdek ve Araçlar Katmanı (Model):** VTK ve `tools` klasöründeki sınıflardan oluşur. Tüm 3D veri işleme, filtreleme ve karmaşık etkileşim mantığı bu katmanda yer alır. Bu katmandaki araçlar, Kontrol Katmanı'ndan bağımsız, yeniden kullanılabilir bileşenlerdir.

---

## Bölüm 3: Kullanılan Teknolojiler ve Kütüphaneler
Projenin geliştirilmesinde, açık kaynak kodlu, endüstri standardı, yüksek performanslı ve geniş topluluk desteğine sahip teknolojiler tercih edilmiştir. Bu seçimler, projenin hem hızlı bir şekilde geliştirilmesini hem de gelecekteki bakım ve genişletme süreçlerinin verimli olmasını sağlamayı amaçlamaktadır.
### 3.1. Ana Programlama Dili: Python 3.x
Python, hızlı prototipleme yeteneği, temiz ve okunabilir sözdizimi (syntax) ve zengin standart kütüphanesi sayesinde projenin ana geliştirme dili olarak seçilmiştir. Özellikle bilimsel hesaplama, veri analizi ve yapay zeka alanlarındaki gücü, projenin medikal veri işleme doğasıyla mükemmel bir şekilde örtüşmektedir. Python'un "glue language" (yapıştırıcı dil) özelliği, C++ gibi yüksek performanslı dillerle yazılmış VTK gibi kütüphanelerin kolayca entegre edilmesini sağlamıştır.
### 3.2. Grafiksel Kullanıcı Arayüzü (GUI): PyQt5
PyQt5, platformdan bağımsız (Windows, macOS, Linux) masaüstü uygulamaları geliştirmek için kullanılan, endüstri standardı Qt C++ kütüphanesinin Python versiyonudur. 
-   **Seçim nedenleri şunlardır:**
- **Olgunluk ve Kararlılık:** Qt, yıllardır geliştirilen, son derece kararlı ve güvenilir bir arayüz çatısıdır.
-   **Sinyal ve Slot Mekanizması:** Arayüz elemanları (View) ile program mantığı (Controller) arasında esnek, güvenli ve ayrıştırılmış (decoupled) bir iletişim sağlar. Bu, mimarimizin temel taşlarından biridir.
-   **Geniş Widget Seti:** Butonlar, listeler, paneller, menüler ve QDockWidget gibi gelişmiş yerleşim araçları, karmaşık ve profesyonel bir kullanıcı arayüzünün hızlıca oluşturulmasına olanak tanır.
-   **VTK Entegrasyonu:** QVTKRenderWindowInteractor widget'ı sayesinde, VTK'nın yüksek performanslı 3D render pencerelerinin bir Qt uygulaması içine sorunsuz bir şekilde gömülmesini ve olay döngülerinin (event loop) entegre çalışmasını sağlar.

### 3.3. 3D Görselleştirme ve İşleme Motoru:** 

VTK (The Visualization Toolkit)
VTK, bilimsel ve medikal verilerin 3 boyutlu olarak işlenmesi, görselleştirilmesi ve analizi için tasarlanmış, C++ tabanlı, yüksek performanslı bir kütüphanedir. Projenin 3D ile ilgili tüm ağır işlerini VTK üstlenir.
- **Veri Akış Hattı Mimarisi (Pipeline Architecture):** VTK'nın temel gücü, `Source -> Filter -> Mapper -> Actor` şeklindeki veri akış modelidir. Bu yapı, karmaşık 3D veri işleme zincirlerinin modüler ve verimli bir şekilde oluşturulmasını sağlar. Bellek yönetimi ve güncellemeler bu pipeline üzerinden otomatik olarak yönetilir.
-    **Zengin Filtre Kütüphanesi:** Projemizde aktif olarak kullandığımız vtkClipPolyData (kesme), vtkTransformPolyDataFilter (döndürme/taşıma) ve vtkSTLReader gibi yüzlerce hazır algoritma içerir. Gelecekteki modüller için vtkFillHolesFilter, vtkSmoothPolyDataFilter gibi filtreler de kullanılacaktır.
-   **Gelişmiş Etkileşim Mekanizmaları:** vtkRenderWindowInteractor ve vtkInteractorStyle alt sınıfları, fare ve klavye ile 3D sahne üzerinde, sadece kamera kontrolü değil, aynı zamanda nesne seçimi (vtkPointPicker), alan çizimi (vtkInteractorStyleRubberBand2D) ve özel araç davranışları gibi karmaşık etkileşimler oluşturmak için güçlü bir altyapı sunar.

### 3.4. Matematiksel ve Bilimsel Hesaplama:** 

NumPy
NumPy, Python'da bilimsel hesaplamalar için temel pakettir. Özellikle çok boyutlu diziler (array) üzerinde yüksek performanslı matematiksel işlemler için kullanılır.
-   **Performans:** Vektör ve matris gibi veri yapıları üzerinde yapılan işlemler, derlenmiş C koduna yakın bir hızda gerçekleştirilir. Bu, binlerce noktadan oluşan 3D modellerin deformasyonu gibi hesaplama-yoğun işlemlerde kritik öneme sahiptir.
- **Vektör Matematiği:** Anatomik hizalama algoritmasında, normal vektörlerin ve eksenlerin hesaplanması için np.cross (çapraz çarpım) ve np.linalg.norm (vektör uzunluğu) gibi fonksiyonlar vazgeçilmezdir.
-   **VTK Uyumluluğu:** vtk.util.numpy_support modülü, NumPy dizileri ile VTK'nın kendi veri dizileri arasında sıfır-kopya (zero-copy) veya minimum-kopya ile veri alışverişi yapılmasını sağlar. Bu, on binlerce noktanın koordinatlarını Python'da işleyip tekrar VTK'ya verimli bir şekilde geri göndermemize olanak tanır.


---

## Bölüm 4: Ana Bileşenlerin Tasarımı ve Sorumlulukları

### 4.1. Kontrol Katmanı (Controller)
Uygulamanın ana pencere sınıfı bu rolü üstlenir.
-   **Sorumluluklar:**
    -   Uygulamanın genel durumunu (state) yönetmek.
    -   Arayüzden gelen sinyalleri işleyip Model katmanına komut göndermek.
    -   Model'den gelen güncellemeleri alıp arayüzün yenilenmesini sağlamak.
    -   Hangi aracın aktif olduğunu yönetmek ve kullanıcı etkileşim modlarını değiştirmek.

### 4.2. Görünüm Katmanı (View)
Tüm `PyQt` widget'ları ve pencerelerinden oluşur.
-   **Sorumluluklar:**
    -   Görsel elemanları ekranda çizmek.
    -   Kullanıcı girdilerini (tıklama, sürükleme vb.) sinyallere dönüştürmek.
    -   Controller'dan gelen veriyle 3D sahneyi ve diğer arayüz elemanlarını güncellemek.

### 4.3. Model Katmanı
Veri yapıları ve bu veriler üzerinde çalışan fonksiyon/sınıf koleksiyonlarından oluşur.
-   **Sorumluluklar:**
    -   3D geometriyi `PolyData` olarak saklamak.
    -   Controller'dan gelen komutlara göre 3D veri üzerinde algoritmik işlemler (kesme, döndürme vb.) gerçekleştirmek.
    -   İşlem sonucunda oluşan yeni veri durumunu oluşturmak.

---

## Bölüm 5: Veri Yönetimi Mimarisi

### 5.1. Ana Veri Yapısı
Uygulama içindeki tüm 3D geometrik veriler, VTK'nın `PolyData` nesnesi ile temsil edilir. Bu yapı, bir 3D modeli oluşturan noktaları, bu noktaları birleştiren poligonları ve bu geometrik elemanlara atanmış ek verileri (renk, normal vektörleri vb.) bir arada tutar.

### 5.2. Durum Yönetimi (State Management)
Uygulamanın kararlılığı ve geri alma (Undo) gibi özelliklerin çalışabilmesi için merkezi ve reaktif bir durum yönetimi benimsenmiştir. Controller, uygulamanın tüm geçmişini ve mevcut durumunu yönetir.
-   **Orijinal Veri:** Yüklenen 3D modelin değiştirilmemiş bir kopyası her zaman saklanır.
-   **Aktif Veri:** Ekranda gösterilen ve üzerinde anlık olarak çalışılan model verisi.
-   **İşlem Yığını (Undo/Redo Stack):** Kullanıcının yaptığı her geri alınabilir değişiklik, bir işlem olarak yığına eklenir. Geri alma istendiğinde, yığından son işlem çıkarılır ve önceki duruma dönülür. Bu yapı, veri tutarlılığını garanti eder.

---

## Bölüm 6: Çekirdek Fonksiyonların Mantıksal Akışı

### 6.1. Fonksiyon: Tarama Temizleme
-   **Amaç:** Kullanıcının 2D bir seçimle 3D modelin istenmeyen kısımlarını silmesi.
-   **Mantıksal Akış:**
    1.  Kullanıcı, 2D ekranda bir alan seçer.
    2.  Sistem, bu 2D alanı 3D uzayda bir seçim hacmine (frustum) dönüştürür.
    3.  Bu hacmin içinde veya dışında kalan tüm 3D geometri, modelden çıkarılır.
    4.  Modelin temizlenmiş hali, yeni "Aktif Veri" olarak ayarlanır.

### 6.2. Fonksiyon: Anatomik Hizalama
-   **Amaç:** Modeli, standart bir anatomik koordinat sistemine göre yeniden yönlendirmek.
-   **Mantıksal Akış:**
    1.  Kullanıcı, model üzerinde stratejik anatomik referans noktaları işaretler.
    2.  Sistem, bu noktalardan yola çıkarak yeni bir koordinat sistemi (yeni X, Y, Z eksenleri) hesaplar.
    3.  Modelin mevcut koordinat sisteminden bu yeni sisteme geçişini sağlayacak bir rotasyon matrisi oluşturulur.
    4.  Tüm model, bu matris kullanılarak döndürülür ve hizalanmış olur.

### 6.3. Fonksiyon: Hacimsel Deformasyon
-   **Amaç:** Modelin belirli bölgelerinde, ölçüleri hassas bir şekilde artırıp azaltmak (rektifikasyon).
-   **Mantıksal Akış:**
    1.  Kullanıcı, model üzerinde çalışmak istediği bir bölgeyi ve etki alanını tanımlar (örn: bir "kesit bandı" ile).
    2.  Sistem, bu etki alanındaki tüm 3D noktaları belirler.
    3.  Kullanıcı bir deformasyon değeri (+/- mm) girdiğinde, sistem bu bölgedeki noktaları, bölgenin merkezinden uzağa veya merkeze doğru, belirlenen miktar kadar kaydırır.
    4.  Bu kaydırma işlemi, yumuşak ve organik bir geçiş sağlamak için etki alanının kenarlarına doğru azalır.

---

## Bölüm 7: Kullanıcı Etkileşim Tasarımı

### 7.1. Modüler Etkileşim Stilleri
Uygulama, farklı görevler için farklı fare ve klavye davranışları gerektirir. Bu, monolitik bir yapı yerine, "Etkileşim Stilleri" adı verilen değiştirilebilir modüllerle yönetilir.
-   **Kamera Stili:** Varsayılan mod. Sahneyi döndürme, kaydırma.
-   **Seçim Stili:** Temizleme aracı aktifken, 2D alan seçimi yapmayı sağlar.
-   **İşaretleme Stili:** Hizalama aracı aktifken, model üzerinde 3D nokta seçmeyi sağlar.
Controller, kullanıcının seçtiği araca göre bu stiller arasında dinamik olarak geçiş yapar.

### 7.2. İletişim Desenleri
-   **Sinyal/Slot (View -> Controller):** Arayüzden gelen kullanıcı eylemlerini Controller'a bildirmek için kullanılır. Bu, arayüzün iş mantığından tamamen habersiz olmasını sağlar.
-   **Gözlemci Deseni (Model/VTK -> Controller):** 3D sahnedeki olayları (fare tıklaması vb.) yakalamak için kullanılır. Controller, 3D motorundaki olayları "dinler" ve bunlara tepki verir.

---

## Bölüm 8: Gelecek Geliştirmeler için Mimari Hazırlık
Mevcut MVC mimarisi, gelecekte eklenecek yeni özellikler için sağlam ve genişletilebilir bir temel sunmaktadır.
-   **Yapay Zeka Entegrasyonu:** Eğitilmiş bir model, "Model" katmanına yeni bir algoritma olarak kolayca eklenebilir ve Controller tarafından çağrılabilir. Örneğin, anatomik noktaları otomatik bulan bir yapay zeka modülü.
-   **Basınç Analizi (FEA):** Bir sonlu elemanlar analizi çözücüsü, yine "Model" katmanında, deforme edilmiş bir geometriyi girdi olarak alıp bir basınç haritası üreten bir fonksiyon olarak entegre edilebilir.
-   **Proje Kaydetme/Yükleme:** Controller, "Durum Yönetimi" bölümünde tanımlanan tüm durumu (aktif veri, bant parametreleri vb.) tek bir dosyaya serileştirip (serialize) daha sonra bu dosyadan durumu geri yükleyebilir. Mimari bu özelliğe tamamen hazırdır.

## 9. Modifikasyon Araçları Mimarisi (Rectification Tools Architecture)
Bu bölüm, protez soketinin dijital olarak şekillendirildiği, klinik olarak en önemli adımları içeren araç setinin mimarisini tanımlar. Bu araçlar, kullanıcının adım adım ilerlediği bir iş akışı (`workflow`) içinde sunulur. Tüm modifikasyon araçları, merkezi bir `ModificationEngine` tarafından yönetilir ve aynı temel prensipleri paylaşır:
-   **Tahribatsız İşlem:** Tüm modifikasyonlar, `active_poly_data` üzerinde yapılır ve `HistoryStack`'e kaydedilir.
-   **Merkezi Kontrol:** `MainWindow` (Controller), hangi aracın aktif olduğunu, aracın parametrelerini (fırça boyutu, azaltma yüzdesi vb.) ve Arayüz ile Araçlar (Model) katmanı arasındaki veri akışını yönetir.
-   **Modüler Araç Tasarımı:** Her bir modifikasyon aracı (`Réduction`, `Lissage` vb.), `tools` klasöründe kendi sınıfına sahip olacak şekilde tasarlanacaktır.

---

### 9.1. Araç 1: Réduction (Hacim Azaltma)

-   **Amaç:** Protez soketinin genel hacmini küçülterek veya belirli bölgelerde lokal baskı oluşturarak daha sıkı bir uyum (fit) sağlamak.
-   **Arayüz Bileşenleri (View):**
    -   "Global Azaltma" ve "Lokal Azaltma" modlarını seçmek için `QRadioButton` veya `QPushButton` grubu.
    -   Global azaltma için yüzde (%) değerinin girileceği bir `QSlider` veya `QSpinBox`.
    -   Lokal azaltma için fırça boyutunu ve etki gücünü ayarlayan `QSlider`'lar.
-   **Kontrol Mantığı (`MainWindow`):**
    -   `current_mode`'u `'REDUCTION_GLOBAL'` veya `'REDUCTION_LOCAL'` olarak ayarlar.
    -   Slider'lardan gelen yüzde veya fırça parametrelerini yakalar.
    -   Global modda "Uygula" butonuna basıldığında veya lokal modda fare sürüklenirken `ReductionTool` üzerindeki ilgili metotları çağırır.
-   **Araç Tasarımı (`tools/ReductionTool.py`):**
    ```python
    class ReductionTool:
        def apply_global_reduction(self, poly_data, percentage):
            # 1. Modelin ağırlık merkezini (centroid) hesapla.
            # 2. 'vtkTransform' kullanarak modeli merkeze doğru 'percentage' oranında ölçekle.
            # 3. Değiştirilmiş poly_data'yı geri döndür.
            ...

        def apply_local_reduction(self, poly_data, brush_center, radius, strength):
            # 1. Fırça merkezine 'radius' mesafesindeki noktaları (vertices) bul.
            # 2. Her bir nokta için, kendi normal vektörü yönünde içeri doğru hareket ettir.
            # 3. Hareket mesafesi, 'strength' ve merkeze olan uzaklığa göre (falloff) belirlenir.
            ...
    ```

---

### 9.2. Araç 2: Creuser / Recharger (Oyma / Ekleme - Sculpting)

-   **Amaç:** Serbest formda, hassas bölgelerdeki (örn: kemik çıkıntıları) basıncı azaltmak için materyal oymak (Creuser) veya zayıf doku alanlarını desteklemek için materyal eklemek (Recharger).
-   **Arayüz Bileşenleri (View):**
    -   "Oy" (Dig) ve "Ekle" (Bulge) modları arasında geçiş yapan butonlar.
    -   Fırça Boyutu ve Etki Gücü için `QSlider`'lar.
    -   Fare imlecinin model üzerindeki izdüşümünü gösteren anlık bir fırça göstergesi.
-   **Kontrol Mantığı (`MainWindow`):**
    -   Aktif fırça modunu (`'DIG'` veya `'BULGE'`) ve fırça parametrelerini `SculptingTool`'a iletir.
    -   Fare model üzerinde sürüklendiği sürece, `mouseMoveEvent` olayından elde edilen 3D koordinatları anlık olarak `SculptingTool`'a gönderir.
-   **Araç Tasarımı (`tools/SculptingTool.py`):**
    ```python
    class SculptingTool:
        def deform(self, poly_data, brush_center, radius, strength, mode):
            # 1. Fırça etki alanındaki noktaları bul.
            # 2. Her nokta için, normal vektörünü al.
            # 3. if mode == 'BULGE': Noktayı normal yönünde dışarı taşı.
            # 4. if mode == 'DIG': Noktayı normal yönünde içeri taşı.
            # 5. Taşıma miktarını 'strength' ve yumuşak bir geçiş için 'falloff' fonksiyonu ile ayarla.
            ...
    ```

---

### 9.3. Araç 3: Lissage (Yumuşatma)

-   **Amaç:** Önceki adımlarda oluşan pürüzlü veya keskin yüzeyleri yumuşatarak daha pürüzsüz ve konforlu bir iç yüzey elde etmek.
-   **Arayüz Bileşenleri (View):** Fırça Boyutu ve Yumuşatma Miktarı için `QSlider`'lar.
-   **Kontrol Mantığı (`MainWindow`):** `SculptingTool`'a benzer şekilde, fare hareketlerini `SmoothingTool`'a yönlendirir.
-   **Araç Tasarımı (`tools/SmoothingTool.py`):**
    ```python
    class SmoothingTool:
        def __init__(self):
            # VTK'nın yerleşik yumuşatma filtresi kullanılır.
            self.smoother = vtk.vtkSmoothPolyDataFilter()
        
        def smooth_area(self, poly_data, brush_center, radius, iterations):
            # 1. Fırça alanındaki noktaları belirle.
            # 2. Yalnızca bu noktaları etkileyecek şekilde 'vtkSmoothPolyDataFilter'ı çalıştır.
            # 3. 'iterations' (döngü sayısı), arayüzdeki yumuşatma miktarına bağlanır.
            ...
    ```
---
# Protez Soketi Modifikasyon Araçları

## Épaisseur (Kalınlık)
**Amaç:**  
Protez soketinin üretim için gerekli olan duvar kalınlığını ayarlamak. Genellikle tüm sokete tek tip bir kalınlık uygulanır.

**Teknoloji:**  
- `vtkPolyDataNormals` ile normal vektörleri hesaplanır.  
- Noktalar, normal yönleri boyunca belirli bir mesafede kaydırılarak yeni bir dış yüzey oluşturulur.  
- `vtkBooleanOperationPolyDataFilter` ile iç ve dış yüzey birleştirilebilir.

---

## Évasés (Kenar Şekillendirme / Flare)
**Amaç:**  
Protez soketinin üst kenarlarını, hastanın uzvuna daha iyi oturacak ve kenar tahrişini önleyecek şekilde içeri veya dışarı doğru şekillendirmek.  
Görüntüdeki renk çarkı, bölgesel kontrolün önemini vurgular.

**Teknoloji:**  
- Soketin üst kenarındaki poligon halkaları (edge loops) seçilir.  
- Bu halkaların noktaları, yüzey normali veya kenar normali boyunca, bölgesel olarak belirlenen miktarlarda hareket ettirilir.  
- Geçişleri yumuşatmak için `vtkSmoothPolyDataFilter` veya özel deformasyon algoritmaları kullanılabilir.

---

## Prise Distale (Distal Tutuş / Arayüz)
**Amaç:**  
Ampute uzvun distal ucu ile protez soketi arasındaki bağlantı noktasını şekillendirmek ve buraya uygun bağlantı elemanlarını (adaptör, kilit mekanizması) dijital olarak yerleştirmek.

**Teknoloji:**  
- Distal uç bölgesinde özel bir deformasyon ve/veya kesme işlemi yapılır.  
- Kullanıcı, STL formatında önceden yüklenmiş distal bağlantı elemanı modellerinden birini seçebilir ve bunu soketin distal ucuna yerleştirebilir.  
- Konumlandırma ve yönlendirme için `vtkTransformWidget` gibi manipülatörler kullanılır.

---

## Alignement (Hizalama)
**Amaç:**  
Protez soketinin, tüm protez sisteminin (diz eklemi, ayak, pelvik bölge) anatomik ve biyomekanik olarak doğru hizalanmasını sağlamak.

**Teknoloji:**  
- `vtkAssembly` veya `vtkProp` ile sanal bir hizalama standı oluşturulur.  
- Soket, diz eklemi ve ayak gibi bileşenler bu stand üzerinde konumlandırılır.  
- Kullanıcı, rotasyon (ön-arka, iç-dış) ve translasyon (yükseklik, yanlara kaydırma) ayarlamaları yapabilir.  
- `vtkTransform` ve `vtkMatrix4x4` bu dönüşümleri yönetir.

---

## Finalisation (Sonlandırma)
**Amaç:**  
Tüm modelleme ve rektifikasyon adımları tamamlandıktan sonra, protez kalıbını üretime hazır hale getirmek ve çıktı almak.

**Teknoloji:**
- **Model Doğrulama:** Son `vtkPolyData` üzerinde topolojik kontroller (delik kontrolü, kesişen üçgenler).  
- **Dışa Aktarma:** `vtkSTLWriter` ile nihai model STL formatında kaydedilir.  
- 