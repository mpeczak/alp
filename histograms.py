from hist import Hist, axis

from config import (
    LHE_FILES,
    HIST_CONFIG,
    DR_BINS,
)


def make_hist(nbins, xmin, xmax, name):
    return [
        Hist(
            axis.Regular(
                nbins,
                xmin,
                xmax,
                name=name,
            )
        )
        for _ in range(len(LHE_FILES))
    ]


def make_dr_hist(name="dR"):
    return [
        Hist(
            axis.Variable(
                DR_BINS,
                name=name,
            )
        )
        for _ in range(len(LHE_FILES))
    ]

HISTS = {}

for key, (nbins, xmin, xmax) in HIST_CONFIG.items():
    HISTS[key] = make_hist(nbins, xmin, xmax, key)
HISTS["gammagamma_dR"] = make_dr_hist("gamma1gamma2_dR")


def get_hist(name):

    return HISTS[name]


def all_hist_names():
    return list(HISTS.keys())
