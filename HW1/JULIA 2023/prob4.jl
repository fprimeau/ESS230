# prob4.jl
using NetCDF, Printf, GibbsSeaWater

cd(dirname(@__FILE__))

# WOA18 annual data for TEOS-10 example
ft = "../woa_downloads/woa23_decav_t00_01.nc"
fs = "../woa_downloads/woa23_decav_s00_01.nc"

lat = Float64.(ncread(ft,"lat"))
lon = Float64.(ncread(ft,"lon"))
depth = Float64.(ncread(ft,"depth"))

t_an = Float64.(ncread(ft,"t_an"))
s_an = Float64.(ncread(fs,"s_an"))

t_an[t_an .> 1e20] .= NaN
s_an[s_an .> 1e20] .= NaN

# same dA, dz as before
b = 6378e3; c = 6356e3; a = (b*b*c)^(1/3)
dphi   = 1 * pi/180
dlam   = 1 * pi/180
dA = [ a^2 * cos(lat[j]*pi/180) * dphi * dlam for i in 1:length(lon), j in 1:length(lat) ]

dz = zeros(length(depth))
dz[1:end-1] = diff(depth)
dz[end]     = dz[end-1]

# volume element
dV = [ dA[i,j] * dz[k] for i in 1:length(lon), j in 1:length(lat), k in 1:length(depth) ]

# TEOS-10 over top 200 m
Kmx = [ sum(.~isnan.(t_an[i,j,:,1])) for i=1:length(lon), j=1:length(lat) ]
K200= map((k)->min(k,25), Kmx)

# make SA, CT, alpha, beta arrays
alpha = zeros(length(lon),length(lat),25)
beta  = zeros(length(lon),length(lat),25)
for i in 1:length(lon), j in 1:length(lat)
  K = K200[i,j]
  for k = 1:K
    p = gsw_p_from_z(-depth[k], lat[j])
    sa = gsw_sa_from_sp(s_an[i,j,k,1], p, lon[i], lat[j])
    ct = gsw_ct_from_t(sa, t_an[i,j,k,1], p)
    alpha[i,j,k] = gsw_alpha(sa, ct, p)
    beta[i,j,k]  = gsw_beta(sa, ct, p)
  end
end

# mask and weight
V200 = sum([ dA[i,j]*sum(dz[1:K200[i,j]]) for i=1:length(lon), j=1:length(lat) ])
Ialpha = sum([ dA[i,j]*trapz(alpha[i,j,1:K200[i,j]], depth[1:K200[i,j]]) for i=1:length(lon), j=1:length(lat) ])
Ibeta  = sum([ dA[i,j]*trapz(beta[i,j,1:K200[i,j]], depth[1:K200[i,j]]) for i=1:length(lon), j=1:length(lat) ])

alphabar = Ialpha / V200
betabar  = Ibeta  / V200

@printf("Volume <200m: %e m3\n", V200)
@printf("Vol. ave alpha (1/K): %e\n", alphabar)
@printf("Vol. ave beta (kg/g):  %e\n", betabar)
