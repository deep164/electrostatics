import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. Page config - Wide layout for YouTube recording
st.set_page_config(page_title="Electric Field Simulator", page_icon="⚡", layout="wide")

st.title("⚡ Electric Field Streamlines")
st.caption("Day 2 of 30: Physics Simulators Challenge")
st.markdown("---")

# 2. Equal 50-50 columns with a gap
col_input, col_graph = st.columns(2, gap="large")

with col_input:
    st.markdown("#### Adjust the Charges:")
    st.write("Slide to change the magnitude and sign (positive/negative) of the charges.")
    
    st.subheader("Charge 1 ($q_1$)")
    q1_val = st.slider("q1 (µC)", -10.0, 10.0, 5.0, step=1.0)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.subheader("Charge 2 ($q_2$)")
    q2_val = st.slider("q2 (µC)", -10.0, 10.0, -5.0, step=1.0)
    
    st.markdown("---")
    st.info("💡 **Physics Note:** Field lines originate from positive (Red) charges and terminate at negative (Blue) charges. If both have the same sign, you will see a 'null point' in the middle!")

# 3. Physics / Math Calculations for Electric Field
def e_field(q, x0, y0, X, Y):
    k = 8.99e9  # Coulomb's constant
    Rx = X - x0
    Ry = Y - y0
    R_sq = Rx**2 + Ry**2 + 0.1 # Added 0.1 to avoid division by zero at the charge center
    E_mag = k * q / R_sq
    Ex = E_mag * (Rx / np.sqrt(R_sq))
    Ey = E_mag * (Ry / np.sqrt(R_sq))
    return Ex, Ey

# Create a 2D grid
x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)

# Fixed positions for the charges on the X-axis
x1, y1 = -2.0, 0.0
x2, y2 = 2.0, 0.0

# Calculate total Electric Field by superposition
Ex1, Ey1 = e_field(q1_val * 1e-6, x1, y1, X, Y)
Ex2, Ey2 = e_field(q2_val * 1e-6, x2, y2, X, Y)
Ex = Ex1 + Ex2
Ey = Ey1 + Ey2

with col_graph:
    # 4. Plotting the Streamlines
    fig, ax = plt.subplots(figsize=(6, 6))
    
    # Calculate intensity for color mapping
    color_intensity = np.log(np.sqrt(Ex**2 + Ey**2))
    
    # Streamplot generates continuous flowing lines
    ax.streamplot(X, Y, Ex, Ey, color=color_intensity, cmap='inferno', density=1.5, linewidth=1.2)
    
    # Plot the charge points
    c1_color = 'red' if q1_val > 0 else 'blue' if q1_val < 0 else 'gray'
    c2_color = 'red' if q2_val > 0 else 'blue' if q2_val < 0 else 'gray'
    
    ax.plot(x1, y1, marker='o', color=c1_color, markersize=15)
    ax.plot(x2, y2, marker='o', color=c2_color, markersize=15)
    
    # Add text labels for the charges
    ax.text(x1, y1+0.6, f"{q1_val} µC", color='white', ha='center', fontsize=9, bbox=dict(facecolor='black', alpha=0.6, edgecolor='none'))
    ax.text(x2, y2+0.6, f"{q2_val} µC", color='white', ha='center', fontsize=9, bbox=dict(facecolor='black', alpha=0.6, edgecolor='none'))

    # Graph Formatting
    ax.set_aspect('equal')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis('off') # Turning off axes lines makes the streamplot look much cleaner
    
    # Display in the right column, filling the space
    st.pyplot(fig, use_container_width=True)
