# Troubleshooting Jekyll Site Issues

## Problem 1: The Site Wouldn't Build (SCSS Variable Errors)

**The Symptom:** You ran `bundle exec jekyll serve` and got a big, red error message in the terminal. The site at http://127.0.0.1:4000/ was either completely down or showing a server error page.

**My Diagnostic Process:**
* I looked at the terminal output you provided.
* I scanned for the word "Error". I found this line: `Conversion error: Jekyll::Converters::Scss ... Undefined variable: "$doc-font-size-medium"`.
* This told me everything I needed to know:
  * **What:** A Sass/SCSS variable was missing (`$doc-font-size-medium`).
  * **Where:** The error was happening during the CSS conversion process, originating from your main.scss file.

**How You Can Do It Yourself:**
* Always look at the terminal first when your site doesn't build.
* Find the line that starts with `Error:`.
* Jekyll will usually name the problematic file and the specific variable or import that's causing the issue. This tells you exactly where to start fixing things.

## Problem 2: The Homepage Was Blank

**The Symptom:** After we fixed the build errors, the site was "running," but the homepage was completely empty. There were no posts, no text—nothing.

**My Diagnostic Process:**
* I checked the terminal again. This time, there were no build errors. This is a critical clue. It means the problem isn't with the site's technical setup but with its content.
* If the homepage is blank, the first file to inspect is the one that generates it: index.md or index.html.
* I examined your index.md and saw it only contained front matter (`--- title: "AI 4 YOU" ---`) but was missing two crucial things:
  * `layout: home`: It didn't know how to structure itself.
  * Any actual content to display.

**How You Can Do It Yourself:**
* If the site builds but a page is blank, check the corresponding .md or .html file for that page.
* Ensure the front matter has a layout defined. For a theme like Minimal Mistakes, this is essential. The homepage almost always needs `layout: home`.
* If you want text on the page, you need to add it below the front matter.

## Problem 3: The New Blog Post Was Missing

**The Symptom:** The site was working, but your new article, "From Python to Thunderbird Extension...", wasn't showing up in the list of recent posts.

**My Diagnostic Process:**
* Again, I knew the site was building correctly, so this had to be an issue with the post file itself.
* I checked the filename: `_posts/2025-08-08_Trello_Thunderbird_extension_with_warp.md`.
* I immediately checked it against Jekyll's strict rules for posts:
  * Rule 1: **Filename Format**. The filename must be `YYYY-MM-DD-your-title.md`. Your filename used underscores instead of hyphens in the title part.
  * Rule 2: **Future-Dating**. The date in the filename (2025-08-08) did not match the date in the file's front matter (date: 2025-08-10). More importantly, Jekyll, by default, will not publish posts with a date in the future.

**How You Can Do It Yourself:**
* If a post is missing, first check the `_posts` folder.
* Verify the filename is in the exact `YYYY-MM-DD-title-with-hyphens.md` format.
* Check the date in the post's front matter. Make sure it's set to today or a past date. If you need to work on a post for the future, you can run the server with the `--future` flag: `bundle exec jekyll serve --future`.
  * **What:** A Sass/SCSS variable was missing (`$doc-font-size-medium`).
  * **Where:** The error was happening during the CSS conversion process, originating from your main.scss file.

**How You Can Do It Yourself:**
* Always look at the terminal first when your site doesn't build.
* Find the line that starts with `Error:`.
* Jekyll will usually name the problematic file and the specific variable or import that's causing the issue. This tells you exactly where to start fixing things.
