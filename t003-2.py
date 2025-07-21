
import matplotlib.pyplot as plt
import numpy as np

def plot_static_figure():
    """Plots the geometric figure for question (2) with auxiliary lines."""
    # --- Define initial points from the problem ---
    A = np.array([0, 3])
    B = np.array([-2, 0])
    D = np.array([3, 0])
    C = np.array([1, -2])
    P = np.array([1, 0]) # From CP perpendicular to OD
    O = np.array([0, 0])

    # --- Calculate Q ---
    # Line CD: y = x - 3
    # Line AP slope: (0-3)/(1-0) = -3
    # Line PQ slope: 1/3
    # Line PQ: y = (1/3)(x-1)
    # x - 3 = (1/3)x - 1/3  => (2/3)x = 8/3 => x=4
    # y = 4 - 3 = 1
    Q = np.array([4, 1])

    # --- Create the plot ---
    fig, ax = plt.subplots(figsize=(9, 9))

    # --- Draw main lines and polygons ---
    # Draw quadrilateral ABCD
    quad = np.array([A, B, C, D, A])
    ax.plot(quad[:, 0], quad[:, 1], 'k-', label='Quadrilateral ABCD')
    # Draw line CDQ
    ax.plot([C[0], Q[0]], [C[1], Q[1]], 'g-', label='Line CDQ')
    # Draw triangle APQ
    tri_apq = np.array([A, P, Q, A])
    ax.plot(tri_apq[:, 0], tri_apq[:, 1], 'r-', label='△APQ')

    # --- Draw Auxiliary Lines for Proof ---
    # Line from A to P (hypotenuse of AOP)
    ax.plot([A[0], P[0]], [A[1], P[1]], 'r--')
    # Line from P to Q (hypotenuse of PQM, where M is (4,0))
    ax.plot([P[0], Q[0]], [P[1], Q[1]], 'r--')
    # Perpendicular from Q to x-axis
    M = np.array([Q[0], 0])
    ax.plot([Q[0], M[0]], [Q[1], M[1]], 'b--', label='Auxiliary Line QM')

    # --- Plot and Label Points ---
    points = {'A': A, 'B': B, 'C': C, 'D': D, 'P': P, 'Q': Q, 'O': O, 'M': M}
    for name, pos in points.items():
        ax.plot(pos[0], pos[1], 'ko')
        ax.text(pos[0], pos[1] + 0.2, name, fontsize=14, ha='center')

    # --- Add annotations and symbols ---
    # Right angle for APQ
    vec_PA = (A - P) / np.linalg.norm(A - P)
    vec_PQ = (Q - P) / np.linalg.norm(Q - P)
    p_perp = P + vec_PA * 0.4 + vec_PQ * 0.4
    ax.plot([P[0] + vec_PA[0]*0.4, p_perp[0]], [P[1] + vec_PA[1]*0.4, p_perp[1]], 'r', lw=1)
    ax.plot([P[0] + vec_PQ[0]*0.4, p_perp[0]], [P[1] + vec_PQ[1]*0.4, p_perp[1]], 'r', lw=1)
    # Right angle for QMP
    ax.plot([M[0], M[0]-0.2], [M[1], M[1]+0.2], 'b', lw=1)
    ax.plot([M[0]-0.2, M[0]-0.2], [M[1], M[1]+0.2], 'b', lw=1)

    # --- Formatting ---
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.grid(True, linestyle=':')
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Geometric Figure for t25-3 (Question 2)')
    ax.set_xlabel('x-axis')
    ax.set_ylabel('y-axis')
    ax.legend()
    plt.show()

# --- Main Execution ---
if __name__ == '__main__':
    plot_static_figure()
