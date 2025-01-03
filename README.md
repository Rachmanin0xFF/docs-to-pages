# docs-to-pages

## What is this?

GitHub (this website) lets users host [static web pages](https://en.wikipedia.org/wiki/Static_web_page) for free with a service called [GitHub Pages](https://pages.github.com/). However, using this service requires a little technical know-how that can seem daunting for non-programmer folk.

**docs-to-pages** is a project that *automatically creates a static website* from a **Google Drive folder**. It takes all the Google Docs in the folder and splats them onto a web page.

## Instructions
*These look messy right now, I'll add some little video snippets to make this more digestible soon.*

### 1. Make a GitHub account (if you don't already have one)
You can do that [here](https://github.com/signup). It'll ask you for an email, username, and password, and might make you verify those things.

### 2. Click the button that says "use this template", and select "Create a new repository"
In the upper right corner of [this page](https://github.com/Rachmanin0xFF/docs-to-pages/tree/main) (hopefully the page you are on), there should be a button that says "Use this template". 

### 3. Type a website name in the "Repository name" slot, and click "Create repository"
Leave everything else on the default settings.

### 4. On the page that appears, go to "Settings", then "Pages", and change the box that say "Deploy from a branch"
You'll want to switch it to "GitHub Actions". (Sorry, we're almost done!)

### 5. Go back to "Code" and click on the file that says "LINK_TO_DRIVE_FOLDER"

### 6. Click on the pencil button in the upper right to edit the file

### 7. Delete the link in there, and paste a link to your own Drive folder
Note: The drive folder needs to contain a Google Doc titled "index" (no caps) for it to work properly.

### 8. Press "Commit changes...", then "Commit changes" in the new box that appears
Your website will be live in a few minutes!
