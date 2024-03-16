'''
TMA4121
16. Mars 2024
Wilhelm Engenes (MTKJ)

Numerisk løsning til varmelikningen (To romlige koordinater) som viser hvordan 2D-materiale i xy-planet nedkjøles,
hvor z aksen viser temperaturen.

2 romlige koordinater + tid + varme -> 4 dimensjoner -> Plotter x, y og varme + animerer tid. Plottingen
representerer varmen med farge.
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import cm

L_x = 0.9 # Lengden i x-retning
L_y = 1.1 # Lengden i y-retning
T = .05 # Total tid

N_x = 20  # Antall punkter i x-retning
N_y = 20  # Antall punkter i y-retning
N_t = 1000  # Antall tidssteg

h_x = L_x/N_x  # Størrelsen på stegene i x-retning
h_y = L_y/N_y  # Størrelsen på stegene i y-retning
k = T/N_t  # Størrelsen på tidsstegene

x = np.linspace(0, L_x, N_x)  # Array med x-verdiene
y = np.linspace(0, L_y, N_y)  # Array med y-verdiene
t = np.linspace(0, T, N_t)  # Array med tidsverdiene

u = np.zeros((N_x, N_y, N_t))  # Array for temperaturfordelingen

# Velger funksjon her (for initialbetingelsene):
func = lambda x, y: np.sin(3*np.pi*np.sqrt((x-.5)**2 + (y-.5)**2))

func_vals = np.array([[func(x_val, y_val) for y_val in y] for x_val in x]) # Initialbetingelse
u[1:-1,1:-1,0] = func_vals[1:-1, 1:-1] # Setter initialbetingelsen for temperaturfordelingen

# Euler eksplisitte metode
def u_next(u):
    u_next = np.zeros((N_x, N_y))
    for i in range(1, N_x-1):
        for j in range(1, N_y-1):
            u_next[i,j] = k/(h_x**2)*(u[i-1,j]-2*u[i,j]+u[i+1,j]) + k/(h_y**2)*(u[i,j-1] - 2*u[i,j] + u[i,j+1]) + u[i,j]
    return u_next

for i in range(N_t-1):
    u[:,:,i+1] = u_next(u[:,:,i])

# Plotting av 3D figur + tid
T_ani = 1 # Total tid for animasjonen i sekunder
fps = 60 # frames per sekund
total_frames = T_ani*fps # Totalt antall frames

fig, ax = plt.subplots(subplot_kw={"projection": "3d"}) # Oppretter 3D-plot
meshX, meshY = np.meshgrid(x, y) # Lager meshgrid for x og y

def update(frame):
    ax.clear()
    surf = ax.plot_surface(meshX, meshY, u[:,:,frame], cmap = cm.coolwarm)
    ax.set_xlabel("$y$") # Setter x-akse navn
    ax.set_ylabel("$x$") # Setter y-akse navn
    ax.set_zlabel("$u$") # Setter z-akse navn
    ax.set_xlim((0,L_x)) # Setter grenser for x-aksen
    ax.set_ylim((0,L_y)) # Setter grenser for y-aksen
    ax.set_zlim((-1,1)) # Setter grenser for z-aksen
    return surf

ani = animation.FuncAnimation(fig, update,
                              frames=np.linspace(0, N_t-1, total_frames).astype(int), interval = 1000/fps)
ani.save("animation2d.gif")
plt.show()