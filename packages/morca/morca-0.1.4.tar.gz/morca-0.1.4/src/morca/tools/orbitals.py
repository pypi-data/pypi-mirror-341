import marimo

__generated_with = "0.12.4"
app = marimo.App(width="medium")


@app.cell
def _():
    from pathlib import Path

    import altair as alt
    import cotwo as co
    import marimo as mo
    import polars as pl

    from morca import (
        parse_active_space_orbitals,
        parse_loewdin_orbital_compositions,
        parse_orbital_energies,
    )
    return (
        Path,
        alt,
        co,
        mo,
        parse_active_space_orbitals,
        parse_loewdin_orbital_compositions,
        parse_orbital_energies,
        pl,
    )


@app.cell
def _(Path):
    import sys

    file_arg = Path(sys.argv[-1])
    if not file_arg.suffix == ".out":
        file_arg = None
    return file_arg, sys


@app.cell
def _(file_arg, mo):
    file_text = mo.ui.text(
        placeholder="Path to output file",
        value=str(file_arg) if file_arg else "",
        full_width=True,
    )
    file_text
    return (file_text,)


@app.cell
def _(Path, file_text, mo):
    mo.stop(not file_text.value)

    file = Path(file_text.value)
    return (file,)


@app.cell
def _(co, file, parse_orbital_energies):
    orbital_energies = parse_orbital_energies(file)
    mol = co.Molecule.from_file(file)
    return mol, orbital_energies


@app.cell
def _(alt):
    def create_chart(df, x, y, color):
        chart = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x=alt.X(f"{x}:O", title=x),
                y=alt.Y(f"{y}:Q", title=y),
                color=alt.Color(f"{color}:O", legend=None),
                # tooltip=["orbital:O", "energy:Q"],
            )
        )
        return chart
    return (create_chart,)


@app.cell
def _(mo, orbital_energies, pl):
    # How does this behave for unrestricted calculations?

    _homo = orbital_energies.filter(pl.col("Occ") != 0).sort(
        by="Energy_Eh", descending=True
    )[0]

    LUMO_RANGE = 5
    frontier_orbitals_df = (
        orbital_energies.with_columns(
            (pl.col("Energy_Eh") - _homo["Energy_Eh"].item())
            .round(6)
            .alias("Rel_Energy_Eh")
        )
        .filter(pl.col("Id") <= _homo["Id"].item() + LUMO_RANGE)
        .sort(by="Id", descending=True)
    )

    orbitals_df = mo.ui.dataframe(frontier_orbitals_df, page_size=20)
    return LUMO_RANGE, frontier_orbitals_df, orbitals_df


@app.cell
def _(file, mo):
    ORBITAL_FILE_SUFFIXES = [".gbw", ".qro", ".unso", ".uno", ".uco"]
    _orbital_files = {
        f.name: f
        for suffix in ORBITAL_FILE_SUFFIXES
        for f in file.parent.glob(f"*{suffix}")
    }

    # Default to .gbw file
    _gbw_file = next((k for k in _orbital_files if k.endswith(".gbw")), None)

    orbital_file_dropdown = mo.ui.dropdown(
        label="Orbital file", options=_orbital_files, value=_gbw_file
    )
    # orbital_file_dropdown
    return ORBITAL_FILE_SUFFIXES, orbital_file_dropdown


@app.cell
def _(mo):
    isovalue_radio = mo.ui.radio(
        label="Isovalue",
        value="0.05",
        options={"0.1": 0.1, "0.05": 0.05, "0.025": 0.025, "0.001": 0.001},
        inline=True,
    )
    # isovalue_radio
    return (isovalue_radio,)


@app.cell
def _(frontier_orbitals_df, mo):
    _orbitals = {
        f"{o['Id']} ({o['Occ']:<8.2f}, {o['Rel_Energy_Eh'] * 2625.5:8.1f} kJ/mol)": o
        for o in frontier_orbitals_df.to_dicts()
    }

    orbital_selector = mo.ui.dropdown(label="Select orbital: ", options=_orbitals)
    # orbital_selector
    return (orbital_selector,)


@app.cell
def _(isovalue_radio, mo, orbital_file_dropdown, orbital_selector):
    mo.hstack([orbital_selector, isovalue_radio, orbital_file_dropdown])
    return


@app.cell
def _(isovalue_radio, mo, mol, orbital_file_dropdown, orbital_selector):
    mo.stop(not orbital_selector.value)

    _orb = orbital_selector.value["Id"]

    with mo.status.spinner(
        title=f"Plotting molecular orbital {_orb}.."
    ) as _spinner:
        _density = mol.create_molecular_orbital(orbital_file_dropdown.value, _orb)
        fig = mol.create_fig_with_isosurface(
            _density, isovalue=isovalue_radio.value
        )
    fig
    return (fig,)


@app.cell
def _(orbitals_df):
    orbitals_df
    return


@app.cell
def _(mo):
    show_spin_density = mo.ui.run_button(label="Show spin density")
    return (show_spin_density,)


@app.cell
def _(isovalue_radio, mo, mol, orbital_file_dropdown, show_spin_density):
    mo.stop(not show_spin_density.value)

    with mo.status.spinner(title="Plotting spin density..") as _spinner:
        _density = mol.create_spin_density(orbital_file_dropdown.value, grid=25)
        mol.show_with_isosurface(
            _density, isovalue=isovalue_radio.value, colors=("#24FF51", "#FA7496")
        )
    return


@app.cell
def _(mo):
    show_active_space = mo.ui.run_button(label="Show active space orbitals")
    return (show_active_space,)


@app.cell
def _(
    file,
    isovalue_radio,
    mo,
    mol,
    orbital_file_dropdown,
    parse_active_space_orbitals,
    parse_loewdin_orbital_compositions,
    pl,
    show_active_space,
):
    mo.stop(not show_active_space.value)

    active_space = parse_active_space_orbitals(file)
    loewdin_orbital_compositions = parse_loewdin_orbital_compositions(file)
    active_space_orbitals = {}

    with mo.status.progress_bar(
        title=f"Plotting active space orbitals..", total=len(active_space)
    ) as _progress_bar:
        for _orb in active_space:
            _density = mol.create_molecular_orbital(
                orbital_file_dropdown.value, _orb
            )
            active_space_orbitals[_orb] = mol.create_fig_with_isosurface(
                _density, isovalue=isovalue_radio.value
            )
            _progress_bar.update()

    mo.hstack(
        [
            mo.vstack(
                [
                    fig,
                    loewdin_orbital_compositions.filter(
                        pl.col("Id") == orbital
                    ).sort(by="Weight", descending=True),
                ],
                align="center",
            )
            for orbital, fig in active_space_orbitals.items()
        ],
        wrap=True,
    )
    return active_space, active_space_orbitals, loewdin_orbital_compositions


@app.cell
def _(mo):
    show_loewdin_orbital_compositions = mo.ui.run_button(
        label="Show Löwdin orbital compositions"
    )
    return (show_loewdin_orbital_compositions,)


@app.cell
def _(
    mo,
    show_active_space,
    show_loewdin_orbital_compositions,
    show_spin_density,
):
    mo.hstack(
        [show_spin_density, show_active_space, show_loewdin_orbital_compositions]
    )
    return


@app.cell
def _(
    file,
    mo,
    parse_loewdin_orbital_compositions,
    show_loewdin_orbital_compositions,
):
    mo.stop(not show_loewdin_orbital_compositions.value)

    _loewdin_orbital_compositions = parse_loewdin_orbital_compositions(file)
    mo.ui.dataframe(_loewdin_orbital_compositions)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
