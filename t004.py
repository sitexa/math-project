
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Arc

class InteractiveGeometry:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.is_dragging = False

        # --- Initial setup ---
        self.A = np.array([0, 4])
        self.B = np.array([4, 0])
        self.O = np.array([0, 0])
        
        # --- Draggable Point E ---
        self.E = np.array([0, 2.0]) # Initial position

        # --- Initialize all plot elements ---
        self.init_plot()

        # --- Connect mouse events to handlers ---
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def calculate_positions(self, e_coord):
        """Calculates C and D based on E's y-coordinate."""
        E = np.array([0, e_coord])
        # Avoid division by zero if E is at (0,0)
        if abs(E[0] - self.B[0]) < 1e-9:
            m_BE = 1e9
        else:
            m_BE = (E[1] - self.B[1]) / (E[0] - self.B[0])
        
        if abs(m_BE) < 1e-9:
             m_AC = 1e9
        else:
            m_AC = -1 / m_BE

        x_C = -4 / m_AC
        C = np.array([x_C, 0])

        x_D = (-4 - 4 * m_BE) / (m_AC - m_BE)
        y_D = m_AC * x_D + 4
        D = np.array([x_D, y_D])
        return E, C, D

    def init_plot(self):
        E, C, D = self.calculate_positions(self.E[1])

        # --- Draw Auxiliary Circle ---
        center_x = (C[0] + self.B[0]) / 2
        radius = np.linalg.norm(C - self.B) / 2
        self.circle = Circle((center_x, 0), radius, color='orange', fill=False, linestyle='-.', linewidth=1.5, label='Auxiliary Circle (C,O,D,B)')
        self.ax.add_patch(self.circle)

        # --- Draw Lines ---
        self.line_AC, = self.ax.plot([self.A[0], C[0]], [self.A[1], C[1]], 'm-')
        self.line_BE, = self.ax.plot([self.B[0], E[0]], [self.B[1], E[1]], 'b-')
        self.line_OD, = self.ax.plot([self.O[0], D[0]], [self.O[1], D[1]], 'k--')
        self.line_CD, = self.ax.plot([C[0], D[0]], [C[1], D[1]], 'k--')
        self.line_DB, = self.ax.plot([D[0], self.B[0]], [D[1], self.B[1]], 'k--')

        # --- Plot and Label Points ---
        self.point_A, = self.ax.plot(self.A[0], self.A[1], 'ko')
        self.point_B, = self.ax.plot(self.B[0], self.B[1], 'ko')
        self.point_O, = self.ax.plot(self.O[0], self.O[1], 'ko')
        self.point_E, = self.ax.plot(E[0], E[1], 'ro', markersize=10, label='Drag E') # Draggable point
        self.point_C, = self.ax.plot(C[0], C[1], 'ko')
        self.point_D, = self.ax.plot(D[0], D[1], 'ko')

        self.text_A = self.ax.text(self.A[0] - 0.2, self.A[1] + 0.2, 'A')
        self.text_B = self.ax.text(self.B[0] + 0.2, self.B[1] + 0.2, 'B')
        self.text_O = self.ax.text(self.O[0] - 0.2, self.O[1] - 0.3, 'O')
        self.text_E = self.ax.text(E[0] + 0.2, E[1], 'E')
        self.text_C = self.ax.text(C[0] - 0.2, C[1] - 0.3, 'C')
        self.text_D = self.ax.text(D[0] + 0.2, D[1] + 0.2, 'D')

        # --- Formatting ---
        self.ax.set_title('Interactive Geometry - Drag Point E')
        self.ax.set_xlabel('x-axis')
        self.ax.set_ylabel('y-axis')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle=':')
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-2, 6)
        self.ax.legend()

    def update_plot(self, e_coord):
        E, C, D = self.calculate_positions(e_coord)
        self.E = E

        # Update lines
        self.line_AC.set_data([self.A[0], C[0]], [self.A[1], C[1]])
        self.line_BE.set_data([self.B[0], E[0]], [self.B[1], E[1]])
        self.line_OD.set_data([self.O[0], D[0]], [self.O[1], D[1]])
        self.line_CD.set_data([C[0], D[0]], [C[1], D[1]])
        self.line_DB.set_data([D[0], self.B[0]], [D[1], self.B[1]])

        # Update points
        self.point_E.set_data([E[0]], [E[1]])
        self.point_C.set_data([C[0]], [C[1]])
        self.point_D.set_data([D[0]], [D[1]])

        # Update text
        self.text_E.set_position((E[0] + 0.2, E[1]))
        self.text_C.set_position((C[0] - 0.2, C[1] - 0.3))
        self.text_D.set_position((D[0] + 0.2, D[1] + 0.2))

        # Update circle
        center_x = (C[0] + self.B[0]) / 2
        radius = np.linalg.norm(C - self.B) / 2
        self.circle.set_center((center_x, 0))
        self.circle.set_radius(radius)

        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        contains, _ = self.point_E.contains(event)
        if contains:
            self.is_dragging = True

    def on_motion(self, event):
        if not self.is_dragging or event.inaxes != self.ax: return
        # Clamp E's movement to be on the y-axis between O and A
        y = event.ydata
        if 0.01 < y < 3.99: # Avoid placing E exactly on O or A
            self.update_plot(y)

    def on_release(self, event):
        self.is_dragging = False

    def show(self):
        plt.show()

# --- Main Execution ---
if __name__ == '__main__':
    plot = InteractiveGeometry()
    plot.show()
