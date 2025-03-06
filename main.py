# Import libraries
import argparse
import numpy as np
import cv2
import sys
from multiprocessing import Pool
from time import time
# Import utility functions
import util.g_func as g_func
import util.perona_malik as pm

# Set up the command line argument parsing
parser = argparse.ArgumentParser(description="Apply the Perona-Malik edge enhancement algorithm to an image")
parser.add_argument("filename", type=str,
                    help="File name of the image you want to process")
parser.add_argument("iterations", type=int, default=10,
                    help="Number of iterations you want the algorithm to run for. This should be greater than 0")
parser.add_argument("time_step", type=float, default=0.25,
                    help="Time step size for the algorithm. Stable when in the range (0, 0.25], should be a positive float")
parser.add_argument("K", type=float, default=0.25,
                    help="Value for constant K in the function g. This should be a positive float")
parser.add_argument("g_func", type=int, choices=[0, 1], default=0,
                    help="Choice of g function for algorithm. See README for what these are. Choose 0 or 1")
parser.add_argument("--animate", action="store_true",
                    help="Display progress of algorithm as it runs")
parser.add_argument("--time", action="store_true",
                    help="Show runtime of algorithm loop")
parsed = parser.parse_args()

# Main body of the script
def main(args):
    # Ensure all of the arguments are valid before running
    try:
        img = cv2.imread(args.filename) # This will throw an exception if it fails to read
        assert args.iterations > 0, "Number of iterations should be greater than 0!"
        assert args.time_step > 0, "The time step size should be greater than 0!"
        assert args.K > 0, "The constant K should be greater than 0!"
    except Exception as e:
        print(e)
        sys.exit(1) # Exit with code 1 due to error with arguments

    # Rescale the colour intensities from [0, 255] to [0, 1]
    img = img/255.0
    
    # Apply Dirchlet border conditions (place a border of 0 around image)
    w = img.shape[1]; h = img.shape[0] # Get image dimensions
    U = np.zeros((h+2, w+2, img.shape[2]))
    U[1:h+1, 1:w+1, :] = img

    # Display initial image before
    cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Original Image", 10, 10)
    cv2.resizeWindow("Original Image", 900, 900)
    cv2.imshow("Original Image", img)

    # Display the image as it updates, if animation is requested
    if args.animate:
        cv2.namedWindow("Processed Image", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Processed Image", 920, 10)
        cv2.resizeWindow("Processed Image", 900, 900)
        cv2.imshow("Processed Image", U)
    
    # Wait until user has moved windows to where they want before starting
    print("\n=======================\n"
          "Press any key to begin!\n"
          "=======================\n")
    cv2.waitKey(0)

    # Store g function, either g_0 or g_1 depending on what was used in the command line argument
    if args.g_func:
        g = g_func.g_1
    else:
        g = g_func.g_0
    
    # Prepare for the loop
    N = args.iterations
    pool = Pool(processes=U.shape[2]) # One process per channel
    U = np.moveaxis(U, 2, 0) # Index as [colour, width, height] for the processing pool
    print(U.shape)
    if args.time:
        start = time() # Tracking runtime

    # Begin the loop
    for n in range(N):
        # The Perona-Malik algorithm is called here, it should run in parallel via the Pool object
        U = np.array( # The pool returns a list of 2D arrays, make it one 3D array
                pool.starmap(pm.perona_malik, [
                        (U[c, :, :], g, args.time_step, args.K, w, h) for c in range(U.shape[0]) # Apply the algorithm to each colour channel with the starmap
                    ]
                )
            )

        # Progress bar
        prog = int(round(50 * (n+1) / N)) 
        bar = "=" * prog + "-" * (50 - prog)
        sys.stdout.write(f"\r[{bar}] {100*(n+1)/N:6.2f} % complete, iteration {n+1}")
        sys.stdout.flush()

        # Update image if animation is requested
        if args.animate:
            cv2.imshow("Processed Image", np.moveaxis(U[:, 1:h+1, 1:w+1], 0, 2))
            cv2.waitKey(1)

    # End of loop
    if args.time:
        print(f"\nFinished! Total runtime: {time() - start:.3f} seconds")
    else:
        print("\nFinished!")

    # Display the image after iterations
    cv2.namedWindow("Processed Image", cv2.WINDOW_NORMAL)
    cv2.moveWindow("Processed Image", 920, 10)
    cv2.resizeWindow("Processed Image", 900, 900)
    cv2.imshow("Processed Image", np.moveaxis(U[:, 1:h+1, 1:w+1], 0, 2))
    print("\n========================\n"
          "Press any key to finish!\n"
          "========================\n")
    cv2.waitKey(0)

    sys.exit(0) # Code executed without any problems

if __name__ == "__main__":
    main(parsed)