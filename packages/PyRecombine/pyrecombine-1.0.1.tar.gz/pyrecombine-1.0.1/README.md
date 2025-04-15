# PyRecombine

Performs a dynamic Caratheodory process and takes a weighted collection of vectors and identifies by pointers, a subset of minimal cardinality among the vectors and new weights so both empirical measures have the same mean.
Software written by Terry Lyons, based on algorithms developed jointly with Christian Litter and then with Maria Tchernychova 2008-2020.
Here minimal is a local notion and means it cannot be further reduced.
There may be other noncomparable cubature sets with fewer points.

The library has a robust and stable C interface and even old dlls from 2008 with the old algorithm still run.
Measures are represented by an array of null pointers (pseudo-points) and an array of equal length of positive doubles adding to `1.`; the calling program provides a feature map that converts each null pointer to a vector, and so recombine never knows or needs to know the real types of the points.
Recombine returns the indexes of the points that should remain and new positive weights so that the mean of these remaining points with the new weights is the same as the old mean.
The new list of survivors is never more than `D+1` long where `D` is the  dimension of the vector space.
If there are `N` points in `D` dimensions the sequential complexity of this algorithm is less  than `ND + log_2(N/D) D^3`.
This reflects the order of magnitude improvement in the algorithm developed with  Maria Tchernychova; the algorithm with Litterer had complexity `ND + log_2(N/D) D^4` although it is quicker for small problems.
The interface remains the same.
The ND comes from touching the points, and `log_2(N/D) D^3` from performing `log_2(N/D)` complex SVD type calculations on `Dx2D` matrices.
This is a linear programming problem under the surface, but the algorithm here has fixed complexity.
In many of the problems we are interested in `N` is approximately `D^2` so the cost is (to logarithms) equated with the cost of touching the points.

The algorithm uses MKL (LAPACK) to do most of the linear algebra, although there is a part that is bespoke.
The operations benefit from some parallelism via OMP.
Say (export OMP_NUM_THREADS=8).
The log factor is truly sequential.
