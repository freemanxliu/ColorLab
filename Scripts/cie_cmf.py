import json
from unittest.mock import right

import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def config_graph(axis, axis_config, id):
    axis[id].set_title(axis_config['title'])
    axis[id].set_xlabel(axis_config['x_label'])
    axis[id].set_ylabel(axis_config['y_label'])

    if axis_config['x_scales'] == 'function':
        axis[id].set_xscale('function', functions=(
            lambda x: np.interp(x, axis_config['x_ticks'],
                                np.linspace(0, 1, len(axis_config['x_ticks']))),
            lambda x: np.abs(x)))
    else:
        axis[id].set_xscale(axis_config['x_scales'])

    axis[id].set_xticks(axis_config['x_ticks'])
    axis[id].set_xticklabels(axis_config['x_labels'])


def plot_graph(axis, graph_data, axis_config, id):

    w = graph_data.iloc[:,0]
    r = graph_data.iloc[:,1]
    g = graph_data.iloc[:,2]
    b = graph_data.iloc[:,3]

    axis[id].clear()

    if axis_config["curve_type"] == "wr, wg, wb":  # color-match graph
        axis[id].plot(w, r, color='red', marker='o')
        axis[id].plot(w, g, color='green', marker='o')
        axis[id].plot(w, b, color='blue', marker='o')
    elif axis_config["curve_type"] == "rg":  # gamut graph
        axis[id].plot(r, g, color='red', marker='o')

        for i in range(len(r)):
            plt.text(r[i], g[i], f'({w[i]:.1f})', fontsize=9, ha='right')

    config_graph(axis, axis_config, id)

def plot_graphs(axis, datas, configs):
    assert len(datas) == len(configs), "graph names and types must be same length"

    for idx in range(len(datas)):
        plot_graph(axis, datas[idx], configs[idx], idx)

    # plt.show()
    plt.draw()


def update():

    with open(graph_configs[left_graph.get()]["config"], 'r', encoding='utf-8') as left_file:
        left_config = json.load(left_file)

    with open(graph_configs[right_graph.get()]["config"], 'r', encoding='utf-8') as right_file:
        right_config = json.load(right_file)

    graph_datas = [pd.read_csv(graph_configs[left_graph.get()]["data"]),
                   pd.read_csv(graph_configs[right_graph.get()]["data"])]

    graph_types = [left_config[graph_configs[left_graph.get()]["type"]],
                   right_config[graph_configs[right_graph.get()]["type"]]]

    plot_graphs(ax, graph_datas, graph_types)

def update_frame(x):
    update()

if __name__ == "__main__":

    # create subplots
    fig, ax = plt.subplots(1, 2, figsize=(20, 8))
    # fig.tight_layout()

    root = tk.Tk()
    root.title("Color Labs")
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    frame = tk.Frame(root)
    frame.pack(side=tk.BOTTOM, fill=tk.X)

    with open('../Data/graph.json', 'r', encoding='utf-8') as file:
        graph_configs = json.load(file)
        graph_options = list(graph_configs.keys())

    left_graph = ttk.Combobox(root, values=graph_options)
    left_graph.current(0)
    left_graph.bind("<<ComboboxSelected>>", update_frame)
    left_graph.pack(side=tk.LEFT, padx=500, pady=10)

    right_graph = ttk.Combobox(root, values=graph_options)
    right_graph.current(1)
    right_graph.bind("<<ComboboxSelected>>", update_frame)
    right_graph.pack(side=tk.RIGHT, padx=500, pady=10)

    update()
    root.mainloop()
