# Weir Interiors — website only

Full refined website: 20 pages and 303 gallery photographs. No WordPress theme, duplicate snapshot, hosting identity or audit reports are included.

## Upload to an existing GitHub repository

Extract this ZIP first. Upload/copy the contents of `Weir-Interiors-GitHub` to the repository root, not the wrapper folder or ZIP itself. Keep `dist`, `source`, `scripts` and `.github` in the root.

GitHub Desktop: clone your existing repository, copy these contents into the cloned folder, commit and push. In Finder, Command + Shift + . shows the hidden `.github`, `.gitignore` and `.nojekyll` items. Keep the cloned repository's `.git` folder.

Terminal: clone your repository, copy these contents into it, then run `git add .`, `git commit -m "Add Weir Interiors website"` and `git push` from the cloned repository folder.

Browser: use the separate browser-batch download. Upload each batch's contents at the repository root and commit before starting the next batch. Uploading a ZIP to GitHub does not extract its contents or make the site run.

## Preview, edit and build

Requires Python 3.9 or later. The ready-to-serve website is `dist/`.

```sh
python3 scripts/build-pages.py
python3 scripts/verify-site.py
python3 -m http.server 8000 --directory dist
```

Open http://localhost:8000/. The checker uses Pillow for image decoding when installed. It otherwise explicitly skips image decoding. Generated check reports are ignored by Git.

Edit `source/home.html` for homepage content, `scripts/build-pages.py` for shared layout and other page content, `dist/styles.css` for styling, and `dist/script.js` for interactions. Gallery source/rights information remains in `source/gallery-data.json`; font provenance and the font licence are included.

## GitHub Pages

After upload, select Settings → Pages → Source → GitHub Actions. Open Actions → Deploy static preview to GitHub Pages → Run workflow. The included workflow builds and checks the site and adapts links and font paths to your repository's URL. The workflow is manual and has not been executed in your account. GitHub Pages availability/access depends on your repository and plan.

For other root-domain static hosts, publish the contents of `dist/`. For a subdirectory, use:

```sh
python3 scripts/export-static.py --output public --base-path /YOUR-REPOSITORY/
```

Preview noindex protections remain. Hosting may be publicly accessible; noindex does not restrict access. Contact opens a validated email draft. Browser visual/keyboard and actual email/phone checks remain outstanding. Original business imagery/logo require appropriate rights before official launch. The official business domain is unchanged.
