# Comprehensive Research & Implementation Plan: Resilient & Heterogeneous Drone Swarms

## 1. Research Overview & Problem Statement
**Title Idea:** *A Decentralized Hybrid Edge-MARL Framework for Resilient Coordination of Heterogeneous Drone Swarms in GPS-Denied and Jamming Environments*

### Research Gaps Addressed:
1. **Resilient Swarm Communication:** Designing a decentralized protocol that handles signal jamming, packet loss, and dynamic node failure without a central controller or GPS.
2. **Heterogeneous Task Allocation & Edge Optimization:** Coordinating drones with different capabilities (e.g., high-compute leader drones vs. lightweight scout drones) while minimizing latency and energy consumption.

---

## 2. Hardware Optimization Strategy (For Your Specs)
**Your Specs:** i5 13th Gen U-Processor | 16GB RAM | 4GB RTX 2050 GPU | Linux (Ubuntu)

* **Challenge:** Running 100+ drones with full 3D rendering in Gazebo will crash the system.
* **Solution (Dual-Tier Simulation):**
  1. **High-Fidelity Physics Tier (10–15 Drones):** Use **ROS 2 + Gazebo (Headless Mode)** + **PX4 SITL** to validate aerodynamics, sensor fusion, and low-level control.
  2. **Large-Scale Swarm Tier (100–500 Drones):** Use **Gym-PyBullet-Drones** or a custom lightweight **Python/C++ 3D Kinematic Simulator** integrated with **NS-3** (Network Simulator) to prove scalability, MARL convergence, and network resilience for top-tier journals.

---

## 3. Step-by-Step Linux Setup & Installation Guide
*(Assuming Ubuntu 22.04 LTS - Jammy Jellyfish, which is standard for ROS 2 Humble)*

### Step 3.1: Install ROS 2 Humble
Open your terminal and run the following commands:
```bash
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade -y
sudo apt install ros-humble-desktop python3-argcomplete python3-colcon-common-extensions -y
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### Step 3.2: Install Gazebo & PX4 Autopilot (For Multi-UAV Physics)
```bash
# Clone PX4 Autopilot
git clone https://github.com/PX4/PX4-Autopilot.git --recursive
bash ./PX4-Autopilot/Tools/setup/ubuntu.sh

# Install Micro XRCE-DDS Agent (Bridges PX4 and ROS 2)
git clone https://github.com/eProsima/Micro-XRCE-DDS-Agent.git
cd Micro-XRCE-DDS-Agent
mkdir build && cd build
cmake ..
make
sudo make install
sudo ldconfig /usr/local/lib/
```

### Step 3.3: Install Lightweight Swarm Simulator & ML Environment (For 100+ Drones)
To train Machine Learning models on your RTX 2050 (4GB VRAM) and simulate 100+ drones:
```bash
# Install Miniconda or Python Virtual Env
sudo apt install python3-pip python3-venv -y
python3 -m venv ~/swarm_env
source ~/swarm_env/bin/activate

# Install PyTorch (CUDA supported for RTX 2050)
pip install torch torchvision torchaudio --index-index-url https://download.pytorch.org/whl/cu118

# Install Gym-PyBullet-Drones (Lightweight multi-drone simulator)
git clone https://github.com/utiasDSL/gym-pybullet-drones.git
cd gym-pybullet-drones
pip install -e .

# Install RL and Graph Neural Network libraries
pip install stable-baselines3 ray[rllib] torch-geometric networkx matplotlib pandas
```

### Step 3.4: Install NS-3 (For Network & Jamming Simulation)
```bash
sudo apt install g++ python3 cmake ninja-build git ccache -y
git clone https://gitlab.com/nsnam/ns-3-dev.git
cd ns-3-dev
./ns3 configure --enable-examples --enable-tests
./ns3 build
```

---

## 4. State-of-the-Art (SOTA) Baseline Models for Comparison
Top-tier journals (like *IEEE Transactions on Robotics*, *IEEE IoT Journal*, or *Robotics and Autonomous Systems*) require rigorous comparison against existing algorithms. You will compare your new model against these **3 Categories**:

### A. Multi-Agent Reinforcement Learning (MARL) Baselines
1. **MAPPO (Multi-Agent Proximal Policy Optimization):** Current SOTA for cooperative navigation. *Weakness:* High communication overhead during centralized training/execution in jamming zones.
2. **QMIX:** Value-based MARL method. *Weakness:* Struggles with non-stationary environments when drones drop out.
3. **MADDPG (Multi-Agent Deep Deterministic Policy Gradient):** Good for continuous control. *Weakness:* Scales poorly past 20–30 agents.

### B. Task Allocation & Swarm Control Baselines
1. **CBBA (Consensus-Based Bundle Algorithm):** The gold standard for decentralized task allocation. *Weakness:* High latency when network topology changes rapidly.
2. **Olfati-Saber Flocking / Artificial Potential Fields (APF):** Classical control baseline for obstacle avoidance. *Weakness:* Gets stuck in local minima in complex environments.

### C. Network Routing Baselines (For Resilience)
1. **AODV (Ad-hoc On-Demand Distance Vector) & OLSR (Optimized Link State Routing):** Standard MANET protocols to compare against your adaptive communication layer.

---

## 5. Proposed Architecture: Your New Custom Model
Name your framework something impactful, e.g., **AERO-Swarm** (*Adaptive Edge-Resilient Optimization for Heterogeneous Swarms*).

### Core Components to Build from Scratch:
1. **Spatio-Temporal Graph Attention Network (ST-GAT):**
   * Models the swarm as a dynamic graph $G = (V, E)$, where nodes $V$ are heterogeneous drones and edges $E$ are communication links.
   * Automatically filters out jammed or noisy communication channels using attention weights $\alpha_{ij}$.
2. **Event-Triggered Decentralized Communication (ETDC):**
   * Instead of broadcasting states every millisecond, drones only transmit data when their state prediction error exceeds a threshold:
     $$\| x_i(t) - \hat{x}_i(t) \| > \delta$$
   * **Result:** Reduces bandwidth usage by 60–80% and lowers latency.
3. **Energy & Compute-Aware Auction Mechanism:**
   * integrates with the MARL policy to assign heavy tasks (like SLAM mapping) to high-compute drones and simple tasks (like perimeter coverage) to low-compute drones.

---

## 6. Experimental Scenarios & Evaluation Metrics

### Scenarios to Simulate:
1. **Scenario 1: Progressive Signal Jamming (GPS-Denied):** A jammer blocks 20%, 50%, and 80% of communication links in an urban canyon.
2. **Scenario 2: Dynamic Attrition (Node Failure):** 30% of the swarm is randomly destroyed mid-mission; the remaining drones must dynamically re-allocate tasks.
3. **Scenario 3: Scalability Stress Test:** Testing computation time and convergence across $N = \{10, 25, 50, 100, 200\}$ drones.

### Quantitative Metrics to Plot (For Paper Graphs):
* **End-to-End Latency ($\text{ms}$):** Time taken to reach consensus during jamming.
* **Packet Delivery Ratio (PDR %):** Communication reliability under attack.
* **Task Completion Rate (%) & Time ($T_{\text{complete}}$):** Efficiency of heterogeneous allocation.
* **Collision Rate:** Number of inter-drone or obstacle collisions.
* **Computational Overhead:** CPU/GPU utilization and energy consumed per drone (in Joules).

---

## 7. Execution Roadmap (Phase-by-Phase)

* **Phase 1 (Weeks 1–2): Setup & Baseline Reproduction**
  * Install Ubuntu packages, ROS 2, and `gym-pybullet-drones`.
  * Run standard MAPPO and CBBA code from open-source repositories and log their baseline metrics.
* **Phase 2 (Weeks 3–4): Environment & Jamming Modeling**
  * Create a custom OpenAI Gym/PettingZoo environment that simulates heterogeneous drones, obstacles, and a probabilistic communication jamming model (Rayleigh fading + signal noise).
* **Phase 3 (Weeks 5–7): Custom Algorithm Development**
  * Code the Graph Attention Network (GAT) + Event-Triggered Communication module in PyTorch.
  * Train the model on your RTX 2050 using lightweight kinematic physics.
* **Phase 4 (Weeks 8–9): ROS 2 / Gazebo Validation**
  * Export the trained PyTorch policy (`.pt` file) into a ROS 2 node.
  * Test it on 10–12 drones in Gazebo (headless mode) to prove real-world physics compatibility (Sim-to-Real readiness).
* **Phase 5 (Week 10): Data Analysis & Paper Writing**
  * Generate high-resolution plots using `matplotlib` / `seaborn` and write the manuscript in LaTeX (IEEE format).