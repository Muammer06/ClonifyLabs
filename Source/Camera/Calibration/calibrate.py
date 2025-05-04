import cv2
import numpy as np
import os
import glob

# Kalibrasyon tahtası boyutları (köşe sayısı)
CHECKERBOARD = (6, 9)  # (iç köşe genişliği, iç köşe yüksekliği)

# Kare boyutu (isteğe bağlı, gerçek dünya birimi cinsinden, örneğin mm)
# Bu, dışsal parametrelerin (rotasyon, translasyon) ölçeğini belirler.
# Eğer sadece içsel parametrelerle ilgileniyorsanız, 1.0 olarak bırakabilirsiniz.
SQUARE_SIZE = 1.0

# Kriterler (köşe bulma hassasiyeti için)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D noktaları (nesne noktaları) hazırlama (0,0,0), (1,0,0), (2,0,0) ..., (CHECKERBOARD[0]-1, CHECKERBOARD[1]-1, 0)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
objp = objp * SQUARE_SIZE # Kare boyutuna göre ölçekle

# Tüm görüntülerden nesne noktaları ve görüntü noktalarını saklamak için diziler
objpoints = []  # 3D nokta (dünya koordinat sistemi)
imgpoints = []  # 2D nokta (görüntü düzlemi)

# Görüntülerin bulunduğu klasör
images_folder = './right' # Bu klasörün var olduğundan ve içinde kalibrasyon görüntülerinin bulunduğundan emin olun
if not os.path.exists(images_folder):
    print(f"Hata: '{images_folder}' klasörü bulunamadı. Lütfen oluşturun ve kalibrasyon görüntülerini içine kopyalayın.")
    exit()

images = glob.glob(os.path.join(images_folder, '*.jpg')) # veya .png, .jpeg vb.

if not images:
    print(f"Hata: '{images_folder}' klasöründe '.jpg' uzantılı görüntü bulunamadı.")
    exit()

print(f"{len(images)} adet görüntü bulundu. Kalibrasyon başlıyor...")

gray = None # Gri tonlamalı görüntünün boyutunu almak için kullanılacak

for fname in images:
    img = cv2.imread(fname)
    if img is None:
        print(f"Uyarı: {fname} yüklenemedi.")
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Dama tahtası köşelerini bul
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

    # Köşeler bulunduysa, nesne noktalarını ve görüntü noktalarını ekle (hassasiyeti artırdıktan sonra)
    if ret == True:
        print(f"{fname}: Köşeler bulundu.")
        objpoints.append(objp)

        # Köşe konumlarını alt piksel hassasiyetinde iyileştir
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # İsteğe bağlı: Köşeleri çiz ve göster
        # cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        # cv2.imshow('img', img)
        # cv2.waitKey(500) # 0.5 saniye bekle
    else:
        print(f"{fname}: Köşeler bulunamadı.")

# cv2.destroyAllWindows()

if not objpoints or not imgpoints:
    print("Hata: Hiçbir görüntüde geçerli köşe bulunamadı. Kalibrasyon yapılamıyor.")
    exit()

if gray is None:
     print("Hata: Geçerli bir görüntü işlenemedi.")
     exit()

print("Kalibrasyon hesaplanıyor...")
# Kamera kalibrasyonunu gerçekleştir
# ret: RMS yeniden projeksiyon hatası
# mtx: Kamera matrisi (içsel parametreler)
# dist: Distorsiyon katsayıları
# rvecs: Rotasyon vektörleri (her görüntü için dışsal parametreler)
# tvecs: Translasyon vektörleri (her görüntü için dışsal parametreler)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

if ret:
    print("Kalibrasyon Başarılı!")
    print("-----------------------------------------------------")
    print("Kamera Matrisi (Intrinsic Matrix):")
    print(mtx)
    print("fx (x ekseni odak uzaklığı):", mtx[0, 0])
    print("fy (y ekseni odak uzaklığı):", mtx[1, 1])
    print("cx (optik merkez x koordinatı):", mtx[0, 2])
    print("cy (optik merkez y koordinatı):", mtx[1, 2])
    print("-----------------------------------------------------")
    print("Distorsiyon Katsayıları (k1, k2, p1, p2, k3):")
    print(dist)
    print("-----------------------------------------------------")
    print(f"Ortalama Yeniden Projeksiyon Hatası (RMS): {ret}")
    print("(Bu değerin mümkün olduğunca düşük olması istenir, ideal olarak 1.0'ın altında)")
    print("-----------------------------------------------------")

    # Kalibrasyon sonuçlarını kaydetme (isteğe bağlı)
    # np.savez('calibration_data.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
    # print("\nKalibrasyon verileri 'calibration_data.npz' dosyasına kaydedildi.")

    # Tüm kalibrasyon görüntülerinin distorsiyonunu düzeltme ve karşılaştırma için kaydetme
    output_folder = "calibration_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    print(f"\nKarşılaştırma görüntüleri '{output_folder}' klasörüne kaydediliyor...")

    for i, fname in enumerate(images):
        img_original = cv2.imread(fname)
        if img_original is not None:
            h, w = img_original.shape[:2]
            # Kırpma olmadan doğrudan düzeltme
            dst = cv2.undistort(img_original, mtx, dist, None, mtx)

            # Görüntüleri yan yana birleştirme
            comparison_image = np.hstack((img_original, dst))

            # Dosya adlarını oluşturma (orijinal adı kullanarak)
            base_filename = os.path.splitext(os.path.basename(fname))[0]
            original_path = os.path.join(output_folder, f"{base_filename}_original.png")
            undistorted_path = os.path.join(output_folder, f"{base_filename}_undistorted.png")
            comparison_path = os.path.join(output_folder, f"{base_filename}_comparison.png")

            # Karşılaştırma için görüntüleri kaydet
            try:
                cv2.imwrite(original_path, img_original)
                cv2.imwrite(undistorted_path, dst)
                cv2.imwrite(comparison_path, comparison_image)
                print(f"- {base_filename}: Orijinal, Düzeltilmiş ve Karşılaştırma kaydedildi.")
            except Exception as e:
                 print(f"Hata: {base_filename} için görüntüler kaydedilemedi: {e}")

        else:
            print(f"Uyarı: Karşılaştırma için {fname} yüklenemedi.")

else:
    print("\nKalibrasyon Başarısız!")