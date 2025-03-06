from scipy.signal import convolve2d
import numpy as np

# Algorithm on one colour channel, to be run in parallel
def perona_malik(U, g, ts, K, w, h) -> np.ndarray:
    grad = g(U, K) # Take gradient
    grad[0, :] = np.zeros((1, w+2)); grad[h+1, :] = np.zeros((1, w+2)) # Apply Neumann boundary conditions
    grad[:, 0] = np.zeros((h+2)); grad[:, w+1] = np.zeros((h+2)) # Gradient on boundary = 0

    # Convolutions. Four for each cardinal direction. It's actually ridiculous how much better this is compared to a nested for loop
    north = convolve2d(U, np.array([[0, 1, 0], [0, -1, 0], [0, 0, 0]]), boundary="symm", mode="same") * convolve2d(grad, np.array([[0, 1, 0], [0, 0, 0], [0, 0, 0]]), boundary="symm", mode="same")
    south = convolve2d(U, np.array([[0, 0, 0], [0, -1, 0], [0, 1, 0]]), boundary="symm", mode="same") * convolve2d(grad, np.array([[0, 0, 0], [0, 0, 0], [0, 1, 0]]), boundary="symm", mode="same")
    east = convolve2d(U, np.array([[0, 0, 0], [0, -1, 1], [0, 0, 0]]), boundary="symm", mode="same") * convolve2d(grad, np.array([[0, 0, 0], [0, 0, 1], [0, 0, 0]]), boundary="symm", mode="same")
    west = convolve2d(U, np.array([[0, 0, 0], [1, -1, 0], [0, 0, 0]]), boundary="symm", mode="same") * convolve2d(grad, np.array([[0, 0, 0], [1, 0, 0], [0, 0, 0]]), boundary="symm", mode="same")

    return U + ts * (north + south + east + west)