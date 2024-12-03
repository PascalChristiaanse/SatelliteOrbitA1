import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Load input data
t = np.loadtxt('t.txt')  # Epochs (seconds)
r = np.loadtxt('r.txt')  # Precise positions (km)
v = np.loadtxt('v.txt')  # Precise velocities (km/s)

# Extract initial state from data
position_0 = r[0, :]  # Initial position (km)
velocity_0 = v[0, :]  # Initial velocity (km/s)
state_0 = np.hstack((position_0, velocity_0))  # Combined state vector

# Constants
c = 299792.458  # Speed of light, km/s
GM = 3.986004415e5  # Earth's gravitational constant, km^3/s^2
R = 6378.13660  # Earth reference radius, km
C20 = -4.841692151273e-4  # Gravity field coefficient, dimensionless
we = 7.292115e-5  # Earth rotation rate, rad/s
CD = 2.6  # Drag coefficient, dimensionless
rho = 1e-2  # Atmospheric density, kg/km^3
A = 1e-6  # Cross-section area, km^2
m = 500  # Satellite mass, kg

# Time span for integration
t_span = (t[0], t[-1])  # Use data range for integration
t_eval = np.linspace(t[0], t[-1], len(t))  # Match evaluation times to input

# Functions to calculate accelerations
def coriolis_centrifugal(state):
    r, v = state[:3], state[3:]
    omega_cross_r = np.cross([0, 0, we], r)
    omega_cross_v = np.cross([0, 0, we], v)
    return -2 * omega_cross_v - np.cross([0, 0, we], omega_cross_r)

def earth_flattening(state):
    r = state[:3]
    r_norm = np.linalg.norm(r)
    z = r[2]
    factor = 1.5 * C20 * GM * R**2 / r_norm**5
    ax = factor * r[0] * (5 * (z**2 / r_norm**2) - 1)
    ay = factor * r[1] * (5 * (z**2 / r_norm**2) - 1)
    az = factor * r[2] * (5 * (z**2 / r_norm**2) - 3)
    return np.array([ax, ay, az])

def atmospheric_drag(state):
    r, v = state[:3], state[3:]
    v_rel = v - np.cross([0, 0, we], r)
    v_rel_norm = np.linalg.norm(v_rel)
    drag_acc = -0.5 * CD * (A / m) * rho * v_rel_norm * v_rel
    return drag_acc

def total_acceleration(state, include_coriolis=False, include_flattening=False, include_drag=False):
    r, v = state[:3], state[3:]
    r_norm = np.linalg.norm(r)
    accel_gravity = -GM * r / r_norm**3
    accel = accel_gravity
    if include_coriolis:
        accel += coriolis_centrifugal(state)
    if include_flattening:
        accel += earth_flattening(state)
    if include_drag:
        accel += atmospheric_drag(state)
    return accel

# Dynamics model for integration
def dynamics(t, state, include_coriolis, include_flattening, include_drag):
    r, v = state[:3], state[3:]
    a = total_acceleration(state, include_coriolis, include_flattening, include_drag)
    if t==0:
        print(a)
    return np.hstack((v, a))

# Integration for different models
results = {}
models = [
    (False, False, False),  # Model 1: No perturbing forces, ignore frame rotation
    (True, False, False),   # Model 2: No perturbing forces, account for frame rotation
    (True, True, False),    # Model 3: Include Earth flattening and frame rotation
    (True, True, True),     # Model 4: Include Earth flattening, frame rotation, and drag
]

print("--------------------------")
print(enumerate(models))
for i, (coriolis, flattening, drag) in enumerate(models):
    print(i)
    sol = solve_ivp(
        dynamics,
        t_span,
        state_0,
        method='RK45',
        args=(coriolis, flattening, drag),
        t_eval=t_eval,
        rtol=1e-14,
        atol=1e-14,
    )
    results[f"Model {i+1}"] = sol
    print(sol)

#print(results)
# Plot the errors in position
plt.figure(figsize=(10, 6))
for i, (label, sol) in enumerate(results.items()):
    # Calculate position error relative to provided precise positions
    pos_error = np.linalg.norm(sol.y[:3, :].T - r, axis=1)
    plt.plot(t / 3600, pos_error, label=label)
    plt.annotate(
        f"{pos_error[-1]*1000:.1e} m", 
        (t_eval[-1] / 3600, pos_error[-1]),
        textcoords="offset points", 
        xytext=(-8/pos_error[-1], 8/pos_error[-1]), 
        ha='center', 
        arrowprops=dict(arrowstyle="->", color="black")
    )
#plt.plot(t[4] / 3600,pos_error[3], 'g*')
#plt.yscale('log')
plt.xlabel("Time (hours)")
plt.ylabel("Position error (km)")
plt.title("Position Error over Time")
plt.legend()
plt.grid()
plt.show()
