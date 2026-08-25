import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Page config - Wide layout
st.set_page_config(page_title="Electric Field Simulator", page_icon="⚡", layout="wide")

# 2. Main layout: Equal columns
col_input, col_graph = st.columns(2, gap="large")

with col_input:
    # TRICK: Title ane caption ne left column ma mukya jethi height balance thay!
    st.title("⚡ Electric Field Streamlines")
    st.caption("Day 2 of 30: Physics Simulators Challenge")
    st.markdown("---")
    
    st.markdown("#### Adjust the Charges:")
    st.write("Slide to change the magnitude and sign (positive/negative) of the charges.")
    
    q1_val = st.slider("Charge 1 ($q_1$) in µC", -10.0, 10.0, 4.0, step=1.0)
    st.markdown("<br>", unsafe_allow_html=True)
    q2_val = st.slider("Charge 2 ($q_2$) in µC", -10.0, 10.0, -5.0, step=1.0)
    
    st.markdown("---")
    st.info("💡 **Physics Note:** Field lines originate from positive (Red) and terminate at negative (Blue) charges.")

# 3. Physics / Math Calculations
def e_field(q, x0, y0, X, Y):
    k = 8.99e9 
    Rx = X - x0
    Ry = Y - y0
    R_sq = Rx**2 + Ry**2 + 0.1 
    E_mag = k * q / R_sq
    Ex = E_mag * (Rx / np.sqrt(R_sq))
    Ey = E_mag * (Ry / np.sqrt(R_sq))
    return Ex, Ey

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

x1, y1 = -2.0, 0.0
x2, y2 = 2.0, 0.0

Ex1, Ey1 = e_field(q1_val * 1e-6, x1, y1, X, Y)
Ex2, Ey2 = e_field(q2_val * 1e-6, x2, y2, X, Y)
Ex = Ex1 + Ex2
Ey = Ey1 + Ey2

with col_graph:
    # 4. Plotting: Figsize ni height thodi nani kari (6, 5) jethi perfect fit thay
    fig, ax = plt.subplots(figsize=(6, 5))
    
    color_intensity = np.log(np.sqrt(Ex**2 + Ey**2))
    
    # cmap changed to 'plasma' for a better look on both light/dark modes
    ax.streamplot(X, Y, Ex, Ey, color=color_intensity, cmap='plasma', density=1.4, linewidth=1.2)
    
    c1_color = 'red' if q1_val > 0 else 'blue' if q1_val < 0 else 'gray'
    c2_color = 'red' if q2_val > 0 else 'blue' if q2_val < 0 else 'gray'
    
    # zorder=5 thi dots lines ni upar dekhase
    ax.plot(x1, y1, marker='o', color=c1_color, markersize=15, zorder=5)
    ax.plot(x2, y2, marker='o', color=c2_color, markersize=15, zorder=5)
    
    # FIXED: Text label ne thoda niche lya (y1 - 0.7) ane black bold text karyu (without box)
    ax.text(x1, y1 - 0.7, f"{q1_val} µC", color='black', ha='center', fontsize=12, fontweight='bold')
    ax.text(x2, y2 - 0.7, f"{q2_val} µC", color='black', ha='center', fontsize=12, fontweight='bold')

    # Graph Formatting
    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    
    st.pyplot(fig, use_container_width=True)
