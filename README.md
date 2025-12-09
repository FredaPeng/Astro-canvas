# Astro-canvas

A small static site consisting of a few HTML pages and an assets folder containing data and images used by the pages.

Quick start

- Open the site locally: double-click `index.html` or serve the folder and open http://localhost:8000
  - To serve quickly from macOS (zsh):

    python3 -m http.server 8000

- Files of interest:
  - `index.html`, `astro.html`, `astro_lucid.html`, `cosmic_draw.html` — main pages
  - `assets/` — images and data used by the site (JSON manifests and images)

About "transform to Pages" showing queued/overtime

If your Pages deployment (or other hosting transform) shows messages like "Queued", "Queued overtime", or long delays, common causes and checks:

- GitHub Pages build queue or GitHub Actions backlog: check the repository's Actions and Pages build logs in the GitHub UI for build progress and errors.
- Large files in the repo (big images, videos): large assets can slow or block deployments. Consider moving large media to a CDN, Git LFS, or an external hosting service.
- Missing or misconfigured deployment settings: GitHub Pages expects either the repository root or `docs/` folder (or `gh-pages` branch). Confirm the Pages source in repository settings.
- Using an external CI/deployer (Netlify/Vercel): check that provider's build/deploy logs — e.g., Netlify UI or Vercel dashboard — for queue/backlog messages.
- Rate limits or outages: intermittently GitHub or third-party hosts can queue builds during high load.

Recommended quick troubleshooting steps

1. In GitHub: open the repository, click "Actions" and "Pages" to view any running or failed builds and their logs.
2. Check for very large files:
   - Run `git ls-files --stage` and inspect file sizes locally or use `du -sh assets/*` to see large directories.
3. If builds are queued repeatedly: try a small test change (e.g., edit `README.md`) and push to see whether the Pages build starts and completes.
4. Consider hosting static pages on Netlify or Vercel (they show clearer deploy logs), or push to a `gh-pages` branch and use a simple deploy action.

If you'd like, I can:
- scan the repository for very large files and list them,
- add a small GitHub Action to deploy to `gh-pages`, or
- add a note to the README about how you currently deploy (if you tell me which provider you use).

License: MIT (add a license file if you want to use a different license)
