import numpy as np
import os

from config import (
    LHE_FILES,
    LABELS,
    CUTS_RUN3,
    CUTS_HLLHC,
    OUTDIR,
)

from physics import (
    pt,
    eta,
    mass,
    dR,
    deta,
    combine_particles,
    get_photons,
    get_final_state_jets,
    leading,
    leading_two,
    passes_cuts,
)

from histograms import HISTS
from plotting import plot_all


os.makedirs(OUTDIR, exist_ok=True)


def load_events(lhe_path):
    with open(lhe_path) as f:
        lines = f.readlines()

    events = []
    start = None

    for i, line in enumerate(lines):

        if line.strip() == "<event>":
            start = i

        elif line.strip() == "</event>" and start is not None:
            events.append(lines[start + 1 : i])
            start = None

    return events


def parse_particles(event_block):
    n = int(event_block[0].split()[0])

    return [
        list(map(float, l.split()))
        for l in event_block[1 : 1 + n]
    ]


accept_run3 = np.zeros(len(LHE_FILES))
accept_hllhc = np.zeros(len(LHE_FILES))
total_events = np.zeros(len(LHE_FILES))


for iF, path in enumerate(LHE_FILES):

    events = load_events(path)

    total_events[iF] = len(events)

    for event in events:

        particles = parse_particles(event)
        photons = get_photons(particles)
        a1, a2 = (sorted(photons, key=pt, reverse=True) + [None, None])[:2]

        jets = get_final_state_jets(particles)
        jets = sorted(jets, key=pt, reverse=True)
        j1, j2 = (jets + [None, None])[:2]

        A = None
        if a1 and a2:
            A = combine_particles([a1, a2])

        photons = get_photons(particles)
        jets = get_final_state_jets(particles)

        g1, g2 = leading_two(photons)
        j1, j2 = leading_two(jets)


        if g1:
            HISTS["gamma1_pt"][iF].fill(pt(g1))

        if g2:
            HISTS["gamma2_pt"][iF].fill(pt(g2))

        if g1 and g2:
            HISTS["gammagamma_dR"][iF].fill(dR(g1, g2))

        if A is not None:
            HISTS["A_pt"][iF].fill(pt(A))
            HISTS["A_eta"][iF].fill(eta(A))
            HISTS["A_mass"][iF].fill(mass(A))

        if j1:
            HISTS["q1_pt"][iF].fill(pt(j1))
            HISTS["q1_eta"][iF].fill(eta(j1))

        if j2:
            HISTS["q2_pt"][iF].fill(pt(j2))
            HISTS["q2_eta"][iF].fill(eta(j2))

        if j1 and j2:

            jj = combine_particles([j1, j2])

            pt1 = pt(j1)
            pt2 = pt(j2)

            mjj = mass(jj)
            deta_val = abs(deta(j1, j2))

            HISTS["qq_pt"][iF].fill(pt(jj))
            HISTS["qq_eta"][iF].fill(eta(jj))
            HISTS["qq_mass"][iF].fill(mjj)
            HISTS["qq_deta"][iF].fill(deta_val)
            HISTS["qq_dR"][iF].fill(dR(j1, j2))

            #acceptance

            if passes_cuts(
                pt1,
                pt2,
                mjj,
                deta_val,
                CUTS_RUN3,
            ):
                accept_run3[iF] += 1

            if passes_cuts(
                pt1,
                pt2,
                mjj,
                deta_val,
                CUTS_HLLHC,
            ):
                accept_hllhc[iF] += 1


#results
print("\nSignal Acceptance: \n")

for i, label in enumerate(LABELS):

    run3_eff = (
        accept_run3[i] / total_events[i]
        if total_events[i] > 0
        else 0
    )

    hllhc_eff = (
        accept_hllhc[i] / total_events[i]
        if total_events[i] > 0
        else 0
    )

    print(f"{label}")
    print(f"  Run 3  : {run3_eff:.4f}")
    print(f"  HL-LHC : {hllhc_eff:.4f}\n")


from config import PLOT_CONFIG

for key, xlabel, title, fname in PLOT_CONFIG:
    plot_all(
        HISTS[key],
        xlabel,
        title,
        fname,
    )
