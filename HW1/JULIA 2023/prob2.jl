# prob2.jl
using NetCDF, Printf

cd(dirname(@__FILE__))

fname = "../etopo_downloads/ETOPO_2022_v1_60s_N90W180_surface.nc"

x = ncread(fname,"lon")    # longitude (degrees)
y = ncread(fname,"lat")    # latitude  (degrees)
z = ncread(fname,"z")    # depth     (m)

# Earth radius
b = 6378e3; c = 6356e3
a = (b*b*c)^(1/3)

phi    = pi*y/180
dphi   = phi[2] - phi[1]
lambda = pi*x/180
dlambda= lambda[2] - lambda[1]

dA = [ a^2 * cos(p) * dphi * dlambda for l in lambda, p in phi ]

# total ocean volume
VO = sum(-dA[:] .* z[:] .* (z[:] .< 0))

@printf("Volume of ocean: %e m3 \n", VO)
