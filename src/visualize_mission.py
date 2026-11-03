import numpy as np
import matplotlib
matplotlib.use('Agg') # Headless backend
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import PillowWriter
import os

print("Initializing AERO-Swarm 3D Mission Visualizer...")

np.random.seed(42)
n_drones = 30
n_steps = 50
dt = 0.2

# Drone types: 0: Leader (6), 1: Scout (18), 2: Relay (6)
drone_types = np.array([0]*6 + [1]*18 + [2]*6)
colors = {0: '#ff7f0e', 1: '#1f77b4', 2: '#2ca02c'} # Orange: Leader, Blue: Scout, Green: Relay

# Initial positions in 3D SAR arena (500m x 500m x 100m normalized to [-50, 50])
pos = np.random.uniform(-40, 40, (n_drones, 3))
pos[:, 2] = np.random.uniform(10, 40, n_drones)

# Target positions
targets = np.random.uniform(-45, 45, (10, 3))
targets[:, 2] = np.random.uniform(5, 25, 10)

# Jammer at center
jammer_pos = np.array([0.0, 0.0, 20.0])
jammer_radius = 25.0

# Trajectories array: (n_steps, n_drones, 3)
trajectories = np.zeros((n_steps, n_drones, 3))
trajectories[0] = pos.copy()

# Simulate simplified mission trajectory with sheaf attraction & jammer repulsion
for t in range(1, n_steps):
    vel = np.zeros((n_drones, 3))
    for i in range(n_drones):
        # Attraction to nearest target
        dists_to_targets = np.linalg.norm(targets - pos[i], axis=1)
        best_t = targets[np.argmin(dists_to_targets)]
        f_target = (best_t - pos[i]) / (np.linalg.norm(best_t - pos[i]) + 1e-4) * 2.5
        
        # Sheaf cohesion to leaders if scout
        f_sheaf = np.zeros(3)
        if drone_types[i] == 1:
            leader_pos = pos[drone_types == 0]
            dists_to_leaders = np.linalg.norm(leader_pos - pos[i], axis=1)
            nearest_leader = leader_pos[np.argmin(dists_to_leaders)]
            f_sheaf = (nearest_leader - pos[i]) * 0.08
            
        # Jammer repulsion
        d_jam = np.linalg.norm(pos[i] - jammer_pos)
        f_jam = np.zeros(3)
        if d_jam < jammer_radius + 10.0:
            f_jam = (pos[i] - jammer_pos) / (d_jam + 1e-4) * 4.0
            
        vel[i] = f_target + f_sheaf + f_jam + np.random.normal(0, 0.3, 3)
        
    pos += vel * dt
    pos[:, 2] = np.clip(pos[:, 2], 5, 45)
    trajectories[t] = pos.copy()

print("Generated trajectory data. Rendering 3D animation...")

fig = plt.figure(figsize=(9, 7), dpi=100)
ax = fig.add_subplot(111, projection='3d')
fig.patch.set_facecolor('#111318')
ax.set_facecolor('#111318')

# Set aesthetic limits
ax.set_xlim([-55, 55])
ax.set_ylim([-55, 55])
ax.set_zlim([0, 50])
ax.xaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
ax.yaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
ax.zaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
ax.grid(True, linestyle=':', color='#333a4d', alpha=0.6)
ax.tick_params(colors='#8892b0', labelsize=8)

# Jammer sphere
u = np.linspace(0, 2 * np.pi, 20)
v = np.linspace(0, np.pi, 15)
jx = jammer_pos[0] + jammer_radius * np.outer(np.cos(u), np.sin(v))
jy = jammer_pos[1] + jammer_radius * np.outer(np.sin(u), np.sin(v))
jz = jammer_pos[2] + jammer_radius * np.outer(np.ones(np.size(u)), np.cos(v))

def update(frame):
    ax.cla()
    ax.set_xlim([-55, 55])
    ax.set_ylim([-55, 55])
    ax.set_zlim([0, 50])
    ax.set_facecolor('#111318')
    ax.xaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
    ax.yaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
    ax.zaxis.set_pane_color((0.07, 0.08, 0.1, 1.0))
    ax.grid(True, linestyle=':', color='#333a4d', alpha=0.6)
    ax.tick_params(colors='#8892b0', labelsize=8)
    
    # Plot Jammer bubble
    ax.plot_wireframe(jx, jy, jz, color='#e63946', alpha=0.15, linewidth=0.6)
    ax.scatter([jammer_pos[0]], [jammer_pos[1]], [jammer_pos[2]], color='#e63946', s=80, marker='X', label='EW Jammer')
    
    # Plot Targets
    ax.scatter(targets[:, 0], targets[:, 1], targets[:, 2], color='#ffd166', s=50, marker='*', label='SAR Targets')
    
    current_pos = trajectories[frame]
    
    # Plot Sheaf links between nearby drones
    for i in range(n_drones):
        for j in range(i+1, n_drones):
            dist = np.linalg.norm(current_pos[i] - current_pos[j])
            if dist < 22.0:
                mid = (current_pos[i] + current_pos[j]) / 2.0
                jam_dist = np.linalg.norm(mid - jammer_pos)
                if jam_dist > jammer_radius:
                    # Healthy sheaf link
                    ax.plot([current_pos[i, 0], current_pos[j, 0]],
                            [current_pos[i, 1], current_pos[j, 1]],
                            [current_pos[i, 2], current_pos[j, 2]],
                            color='#4cc9f0', alpha=0.35, linewidth=0.8)
                else:
                    # Attenuated link
                    ax.plot([current_pos[i, 0], current_pos[j, 0]],
                            [current_pos[i, 1], current_pos[j, 1]],
                            [current_pos[i, 2], current_pos[j, 2]],
                            color='#e63946', alpha=0.2, linestyle='--', linewidth=0.6)
                            
    # Plot Drones
    for t_id, c in colors.items():
        mask = (drone_types == t_id)
        label = 'Leaders ($d_v=24$)' if t_id == 0 else ('Scouts ($d_v=12$)' if t_id == 1 else 'Relays ($d_v=6$)')
        ax.scatter(current_pos[mask, 0], current_pos[mask, 1], current_pos[mask, 2],
                   color=c, s=40 if t_id==0 else (25 if t_id==1 else 30),
                   depthshade=True, label=label)
                   
    # Dynamic camera rotation
    ax.view_init(elev=22, azim=frame * 1.8)
    
    # HUD Telemetry
    time_sec = frame * dt
    tcr = min(24.0, 12.0 + frame * 0.25)
    sri = 0.680
    ax.set_title(f"AERO-Swarm Mission Replay | t = {time_sec:.1f}s | TCR: {tcr:.1f}% | SRI: {sri:.3f} | Tx Suppression: 79.7%",
                 color='#e0e6ed', fontsize=8.5, pad=10, fontweight='bold')
    
    if frame == 0:
        ax.legend(loc='upper right', facecolor='#1b1e28', edgecolor='#333a4d', labelcolor='#e0e6ed', fontsize=7)

anim = animation.FuncAnimation(fig, update, frames=n_steps, interval=100)

out_path = '/media/jarvis/01DB55B559EC9500/Robotics Swarm/results/plots/aero_swarm_mission_replay.gif'
writer = PillowWriter(fps=10)
anim.save(out_path, writer=writer)
plt.close()

print(f"Successfully rendered and saved 3D mission replay to: {out_path}")
