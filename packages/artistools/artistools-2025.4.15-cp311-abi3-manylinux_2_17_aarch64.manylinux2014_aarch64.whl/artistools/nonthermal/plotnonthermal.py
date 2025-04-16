#!/usr/bin/env python3

import argparse
import typing as t
from collections.abc import Sequence
from functools import lru_cache
from pathlib import Path

import matplotlib.axes as mplax
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl

import artistools as at

defaultoutputfile = "plotnonthermal_cell{0:03d}_timestep{1:03d}.pdf"
ERG_TO_EV = 6.242e11


@lru_cache(maxsize=4)
def read_files(modelpath: Path, timestep: int = -1, modelgridindex: int = -1) -> pd.DataFrame:
    """Read ARTIS -thermal spectrum data into a pandas DataFrame."""
    nonthermaldata_allfiles: list[pd.DataFrame] = []

    mpiranklist = at.get_mpiranklist(modelpath, modelgridindex=modelgridindex)
    for folderpath in at.get_runfolders(modelpath, timestep=timestep):
        for mpirank in mpiranklist:
            filepath = at.firstexisting(f"nonthermalspec_{mpirank:04d}.out", folder=folderpath, tryzipped=True)

            if modelgridindex > -1:
                filesize = Path(filepath).stat().st_size / 1024 / 1024
                print(f"Reading {Path(filepath).relative_to(modelpath.parent)} ({filesize:.2f} MiB)")

            nonthermaldata_thisfile = pd.read_csv(filepath, sep=r"\s+", on_bad_lines="skip")
            # radfielddata_thisfile[['modelgridindex', 'timestep']].apply(pd.to_numeric)

            if timestep >= 0:
                nonthermaldata_thisfile = nonthermaldata_thisfile[nonthermaldata_thisfile["timestep"] == timestep]

            if modelgridindex >= 0:
                nonthermaldata_thisfile = nonthermaldata_thisfile[
                    nonthermaldata_thisfile["modelgridindex"] == modelgridindex
                ]

            if not nonthermaldata_thisfile.empty:
                if timestep >= 0 and modelgridindex >= 0:
                    return nonthermaldata_thisfile

                nonthermaldata_allfiles.append(nonthermaldata_thisfile)

    return pd.concat(nonthermaldata_allfiles, ignore_index=True)


def make_xs_plot(axis: mplax.Axes, nonthermaldata: pd.DataFrame, args: argparse.Namespace) -> None:
    import pynonthermal as pynt

    dfcollion = pynt.collion.read_colliondata()

    arr_en = nonthermaldata["energy_ev"].unique()

    # arr_xs_old = [xs_fe2_old(en) for en in arr_en]
    # arr_xs_times_y = [xs_fe1(en) * y for en, y in zip(nonthermaldata['energy_ev'], nonthermaldata['y'])]

    axis.plot(arr_en, pynt.collion.get_arxs_array_ion(arr_en, dfcollion, 26, 2), linewidth=2.0, label="Fe II")
    axis.plot(arr_en, pynt.collion.get_arxs_array_ion(arr_en, dfcollion, 28, 2), linewidth=2.0, label="Ni II")

    axis.set_ylabel(r"cross section (cm2)")

    if not args.nolegend:
        axis.legend(loc="upper center", handlelength=2, frameon=False, numpoints=1, prop={"size": 13})


def plot_contributions(
    axis: mplax.Axes, modelpath: Path | str, timestep: int, modelgridindex: int, nonthermaldata: pd.DataFrame
) -> None:
    from scipy import integrate

    estim_tsmgi = at.estimators.read_estimators(modelpath, modelgridindex=modelgridindex, timestep=timestep)[
        timestep, modelgridindex
    ]

    total_depev = estim_tsmgi["total_dep"] * ERG_TO_EV

    print(f"Deposition: {total_depev:.1f} [eV/cm³/s]")

    arr_enev = nonthermaldata["energy_ev"].to_numpy()
    arr_y = nonthermaldata["y"].to_numpy()

    frac_ionisation = 0.0

    import pynonthermal as pynt

    dfcollion = pynt.collion.read_colliondata()

    elementlist = at.get_composition_data(modelpath)
    totalpop = estim_tsmgi["nntot"]
    nelements = len(elementlist)
    for element in range(nelements):
        Z = elementlist.Z[element]
        elsymbol = at.get_elsymbol(Z)
        elpop = estim_tsmgi[f"nnelement_{elsymbol}"]
        if elpop <= 1e-4 * totalpop:
            continue

        arr_ionisation_element = np.zeros(len(arr_enev), dtype=float)
        frac_ionisation_element = 0.0

        nions = elementlist.nions[element]
        for ion in range(nions):
            ion_stage = ion + elementlist.lowermost_ion_stage[element]
            ionstr = at.get_ionstring(Z, ion_stage, sep="_", style="spectral")
            ionpop = estim_tsmgi[f"nnion_{ionstr}"]

            dfcollion_thision = dfcollion.filter(pl.col("Z") == Z).filter(pl.col("ion_stage") == ion_stage)

            # print(at.get_ionstring(Z, ion_stage), ionpop)

            arr_ionisation_ion = np.zeros(len(arr_enev), dtype=float)
            frac_ionisation_ion = 0.0

            for row in dfcollion_thision.iter_rows(named=True):
                arr_xs = pynt.collion.get_arxs_array_shell(arr_enev, row)
                arr_ionisation_shell = ionpop * arr_y * arr_xs * row["ionpot_ev"] / total_depev
                arr_ionisation_ion += arr_ionisation_shell

                frac_ionisation_shell = integrate.trapezoid(x=arr_enev, y=arr_ionisation_shell)
                frac_ionisation_ion += frac_ionisation_shell

            arr_ionisation_element += arr_ionisation_ion
            frac_ionisation_element += frac_ionisation_ion

        frac_ionisation += frac_ionisation_element

        if frac_ionisation_element > 1e-5:
            axis.plot(arr_enev, arr_ionisation_element, label=f"Ionisation Z={Z}")

    nne = estim_tsmgi["nne"]
    arr_heating = np.array([pynt.electronlossfunction(enev, nne) / total_depev for enev in arr_enev])

    frac_heating = integrate.trapezoid(x=arr_enev, y=arr_heating)

    print(f"   frac_heating: {frac_heating}")
    print(f"frac_ionisation: {frac_ionisation}")

    axis.plot(arr_enev, arr_heating, label="Heating")

    axis.legend(loc="best", handlelength=2, frameon=False, numpoints=1, prop={"size": 11})


def make_plot(modelpaths: list[Path], args: argparse.Namespace) -> None:
    nplots = 1
    if args.xsplot:
        nplots += 1
    if args.showcontributions:
        nplots += 1
    fig, axes = plt.subplots(
        nrows=nplots,
        ncols=1,
        sharex=True,
        figsize=(
            args.figscale * at.get_config()["figwidth"],
            args.figscale * at.get_config()["figwidth"] * 0.7 * nplots,
        ),
        tight_layout={"pad": 0.2, "w_pad": 0.0, "h_pad": 0.0},
    )

    if nplots == 1:
        axes = np.array([axes])

    assert isinstance(axes, np.ndarray)

    if args.kf1992spec:
        kf92spec = pd.read_csv(Path(modelpaths[0], "KF1992spec-fig1.txt"), header=None, names=["e_kev", "log10_y"])
        kf92spec["energy_ev"] = kf92spec["e_kev"] * 1000.0
        kf92spec["y"] = 10 ** kf92spec["log10_y"]
        axes[0].plot(
            kf92spec["energy_ev"], kf92spec["log10_y"], linewidth=2.0, color="red", label="Kozma & Fransson (1992)"
        )

    for index, modelpath in enumerate(modelpaths):
        modelname = at.get_model_name(modelpath)
        modelgridindex = (
            at.inputmodel.get_mgi_of_velocity_kms(modelpath, args.velocity)
            if args.velocity >= 0.0
            else args.modelgridindex
        )

        timestep = at.get_timestep_of_timedays(modelpath, args.timedays) if args.timedays else args.timestep

        nonthermaldata = read_files(modelpath=Path(modelpath), modelgridindex=modelgridindex, timestep=timestep)

        if args.xmin:
            nonthermaldata = nonthermaldata.query("energy_ev >= @args.xmin")

        if nonthermaldata.empty:
            print(f"No data for timestep {timestep:d}")
            continue

        if index < len(args.modellabels):
            model_label = args.modellabels[index]
        else:
            model_label = f"{modelname} cell {modelgridindex} at timestep {timestep}"
            try:
                time_days = at.get_timestep_time(Path(), timestep)
            except FileNotFoundError:
                time_days = 0
            else:
                model_label += f" ({time_days:.2f}d)"

        outputfile = str(args.outputfile).format(modelgridindex, timestep)
        print(f"Plotting timestep {timestep:d}")
        # ymax = max(nonthermaldata['y'])

        # nonthermaldata.plot(x='energy_ev', y='y', linewidth=1.5, ax=axis, color='blue', legend=False)
        axes[0].plot(
            (nonthermaldata["energy_ev"]),
            np.log10(nonthermaldata["y"]),
            label=model_label,
            linewidth=2.0,
            color="black" if index == 0 else None,
            alpha=0.95,
        )
        axes[0].set_ylabel(r"log [y (e$^-$ / cm$^2$ / s / eV)]")

        if args.showcontributions:
            assert isinstance(modelgridindex, int)
            plot_contributions(axes[1], modelpath, timestep, modelgridindex, nonthermaldata)

        if args.xsplot:
            make_xs_plot(axes[-1], nonthermaldata, args)

    if not args.nolegend:
        axes[0].legend(loc="best", handlelength=2, frameon=False, numpoints=1)

    axes[-1].set_xlabel(r"Energy (eV)")
    # axis.yaxis.set_minor_locator(ticker.MultipleLocator(base=0.1))
    # axis.set_yscale("log", nonposy='clip')
    for ax in axes:
        if args.xmin is not None:
            ax.set_xlim(left=args.xmin)
        if args.xmax:
            ax.set_xlim(right=args.xmax)
    # axis.set_ylim(bottom=0.0, top=ymax)

    # axis.legend(loc='upper center', handlelength=2,
    #             frameon=False, numpoints=1, prop={'size': 13})

    print(f"Saving to {outputfile:s}")
    fig.savefig(outputfile, format="pdf")
    plt.close()


def addargs(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-modelpath",
        default=[],
        nargs="*",
        action=at.AppendPath,
        help="Paths to ARTIS folders with spec.out or packets files",
    )

    parser.add_argument("-modellabels", default=[], nargs="*", help="Model name overrides")

    parser.add_argument("-listtimesteps", action="store_true", help="Show the times at each timestep")

    parser.add_argument("-xsplot", action="store_true", help="Show the cross section plot")

    parser.add_argument("-timedays", "-time", "-t", help="Time in days to plot")

    parser.add_argument("-timestep", "-ts", type=int, default=-1, help="Timestep number to plot")

    parser.add_argument("-modelgridindex", "-cell", type=int, default=0, help="Modelgridindex to plot")

    parser.add_argument("-velocity", "-v", type=float, default=-1, help="Specify cell by velocity")

    parser.add_argument("-xmin", type=float, default=0.0, help="Plot range: minimum energy in eV")

    parser.add_argument("-xmax", type=float, help="Plot range: maximum energy in eV")

    parser.add_argument("--nolegend", action="store_true", help="Suppress the legend from the plot")

    parser.add_argument(
        "--showcontributions", action="store_true", help="Plot the NT contributions to ionisation and heating energy"
    )

    parser.add_argument(
        "--kf1992spec", action="store_true", help="Show the pure-oxygen result form Figure 1 of Kozma & Fransson 1992"
    )

    parser.add_argument(
        "-figscale", type=float, default=1.0, help="Scale factor for plot area. 1.0 is for single-column"
    )

    parser.add_argument(
        "-o", action="store", dest="outputfile", type=Path, default=defaultoutputfile, help="Filename for PDF file"
    )


def main(args: argparse.Namespace | None = None, argsraw: Sequence[str] | None = None, **kwargs: t.Any) -> None:
    """Plot ARTIS non-thermal electron energy spectrum."""
    if args is None:
        parser = argparse.ArgumentParser(formatter_class=at.CustomArgHelpFormatter, description=__doc__)

        addargs(parser)
        at.set_args_from_dict(parser, kwargs)
        args = parser.parse_args([] if kwargs else argsraw)

    if not args.modelpath:
        args.modelpath = [Path()]
    elif isinstance(args.modelpath, str | Path):
        args.modelpath = [args.modelpath]

    # flatten the list
    modelpaths = []
    for elem in args.modelpath:
        if isinstance(elem, list):
            modelpaths.extend(elem)
        else:
            modelpaths.append(elem)

    if Path(args.outputfile).is_dir():
        args.outputfile = Path(args.outputfile, defaultoutputfile)

    if args.listtimesteps:
        at.showtimesteptimes()
    else:
        make_plot(modelpaths, args)


if __name__ == "__main__":
    main()
