
v0.10.2 (2015-05-22)
--------------------

- Various minor documentation and packaging updates. PSAMM is now available
  through [PyPI](https://pypi.python.org/pypi/psamm) and the documentation has
  been updated to reflect this. The documentation is available through
  [Read the Docs](https://psamm.readthedocs.org/). Lastly, the test suite is
  automatically run by [Travis CI](https://travis-ci.org/zhanglab/psamm).

v0.10.1 (2015-05-21)
--------------------

- Update README with new repository names and improved install instructions.
- docs: Add improved install instructions based on README.

v0.10 (2015-05-14)
------------------

- This software is now GPLv3 licensed. A copy of the license is included in
  [LICENSE](LICENSE).
- Allow setting the default flux limit in `model.yaml`. Previously a limit
  of 1000 units was used, and this value is still used if not specified.
- Allow setting the reaction name of the implicit exchange reactions
  specified in the medium definition.
- sbml: Change the SBML writer to avoid negative values for reaction
  stoichiometry. Some software packages do not handle negative values
  correctly when loading SBML files.
- command: Add a new option to `fluxcheck` where the restrictions imposed on
  the exchange reactions are removed before the consistency check.
- cplex: Use numerical emphasis mode by default.

v0.9 (2015-05-07)
-----------------

- Add methods the internal metabolic model representation to provide the
  compartments. This is used by commands instead of hardcoding specific
  model compartments when running `gapfill` or `fastgapfill`.
- docs: Update documentation on `psamm-model` commands.
- docs: Update information on installing the linear programming solvers.

v0.8 (2015-04-30)
-----------------

- The name of the project (in `setup.py`) changed name to `psamm`.
- The name of the main package changed from `metnet` to `psamm`.
- Remove unused scripts related to obsolete GAMS modeling.
- Assume TSV format for `.tsv` compound files. This removes the need for
  explicitly specifying `format: tsv` in the include.
- By default FVA and the flux consistency check will apply thermodynamic
  constraints. A command line option was added to go back to the previous
  behavior.
- Properly report compound names when multiple files are included.
- Add possibility of supplying additional solver parameters through the command
  line. Currently, the Cplex solver supports the parameters `threads` (the max
  number of threads allowed globally) and `feasibility_tolerance` (how much the
  basic variables of a model are allowed to violate their bounds).
- command: The command `randomsparse` now defaults to normal FBA without
  thermodynamic constraints. This is much faster and the additional constraints
  are guaranteed to not change the result in this case.
- docs: Enabled napoleon Sphinx extension for Google-style docstring support.
  This makes docstrings more readable while at the same time improving the
  generated docs. The `fluxanalysis` module was updated with additional
  documentation in this format.
- fluxanalysis: Change the API so that the `tfba` parameter can be given to
  functions that support thermodynamic constraints to select this mode. The
  support for thermodynamic constraints was extended to the flux consistency
  check and FVA.
- fluxanalysis: Slightly improve FVA by avoiding copying the model.
- sbml: Provide access to species charge.
- qsoptex: Fix error when calling the `status()` method of a result.
- command: Add option to see current version.

v0.7 (2015-04-23)
-----------------

- Change name of `model` script to `psamm-model`.
- native: Add YAML format for flux limits. The documentation has been updated
  to include more information on this format. This changes the `limits` key in
  `model.yaml` to a list of dicts.
- Add `--exchange` option to the `randomsparse` command to find random
  minimal sets of exchange reactions.
- Change name of `fluxconsistency` command to `fluxcheck`.
- Allow compounds to be marked as zero-mass (e.g. photons) by setting
  `zeromass: yes`. These compounds will be exempt from the mass requirements
  in the `masscheck` command.
- sbml: Provide access to model ID and name.
- sbml: Add option to skip boundary condition species when parsing.
- massconsistency: Fix bugs occurring when zero-mass compounds are specified.
- command: Log number of consistent reactions in `masscheck`.
- sbml: Fix a number of minor bugs.
- command: Fix search command when no alternative compound names are present

v0.6.1 (2015-04-20)
-------------------

- sbml: Fix bug where boundary conditions were parsed incorrectly.

v0.6 (2015-04-17)
-----------------

- Apply changes to the SBML parser in order for it to interoperate with
  `model-import`. This makes it easier to implement the SBML importer in
  `model-import`.
- Add non-strict mode to the SBML parser. This makes it possible to load
  almost-compliant SBML documents that are accepted by COBRA.
- `masscheck` command: Allow reactions to be marked as checked.
- cplex: Consider status `optimal_tolerance` to be successful.
- docs: Expand documentation on the `masscheck` command.
- docs: Change order of API documentation to `bysource`.

v0.5 (2015-04-09)
-----------------

- Add `sbmlexport` command to export current model as an SBML file.
- Add a generic interface to the linear programming solvers that delegates to
  an actual solver that is installed and has the required features. This adds
  a `--solver` option to a number of command which can be used to influence
  which solver is selected.
- Add `--epsilon` option to a number of commands that previously had the
  epsilon value hardcoded.
- Refactor functions in `fastcore` for easier use.
- docs: Extend docstring documentation of various modules.
- docs: Add DOI links for references.

v0.4 (2015-04-06)
-----------------

- Add documentation generated by Sphinx. The main contents of the
  [README](README.md) file has been moved to the new documentation.
- Generate the entry-point script using `setup.py`. This ensures that the
  package is correctly installed before the main script can be called. This
  also changes the name of the entry-point from `model.py` to `model`.
- Refactor functions in `massconsistency` for easier use.
- Add `__version__` attribute to main module.
- docs: Move references to separate section.
- docs: Fix file format documentation for medium file.
- Unit tests: Skip tests requiring a linear programming solver if Cplex is
  present.

v0.3 (2015-03-27)
-----------------

- Require reaction files to be explicitly listed in `model.yaml`.
- Add support for TSV reaction file format.
- Change format of YAML reactions (see [README](README.md) for details).
- Add tables of recognized compounds and reaction properties to
  [README](README.md).
- `masscheck` command: Automatically exclude biomass reaction from check.

v0.2 (2015-03-20)
-----------------

- Allow compounds to be specified using YAML, TSV or ModelSEED format. This
  changes the format of the `compounds` key in `model.yaml` (see
  [README](README.md) for more information).
- Allow specifying biomass reaction in `model.yaml` using the `biomass` key.
  The biomass reaction will be used by default for FBA, FVA, etc.
- Allow explicit definition of media. This can be defined using a table format
  or YAML format. See [README](README.md) for more information.
- `chargecheck`/`formulacheck` commands: Only check reactions where all
  compounds have charge/formula specified. The number of skipped reactions is
  reported separately.
- `chargecheck` command: Use charge information from model definition instead
  of requiring a separate charge table file.

v0.1 (2015-03-18)
-----------------

- Initial release.
