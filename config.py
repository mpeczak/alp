import numpy as np


OUTDIR = "plots_final_git"

LHE_FILES = [
    "/home/marielpeczak/MG5_aMC_v3_7_0/no_photon_cut_10/Events/run_01/unweighted_events.lhe",
    "/home/marielpeczak/MG5_aMC_v3_7_0/no_photon_cut_100/Events/run_01/unweighted_events.lhe",
    "/home/marielpeczak/MG5_aMC_v3_7_0/no_photon_cut_1/Events/run_01/unweighted_events.lhe",
    "/home/marielpeczak/MG5_aMC_v3_7_0/no_photon_cut10G/Events/run_01/unweighted_events.lhe",
]

#must have same length as lhe_files

LABELS = [
    "10 MeV",
    "100 MeV",
    "1 GeV",
    "10 GeV",
]

COLORS = [
    "C0",
    "C1",
    "C2",
    "C3",
]


NBINS = 50

NBINS_DR = 50
DR_BINS = np.logspace(-4, 1, NBINS_DR + 1
)

LOGLOG = False

#vbf cuts
CUTS_RUN3 = {
    "q1_pt": 105, 
    "q2_pt": 40,  
    "mjj": 720, 
    "deta": 3.0, 
}

CUTS_HLLHC = {
    "q1_pt": 0,
    "q2_pt": 0,
    "mjj": 0,
    "deta": 0,
}

#format is key : (nbins, xmin, xmax)
HIST_CONFIG = {
    "gamma1_pt": (NBINS, 0, 500),
    "gamma2_pt": (NBINS, 0, 500),
    "A_pt":   (NBINS, 0, 200),
    "A_eta":  (NBINS, -5, 5),
    "A_mass": (NBINS, 0, 10),
    "q1_pt":  (NBINS, 0, 150),
    "q2_pt":  (NBINS, 0, 150),
    "qq_pt":  (NBINS, 0, 150),

    "q1_eta": (NBINS, -5, 5),
    "q2_eta": (NBINS, -5, 5),
    "qq_eta": (NBINS, -5, 5),

    "qq_dR":   (NBINS, 0, 10),
    "qq_deta": (NBINS, -10, 10),

    "qq_mass": (NBINS, 0, 1000),
}

PLOT_CONFIG = [

    (
        "q1_pt",
        "q1 pT [GeV]",
        "Leading Jet pT",
        "hist_q1_pt",
    ),

    (
        "q2_pt",
        "q2 pT [GeV]",
        "Subleading Jet pT",
        "hist_q2_pt",
    ),

    (
        "qq_mass",
        "qq Mass [GeV]",
        "Dijet Mass",
        "hist_mqq",
    ),

    (
        "A_pt",
        "A pT [GeV]",
        "Axion pT",
        "hist_A_pt",
    ),

    (
        "A_eta",
        "A eta",
        "Axion Eta",
        "hist_A_eta",
    ),

    (
        "gamma1_pt",
        "gamma1 pT [GeV]",
        "Leading Photon pT",
        "hist_gamma1_pt",
    ),

    (
        "gamma2_pt",
        "gamma2 pT [GeV]",
        "Subleading Photon pT",
        "hist_gamma2_pt",
    ),

    (
        "gammagamma_dR",
        r"$\Delta R(\gamma_1,\gamma_2)$",
        "Photon Separation",
        "hist_gamma1gamma2_dR",
    ),

    (
        "q1_eta",
        "q1 eta",
        "Leading Jet Eta",
        "hist_q1_eta",
    ),

    (
        "q2_eta",
        "q2 eta",
        "Subleading Jet Eta",
        "hist_q2_eta",
    ),

    (
        "qq_eta",
        "qq eta",
        "Dijet Eta",
        "hist_qq_eta",
    ),

    (
        "qq_dR",
        r"$\Delta R(q_1,q_2)$",
        "Jet Separation",
        "hist_q1q2_dR",
    ),

    (
        "qq_deta",
        r"$\Delta \eta(q_1,q_2)$",
        "Jet Δη",
        "hist_q1q2_deta",
    ),
]
