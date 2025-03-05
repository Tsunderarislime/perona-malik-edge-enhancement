import argparse
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import cv2
import g_func as g_func
import sys

# Set up the command line argument parsing
parser = argparse.ArgumentParser(description="Apply the Perona-Malik edge enhancement algorithm to an image")
parser.add_argument("filename", type=str,
                    help="File name of the image you want to process")
parser.add_argument("iterations", type=int, default=10,
                    help="Number of iterations you want the algorithm to run for. This should be greater than 0")
parser.add_argument("time_step", type=float, default=0.25,
                    help="Time step size for the algorithm. Stable when in the range (0, 0.25]")
parser.add_argument("K", type=float, default=0.25,
                    help="Value for constant K in the function g. This should be a positive float")
parser.add_argument("g_func", type=int, choices=[0, 1], default=0,
                    help="Choice of g function for algorithm. See README for what these are. Choose 0 or 1")
parser.add_argument("--animate", action="store_true",
                    help="Display progress of algorithm as it runs")
parsed = parser.parse_args()

# Main body of the script
def main(args):
    # Ensure all of the arguments are valid before running
    try:
        img = cv2.imread(args.filename) # Valid image file?
        assert(args.iterations > 0) # Number of iterations greater than 0?
        assert(args.time_step > 0) # Time step size greater than 0?
        assert(args.K > 0) # Constant K greater than 0?
    except AssertionError:
        print("At least one of the passed arguments failed the assertion check! Please use the -h flag to see valid arguments!")
        return # Self-explanitory
    except Exception as e:
        print(e)
        return # This exception is most likely the file not found error

    # Rescale the colour intensities from [0, 255] to [0, 1]
    mm_scaler = MinMaxScaler()
    img = mm_scaler.fit_transform(img.reshape(-1, img.shape[-1])).reshape(img.shape)

    # Apply Dirchlet border conditions (place a border of 0 around image)
    w = img.shape[1]; h = img.shape[0] # Get image dimensions
    U = np.zeros(shape=(h+2, w+2, img.shape[2])) # Array of zeros
    U[1:h+1, 1:w+1, :] = img # Place the image in the center of the zero array

    # Display initial image before
    cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Original Image", 10, 10)
    cv2.resizeWindow("Original Image", 900, 900)
    cv2.imshow("Original Image", img)

    # Display the image as it updates, if animation is requested
    if args.animate:
        cv2.namedWindow("Altered Image", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Altered Image", 920, 10)
        cv2.resizeWindow("Altered Image", 900, 900)
        cv2.imshow("Altered Image", U)
    
    # Wait until user has moved windows to where they want before starting
    print("\n=======================\n"
          "Press any key to begin!\n"
          "=======================\n")
    cv2.waitKey(0)

    # Store g function
    if args.g_func:
        g = g_func.g_1
    else:
        g = g_func.g_0
    
    N = args.iterations
    # Begin the loop
    for n in range(args.iterations):

        # Progress bar
        prog = int(round(50 * (n+1) / N))
        bar = "=" * prog + "-" * (50 - prog)
        sys.stdout.write(f"\r[{bar}] {100*(n+1)/N:6.2f} % complete, iteration {n+1}")
        sys.stdout.flush()
    print()

if __name__ == "__main__":
    main(parsed)