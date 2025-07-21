import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = 'Heiti TC'

# --- 1. 定义点和线 ---
# E点作为原点
E = np.array([0.0, 0.0])

# AB线是x轴
# CD线平行于AB，假设在y=-5的位置
CD_y = -5.0

# 直线PQ与AB交于E，与CD交于F
# ∠PEB = 58度。PE是∠MEB的角平分线。
# 假设P在E的右上方，Q在E的左下方。
# PQ与AB的夹角是 58度 (与EB方向的夹角)
# 那么PQ的斜率是 tan(180 - 58) = tan(122)
angle_peb_rad = np.deg2rad(58)
angle_pq_from_positive_x_axis = np.deg2rad(180 - 58) # PQ与AB的夹角，假设P在上方

# F点在CD上，是PQ与CD的交点
# 直线方程 y - y1 = m(x - x1)
# y - 0 = tan(angle_pq_from_positive_x_axis) * (x - 0)
# 当 y = CD_y 时，x = CD_y / tan(angle_pq_from_positive_x_axis)
F_x = CD_y / np.tan(angle_pq_from_positive_x_axis)
F = np.array([F_x, CD_y])

# M点在AB上方，PE平分∠MEB
# ∠MEB = 2 * ∠PEB = 116度
# PE与EB的夹角是58度。ME与EB的夹角是116度。
# 假设M在E的左上方，那么ME与正x轴的夹角是 180 - 116 = 64度
angle_meb_rad = np.deg2rad(116)
angle_me_from_positive_x_axis = np.deg2rad(180 - 116) # M在E的左上方

# 假设ME长度为5
ME_length = 5
M = E + ME_length * np.array([np.cos(angle_me_from_positive_x_axis), np.sin(angle_me_from_positive_x_axis)])

# N点在CD上
# MN交AB于H
# ∠NHE = 109度。H在AB上。
# H点的位置需要通过MN和AB的交点来确定。
# 这是一个反推的过程，为了绘图方便，我们先假设H点，然后确定N点。
# 假设H在E的左侧，距离E为2
H = np.array([-2.0, 0.0])

# 直线MN通过M和H
# N点是直线MH与CD的交点
# 直线MH的斜率 m_mh = (M[1] - H[1]) / (M[0] - H[0])
m_mh = (M[1] - H[1]) / (M[0] - H[0])
# 直线MH的方程 y - H[1] = m_mh * (x - H[0])
# 当 y = CD_y 时，x = (CD_y - H[1]) / m_mh + H[0]
N_x = (CD_y - H[1]) / m_mh + H[0]
N = np.array([N_x, CD_y])

# --- 2. 绘制图形 ---
fig, ax = plt.subplots(figsize=(10, 8))

# 绘制平行线 AB 和 CD
ax.plot([-10, 10], [0, 0], 'k-', linewidth=1.5, label='AB')
ax.plot([-10, 10], [CD_y, CD_y], 'k-', linewidth=1.5, label='CD')

# 绘制直线 PQ
# P点和Q点，取足够远
P_x = E[0] + 10 * np.cos(angle_pq_from_positive_x_axis)
P_y = E[1] + 10 * np.sin(angle_pq_from_positive_x_axis)
Q_x = E[0] - 10 * np.cos(angle_pq_from_positive_x_axis)
Q_y = E[1] - 10 * np.sin(angle_pq_from_positive_x_axis)
ax.plot([Q_x, P_x], [Q_y, P_y], 'k--', linewidth=1, label='PQ')

# 绘制线段 ME, MN
ax.plot([E[0], M[0]], [E[1], M[1]], 'b-', linewidth=2, label='ME')
ax.plot([M[0], N[0]], [M[1], N[1]], 'g-', linewidth=2, label='MN')

# 绘制点
points = {'A': np.array([-8, 0]), 'B': np.array([8, 0]), 'C': np.array([-8, CD_y]), 'D': np.array([8, CD_y]),
          'E': E, 'F': F, 'M': M, 'N': N, 'H': H}

for name, coord in points.items():
    ax.plot(coord[0], coord[1], 'ko', markersize=5)
    ax.text(coord[0] + 0.2, coord[1] + 0.2, name, fontsize=12)

# 标注P和Q点
ax.text(P_x + 0.2, P_y + 0.2, 'P', fontsize=12)
ax.text(Q_x - 0.5, Q_y - 0.5, 'Q', fontsize=12)


# --- 3. 标注角度 ---

# 辅助函数：绘制角度弧线
def draw_angle_arc(ax, center, p1, p2, radius, text, text_offset=0.5):
    v1 = p1 - center
    v2 = p2 - center
    angle1 = np.arctan2(v1[1], v1[0])
    angle2 = np.arctan2(v2[1], v2[0])

    # 确保角度是顺时针或逆时针的正确范围
    if angle2 < angle1:
        angle2 += 2 * np.pi

    # 绘制弧线
    arc = plt.matplotlib.patches.Arc(center, 2 * radius, 2 * radius,
                                     angle=0, theta1=np.degrees(angle1), theta2=np.degrees(angle2),
                                     color='red', linewidth=1)
    ax.add_patch(arc)

    # 标注角度文本
    mid_angle = (angle1 + angle2) / 2
    text_x = center[0] + (radius + text_offset) * np.cos(mid_angle)
    text_y = center[1] + (radius + text_offset) * np.sin(mid_angle)
    ax.text(text_x, text_y, text, color='red', fontsize=10, ha='center', va='center')

# 标注 ∠PEB = 58°
# P点在E的右上方，B点在E的右侧
# 为了画弧线，需要一个在PE方向上的点和在EB方向上的点
# PE方向上的点
P_on_line = E + np.array([np.cos(angle_pq_from_positive_x_axis), np.sin(angle_pq_from_positive_x_axis)]) * 1
# EB方向上的点
B_on_line = E + np.array([1, 0]) * 1
draw_angle_arc(ax, E, P_on_line, B_on_line, 0.8, '58°')

# 标注 ∠NHE = 109°
# N点，H点，E点
# N在H的左下方，E在H的右侧
# HN方向上的点
N_on_line = H + (N - H) / np.linalg.norm(N - H) * 1
# HE方向上的点
E_on_line = H + (E - H) / np.linalg.norm(E - H) * 1
draw_angle_arc(ax, H, N_on_line, E_on_line, 0.8, '109°')

# 标注 ∠M = 51°
# E点，M点，H点
# ME方向上的点
E_for_M = M + (E - M) / np.linalg.norm(E - M) * 1
# MH方向上的点
H_for_M = M + (H - M) / np.linalg.norm(H - M) * 1
draw_angle_arc(ax, M, E_for_M, H_for_M, 0.8, '51°')


# 设置图表属性
ax.set_aspect('equal', adjustable='box')
ax.set_xlim(-10, 10)
ax.set_ylim(-7, 7)
ax.set_title('几何题目 (1) 示意图')
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()
plt.show()