# prob5.jl  (optional oblate‐spheroid area & arclength)
using NetCDF, Printf, GibbsSeaWater

cd(dirname(@__FILE__))

fname = "../etopo_downloads/ETOPO_2022_v1_60s_N90W180_surface.nc"

x = ncread(fname,"lon"); y = ncread(fname,"lat"); z = ncread(fname,"z")

b = 6378.137e3; c = 6356.752e3
eps2 = 1 - (c/b)^2

# angles
phi = pi*y/180
lambda = pi*x/180

dphi   = phi[2] - phi[1]
dlambda= lambda[2] - lambda[1]

# spheroid radii factors
X = [ b*cos(phi[j]) / sqrt(1-eps2*sin(phi[j])^2) for j in 1:length(phi) ]
Z = [ b*(1-eps2)*sin(phi[j]) / sqrt(1-eps2*sin(phi[j])^2) for j in 1:length(phi) ]
r = sqrt.(X.^2 .+ Z.^2)
phi_s = sign.(Z) .* acos.(X ./ r)

# meridian arclength element
ds = [ b*(1-eps2) / (1-eps2*sin(phi[j])^2)^(3/2) for j in 1:length(phi) ]

# cumulative arclength (trapz)
function trapz(f,z)
  I = 0.0
  for k in 2:length(z)
    dz = z[k] - z[k-1]
    h  = 0.5*(f[k] + f[k-1])
    I += dz*h
  end
  return I
end
s = [ trapz(ds[1:j], phi[1:j]) for j in 1:length(phi) ]

using Plots
plot(s/1e6, (phi.-phi_s)*(180/pi)*1e5,
     xlabel="Distance (10^3 km)", ylabel="∆φ (10⁻⁵°)",
     legend=false)
