import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import sys


def lorenz_func(xyz: tuple, rho: float, sigma: float, beta: float):
    x, y, z = xyz
    dxdt = sigma*(y - x)
    dydt = x*(rho - z) - y
    dzdt = x*y - beta*z

    return np.array([dxdt, dydt, dzdt])


def update(num, coords, line):
    # NOTE: there is no .set_data() for 3 dim data
    line.set_data(coords[:num, 0], coords[:num, 1])
    line.set_3d_properties(coords[:num, 2])
    
    return line


def render_argv():
    args = sys.argv[1:]

    rho_str, sigma_str, beta_str = None, None, None
    for arg in args:
        if 'rho' in arg or 'r' in arg:
            rho_str = arg.split('=')[1]
        elif 'sigma' in arg or 's' in arg:
            sigma_str = arg.split('=')[1]
        elif 'beta' in arg or 'b' in arg:
            beta_str = arg.split('=')[1]
        
    if not rho_str:
        rho_str = '28'
    if not sigma_str:
        sigma_str = '10'
    if not beta_str:
        beta_str = '8/3'

    return rho_str, sigma_str, beta_str


rho_str, sigma_str, beta_str = render_argv()
rho = eval(rho_str)
sigma = eval(sigma_str)
beta = eval(beta_str)

t0, t1 = 0, 10000
dt = 0.005

coords = np.empty((t1 - t0 + 1, 3))
coords[0] = (0., 1., 1.05)

for i in range(t1):
    coords[i+1] = coords[i] + lorenz_func(coords[i], rho, sigma, beta)*dt


fig = plt.figure(figsize=(7, 7), facecolor='black')
ax = fig.add_subplot(projection='3d', facecolor='black')
line = ax.plot(*coords.T, color='white', linewidth=0.5)[0]

params_str = fr"$\rho$ = {rho_str}, $\sigma$ = {sigma_str}, $\beta$ = {beta_str}"
ax.text2D(0.5, 0.98, params_str, transform=ax.transAxes, ha='center', va='top', color='white')

ani = animation.FuncAnimation(fig, update, int(t1/dt), fargs=(coords, line), interval=1, repeat=False)

plt.axis('off')
plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
fig.canvas.manager.set_window_title(f"Lorenz Attractor")
plt.show()
