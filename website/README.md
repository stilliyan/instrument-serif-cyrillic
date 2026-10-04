# Spasov Type website

The Lirena specimen website at https://spasovtype.com/.

This directory contains the production HTML, styles, interactions, fonts,
glyph comparisons and the Regular + Italic download package.

## Local preview

From this directory, run:

```sh
npm start
```

Open http://127.0.0.1:3040/. No dependencies or build step are required.

## Vercel

The Vercel project is `spasovtype`. Use `website` as the root directory when
connecting this repository. The included `vercel.json` publishes the static
files without a build step.

The primary domain is https://spasovtype.com/. The `www` domain redirects to it.
Canonical, social image and sitemap URLs use the primary domain.

The download includes font licenses, credits and installation instructions.
Font source files and adaptation scripts are in the repository root.
