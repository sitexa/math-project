
import matplotlib.pyplot as plt
import numpy as np

class InteractiveRotation:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.is_dragging = False

        # --- Fixed Points ---
        self.A = np.array([0, 4])
        self.B = np.array([4, 0])
        self.C = np.array([2, 2])

        # --- Draggable Point P and dependent Point E ---
        self.P = np.array([-2.0, 0]) # Initial position
        self.E = self.calculate_e(self.P)
        
        # --- Trace of E ---
        self.trace_x = [self.E[0]]
        self.trace_y = [self.E[1]]

        # --- Initialize plot elements ---
        self.init_plot()

        # --- Connect mouse events ---
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def calculate_e(self, p_point):
        """Calculates E by rotating P around C by -90 degrees (clockwise)."""
        # Vector CP
        vec_cp = p_point - self.C
        # Rotate vector CP 90 degrees counter-clockwise: (x, y) -> (-y, x)
        vec_ce = np.array([-vec_cp[1], vec_cp[0]])
        # E = C + CE
        return self.C + vec_ce

    def init_plot(self):
        # --- Lines ---
        self.line_ab, = self.ax.plot([self.A[0], self.B[0]], [self.A[1], self.B[1]], 'g-', label='Line AB')
        self.line_pc, = self.ax.plot([self.P[0], self.C[0]], [self.P[1], self.C[1]], 'b-', label='PC')
        self.line_ce, = self.ax.plot([self.C[0], self.E[0]], [self.C[1], self.E[1]], 'r-', label='CE (Rotated PC)')
        self.line_ae, = self.ax.plot([self.A[0], self.E[0]], [self.A[1], self.E[1]], 'k--')
        self.trace_line, = self.ax.plot(self.trace_x, self.trace_y, 'r:', label="E's Path")

        # --- Points ---
        self.ax.plot(self.A[0], self.A[1], 'ko')
        self.ax.plot(self.B[0], self.B[1], 'ko')
        self.ax.plot(self.C[0], self.C[1], 'ko')
        self.point_p, = self.ax.plot(self.P[0], self.P[1], 'bo', markersize=10, label='Drag P')
        self.point_e, = self.ax.plot(self.E[0], self.E[1], 'ro')

        # --- Text Labels ---
        self.ax.text(self.A[0], self.A[1] + 0.2, 'A')
        self.ax.text(self.B[0] + 0.2, self.B[1], 'B')
        self.ax.text(self.C[0] + 0.2, self.C[1] + 0.2, 'C')
        self.text_p = self.ax.text(self.P[0], self.P[1] - 0.5, 'P')
        self.text_e = self.ax.text(self.E[0] + 0.2, self.E[1], 'E')

        # --- Formatting ---
        self.ax.set_title('Interactive Rotation - Drag Point P on the x-axis')
        self.ax.set_xlabel('x-axis')
        self.ax.set_ylabel('y-axis')
        self.ax.axhline(0, color='black', linewidth=1)
        self.ax.axvline(0, color='black', linewidth=1)
        self.ax.grid(True, linestyle=':')
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(-15, 10)
        self.ax.set_ylim(-15, 10)
        self.ax.legend()

    def update_plot(self, p_x_coord):
        self.P = np.array([p_x_coord, 0])
        self.E = self.calculate_e(self.P)
        
        # Update lines
        self.line_pc.set_data([self.P[0], self.C[0]], [self.P[1], self.C[1]])
        self.line_ce.set_data([self.C[0], self.E[0]], [self.C[1], self.E[1]])
        self.line_ae.set_data([self.A[0], self.E[0]], [self.A[1], self.E[1]])
        
        # Update points
        self.point_p.set_data([self.P[0]], [self.P[1]])
        self.point_e.set_data([self.E[0]], [self.E[1]])
        
        # Update text
        self.text_p.set_position((self.P[0], self.P[1] - 0.5))
        self.text_e.set_position((self.E[0] + 0.2, self.E[1]))
        
        # Update trace
        self.trace_x.append(self.E[0])
        self.trace_y.append(self.E[1])
        self.trace_line.set_data(self.trace_x, self.trace_y)

        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        contains, _ = self.point_p.contains(event)
        if contains:
            self.is_dragging = True
            # Clear trace on new drag
            self.trace_x = [self.E[0]]
            self.trace_y = [self.E[1]]

    def on_motion(self, event):
        if not self.is_dragging or event.inaxes != self.ax: return
        self.update_plot(event.xdata)

    def on_release(self, event):
        self.is_dragging = False

    def show(self):
        plt.show()

if __name__ == '__main__':
    plot = InteractiveRotation()
    plot.show()
