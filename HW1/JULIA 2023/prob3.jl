# prob3.jl
using NetCDF, Printf

cd(dirname(@__FILE__))

# Paths to WOA23 files
ft = "../woa_downloads/woa23_decav_t00_01.nc"
fs = "../woa_downloads/woa23_decav_s00_01.nc"

lat = Float64.(ncread(ft,"lat"))
lon = Float64.(ncread(ft,"lon"))
depth = Float64.(ncread(ft,"depth"))

t_an = Float64.(ncread(ft,"t_an"))
s_an = Float64.(ncread(fs,"s_an"))

# mask missing
t_an[t_an .> 1e20] .= NaN
s_an[s_an .> 1e20] .= NaN

# simple trapezoid rule
function trapz(f,z)
  I = 0.0
  for k in 2:length(z)
    dz = z[k] - z[k-1]
    h  = 0.5*(f[k] + f[k-1])
    I += dz*h
  end
  return I
end

# Earth radius & grid
b = 6378e3; c = 6356e3; a = (b*b*c)^(1/3)
dphi   = 1 * pi/180
dlam   = 1 * pi/180
dA = [ a^2 * cos(lat[j]*pi/180) * dphi * dlam for i in 1:length(lon), j in 1:length(lat) ]

# max depth index per column
Kmx = [ sum(.~isnan.(t_an[i,j,:,1])) for i in 1:length(lon), j in 1:length(lat) ]

# volume, integrated T and S per column
dV  = [ dA[i,j] * trapz(ones(Kmx[i,j]), depth[1:Kmx[i,j]])        for i in 1:length(lon), j in 1:length(lat) ]
dIT = [ dA[i,j] * trapz(t_an[i,j,1:Kmx[i,j],1], depth[1:Kmx[i,j]]) for i in 1:length(lon), j in 1:length(lat) ]
dIS = [ dA[i,j] * trapz(s_an[i,j,1:Kmx[i,j],1], depth[1:Kmx[i,j]]) for i in 1:length(lon), j in 1:length(lat) ]

V  = sum(dV[:])
IT = sum(dIT[:])
IS = sum(dIS[:])

Tbar = IT / V
Sbar = IS / V

@printf("Total volume: %e \n", V)
@printf("Volumetric average temperature: %f °C\n", Tbar)
@printf("Volumetric average salinity:    %f PSU\n", Sbar)
