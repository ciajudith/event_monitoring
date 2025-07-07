import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict

def plot_level_counts(level_counts: Dict[str, int], save_path: Path = None, show: bool = False, figsize: tuple = (6, 4)) -> None:
    level_colors = {
        "INFO": "green",
        "WARN": "orange",
        "ERROR": "red",
        "CRITICAL": "darkred"
    }
    levels = list(level_counts.keys())
    values = list(level_counts.values())
    colors = [level_colors.get(lvl, "gray") for lvl in levels]

    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(levels, values, color=colors)
    ax.set_title("Fréquence des évenements par niveau de priorité", pad=10)
    ax.set_xlabel("Niveau de priorité")
    ax.set_ylabel("Nombre d'évenements")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path)
    if show:
        plt.show()
    plt.close(fig)
