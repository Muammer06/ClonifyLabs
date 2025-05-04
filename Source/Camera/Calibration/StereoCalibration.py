import cv2
import numpy as np
import glob
import os

# Checkerboard (satranç tahtası) boyutu (iç köşe sayısı)
CHECKERBOARD = (6, 9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 3D dünya noktaları (aynı tüm görüntüler için)
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[1], 0:CHECKERBOARD[0]].T.reshape(-1, 2)

objpoints = []        # Gerçek dünya 3D noktaları
imgpoints_left = []   # Sol kamera köşe noktaları
imgpoints_right = []  # Sağ kamera köşe noktaları

# Kameraların iç parametreleri (senin verdiğin kalibrasyon sonuçları)
mtx_left = np.array([[1378.04126035, 0, 994.64381446],
                     [0, 1377.69112834, 583.77112018],
                     [0, 0, 1]])
dist_left = np.array([[-0.37361468, 0.24661036, -0.00053245, -0.00002368, -0.15102664]])

mtx_right = np.array([[1381.39263029, 0, 948.86163087],
                      [0, 1380.98087894, 542.56696605],
                      [0, 0, 1]])
dist_right = np.array([[-0.36719888, 0.18291666, -0.00011446, -0.00009369, -0.05153168]])

# Görüntüleri oku
left_images = sorted(glob.glob("left/*.jpg"))
right_images = sorted(glob.glob("right/*.jpg"))

if len(left_images) != len(right_images):
    print("❌ Sol ve sağ görüntü sayısı eşleşmiyor.")
    exit()

print(f"{len(left_images)} çift görüntü bulundu. Köşe algılama başlıyor...")

for left_path, right_path in zip(left_images, right_images):
    img_left = cv2.imread(left_path)
    img_right = cv2.imread(right_path)
    gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

    ret_l, corners_l = cv2.findChessboardCorners(gray_left, CHECKERBOARD, None)
    ret_r, corners_r = cv2.findChessboardCorners(gray_right, CHECKERBOARD, None)

    if ret_l and ret_r:
        objpoints.append(objp)

        corners_l = cv2.cornerSubPix(gray_left, corners_l, (11,11), (-1,-1), criteria)
        corners_r = cv2.cornerSubPix(gray_right, corners_r, (11,11), (-1,-1), criteria)

        imgpoints_left.append(corners_l)
        imgpoints_right.append(corners_r)

        print(f"{os.path.basename(left_path)}: ✅ köşeler bulundu.")
    else:
        print(f"{os.path.basename(left_path)}: ❌ köşeler bulunamadı.")

print("🎯 Stereo kalibrasyon başlıyor...")

# Stereo kalibrasyon
ret, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objectPoints=objpoints,
    imagePoints1=imgpoints_left,
    imagePoints2=imgpoints_right,
    cameraMatrix1=mtx_left,
    distCoeffs1=dist_left,
    cameraMatrix2=mtx_right,
    distCoeffs2=dist_right,
    imageSize=gray_left.shape[::-1],
    criteria=criteria,
    flags=cv2.CALIB_FIX_INTRINSIC
)

print("✅ Stereo kalibrasyon tamamlandı.")
print("RMS hatası:", ret)
print("R (Rotation):\n", R)
print("T (Translation):\n", T)

# Kayıt
np.savez("stereo_params.npz",
         R=R,
         T=T,
         E=E,
         F=F,
         mtx_left=mtx_left,
         dist_left=dist_left,
         mtx_right=mtx_right,
         dist_right=dist_right)

print("💾 'stereo_params.npz' dosyasına kaydedildi.")
