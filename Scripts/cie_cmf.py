import json
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def config_graph(axis, axis_config, id):
    axis[id].set_title(axis_config[f'graph{id}']['title'])
    axis[id].set_xlabel(axis_config[f'graph{id}']['x_label'])
    axis[id].set_ylabel(axis_config[f'graph{id}']['y_label'])

    if axis_config[f'graph{id}']['x_scales'] == 'function':
        axis[id].set_xscale('function', functions=(
            lambda x: np.interp(x, axis_config[f'graph{id}']['x_ticks'],
                                np.linspace(0, 1, len(axis_config[f'graph{id}']['x_ticks']))),
            lambda x: np.abs(x)))
    else:
        axis[id].set_xscale(axis_config[f'graph{id}']['x_scales'])

    axis[id].set_xticks(axis_config[f'graph{id}']['x_ticks'])
    axis[id].set_xticklabels(axis_config[f'graph{id}']['x_labels'])



def plot_graph(axis, graph_data, axis_config, id, type):

    w = graph_data.iloc[:,0]
    r = graph_data.iloc[:,1]
    g = graph_data.iloc[:,2]
    b = graph_data.iloc[:,3]

    if type == 0:  # color-match graph
        axis[id].plot(w, r, color='red', marker='o')
        axis[id].plot(w, g, color='green', marker='o')
        axis[id].plot(w, b, color='blue', marker='o')
    elif type == 1:  # garmut graph
        axis[id].plot(r, g, color='red', marker='o')

        for i in range(len(r)):
            plt.text(r[i], g[i], f'({w[i]:.1f})', fontsize=9, ha='right')

    config_graph(axis, axis_config, id)

def plot_graphs(graph_name):
    fig, axis = plt.subplots(1, 2, figsize=(20, 8))

    with open('../Data/graph.json', 'r', encoding='utf-8') as file:
        graph_config = json.load(file)
    with open(graph_config[graph_name]["config"], 'r', encoding='utf-8') as file:
        axis_config = json.load(file)

    graph_data = pd.read_csv(graph_config[graph_name]["data"])

    plot_graph(axis, graph_data, axis_config, 0, 0)
    plot_graph(axis, graph_data, axis_config, 1, 1)

    # w = graph_data.iloc[:,0]
    # r = graph_data.iloc[:,1]
    # g = graph_data.iloc[:,2]
    # b = graph_data.iloc[:,3]
    #
    # # graph 0
    # axis[0].plot(w, r, color='red', marker='o')
    # axis[0].plot(w, g, color='green', marker='o')
    # axis[0].plot(w, b, color='blue', marker='o')
    # config_graph(axis, axis_config, 0)
    #
    # # graph 1
    # axis[1].plot(r, g, color='red', marker='o')
    # config_graph(axis, axis_config, 1)

    plt.show()
    return fig, axis



# x1 = np.linspace(0, 10, 100)
# y1 = np.piecewise(x1, [x1 < 5, x1 >= 5], [lambda x: x, lambda x: 10 - x])  # 分段函数
# x2 = np.linspace(0, 10, 100)
# y2 = np.sin(x2)
# # 创建图形和子图
# fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
# # 绘制第一张图，x轴为分段函数
# ax1.plot(x1, y1)
# ax1.set_title('Piecewise Function Scale X-Axis')
# ax1.set_xscale('function', functions=(lambda x: x, lambda x: x))  # 这里使用线性函数作为示例
# # 设置分段函数的自定义函数
# def piecewise_function(x):
#     return np.piecewise(x, [x < 5, x >= 5], [lambda x: x, lambda x: 10 - x])
# # 设置x坐标
# ax1.set_xticks(np.arange(0, 11, 1))
# ax1.set_xticklabels([f"{x:.1f}" for x in np.arange(0, 11, 1)])
# ax1.axhline(0, color='grey', lw=0.5, ls='--')
# # 绘制第二张图，x轴为linear
# ax2.plot(x2, y2)
# ax2.set_title('Linear Scale X-Axis')
# ax2.set_xscale('linear')
# # 显示图形
# plt.tight_layout()
# plt.show()


# 创建主窗口
# root = tk.Tk()
# root.title("多页签 Matplotlib 示例")
# # 创建 Notebook
# notebook = ttk.Notebook(root)
# notebook.pack(fill='both', expand=True)
# # 创建多个标签页
#
# for i in range(1):  # 创建3个页签
#     frame = ttk.Frame(notebook)
#     notebook.add(frame, text=f"页签 {i+1}")
#     # 生成示例数据
#
#
#     fig, ax = plot_graphs("wright_1929")
#     # plot_curve(ax, x, y, f"曲线 {i+1}")
#     # 将 Matplotlib 图形嵌入 Tkinter
#     canvas = FigureCanvasTkAgg(fig, master=frame)
#     canvas.draw()
#     canvas.get_tk_widget().pack(fill='both', expand=True)
# # 运行主循环
# root.mainloop()

fig, ax = plot_graphs("wright_1929")
