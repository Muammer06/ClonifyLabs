import cv2
import numpy as np

# Kamera ayarları
width = 1920
height = 1080
cam_left_idx = 4
cam_right_idx = 6

# Kameraları aç
cam_left = cv2.VideoCapture(cam_left_idx)
cam_right = cv2.VideoCapture(cam_right_idx)

cam_left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('G', 'R', 'E', 'Y'))
cam_right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('G', 'R', 'E', 'Y'))
cam_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam_left.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam_right.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam_left.set(cv2.CAP_PROP_EXPOSURE, 75)
cam_right.set(cv2.CAP_PROP_EXPOSURE, 75)
cam_left.set(cv2.CAP_PROP_GAIN, 0)
cam_right.set(cv2.CAP_PROP_GAIN, 0)

# Kalibrasyon verileri
calib = np.load("stereo_calib.npz")
mtx_left = calib["mtx_left"]
dist_left = calib["dist_left"]
mtx_right = calib["mtx_right"]
dist_right = calib["dist_right"]
R = calib["R"]
T = calib["T"]

# Stereo rectification
image_size = (width, height)
R1, R2, P1, P2, Q, _, _ = cv2.stereoRectify(
    mtx_left, dist_left,
    mtx_right, dist_right,
    image_size, R, T,
    flags=cv2.CALIB_ZERO_DISPARITY,
    alpha=0
)

# Stereo eşleyici (SGBM - CPU)
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,
    blockSize=5,
    P1=8 * 3 * 5 ** 2,
    P2=32 * 3 * 5 ** 2,
    disp12MaxDiff=1,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=32,
    preFilterCap=63,
    mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY
)

# Haritaları oluştur
left_map1, left_map2 = cv2.initUndistortRectifyMap(
    mtx_left, dist_left, R1, P1, image_size, cv2.CV_16SC2)
right_map1, right_map2 = cv2.initUndistortRectifyMap(
    mtx_right, dist_right, R2, P2, image_size, cv2.CV_16SC2)

print("🔴 ESC ile çık, disparity penceresi canlı gösteriliyor...")
while True:
    cam_left.grab()
    cam_right.grab()
    ret_l, frame_l = cam_left.retrieve()
    ret_r, frame_r = cam_right.retrieve()

    if not ret_l or not ret_r:
        print("❌ Kamera verisi alınamadı.")
        break

    # Gri tonlama
    gray_l = cv2.cvtColor(frame_l, cv2.COLOR_BGR2GRAY)
    gray_r = cv2.cvtColor(frame_r, cv2.COLOR_BGR2GRAY)

    # Düzelt (rectify)
    rect_l = cv2.remap(gray_l, left_map1, left_map2, cv2.INTER_LINEAR)
    rect_r = cv2.remap(gray_r, right_map1, right_map2, cv2.INTER_LINEAR)

    # Disparity hesapla
    disparity = stereo.compute(rect_l, rect_r).astype(np.float32) / 16.0

    # Derinlik hesapla: Z = f * B / d
    focal_length = P1[0, 0]  # fx
    baseline = np.linalg.norm(T)  # kamera arası mesafe (metre)
    depth_map = (focal_length * baseline) / (disparity + 1e-6)

    # Görselleştir
    disp_vis = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disp_vis = np.uint8(disp_vis)

    depth_vis = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_vis = np.uint8(depth_vis)
    cv2.imshow("Depth Map (Z-distance)", depth_vis)

    cv2.imshow("Disparity Map", disp_vis)



    if cv2.waitKey(1) & 0xFF == 27:
        break

# Temizle
cam_left.release()
cam_right.release()
cv2.destroyAllWindows()
print("🟢 Gerçek zamanlı depth map işlemi bitti.")
