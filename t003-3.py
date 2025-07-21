
import matplotlib.pyplot as plt
import numpy as np

class InteractiveProblem3:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.is_dragging = False

        # --- Fixed Points ---
        self.A = np.array([0, 3])
        self.B = np.array([-2, 0])
        self.C = np.array([1, -2])
        self.D = np.array([3, 0])

        # --- Draggable Point P and dependent points ---
        self.P = np.array([5.0, 0]) # Initial position
        self.Q, self.F, self.F_prime = self.update_dependent_points(self.P)

        # --- Initialize plot elements ---
        self.init_plot()

        # --- Connect mouse events ---
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)

    def update_dependent_points(self, p_point):
        # 1. Calculate Q
        k_ap = (p_point[1] - self.A[1]) / (p_point[0] - self.A[0])
        k_pq = -1 / k_ap
        # Line PQ: y - p_y = k_pq * (x - p_x) => y = k_pq * (x - p_point[0])
        # Line CD: y = x - 3 (slope is 1)
        # k_pq * (x_q - p_point[0]) = x_q - 3
        # k_pq*x_q - k_pq*p_point[0] = x_q - 3
        # x_q * (k_pq - 1) = k_pq*p_point[0] - 3
        x_q = (k_pq * p_point[0] - 3) / (k_pq - 1)
        y_q = x_q - 3
        Q = np.array([x_q, y_q])

        # 2. Calculate F
        k_bq = (Q[1] - self.B[1]) / (Q[0] - self.B[0])
        # From tan(45)=1, we get k_bf = (k_bq - 1) / (k_bq + 1) or (k_bq+1)/(1-k_bq)
        # We test both to find the one on the correct side of the line
        k_bf1 = (k_bq - 1) / (k_bq + 1)
        k_bf2 = (k_bq + 1) / (1 - k_bq)
        # Line DA: y = -x + 3
        # Line BF: y = k_bf * (x + 2)
        # -x + 3 = k_bf*x + 2*k_bf => x(-1-k_bf) = 2*k_bf - 3 => x = (3-2k_bf)/(1+k_bf)
        x_f1 = (3 - 2*k_bf1) / (1 + k_bf1)
        x_f2 = (3 - 2*k_bf2) / (1 + k_bf2)
        # F must be on DA extension, so x_f < 0
        x_f = x_f1 if x_f1 < 0 else x_f2
        y_f = -x_f + 3
        F = np.array([x_f, y_f])

        # 3. Calculate F_prime (F rotated -90 deg around B)
        vec_bf = F - self.B
        vec_bf_rotated = np.array([vec_bf[1], -vec_bf[0]]) # (x,y) -> (y,-x) for -90 deg
        F_prime = self.B + vec_bf_rotated
        
        return Q, F, F_prime

    def init_plot(self):
        # --- Main Lines ---
        self.line_cdq, = self.ax.plot([self.C[0], self.Q[0]], [self.C[1], self.Q[1]], 'g-', label='Line CDQ')
        self.line_ap, = self.ax.plot([self.A[0], self.P[0]], [self.A[1], self.P[1]], 'r--')
        self.line_pq, = self.ax.plot([self.P[0], self.Q[0]], [self.P[1], self.Q[1]], 'r--')
        self.line_bq, = self.ax.plot([self.B[0], self.Q[0]], [self.B[1], self.Q[1]], 'b-', label='BQ')
        self.line_bf, = self.ax.plot([self.B[0], self.F[0]], [self.B[1], self.F[1]], 'b--', label='BF')
        self.line_qf, = self.ax.plot([self.Q[0], self.F[0]], [self.Q[1], self.F[1]], 'b-', lw=2, label='QF')
        self.line_da, = self.ax.plot([self.D[0], self.A[0]], [self.D[1], self.A[1]], 'k-')
        self.line_ab, = self.ax.plot([self.A[0], self.B[0]], [self.A[1], self.B[1]], 'k-', label='Line AB')
        self.line_af, = self.ax.plot([self.A[0], self.F[0]], [self.A[1], self.F[1]], 'k-') # Extension to F

        # --- Auxiliary Proof Lines ---
        self.line_cbf_prime, = self.ax.plot([self.C[0], self.B[0], self.F_prime[0]], [self.C[1], self.B[1], self.F_prime[1]], 'm--', label="CBF' (Rotated ABF)")
        self.line_qcf_prime, = self.ax.plot([self.Q[0], self.C[0], self.F_prime[0]], [self.Q[1], self.C[1], self.F_prime[1]], 'm:', lw=3, label="Line QCF'")

        # --- Points and Labels ---
        points = {'A': self.A, 'B': self.B, 'C': self.C, 'D': self.D}
        for name, pos in points.items(): self.ax.plot(pos[0], pos[1], 'ko'); self.ax.text(pos[0], pos[1]+0.3, name)
        self.point_p, = self.ax.plot(self.P[0], self.P[1], 'ro', markersize=10, label='Drag P')
        self.point_q, = self.ax.plot(self.Q[0], self.Q[1], 'go'); self.text_q = self.ax.text(self.Q[0], self.Q[1]+0.3, 'Q')
        self.point_f, = self.ax.plot(self.F[0], self.F[1], 'bo'); self.text_f = self.ax.text(self.F[0], self.F[1]+0.3, 'F')
        self.point_f_prime, = self.ax.plot(self.F_prime[0], self.F_prime[1], 'mo'); self.text_f_prime = self.ax.text(self.F_prime[0], self.F_prime[1]+0.3, "F'")

        # --- Formatting ---
        self.ax.set_title('Interactive Proof for Q3 - Drag Point P')
        self.ax.set_xlabel('x-axis'); self.ax.set_ylabel('y-axis')
        self.ax.axhline(0, color='black'); self.ax.axvline(0, color='black')
        self.ax.grid(True, linestyle=':'); self.ax.set_aspect('equal')
        self.ax.set_xlim(-10, 15); self.ax.set_ylim(-10, 15)
        self.ax.legend(fontsize='small')

    def update_plot(self, p_x_coord):
        self.P = np.array([p_x_coord, 0])
        self.Q, self.F, self.F_prime = self.update_dependent_points(self.P)

        # Update lines
        self.line_cdq.set_data([self.C[0], self.Q[0]], [self.C[1], self.Q[1]])
        self.line_ap.set_data([self.A[0], self.P[0]], [self.A[1], self.P[1]])
        self.line_pq.set_data([self.P[0], self.Q[0]], [self.P[1], self.Q[1]])
        self.line_bq.set_data([self.B[0], self.Q[0]], [self.B[1], self.Q[1]])
        self.line_bf.set_data([self.B[0], self.F[0]], [self.B[1], self.F[1]])
        self.line_qf.set_data([self.Q[0], self.F[0]], [self.Q[1], self.F[1]])
        self.line_af.set_data([self.A[0], self.F[0]], [self.A[1], self.F[1]])
        self.line_cbf_prime.set_data(*zip(self.C, self.B, self.F_prime))
        self.line_qcf_prime.set_data(*zip(self.Q, self.C, self.F_prime))

        # Update points and text
        self.point_p.set_data([self.P[0]], [self.P[1]])
        for point, text, name in [(self.point_q, self.text_q, 'Q'), (self.point_f, self.text_f, 'F'), (self.point_f_prime, self.text_f_prime, "F'")]:
            attr_name = name.replace("'", "_prime")
            point_coords = getattr(self, attr_name)
            point.set_data([point_coords[0]], [point_coords[1]])
            text.set_position((point_coords[0], point_coords[1] + 0.3))

        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax: return
        contains, _ = self.point_p.contains(event)
        if contains: self.is_dragging = True

    def on_motion(self, event):
        if not self.is_dragging or event.inaxes != self.ax: return
        if event.xdata > self.D[0]: self.update_plot(event.xdata)

    def on_release(self, event):
        self.is_dragging = False

    def show(self):
        plt.show()

if __name__ == '__main__':
    plot = InteractiveProblem3()
    plot.show()
