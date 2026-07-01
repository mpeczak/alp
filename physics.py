import numpy as np
from scipy.ndimage import gaussian_filter1d


def pt(p):
    return np.hypot(p[6], p[7])


def phi(p):
    return np.arctan2(p[7], p[6])


def eta(p):

    pabs = np.linalg.norm(p[6:9])

    if pabs < 1e-12:
        return 0.0

    cos_theta = np.clip(
        p[8] / pabs,
        -0.999999,
        0.999999,
    )

    return np.arctanh(cos_theta)


def mass(p):
    if len(p) <= 10:
        return 0.0

    return p[10]


def energy(p):
    return p[9]


def momentum_magnitude(p):

    return np.linalg.norm(p[6:9])


def delta_phi(phi1, phi2):

    dphi = abs(phi1 - phi2)

    return min(dphi, 2 * np.pi - dphi)


def deta(p1, p2):
    return eta(p1) - eta(p2)


def dR(p1, p2):
    d_eta = eta(p1) - eta(p2)

    d_phi = delta_phi(
        phi(p1),
        phi(p2),
    )

    return np.hypot(d_eta, d_phi)



def combine_particles(particles):

    out = [0.0] * 13

    for p in particles:

        out[6] += p[6]   # px
        out[7] += p[7]   # py
        out[8] += p[8]   # pz
        out[9] += p[9]   # E

        if len(p) > 12:
            out[12] += p[12]

    p_tot = np.linalg.norm(out[6:9])

    m2 = out[9]**2 - p_tot**2

    out[10] = np.sqrt(m2) if m2 > 0 else 0.0

    return out


def get_photons(particles):

    return [
        p for p in particles
        if int(p[0]) == 22
    ]


def get_final_state_jets(particles):
    return [
        p for p in particles
        if (
            int(p[0]) in [1, 2, 3, 4, 5, 6, 21]
            and int(p[1]) == 1
        )
    ]


def sort_by_pt(particles):
    return sorted(
        particles,
        key=pt,
        reverse=True,
    )


def leading_two(particles):
    return (
        sort_by_pt(particles)
        + [None, None]
    )[:2]


def normalize_hist(h):
    h_norm = h.copy()

    total = np.sum(h_norm.values())

    if total > 0:
        h_norm /= total

    return h_norm


def get_hist_xmax(h):

    values = h.values()
    edges = h.axes[0].edges

    for i in reversed(range(len(values))):

        if values[i] > 0:
            return edges[i + 1] * 1.05

    return edges[-1]


def get_hist_ymax(h_norm, minimum=1e-5):

    vals = h_norm.values()

    if len(vals):
        return max(
            np.max(vals) * 1.2,
            minimum,
        )

    return minimum


def get_hist_min_nonzero(h):

    vals = h.values()
    edges = h.axes[0].edges

    for i, val in enumerate(vals):

        if val > 0:
            return edges[i]

    return None


def find_shape_peak(hist, sigma=3, logx=False):

    counts = hist.values()

    if len(counts) == 0:
        return None

    edges = hist.axes[0].edges

    centers = 0.5 * (
        edges[:-1]
        + edges[1:]
    )

    if logx:

        mask = centers > 0

        centers = centers[mask]
        counts = counts[mask]

    if len(counts) == 0:
        return None

    smooth = gaussian_filter1d(
        counts,
        sigma=sigma,
    )

    peak_index = np.argmax(smooth)

    return centers[peak_index]


def passes_cuts(pt1, pt2, mjj, deta_abs, cuts):
    return (
        pt1 > cuts["q1_pt"]
        and pt2 > cuts["q2_pt"]
        and mjj > cuts["mjj"]
        and deta_abs > cuts["deta"]
    )
