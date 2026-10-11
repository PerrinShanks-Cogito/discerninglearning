# Discerning Learning

The published pages from the **Discerning Learning** WordPress site
(perrinshanks.com), migrated to a [Jekyll](https://jekyllrb.com/) static site.
It can be hosted on **Netlify** or **GitHub Pages**; the code lives here on GitHub.

## What was migrated

| Page | URL | Source file |
| --- | --- | --- |
| Home | `/` | `index.html` |
| My Approach | `/my-approach/` | `_pages/my-approach.md` |
| Design Thinking | `/knowledge-management/` | `_pages/knowledge-management.md` |
| 5 Moments of Learning Need | `/5-moments-of-learning-need/` | `_pages/5-moments-of-learning-need.md` |
| No Training Training | `/no-training-training/` | `_pages/no-training-training.md` |
| Data Discoveries | `/data-discoveries/` | `_pages/data-discoveries.md` |
| Hypothesis test selection road map | `/hypothesis-test-selection-road-map/` | `_pages/hypothesis-test-selection-road-map.md` |
| Statistics Glossary | `/statistics-glossary/` | `_pages/statistics-glossary.md` |
| Videos | `/video-2/` | `_pages/video.html` |
| Midlife Musings (blog index) | `/blog/` | `_pages/blog.html` |
| Blog posts (17) | `/YYYY/MM/DD/slug/` | `_posts/` |
| Category archives | `/category/analytics/` etc. | `_pages/category/` |
| About | `/about/` | `_pages/about.md` |

URLs match the WordPress ones (pages and posts), so existing links keep
working. There is also an RSS feed at `/feed.xml`. The old
`/blog-2/`, `/blog-3/` and `/colibri-wp/` pages redirect to their new homes.

Not migrated: the template placeholder **Contact** page (sample address and
email), the empty **Test** and **Blog 2** pages, and the H5P **xAPI Test** and
**SMART drag-and-drop** pages, whose content lives inside the WordPress H5P
plugin. The original About page was also a template placeholder, so the new
About page uses your own intro text from the site.

## Editing

- Pages are Markdown files in `_pages/`. Edit the text and commit.
- To write a new blog post, add `_posts/YYYY-MM-DD-your-title.md` starting
  with front matter like:

  ```yaml
  ---
  title: "My new post"
  categories: [Reflections]
  ---
  ```

  Optionally add an `excerpt:` line for the summary shown on the blog cards.
- Add images with a plain path from the repo root, e.g.
  `![Alt text](/assets/images/my-picture.png)`. They show in GitHub's file
  preview, and `_plugins/asset_baseurl.rb` fixes the path when the site is
  built for GitHub Pages.
- The menu is in `_data/navigation.yml`.
- Site title, author and tagline are in `_config.yml`.
- Styles are in `assets/css/main.scss`.

## Publishing from Word

You can write in Word and let GitHub do the rest — no commands needed.

1. On GitHub, open the `word` folder (or `word/pages` for a page rather than
   a blog post) and choose **Add file → Upload files**.
2. Drag in your `.docx` and click **Commit changes**.

The **Convert Word documents** GitHub Action then runs Pandoc on GitHub's
servers, turns the document into Markdown in `_posts/` (or `_pages/`), saves
any pictures under `assets/images/uploads/word/`, and commits the result.
GitHub Pages redeploys automatically afterwards (and Netlify rebuilds on the
new commit). Watch progress on the repo's **Actions** tab.

- **Title:** the document's Title (File → Info → Properties in Word), or a
  heading at the very top of the document, or else the file name.
- **Date:** start the file name with a date, e.g.
  `2025-07-04 Lean machine.docx`; otherwise the post is dated the day it is
  first converted.
- **Web address:** comes from the file name, e.g. `word/pages/My Page.docx`
  becomes `/my-page/`.
- **Updating:** upload a new version with the same file name and the same
  post or page is updated. Front matter you added by hand (e.g.
  `categories:` or `excerpt:`) is kept; the body is replaced.
- To re-convert every document, go to **Actions → Convert Word documents →
  Run workflow**. To run it on your own computer instead:
  `./scripts/word-to-markdown.sh` (needs Pandoc).

## Images

Images are stored under `assets/images/uploads/`. `scripts/fetch-images.sh`
downloads any missing ones from the WordPress site (the list is in
`scripts/wp-images.txt`), and both deploy setups run it on every build.
The **Fetch WordPress images** GitHub Action does this for you: it runs the
script on GitHub and commits any missing images. It runs automatically when
the image list changes, and you can start it any time from the repo's
**Actions** tab → **Fetch WordPress images** → **Run workflow**. To do it by
hand instead:

```sh
./scripts/fetch-images.sh
git add assets/images && git commit -m "Add images from WordPress"
```

## Run locally

Needs Ruby 3.x. (Or open the repo in GitHub Codespaces — the dev container has
Jekyll ready.)

```sh
bundle install
./scripts/fetch-images.sh
bundle exec jekyll serve
```

Then open http://localhost:4000.

## Deploy to Netlify

1. In Netlify, choose **Add new site → Import an existing project** and pick
   this GitHub repo.
2. Netlify reads `netlify.toml`, so the build command
   (`./scripts/fetch-images.sh && bundle exec jekyll build`) and publish
   directory (`_site`) are filled in for you. Click **Deploy**.
3. Optional: under **Domain management**, add your custom domain.

## Deploy to GitHub Pages

1. Merge this branch into `main`.
2. In the repo on GitHub, go to **Settings → Pages** and set **Source** to
   **GitHub Actions**.
3. The workflow in `.github/workflows/pages.yml` builds and deploys on every
   push to `main`. The site appears at
   `https://<your-username>.github.io/discerninglearning/` (the workflow sets
   the base URL for you), or at your custom domain if you add one under
   **Settings → Pages**.

## Moving perrinshanks.com off WordPress

All published pages and posts are now here, with the same URLs. Commit the
images first (see above), then point the perrinshanks.com DNS at Netlify or
GitHub Pages. Comments and email subscriptions from WordPress are not carried
over.
