# perona-malik-edge-enhancement
This is a Python port of my Perona-Malik edge enhancement script. My original script was written in MATLAB and was used for a project in MACM 416 (numerical optimization course in SFU). The project was mainly about analyzing the properties of the time-stepping and spatial derivative schemes used by the Perona-Malik edge enhancement algorithm. 
<p align="center">
  <img align="center" src="https://github.com/user-attachments/assets/b11fd03f-bc8c-471c-ace0-f1ecaaa20ac3">
</p>

## Usage
Clone this repository somewhere on your computer and install necessary libraries with `pip install -r requirements.txt`.

Run the command as follows:

`python main.py <filename> <iterations> <time_step> <K> <g_func> --options`

### Parameters
- `filename`: Path to the image file you want to run the algorithm on.
- `iterations`: Number of iterations to run the algorithm for.
- `time_step`: Time step size for the algorithm. The algorithm is stable if this is in the range **(0, 0.25]**.
- `K`: The constant K to be used in the function g. K effectively defines what an ‘edge’ is in the detector. If the gradients of neighboring pixels are large, then it scales down the differences. Increasing K reduces the amount of scaling that the function g does. This may cause the image to become blurry with enough iterations.
- `g_func`: The function g to use in the algorithm. These choices of the function g were mentioned in the paper, so this implementation decided to stick with them. Technically, any monotonically decreasing function can be used. Below are the equations for the g functions. $G$ is the magnitude of the image gradient.
  - `g_0`: $e^{-(\frac{G}{K})^2}$
  - `g_1`: $\frac{1}{1 + (\frac{G}{K})^2}$

### Optional Flags
- `--animate`: Add this flag to display the image after each iteration in a window. Note that this may negatively affect performance, as it will draw the image every iteration.
- `--time`: Add this flag to display the runtime of the algorithm.

## Example
Here's an image before running the algorithm.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f3c52785-0626-4163-9712-31f303690aa9">
</p>

Now here are three different outputs.
<p align="center">
  <img src="https://github.com/user-attachments/assets/f4d0454b-339f-482e-9182-6978b3dab614"> <img src="https://github.com/user-attachments/assets/d7ca9fcc-3801-4588-9aa0-5fb037baa7a8"> <img src="https://github.com/user-attachments/assets/b11f6158-3435-44fc-9816-5e01f7046c16">
</p>

- Left (A normal set of parameters):
  - N = 250
  - Time-step Size = 0.05
  - K = 0.15
  - g = 0
- Center (Unstable time-step size):
  - N = 250
  - Time-step Size = 1.5 `<-- unstable because this is not in the range (0, 0.25]` 
  - K = 0.15
  - g = 0
- Right (Stable, but very blurry):
  - N = 250
  - Time-step Size = 0.05
  - K = 1 `<-- high values of K cause blurring to occur`
  - g = 0

## Special Thanks
- [ほったりょう](https://x.com/hottaryou): I like their illustrations, so I used some of them to showcase the edge enhancement effect of the Perona-Malik equation. Give them a follow on X (formerly known as Twitter).
- [SciPy](https://scipy.org/): Their __convolve2d()__ method dramatically improved the speed of my scripts. I had a naive, nested loop approach in my original MATLAB script and MATLAB did not seem to mind and executed the code quickly. In Python, this is not the case. The nested loop approach took a painfully long time to execute, even for relatively small images. The current approach which calls __convolve2d()__ eight times, looks ridiculous. Yet, it is soooooo much better than my naive approach. Thank you SciPy team for creating such an efficient method for doing 2D convolutions in Python.

## Citation
P. Perona and J. Malik, "Scale-space and edge detection using anisotropic diffusion," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 12, no. 7, pp. 629-639, July 1990, doi: 10.1109/34.56205.
keywords: {Image edge detection;Anisotropic magnetoresistance;Smoothing methods;Diffusion processes;Detectors;Hardware},
