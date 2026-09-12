---
name: ning-python-scientific-plotting
description: >-
  Create, refine, or review scientific figures in Python using the bundled
  plotting notes. Use for research and publication plots, choosing charts for
  experimental data, distributions, model comparisons, geospatial figures,
  multi-panel layouts, color choices, and figure export. Not for generic website
  styling, image generation, or statistical conclusions unsupported by data.
---

# Python Scientific Plotting

Use the nine chapter notes as a task-specific reference library, not a sequence
to read in full. Preserve the user's research question, data, existing plotting
code, and requested output.

## Workflow

1. Identify the question the figure must answer, the actual input files and
   columns, variable types, units, groups or paired observations, and output
   constraints. Inspect existing code before changing it. Ask only for missing
   information that materially changes the result.
2. Read the relevant chapter from the table below. Consult design or tool notes
   when those choices are in scope; use the glossary for unfamiliar terms.
3. For implementation, adapt the project's existing plotting stack. Prefer
   explicit Matplotlib Figure/Axes objects and use Seaborn for statistical
   mappings when appropriate. Optional style or specialist packages are not
   mandatory dependencies. Chapter snippets contain illustrative inputs and
   environment assumptions: check data definitions, imports, installed APIs,
   style registration, and fonts before reusing them.
4. Generate the requested figure and inspect the exported result at its intended
   size. Check labels, units, legends, panel alignment, colorbars, clipping, and
   whether comparison panels use comparable scales. For figure review or
   conceptual advice, limit the work to the requested review or explanation.

## Choose References

All links are relative to this skill directory.

| Task | Read |
| --- | --- |
| Figure purpose, typography, color semantics, accessibility, vector/raster choices | [Chapter 1: Design and color](chapters/ch01-figure-design-and-color.md) |
| Matplotlib/Seaborn objects, styling, layout, optional ProPlot/SciencePlots | [Chapter 2: Plotting tools](chapters/ch02-plotting-tools.md) |
| Histograms, KDE, Q-Q/P-P plots, ECDF, distribution diagnostics | [Chapter 3: Univariate plots](chapters/ch03-univariate-plots.md) |
| Group comparisons, error bars, scatter/regression, time series, ROC and survival plots | [Chapter 4: Bivariate plots](chapters/ch04-bivariate-plots.md) |
| Contours, vector fields, bubbles, ternary/3D plots, PCA, parallel coordinates, flows | [Chapter 5: Multivariate plots](chapters/ch05-multivariate-plots.md) |
| CRS, projections, spatial joins, choropleths, proportional symbols, inset maps | [Chapter 6: Geospatial plots](chapters/ch06-geospatial-plots.md) |
| Bland-Altman, paired observations, Taylor, forest/funnel, Venn and Smith plots | [Chapter 7: Specialized plots](chapters/ch07-specialized-plots.md) |
| Observed-versus-predicted comparisons and coherent multi-panel model evaluation | [Chapter 8: Academic figure case study](chapters/ch08-academic-figure-case-study.md) |
| Submission dimensions, formats, fonts, captions, export checks | [Chapter 9: Journal figure requirements](chapters/ch09-journal-figure-requirements.md) |
| Reusable workflows spanning several chapters | [Patterns](patterns.md) |
| Definitions and the chapter associated with a plotting term | [Glossary](glossary.md) |

## Interpretation and Output

- Compute plotted values and annotations from the supplied data. Do not invent
  observations, sample sizes, significance, or model metrics. Clearly label
  synthetic demonstration data when an example calls for it.
- Preserve pairing, explain exclusions or transformations, and state what error
  bars represent. Specialized plots require their statistical inputs and
  assumptions; correlation, agreement, and causation are not interchangeable.
- Use Chapter 9 as a historical checklist, not verified current journal policy.
  It summarizes a 2023 book edition. For journal-specific submission work, use
  the journal's current official instructions or the user's supplied guidelines;
  identify anything unverified when those instructions cannot be checked.
- For figure creation or revision, deliver the requested exports and the
  reproducible plotting code, preferably by updating the existing script.
  Record relevant input paths, transformations, export settings, and any
  environment requirements. Prefer vector output for line art when compatible
  with the requested format; do not mandate extra formats or style packages.
- Report whether rendering and visual inspection actually succeeded. If inputs,
  dependencies, or preview tools are unavailable, explain the limitation rather
  than claiming the figure was verified.
