from cv2 import Sobel, CV_64F
import numpy as np

# exp(-(imgradient(img)./K).^2)
def g_0(img, K) -> np.ndarray:
    # Magnitude of gradients = sqrt(x_gradient^2 + y_gradient^2)
    s_x = Sobel(img, dx=1, dy=0, ddepth=CV_64F)
    s_y = Sobel(img, dx=0, dy=1, ddepth=CV_64F)
    return np.exp(-(np.hypot(s_x, s_y) / K)**2.0)

# 1 ./ (1 + (imgradient(x)./K).^2)
def g_1(img, K) -> np.ndarray:
    # Magnitude of gradients = sqrt(x_gradient^2 + y_gradient^2)
    s_x = Sobel(img, dx=1, dy=0, ddepth=CV_64F)
    s_y = Sobel(img, dx=0, dy=1, ddepth=CV_64F)
    return 1 / (1 + (np.hypot(s_x, s_y) / K)**2.0)