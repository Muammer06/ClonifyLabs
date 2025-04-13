import cv2
import numpy as np
import glob

# Satranç tahtasının köşe sayısı (iç köşeler)
CHECKERBOARD = (6, 9)  # Örneğin 6x9, tahtaya göre ayarlayın

# Kalibrasyon kriterleri
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, 0.001)

# 3D noktaların oluşturulması (dünya koordinat sistemi)
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# 3D ve 2D noktaları saklamak için listeler
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

# Görüntü dosyalarını yükle
images = glob.glob('*.jpg')  # Tüm JPG dosyalarını alır, dosya adlarını düzenleyin
counter = 0
for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img,(int(1280),int(922)))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    # Köşeleri bul
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_NORMALIZE_IMAGE)

    # Köşeler bulunursa, noktaları ekle
    if ret == True:
        print(f"Found corners in {fname}")
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Köşeleri çiz (isteğe bağlı, görselleştirme için)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        counter += 1
    cv2.imshow('img', img)
    cv2.waitKey(100)

cv2.destroyAllWindows()

# Kalibrasyonu gerçekleştir
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Kalibrasyon sonuçlarını yazdır
print("Kamera Matrisi:\n", mtx)
print("\nBozulma Katsayıları:\n", dist)
print("\nDöndürme Vektörleri:\n", rvecs)
print("\nÖteleme Vektörleri:\n", tvecs)
#print counter and total images diffrence
print(f"Toplam {len(images)} görüntüden {counter} görüntüde köşe bulundu.")



# Kalibrasyon sonuçlarını kaydet (isteğe bağlı)
np.savez("calibration_data.npz", mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)

print("Kalibrasyon verileri calibration_data.npz dosyasına kaydedildi.")