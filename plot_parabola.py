import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider


# 二次曲线 y = a(x-h)**2 + k

# --- Initial Parameters ---
init_a = 1.0
init_h = 2.0
init_k = 1.0

# --- Create the figure and the main axes for the plot ---
fig, ax = plt.subplots(figsize=(8, 8))
# Adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.1, bottom=0.35)

# --- Generate initial data ---
x = np.linspace(-10, 10, 400)
y = init_a * (x - init_h)**2 + init_k

# --- Plot the initial parabola ---
line, = ax.plot(x, y, lw=2, color='blue')
vertex_dot, = ax.plot(init_h, init_k, 'ro') # Mark the vertex

# --- Set plot properties ---
ax.set_title('Interactive Parabola: y = a(x - h)^2 + k')
ax.set_xlabel('x-axis')
ax.set_ylabel('y-axis')
ax.grid(True)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)
ax.set_xlim([-10, 10])
ax.set_ylim([-10, 10])
ax.set_aspect('equal', adjustable='box')

# Add a text label for the vertex, which we will update
vertex_text = ax.text(init_h, init_k, f'  ({init_h:.2f}, {init_k:.2f})', verticalalignment='bottom')

# --- Create axes for the sliders ---
ax_a = plt.axes([0.15, 0.20, 0.65, 0.03])
ax_h = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_k = plt.axes([0.15, 0.10, 0.65, 0.03])

# --- Create the Slider widgets ---
slider_a = Slider(
    ax=ax_a,
    label='a',
    valmin=-5.0,
    valmax=5.0,
    valinit=init_a
)

slider_h = Slider(
    ax=ax_h,
    label='h (vertex x)',
    valmin=-10.0,
    valmax=10.0,
    valinit=init_h
)

slider_k = Slider(
    ax=ax_k,
    label='k (vertex y)',
    valmin=-10.0,
    valmax=10.0,
    valinit=init_k
)

# --- The update function. This is called whenever a slider's value changes. ---
def update(val):
    # Get the current values from the sliders
    a = slider_a.val
    h = slider_h.val
    k = slider_k.val
    
    # Recalculate the y-values
    new_y = a * (x - h)**2 + k
    
    # Update the line data
    line.set_ydata(new_y)
    
    # Update the vertex marker's position
    vertex_dot.set_data([h], [k])
    
    # Update the vertex text label
    vertex_text.set_position((h, k))
    vertex_text.set_text(f'  ({h:.2f}, {k:.2f})')
    
    # Redraw the canvas
    fig.canvas.draw_idle()

# --- Register the update function with each slider ---
slider_a.on_changed(update)
slider_h.on_changed(update)
slider_k.on_changed(update)

# Display the plot
plt.show()