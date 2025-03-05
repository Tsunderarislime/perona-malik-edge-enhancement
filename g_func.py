from cv2 import Laplacian, CV_64F
import numpy as np

# exp(-(imgradient(img)./K).^2)
def g_0(img, K):
    return np.exp(-(Laplacian(img, CV_64F) / K)**2.0)

# 1 ./ (1 + (imgradient(x)./K).^2)
def g_1(img, K):
    return 1 / (1 + (Laplacian(img, CV_64F) / K)**2.0)