Naiomi Summers · Projects

Preview
Extract the ZIP, then open index.html in a browser. The portfolio includes its
photograph, app logos, fonts, and navigation. App releases and GitHub links
open online. The portfolio itself needs no installation or build step.

GitHub Pages
Place the extracted contents in the publishing folder of NaiomiSummers/Projects,
with index.html at the top of that folder. Keep about/ and assets/ alongside it.
The relative links work under the repository's /Projects/ address.

Pages
index.html is the About Me homepage. projects.html is the project directory.
The six app guides use the original about/ addresses to preserve bookmarks.
about-me.html also serves the biography for visitors with the earlier URL.

Releases
Five guides link to the apps running on GitHub Pages. FirmQuill Full Suite
links to a pinned ZIP of the runnable source for version 0.1.0-preview.1.
That preview runs on a local host with Node.js. Its repository README includes
the startup steps for the books and worker portals.

Keep the “Early Development” label, Early Development Build notice, feedback links and Terms of Service available in future releases, including after launch. Change the terms version only when issuing new terms. Review copies require publisher approval.

Updating a browser app agreement
Keep the Projects checkout alongside FQ-Lite, CurbQuill, Day-Leaf, MileQuill-Lite
and PocketQuill. Prepare a UTF-8 .txt agreement with its existing title, a blank
line, then a higher numbered version and its date, e.g. Version 1.1  |  [date].
From the parent directory on Windows, run:

  .\Projects\tools\Update-Terms.ps1 -App Day-Leaf -Agreement "C:\path\to\revised.txt"

That prepares a labeled local draft. After approval run the same command with
-Approved. The helper refreshes the agreement bundled in the app, the matching
Projects terms page, and the offline release files. It also refreshes the DayLeaf
download. Python 3 users can run tools/update_terms.py directly. Use
node Projects/tools/check-terms.mjs from the parent directory to compare all six
app agreements with their public pages. Review the changes in both repos before
you publish them. The helper only writes local files.

The five browser apps check their own published terms.json on open, return to
the foreground, and reconnection. Once Pages serves a higher version, the app
asks for a new agreement. Offline users can open the latest available agreement
on their device. Existing installations first need the release containing this
feature through their ordinary app-update flow.

FirmQuill Full Suite uses the version bundled on its company host. Installing
a new host agreement prompts each account before either portal can serve records.
The Projects website itself has a public terms page at terms/index.html.
