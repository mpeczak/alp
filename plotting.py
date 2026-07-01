import numpy as np
import matplotlib.pyplot as plt
import mplhep

from scipy.ndimage import gaussian_filter1d

from config import (
    OUTDIR,
    COLORS,
    LABELS,
    LOGLOG,
)

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "stix",

    "font.size": 20,

    "axes.labelsize": 32,
    "axes.titlesize": 30,

    "xtick.labelsize": 20,
    "ytick.labelsize": 20,

    "legend.fontsize": 22,

    "axes.linewidth": 2,

    "xtick.major.size": 8,
    "ytick.major.size": 8,
    "xtick.major.width": 2,
    "ytick.major.width": 2,

    "xtick.direction": "in",
    "ytick.direction": "in",

    "xtick.top": False,
    "ytick.right": False,
})


def normalize_hist(h):
    h2 = h.copy()
    s = np.sum(h2.values())
    if s > 0:
        h2 /= s
    return h2


def get_hist_xmax(h):
    vals = h.values()
    edges = h.axes[0].edges

    for i in reversed(range(len(vals))):
        if vals[i] > 0:
            return edges[i + 1] * 1.05

    return edges[-1]


def get_hist_ymax(h, min_val=1e-5):
    v = h.values()
    if len(v):
        return max(np.max(v) * 1.2, min_val)
    return min_val


def find_shape_peak(hist, sigma=3, logx=False):
    vals = hist.values()

    if len(vals) == 0:
        return None

    edges = hist.axes[0].edges
    x = 0.5 * (edges[:-1] + edges[1:])

    if logx:
        mask = x > 0
        x = x[mask]
        vals = vals[mask]

    if len(vals) == 0:
        return None

    smooth = gaussian_filter1d(vals, sigma=sigma)

    return x[np.argmax(smooth)]

def draw_peak(ax, peak, ymax, color, label, ypos=0.8):
    ax.axvline(
        peak,
        color=color,
        ls="--",
        lw=2.5,
        alpha=0.9,
    )

    ax.text(
        peak * 1.05,
        ymax * ypos,
        label,
        color=color,
        fontsize=20,
        bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
    )

def get_hist_xmin(h):
    vals = h.values()
    edges = h.axes[0].edges

    for i, v in enumerate(vals):
        if v > 0:
            return edges[i] * 0.95

    return edges[0]


def plot_all(hist_list, xlabel, title, fname):

    for i, h in enumerate(hist_list):

        if np.sum(h.values()) == 0:
            continue

        fig, ax = plt.subplots(figsize=(12, 8))

        h_norm = normalize_hist(h)

        mplhep.histplot(
            normalize_hist(h),
            ax=ax,
            color=COLORS[i],
            linewidth=2.8,
            label=LABELS[i],
        )
        

        xmin = min(get_hist_xmin(h) for h in hist_list)
        xmax = max(get_hist_xmax(h) for h in hist_list)

        ax.set_xlim(xmin, xmax)

        ax.set_ylim(0, get_hist_ymax(h_norm))

        ax.set_xlabel(xlabel)
        ax.set_ylabel("Normalized Events")
        ax.set_title(f"{title} ({LABELS[i]})")

        if fname != "hist_gamma1gamma2_dR":
            ax.legend(frameon=False, loc="best")

        if LOGLOG or fname == "hist_gamma1gamma2_dR":
            ax.set_xscale("log")

        plt.tight_layout()

        plt.savefig(f"{OUTDIR}/{fname}_{LABELS[i].replace(' ', '_')}.png")

        plt.close(fig)

    #combined plots for all masses
    fig, ax = plt.subplots(figsize=(10, 6))

    drawn = False

    for i, h in enumerate(hist_list):

        if np.sum(h.values()) == 0:
            continue

        mplhep.histplot(
            normalize_hist(h),
            ax=ax,
            color=COLORS[i],
            linewidth=2.8,
            label=LABELS[i],
        )

        drawn = True

    if not drawn:
        plt.close(fig)
        return

    ymax = max(get_hist_ymax(normalize_hist(h)) for h in hist_list)

    if fname == 'hist_A_pt':

        ax.axvline(175, color='black', linestyle='--', linewidth=1.5)

        ax.text(
            175 * 0.98,
            ymax * 0.9,
            'Single photon trigger',
            color='black',
            fontsize=20,
            ha='right'
        )

    if fname == 'hist_q1_pt':

        ax.axvline(55, color='black', linestyle='--', linewidth=1.0)
        ax.text(55 * 1.02, ymax * 0.75, 'Data scouting', fontsize=20)

        ax.axvline(105, color='black', linestyle='--', linewidth=1.5)
        ax.text(105 * 1.02, ymax * 0.9, 'Data parking', fontsize=20)
        
    if fname == 'hist_q2_pt':

        ax.axvline(20, color='black', linestyle='--', linewidth=1.0)
        ax.text(20 * 1.02, ymax * 0.75, 'Data scouting', fontsize=20)

        ax.axvline(40, color='black', linestyle='--', linewidth=1.5)
        ax.text(40 * 1.02, ymax * 0.9, 'Data parking', fontsize=20)
    
    if fname == 'hist_mqq':

        ax.axvline(420, color='black', linestyle='--', linewidth=1.0)
        ax.text(420 * 1.02, ymax * 0.75, 'Data scouting', fontsize=20)

        ax.axvline(720, color='black', linestyle='--', linewidth=1.5)
        ax.text(720 * 1.02, ymax * 0.9, 'Data parking', fontsize=20)
    
    if fname == 'hist_q1q2_deta':

        ax.axvline(2.0, color='black', linestyle='--', linewidth=1.0)
        ax.axvline(-2.0, color='black', linestyle='--', linewidth=1.0)
        ax.text(2.0 * 1.02, ymax * 0.75, 'Data scouting', fontsize=20)

        ax.axvline(3.0, color='black', linestyle='--', linewidth=1.5)
        ax.axvline(-3.0, color='black', linestyle='--', linewidth=1.5)
        ax.text(3.0 * 1.02, ymax * 0.9, 'Data parking', fontsize=20)
        
    if fname == "hist_gamma1gamma2_dR":

        for i, h in enumerate(hist_list):

            if np.sum(h.values()) == 0:
                continue

            sigma = 1 if LABELS[i] == "10 MeV" else 3

            peak = find_shape_peak(h, sigma=sigma, logx=True)

            if peak is not None:
                draw_peak(ax, peak, ymax, COLORS[i], LABELS[i], 0.8 - 0.1 * i)

    #final format

    xmin = min(get_hist_xmin(h) for h in hist_list)
    xmax = max(get_hist_xmax(h) for h in hist_list)

    ax.set_xlim(xmin, xmax)

    ax.set_ylim(0, ymax)

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Normalized Events")

    #ax.set_title(f"{title} (all masses)")

    if LOGLOG or fname == "hist_gamma1gamma2_dR":
        ax.set_xscale("log")
        
    if fname != "hist_gamma1gamma2_dR":
        ax.legend(
            frameon=False,
            loc="best",
            handlelength=2.5,
        )
    ax.minorticks_on()

    ax.tick_params(
        which="major",
        length=10,
        width=2,
    )

    ax.tick_params(
        which="minor",
        length=5,
        width=1.5,
    )

    plt.tight_layout()

    plt.savefig(
        f"{OUTDIR}/{fname}_all_full.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)
