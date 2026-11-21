# NESE Public Regulatory Watch

Two public-facing research sites for the Northeast Supply Enhancement (NESE) / Transco project.

- `/lighthouse/` — Romer Shoal & West Bank preservation and geospatial evidence watch.
- `/pipeline/` — General Northeast Supply Enhancement news and regulatory watch.

The index page links both reports. Host this repository root as a static site on Vercel under the `romer-shoal-light` team. Set Framework Preset to **Other**, Root Directory to `./`, with no build command. Vercel will supply the actual public domain after deployment.

## Automated updates

`.github/workflows/daily-update.yml` runs `scripts/daily.py` once daily and on manual dispatch. It checks accessible official project pages for change signals and Google News RSS for matching press items, recording discovery dates and source URLs. Monitoring results remain **unverified** until the linked filing or article is reviewed. The workflow does NOT establish exact legal deadlines, verify every FERC filing, or perform new GIS overlays. No change signal is not proof of absence of filings. Do not describe candidate headlines as confirmed agency actions.

## Editorial policy

A verified item means a primary source was reviewed or an official site was observed. An unverified item is a discovery candidate or unresolved issue. All data from the November 2026 baseline is explicitly labeled, and publication is independent of NJDEP, FERC and Williams. Historic-distance calculations are evidence-dependent; pipeline centerline distance is not construction workspace clearance.

## Workflow

The daily scheduler is about 8am US/Eastern, subject to GitHub Actions queue delay. GitHub Actions must be enabled and the workflow needs `contents: write` to commit the daily update. Any changes automatically deploy when Vercel is connected to the GitHub repository and production branch `main`.

Official sources: https://dep.nj.gov/nese/ ; https://www.williams.com/nese-njdep-application/ ; https://elibrary.ferc.gov/eLibrary/ ; https://dec.ny.gov/news/environmental-notice-bulletin ; https://www.achp.gov/ .
