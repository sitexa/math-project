import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import Polygon

# --- 字体设置函数 ---
def set_chinese_font():
    """
    自动查找并设置可用的中文字体。
    """
    font_names = ['Heiti TC', 'Arial Unicode MS', 'STHeiti', 'SimHei']
    found_font = next((name for name in font_names if fm.findfont(name, fallback_to_default=False)), None)
    if found_font:
        print(f"找到可用中文字体: {found_font}")
        plt.rcParams['font.sans-serif'] = [found_font]
    else:
        print("警告: 未找到指定的中文字体。图例和标题可能显示为方框。")
    plt.rcParams['axes.unicode_minus'] = False

# --- 调用字体设置 ---
set_chinese_font()

# 1. --- 初始几何设置 ---
C = np.array([0, 0])
A = np.array([4, 0])
B = np.array([0, 4])
N = np.array([0, -4]) # N点是固定的
m_initial = 6.0

# 2. --- 创建图形和坐标轴 ---
fig, ax = plt.subplots(figsize=(10, 10)) # 稍微调整画布大小
plt.subplots_adjust(top=0.88, bottom=0.1) # 调整顶部和底部边距

# --- 添加问题描述 ---
problem_text = (
    '如图2, 点M为线段CA延长线上一点, 过点A作AQ⊥AB, 过点M作BM的垂线交AQ于点P,\n'
    '线段PA的延长线与线段BC的延长线交于点N, 是否存在点M, 使S△AMP = (3/2)S△AMN,\n'
    '若存在, 求CM的长; 若不存在, 请说明理由.'
)
fig.suptitle(problem_text, fontsize=13, y=0.97, va='top')

ax.set_aspect('equal', adjustable='box')
ax.grid(True, linestyle='--')
# ax.set_title("问题 (2) 的动态几何演示 (可拖动M点)", fontsize=16) # 由 suptitle 代替
ax.set_xlabel("X轴")
ax.set_ylabel("Y轴")
ax.set_xlim(-5, 15)
ax.set_ylim(-5, 15)

# 3. --- 绘制静态元素和标签 ---
ax.plot(A[0], A[1], 'ko', markersize=8, label='点 A')
ax.text(A[0] + 0.2, A[1] + 0.2, 'A', fontsize=14, color='black', va='bottom')
ax.plot(B[0], B[1], 'ko', markersize=8, label='点 B')
ax.text(B[0] + 0.2, B[1] + 0.2, 'B', fontsize=14, color='black', va='bottom')
ax.plot(C[0], C[1], 'ko', markersize=8, label='点 C')
ax.text(C[0] - 0.5, C[1] - 0.2, 'C', fontsize=14, color='black', va='top', ha='right')
ax.plot(N[0], N[1], 'go', markersize=8, label='点 N')
ax.text(N[0] + 0.2, N[1], 'N', fontsize=14, color='green', va='center')

ax.plot([A[0], B[0], C[0], A[0]], [A[1], B[1], C[1], A[1]], 'k-', label='△ABC')
ax.plot([C[0], N[0]], [C[1], N[1]], 'g--', lw=1.5, label='线段 CN')
ax.plot([A[0], N[0]], [A[1], N[1]], 'g--', lw=1.5, label='线段 AN')
ax.axhline(0, color='gray', linestyle='--', lw=0.5)
ax.axvline(0, color='gray', linestyle='--', lw=0.5)

# 4. --- 绘制动态元素 (初始化) ---
M_init = np.array([m_initial, 0])
P_init = np.array([m_initial + 4, m_initial])

poly_pam = Polygon([A, M_init, P_init], facecolor='cyan', alpha=0.4, zorder=0)
poly_amn = Polygon([A, M_init, N], facecolor='yellow', alpha=0.4, zorder=0)
ax.add_patch(poly_pam)
ax.add_patch(poly_amn)

point_m_plot, = ax.plot(M_init[0], M_init[1], 'ro', markersize=10, label='动点 M (可拖动)')
point_p_plot, = ax.plot(P_init[0], P_init[1], 'bo', markersize=8, label='动点 P')
line_bm_plot, = ax.plot([B[0], M_init[0]], [B[1], M_init[1]], 'r--', label='线段 BM')
line_mp_plot, = ax.plot([M_init[0], P_init[0]], [M_init[1], P_init[1]], 'b--', label='线段 MP (⊥BM)')
line_aq_plot, = ax.plot([N[0], P_init[0]], [N[1], P_init[1]], 'g-', label='直线 NP')
line_mn_plot, = ax.plot([M_init[0], N[0]], [M_init[1], N[1]], 'y--', lw=1.5, label='线段 MN')

# 动态标签
label_m = ax.text(M_init[0], M_init[1] - 0.8, 'M', fontsize=14, color='red', ha='center')
label_p = ax.text(P_init[0], P_init[1] + 0.3, 'P', fontsize=14, color='blue', ha='center')

area_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, verticalalignment='top', fontsize=12,
                    bbox=dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.7))

# 5. --- 核心更新逻辑 ---
def update_geometry(m_new):
    m_new = max(4.01, m_new)
    M_new = np.array([m_new, 0])
    P_new = np.array([m_new + 4, m_new])
    
    point_m_plot.set_data([M_new[0]], [M_new[1]])
    point_p_plot.set_data([P_new[0]], [P_new[1]])
    
    line_bm_plot.set_data([B[0], M_new[0]], [B[1], M_new[1]])
    line_mp_plot.set_data([M_new[0], P_new[0]], [M_new[1], P_new[1]])
    line_aq_plot.set_data([N[0], P_new[0]], [N[1], P_new[1]])
    line_mn_plot.set_data([M_new[0], N[0]], [M_new[1], N[1]])
    
    poly_pam.set_xy(np.array([A, M_new, P_new]))
    poly_amn.set_xy(np.array([A, M_new, N]))
    
    label_m.set_position((M_new[0], M_new[1] - 0.8))
    label_p.set_position((P_new[0], P_new[1] + 0.3))
    
    s_amp = 0.5 * (m_new - 4) * m_new
    s_amn = 0.5 * (m_new - 4) * 4
    ratio = s_amp / s_amn if s_amn != 0 else 0
    text_content = (f"CM = {m_new:.2f}\nS△PAM = {s_amp:.2f}\nS△AMN = {s_amn:.2f}\n比值 = {ratio:.2f}")
    area_text.set_text(text_content)
    
    if np.isclose(ratio, 1.5, atol=0.01):
        area_text.set_bbox(dict(boxstyle='round,pad=0.5', fc='lightgreen', alpha=0.8))
    else:
        area_text.set_bbox(dict(boxstyle='round,pad=0.5', fc='wheat', alpha=0.7))
        
    fig.canvas.draw_idle()

# 6. --- 实现M点拖动功能 ---
class PointDragger:
    def __init__(self, point_to_drag):
        self.point = point_to_drag
        self.is_dragging = False
        self.press_data = None
        fig.canvas.mpl_connect('button_press_event', self.on_press)
        fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        fig.canvas.mpl_connect('button_release_event', self.on_release)

    def on_press(self, event):
        if event.inaxes != self.point.axes or not self.point.contains(event)[0]: return
        self.press_data = self.point.get_xdata()[0], event.xdata
        self.is_dragging = True

    def on_motion(self, event):
        if not self.is_dragging or event.inaxes != self.point.axes: return
        x0, xpress = self.press_data
        update_geometry(x0 + (event.xdata - xpress))

    def on_release(self, event):
        self.is_dragging = False
        self.press_data = None

# --- 实例化拖动器, 初始化并显示 ---
dragger = PointDragger(point_m_plot)
update_geometry(m_initial)
ax.legend(loc='upper right', fontsize='small')
plt.show()