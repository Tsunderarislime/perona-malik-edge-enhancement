# perona-malik-edge-enhancement
This is a Python port of my Perona-Malik edge enhancement script. My original script was written in MATLAB and was used for a project in MACM 416 (numerical optimization course in SFU). The project was mainly about analyzing the properties of the time-stepping and spatial derivative schemes used by the Perona-Malik edge enhancement algorithm. 

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

## Citation
P. Perona and J. Malik, "Scale-space and edge detection using anisotropic diffusion," in IEEE Transactions on Pattern Analysis and Machine Intelligence, vol. 12, no. 7, pp. 629-639, July 1990, doi: 10.1109/34.56205.
keywords: {Image edge detection;Anisotropic magnetoresistance;Smoothing methods;Diffusion processes;Detectors;Hardware},
