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
5.  [**Veri Yönetimi Mimarisi**](#bölüm-5-veri-yönetimi-mimarisi)
    5.1. [Ana Veri Yapıları: `vtkPolyData`](#51-ana-veri-yapıları-vtkpolydata)
    5.2. [Durum Yönetimi (State Management)](#52-durum-yönetimi-state-management)
6.  [**Çekirdek Fonksiyonların Algoritmik Detayları**](#bölüm-6-çekirdek-fonksiyonların-algoritmik-detayları)
    6.1. [Modül: Tarama Temizleme (`CutTool`)](#61-modül-tarama-temizleme-cuttool)
    6.2. [Modül: Anatomik Hizalama](#62-modül-anatomik-hizalama)
    6.3. [Modül: Kesit Bantları ile Deformasyon (Planlanan)](#63-modül-kesit-bantları-ile-deformasyon-planlanan)
7.  [**Kullanıcı Etkileşim Tasarımı**](#bölüm-7-kullanıcı-etkileşim-tasarımı)
    7.1. [Etkileşim Stilleri (Interactor Styles)](#71-etkileşim-stilleri-interactor-styles)
    7.2. [Sinyal/Slot ve Gözlemci (Observer) Mekanizmaları](#72-sinyalslot-ve-gözlemci-observer-mekanizmaları)
8.  [**Gelecek Geliştirmeler için Mimari Hazırlık**](#bölüm-8-gelecek-geliştirmeler-için-mimari-hazırlık)

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

### 2.3. Mimari Şeması ve Veri Akışı

```mermaid
graph TD
    subgraph Arayüz Katmanı (UI Layer - PyQt5)
        A[Kullanıcı Etkileşimi] --> B(Arayüz Bileşenleri);
        B -- Sinyal Gönderir (Signal) --> C;
    end
    subgraph Kontrol & Mantık Katmanı (Controller - main.py)
        C(Olay Yönetim Fonksiyonları) --> D{Durum Yönetimi};
        C --> E(Algoritmalar);
    end
    subgraph 3D Çekirdek & Araçlar (Model - VTK)
        F(VTK Pipeline) --> G((3D Sahne));
        E -- Komut Gönderir --> H(Araç Sınıfları);
        H -- Sonuç Bildirir (Callback) --> C;
        E -- Veriyi Günceller --> F;
    end
```

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

### 4.1. Kontrol Katmanı: `MainWindow` (`main.py`)
Uygulamanın ana orkestrasyon merkezidir.
-   **Sorumlulukları:**
    -   Ana pencereyi ve alt arayüz bileşenlerini (`DockWidget`'lar) oluşturmak.
    -   VTK'nın temel bileşenlerini (`renderer`, `interactor`) başlatmak.
    -   Tüm uygulama durumunu yönetmek (bkz. Bölüm 5.2).
    -   Arayüzden gelen sinyalleri (`align_requested`, `toggled` vb.) ilgili fonksiyonlara bağlamak.
    -   `CutTool` gibi araçları doğru zamanda, doğru veriyle başlatmak ve bu araçlardan gelen sonuçları işlemek.

### 4.2. Arayüz Katmanı: `ui` Modülleri
-   **`section_panel.py`:** Kesit bantlarının listesini ve bu bantların parametrelerini (yüzde, yükseklik) kontrol eden arayüzü barındırır. Sadece `main.py`'e sinyal gönderir.
-   **`alignment_widget.py`:** Anatomik hizalama için gereken 3'lü görüntüleme pencerelerini ve referans noktası seçme butonlarını içerir.

### 4.3. Araç Katmanı: `tools` Modülleri
-   **`cut_tool.py`:** "Tarama Temizleme" özelliğinin mantığını içerir. Kendi özel etkileşim stili olan `CutInteractorStyle`'ı yönetir.
-   **`section_tool.py` (Planlanan):** Etkileşimli kesit bandı aracının temelini oluşturacak olan görünmez `vtkImplicitPlaneWidget2`'yi yönetir.

---

## Bölüm 5: Veri Yönetimi Mimarisi

### 5.1. Ana Veri Yapıları: `vtkPolyData`
Yazılımdaki tüm 3D geometrik veriler, VTK'nın standart `vtkPolyData` nesnesi içinde saklanır. Veri bütünlüğünü sağlamak için iki ana `vtkPolyData` nesnesi kullanılır:
-   `self.original_polydata`: STL dosyasından ilk yüklendiği andaki temiz ve bozulmamış veriyi tutar. Bu nesne, hizalama gibi kalıcı bir işlem yapılmadığı sürece **asla değiştirilmez**.
-   `self.deformed_polydata`: O anda ekranda gösterilmesi gereken, üzerinde tüm deformasyonların ve modifikasyonların uygulandığı veriyi tutar.

Bu ayrım, veri akışını tek yönlü ve yönetilebilir kılar.
```mermaid
graph LR
    A[<b>original_polydata</b><br/>(Değişmez, Temiz Veri)] -- Her Deformasyon Başlangıcında Kopyalanır --> B{<b>apply_all_deformations()</b><br/>(Algoritma)};
    B -- Hesaplama Sonucu --> C[<b>deformed_polydata</b><br/>(Geçici, Değişken Veri)];
    C -- Her Karede Renklendirilir --> D{<b>update_band_colors()</b><br/>(Görselleştirme)};
    D --> E((<b>Ekranda Görünen Model</b><br/>(vtkActor)));
```

### 5.2. Durum Yönetimi (State Management)
Uygulamanın o anki durumunu yönetmek için `MainWindow` içinde çeşitli değişkenler kullanılır:
-   `self.sections_data`: Sahnedeki her bir kesit bandının tüm bilgilerini (tool nesnesi, yüzde, yükseklik, renk) tutan bir Python listesi.
-   `self.active_tool`: O anda hangi aracın (`'cut'`, `'pick'`, `'none'`) aktif olduğunu belirten bir string. Bu, fare etkileşim stilleri arasında doğru geçiş yapılmasını sağlar.

---
### Bölüm 6: Çekirdek Fonksiyonların Algoritmik Detayları

#### 6.1. Modül: Tarama Temizleme (`CutTool`)
- **Algoritma:** `vtkClipPolyData` ile Gerçek 3D Kesim.
- **Akış:**
  1.  `CutInteractorStyle`, kullanıcının 2D ekran üzerinde çizdiği kutunun piksel koordinatlarını yakalar.
  2.  `perform_cut` fonksiyonu, `vtkCamera`'nın o anki durumunu kullanarak bu 2D kutuyu bir 3D kesim hacmine (frustum) dönüştürür.
  3.  `vtkClipPolyData` filtresi, bu 3D hacmin **içinde kalan** geometriyi korur, dışındakileri siler. Bu, modelin arkasının da doğru kesilmesini sağlar.
  4.  İşlem, `QTimer.singleShot` ile bir sonraki olay döngüsüne ertelenerek VTK-PyQt çökme riski ortadan kaldırılır.

#### 6.2. Modül: Anatomik Hizalama
- **Algoritma:** Koordinat Sistemi Dönüşümü.
- **Akış:**
  1.  Kullanıcı iki 3D referans noktası (`P_tip`, `P_apex`) seçer.
  2.  Vektör matematiği (`normalize`, `np.cross`) kullanılarak bu iki noktadan yeni bir ortonormal koordinat sistemi (yeni X, Y, Z eksenleri) oluşturulur.
  3.  Bu yeni eksenlerden bir 4x4 dönüşüm matrisi (`vtkMatrix4x4`) oluşturulur.
  4.  `vtkTransform` ile model önce `P_tip` noktası orijine gelecek şekilde taşınır, ardından dönüşüm matrisinin tersi (`Inverse`) ile döndürülür.
  5.  `vtkTransformPolyDataFilter`, bu nihai dönüşümü modele uygular.

#### 6.3. Modül: Kesit Bantları ile Deformasyon (Planlanan)
- **Algoritma:** Yönelimden Bağımsız Vertex Boyama ve Radyal Deformasyon.
- **Akış:**
  1.  **Görselleştirme (`update_band_colors`):**
      -   Tüm model noktaları varsayılan renge boyanır.
      -   Her bir bant için, tüm model noktaları tekrar taranır.
      -   Bir noktanın, bandın düzlemine olan **dik mesafesi** `vtk.vtkPlane.Evaluate()` ile hesaplanır.
      -   Eğer bu mesafe bandın yarı-yüksekliğinden küçükse, o noktanın rengi bandın rengiyle güncellenir.
  2.  **Deformasyon (`apply_all_deformations`):**
      -   Tüm bantlar, ana eksen (genellikle ilk bandın normali) üzerindeki izdüşümlerine göre sıralanır.
      -   Her bir model noktası için, hangi iki bant arasında kaldığı ve bu bantlara olan göreceli uzaklığı (ağırlık) hesaplanır.
      -   Bu ağırlık kullanılarak, iki bandın yüzde değerleri arasında **lineer interpolasyon** yapılır ve noktaya etki edecek nihai deformasyon yüzdesi bulunur.
      -   Nokta, modelin merkezi eksenine göre **radyal bir vektör** boyunca, bu nihai yüzdeye göre ötelenir.

---
### Bölüm 7: Kullanıcı Etkileşim Tasarımı
### 7.1. Etkileşim Stilleri (Interactor Styles)**

Yazılım, kullanıcının o anda hangi aracı kullandığına bağlı olarak fare davranışını değiştiren bir durum makinesi (state machine) mantığı kullanır. Bu, VTK'nın vtkInteractorStyle mekanizması üzerine kurulmuştur. Çökmeleri engellemek için, programın başında ihtiyaç duyulan tüm stiller kalıcı olarak oluşturulur ve modlar arasında bu kalıcı nesneler arasında geçiş yapılır.
-   **vtkInteractorStyleTrackballCamera (Varsayılan Mod):** Standart 3D kamera kontrollerini (döndürme, taşıma, yakınlaştırma) sağlar.
CutInteractorStyle (Kesme Modu): vtkInteractorStyleRubberBand2D'den türetilmiştir. Kamera kontrollerini devre dışı bırakır ve kullanıcının ekrana 2D bir seçim kutusu çizmesine olanak tanır.
-   **PointPickerInteractorStyle (Nokta Seçim Modu):** Sadece sol tıklama olayını dinler ve tıklanan noktayı ana programa bildirir. Diğer tüm kamera etkileşimlerini engeller.
### 7.2. Sinyal/Slot ve Gözlemci (Observer) Mekanizmaları
Yazılımın katmanları arasındaki iletişim iki temel mekanizma ile sağlanır:
PyQt Sinyal/Slot: Arayüz (ui) ve Kontrol (main.py) katmanları arasındaki iletişim için kullanılır. Örneğin, SectionPanel'deki bir buton tıklandığında add_section_requested sinyali yayılır. MainWindow bu sinyali add_new_section isimli slot'una (fonksiyonuna) bağlamıştır. Bu, arayüzün mantıktan tamamen habersiz olmasını sağlar.
-   **VTK Gözlemci/Komut (Observer/Command):** 3D Çekirdek (VTK) ve Kontrol (main.py) katmanları arasındaki iletişim için kullanılır. Örneğin, CutInteractorStyle bir LeftButtonReleaseEvent yakaladığında, bu olayı bir "gözlemci" aracılığıyla MainWindow'daki perform_cut fonksiyonuna bildirir. Bu, 3D dünyasında olan bir olayın, ana program mantığını tetiklemesini sağlar.
Bu iki mekanizmanın bir arada kullanılması, karmaşık etkileşimlerin yönetildiği sağlam ve modüler bir mimari oluşturur.



### Bölüm 8: Gelecek Geliştirmeler için Mimari Hazırlık
Mevcut mimari, gelecekte eklenecek yeni özellikler için sağlam bir temel sunmaktadır.
### 8.1. Yapay Zeka Entegrasyonu
-   **Otomatik Hizalama:** Kullanıcının manuel olarak işaretlediği anatomik noktalar (olecranon tip, apex vb.) üzerinde eğitilmiş bir Konvolüsyonel Sinir Ağı (CNN) modeli, gelecekte bu noktaları 3D model üzerinde otomatik olarak tespit edebilir.
-   **Optimum Baskı Parametreleri:** Bir makine öğrenmesi modeli, belirli bir geometri için en uygun 3D baskı parametrelerini (katman kalınlığı, dolgu oranı vb.) otomatik olarak önerebilir.
### 8.2. Sonlu Elemanlar Analizi (FEA) ile Basınç Haritalama
Amaç: Tasarlanan soketin, hastanın güdüğüne uygulayacağı basınçları simüle etmek.
-   **Mimari Entegrasyonu:**
-  Deforme edilmiş deformed_polydata nesnesi, FEniCS gibi bir Python tabanlı FEA kütüphanesine girdi olarak verilir.
-   FEA çözücüsü, modelin yüzeyindeki her bir nokta için bir basınç (stres) değeri hesaplar.
-   Bu basınç değerleri, vtkPolyData'ya bir "scalar" dizisi olarak eklenir ve model üzerinde bir renk haritasıyla görselleştirilir.
### 8.3. Geri Al/İleri Al (Undo/Redo) Mekanizması
-   **Mimari Entegrasyonu:** "Komut (Command)" tasarım deseni uygulanacaktır. Her geri alınabilir işlem (bant taşıma, kesme vb.), execute() ve unexecute() metotlarına sahip ayrı bir sınıf olarak tasarlanacaktır. MainWindow, bir undo_stack ve redo_stack tutarak bu komut nesnelerini yönetecektir.
### 8.4. Proje Kaydetme ve Yükleme
-   **Mimari Entegrasyonu:** MainWindow'daki tüm durum (state) bilgisi (orijinal STL dosyasının yolu, sections_data listesindeki her bandın tüm parametreleri vb.) tek bir Python sözlüğüne toplanacaktır. Python'un json kütüphanesi, bu sözlüğü insan tarafından okunabilir bir metin dosyasına (.qcad_proj) yazmak için kullanılacaktır.


## Bölüm 9: Modül Bazlı Teknik Açıklamalar

### 9.1.  Hazırlık ve Veri Yönetimi (Correct Scan)
**Amaç:** Ham 3D taramayı temiz, işlenebilir bir dijital modele dönüştürmek.  
**Araçlar ve Teknik Karşılıklar:**
- **Çoklu Tarama Yönetimi:** Hasta bazlı klasör yapısı + metadata (JSON)  
- **Tarama Temizleme:** `vtkClipPolyData` + kamera frustum hacmi  
- **Delik Doldurma:** `vtkFillHolesFilter`  
- **Distal Kilit Konumlandırma:** `vtkPointPicker` ile 3D nokta seçimi

---

### 9.2.  Anatomik Hizalama (Define Axes)
**Amaç:** Modeli standart referans eksenlerine oturtmak.  
**Araçlar ve Teknik Karşılıklar:**
- **Çoklu Pencere ile Referans Noktası Belirleme:** Posterior/Sagittal/Transversal görünümler  
- **Otomatik Eksen Oluşturma:** `perform_alignment`, vektör matematiği, `vtkTransformPolyDataFilter`  
- **Karşılaştırma:** Birden fazla `vtkActor` + `SetOpacity(0.5)`

---

### 9.3. Modifikasyon
**Amaç:** Model üzerinde lokal ve global değişiklikler yapmak.  
**Araçlar ve Teknik Karşılıklar:**
- **Global Deformasyon:** `apply_all_deformations` → tüm modeli tek oranda ölçekleme  
- **Bölgesel Deformasyon:** `vtkImplicitPlaneWidget2` + vertex boyama  
- **Serbest Form Modelleme:** `vtkPointPicker` + `vtkSmoothPolyDataFilter`  
- **Bölgesel Kilitleme:** Vertex ağırlık sistemi (weight=0 → etkilenmez)  
- **Soket Kenarı Tasarımı:** `vtkSplineWidget` / `vtkContourWidget` + `vtkClipPolyData`

---

### 9.4.  Üretim ve Son Kontrol
**Amaç:** Üretime hazır nihai soket modelini oluşturmak.  
**Araçlar ve Teknik Karşılıklar:**
- **Soket Oluşturma:** `vtkLinearExtrusionFilter` ile kalınlık verme  
- **Otomatik Kenar Yuvarlatma:** `vtkWindowedSincPolyDataFilter` ile yumuşatma  
- **Dışa Aktarma:** `vtkSTLWriter` + `reportlab` ile PDF rapor