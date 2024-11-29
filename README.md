# Brain Fiber Bundle Simulator for validating tractography-based parcellation algorithms

## Overview
This code implements a brain fiber bundle simulator using spline curves for fiber representation. This simulator enhances and expands the functionality of an earlier version, offering the ability to simulate realistic bundles with complex ends that align with the shape of cortical parcels. The first version is available at https://github.com/elidapoo/Brain_bundle_simulator

## Prerequisites
- The code has been executed on both Windows and Ubuntu platforms.
- Tested on Python 3.9.

## Code Dependencies
To use the code, install the following libraries:
- [Numpy](https://numpy.org/)
- [Geomdl](https://pypi.org/project/geomdl/)
- [Scipy](https://www.scipy.org/)

### Dependency installation on Windows and Ubuntu
- pip3 install numpy
- pip3 install geomdl
- pip3 install scipy

## Example
The following folder contains resampled centroids with 21 points, as well as the vertices of the parcels connecting the centroids.

## Simulated Data
The following folder contains an example of the simulated connections generated by the simulator..

## Input parameters
- **centroids**: Centroids in format .bundles/.bundlesdata. The default path is the example folder. (Fibers must have 21 points).
- **vertex**: Dictionary with the vertices of the pair of parcels connecting the centroid.
- **mu, sigma_range**: Mean and variance to optionally add Gaussian noise to the first 5 points at each end of the fiber.

## Output files
All output files are stored in the results folder:
- **Simulated_tractography.bundles/.bundlesdata**: Contains all the simulated resulting clusters together in .bundles/.bundlesdata format.
-
