#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# -----------------------
#  Parameters & Functions 
# -----------------------
b = 20.0                # deg C intercept
c = -10.0 / 300.0       # deg C per km
a = 100.0               # km (vortex core radius)
Gamma = 2*np.pi*a**2/(24*3600)   # s⁻¹

def v_theta(r):
    """Rankine vortex tangential speed (km/s)"""
    return Gamma * ( (r/a**2)*(r<=a) + (1.0/r)*(r>a) )

def r(x,y):
    return np.hypot(x, y)

def theta(x,y):
    return np.arctan2(y, x)

def omega(r):
    """Angular frequency (rad/s)"""
    # avoid /0 at r=0
    out = np.zeros_like(r)
    mask = r>0
    out[mask] = v_theta(r[mask]) / r[mask]
    return out

def theta0(x, y, t):
    return theta(x,y) - omega(r(x,y)) * t

def X0(x, y, t):
    return r(x,y) * np.cos(theta0(x,y,t))

def Y0(x, y, t):
    return r(x,y) * np.sin(theta0(x,y,t))

def T0(x, y):
    return b + c*y

def T(x, y, t):
    """Temperature advected by the vortex"""
    return T0(X0(x,y,t), Y0(x,y,t))


# -----------------------
#  1) Temperature field at t = 1 day
# -----------------------
# 1 day in seconds
t1 = 24*3600  

# high‐resolution mesh for contour plot
x = np.arange(-300, 301, 1)   # km
y = np.arange(-300, 301, 1)   # km
X, Y = np.meshgrid(x, y)
Tfield = T(X, Y, t1)

plt.figure(figsize=(6,5))
cf = plt.contourf(X, Y, Tfield, levels=np.arange(0,41,1), cmap='viridis')
plt.colorbar(cf, label='Temperature (°C)')
plt.title('T at t = 1 day')
plt.xlabel('x (km)')
plt.ylabel('y (km)')
plt.axis('equal')
plt.tight_layout()
plt.show()


# -----------------------
#  2) Gradient magnitude: FD vs Analytic
# -----------------------
# coarser mesh for finite‐difference (as in the MATLAB script)
dx = dy = 2.0  # km
x2 = np.arange(-300, 301, dx)
y2 = np.arange(-300, 301, dy)
X2, Y2 = np.meshgrid(x2, y2)

# temperature on the coarse grid
T2 = T(X2, Y2, t1)

# --- 2a) centered finite differences on the interior ---
Tx = (T2[1:-1, 2:] - T2[1:-1, :-2]) / (2*dx)
Ty = (T2[2:, 1:-1] - T2[:-2, 1:-1]) / (2*dy)
mag_fd = np.sqrt(Tx**2 + Ty**2)

# --- 2b) analytic gradient via chain rule ---
R2 = r(X2, Y2)
ω2 = omega(R2)

# ∂ω/∂r
ω_r = np.zeros_like(R2)
mask = R2 > a
ω_r[mask] = Gamma * (-2.0) / (R2[mask]**3)

# ∂r/∂x and ∂r/∂y
Rx = np.zeros_like(R2)
Ry = np.zeros_like(R2)
nonzero = R2>0
Rx[nonzero] =  X2[nonzero] / R2[nonzero]
Ry[nonzero] =  Y2[nonzero] / R2[nonzero]

# ∂ω/∂x = ω_r * ∂r/∂x, etc.
ω_x = ω_r * Rx
ω_y = ω_r * Ry

sin_ot = np.sin(-ω2*t1)
cos_ot = np.cos(-ω2*t1)
common = X2*cos_ot - Y2*sin_ot

y0_x = sin_ot - t1 * common * ω_x
y0_y = cos_ot - t1 * common * ω_y

Tx_an = c * y0_x
Ty_an = c * y0_y
mag_an = np.sqrt(Tx_an**2 + Ty_an**2)

# -----------------------
#  3) Plot comparison
# -----------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,5), sharey=True)

im1 = ax1.contourf(X2[1:-1,1:-1], Y2[1:-1,1:-1], mag_fd,  levels=50, cmap='plasma')
fig.colorbar(im1, ax=ax1, label='|∇T| (°C/km)')
ax1.set_title('Finite Difference')
ax1.set_xlabel('x (km)')
ax1.set_ylabel('y (km)')
ax1.axis('equal')

im2 = ax2.contourf(X2, Y2, mag_an, levels=50, cmap='plasma')
fig.colorbar(im2, ax=ax2, label='|∇T| (°C/km)')
ax2.set_title('Analytic (Chain Rule)')
ax2.set_xlabel('x (km)')
ax2.axis('equal')

plt.tight_layout()
plt.show()
