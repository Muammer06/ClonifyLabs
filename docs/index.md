---
layout: home
title: Ana Sayfa
nav_order: 1
---

# ClonifyLabs

ClonifyLabs, yüksek hassasiyetli 3B tarama çözümleri sunan açık kaynaklı bir projedir.

## Dokümantasyon

- [Yazılım Gereksinimleri Belirtimi (SRD)](srd.html)
- [Diyagram Örnekleri](diagram-example.html)

## Özellikler

- Stereo kamera desteği
- Yapılandırılmış ışık tarama
- Marker tabanlı konum tespiti
- Açık kaynak SDK
- Çoklu çıktı formatları (STL, OBJ, PLY)

## Başlarken

Projeyi yerel makinenizde çalıştırmak için [GitHub reposunu](https://github.com/yourusername/ClonifyLabs) ziyaret edin.

# ClonifyLabs 3D Tarama Cihazı

![Versiyon](https://img.shields.io/badge/version-0.1.0-blue)
![Lisans](https://img.shields.io/badge/license-MIT-green)

3B Tarama Cihazı, yüksek çözünürlüklü ve hassas 3D tarama yapabilen açık kaynak kodlu bir donanım-yazılım bütünüdür. Lazer tabanlı yapılandırılmış ışık, stereo kamera veya bu iki yaklaşımın birleşimi gibi farklı tarama yöntemlerini destekler.

## Özellikler

- 📷 **Çoklu Tarama Yöntemleri**: 
  - Stereo kamera ile derinlik algılama
  - Lazer tabanlı yapılandırılmış ışık desenleriyle yüzey analizi
  - İki yöntemin birleşimi ile yüksek hassasiyet

- 🔍 **Marker Tabanlı Konumlandırma**: 
  - PnP algoritması ile kamera pozisyonunun doğru tespiti
  - Gerçek zamanlı konum takibi

- 💾 **Çeşitli Çıktı Formatları**:
  - STL, OBJ ve PLY formatlarında 3D model dışa aktarımı

- 🧪 **Algoritma Test Arayüzü**:
  - Farklı işleme algoritmalarının etkisini karşılaştırma
  - Önce/sonra sonuçlarını görsel olarak inceleme

## Kurulum

### Gereksinimler

- Ubuntu 22.04 LTS işletim sistemi
- Intel i7 veya üzeri işlemci (önerilen)
- En az 32GB RAM
- USB 3.0 portları
- Uyumlu kameralar (e-con Systems IMX900 önerilir)

### Yazılım Kurulumu

```bash
# Gerekli bağımlılıkları kur
sudo apt update
sudo apt install -y build-essential cmake git python3-dev python3-pip

# OpenCV ve PCL kütüphanelerini kur
sudo apt install -y libopencv-dev python3-opencv
sudo apt install -y libpcl-dev

# Depoyu klonla
git clone https://github.com/yourusername/ClonifyLabs.git
cd ClonifyLabs

# Bağımlılıkları kur
pip3 install -r requirements.txt

# Derleme
mkdir build && cd build
cmake ..
make -j4

# Çalıştır
./bin/clonify_scanner
```

## Kullanım

1. Kameraların doğru bağlandığından emin olun
2. Kalibrasyon dosyasını yükleyin veya yeni kalibrasyon yapın
3. Tarama modunu seçin (Stereo, Structured Light, veya Hibrit)
4. İşaretçileri (marker) görüş alanına yerleştirin
5. Taramak istediğiniz nesneyi konumlandırın
6. Tarama işlemini başlatın
7. 3D modeli istediğiniz formatta dışa aktarın

## Belgelendirme

Detaylı teknik belgelendirme için [Yazılım Gereksinimleri Belirtimi](docs/SRD.md) dokümanına bakabilirsiniz.

## Katkıda Bulunma

Projeye katkıda bulunmak isteyenler için aşağıdaki adımları takip edin:

1. Bu depoyu forklayın
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inize push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında dağıtılmaktadır. Detaylı bilgi için `LICENSE` dosyasına bakın.

## İletişim

Ahmet Furkan KARAARSLAN - [karaarslan@example.com](mailto:karaarslan@example.com)

Proje Bağlantısı: [https://github.com/yourusername/ClonifyLabs](https://github.com/yourusername/ClonifyLabs)
