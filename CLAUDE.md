# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Static HTML/CSS portfolio website used in the **DevOps Micro Internship (DMI) Week 1** exercise. Students deploy it on an **Ubuntu VM behind Nginx** and keep it live (reachable at `http://<public-ip>`) for 24 hours to practice Linux basics, Nginx hosting, and deployment/ownership proof.

## Architecture

- Pure HTML5 and CSS3 — **no JavaScript, no build step, no framework, no package manifest**
- There are **no tests and no linter**. Do not add npm/build tooling unless a task explicitly calls for it.

## Structure

- `index.html` — single-page site; content is organized into `<section>` elements anchored by id: `home`, `about`, `services`, `courses`, `book`, `community`, `contact`. Nav links target these anchors.
- `privacy.html`, `terms.html` — standalone legal pages sharing `style.css`.
- `style.css` — all styling for every page (there is no per-page stylesheet). Mobile-first, with breakpoints at 900px, 768px, and 600px.
- `images/` — logo, profile, signature, and section imagery referenced by relative path.

## Running / previewing

Nothing to build or compile. Open `index.html` in a browser, or serve the directory:

```bash
python -m http.server 8000   # then visit http://localhost:8000
```

## Deployment (the project's actual purpose)

The intended target is **Ubuntu + Nginx**, serving the repository contents as the web root (e.g. copy all files into `/var/www/html/`). Because it is fully static, GitHub Pages, Netlify, Vercel, or Cloudflare Pages also work with zero configuration.

> Note: this repo contains **no Terraform, no GitHub Actions, and no AWS/IaC configuration**. If a task asks for those, they must be created from scratch — they do not exist here yet.

## Mandatory DMI ownership rule (from README)

Before deploying, the footer in `index.html` must be edited to add a "Deployed by" proof line. The existing line is around line 604:

```html
<p>Crafted with <span>cloud</span> excellence by Pravin Mishra</p>
```

Add a line such as `<p><strong>Deployed by:</strong> DMI Cohort N | Name | Group N | Week 1 | DD-MM-YYYY</p>`. This proof must be visible in the browser screenshot submission.

## Known quirk: missing JavaScript

The markup references client-side behavior that **is not implemented anywhere in the repo** (there are no `<script>` tags and no `.js` files):

- `onclick="goToSection('...')"` handlers on the logo and mobile-menu buttons call an undefined function (no-op) — `index.html:20`, `48`, `51`, `52`, `53`.
- `onclick="toggleMenu()"` on the hamburger (`index.html:42`) is likewise undefined.
- `<span id="year"></span>` in the footer (`index.html:603`) is meant to be filled by script and renders empty.

Nav still works via plain anchor `href="#section"` links. If asked to "fix the navigation," "make the mobile menu work," or "show the current year," the fix is to add the missing JavaScript (define `goToSection` / `toggleMenu` and populate `#year`), not to rework the existing HTML.

## Conventions

- No JavaScript in this project (see the quirk above — adding JS is only appropriate when a task explicitly asks to fix that behavior).
- CSS uses a mobile-first approach with breakpoints at 900px, 768px, and 600px.
