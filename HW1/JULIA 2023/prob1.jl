# prob1.jl
using NetCDF, Printf

cd(dirname(@__FILE__))

fname = "../etopo_downloads/ETOPO_2022_v1_60s_N90W180_surface.nc"

x = ncread(fname,"lon")    # longitude (degrees)
y = ncread(fname,"lat")    # latitude  (degrees)
z = ncread(fname,"z")      # depth     (m)

# geometric mean Earth radius
b = 6378e3    # equatorial radius [m]
c = 6356e3    # polar      radius [m]
a = (b*b*c)^(1/3)

# convert to radians
phi    = pi*y/180        # latitudes
dphi   = phi[2] - phi[1]
lambda = pi*x/180        # longitudes
dlambda= lambda[2] - lambda[1]

# surface element dA for every grid cell
dA = [ a^2 * cos(p) * dphi * dlambda for l in lambda, p in phi ]

# sum where ocean (z<0)
AO = sum(dA[:] .* (z[:] .< 0))
AE = sum(dA[:])

@printf("Area of ocean: %e m2 \n", AO)
@printf("Area of whole Earth: %e m2 \n", AE)
@printf("Fraction covered by ocean: %f \n", AO/AE)
