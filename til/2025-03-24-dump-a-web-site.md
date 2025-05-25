---
title: Dump a web site directly to local
date: 2025-03-24
---

Find a simple way to dump a web site directly to local, including all HTML, CSS, JS, images, and other assets.

```sh
wget -c -m -k -K -E -l 7 -t 3 -w 2 https://example.org
```

- `-c`: Continues a download that was interrupted. If the download was partially completed before, this flag tells wget to resume rather than start over.
- `-m`: Activates "mirror" mode. This is equivalent to a combination of several options (like `-r` for recursive retrieval, `-N` to timestamp, and `-l inf` for infinite recursion by default) but here combined with other options you effectively create a mirror of the site.
- `-k`: After the download is complete, converts the links in the downloaded files so that they point to the locally downloaded copies rather than the online versions. This is particularly useful for offline browsing.
- `-K`: Keeps the original files (the ones downloaded from the server) in addition to the converted files. Files are typically saved with a .orig extension. This allows you to reference the original state if needed.
- `-E`: Adjusts the file extensions. When downloading HTML or text files that don't have a `.html` extension, `wget` will automatically give them the `.html` extension so they can be easily viewed locally in a browser.
- `-l 7`: Sets the maximum recursion depth to 7 levels. That means wget will follow links recursively up to 7 levels deep from the starting page.
- `-t 3`: Limits the number of tries for each download to 3. If a file cannot be downloaded on the first attempt, wget will retry up to 2 additional times.
- `-w 2`: Tells wget to wait 2 seconds between retrievals. This pause helps reduce the load on the remote server and can avoid triggering rate limits.

Refs:

- [html - How can I scrape a website and store all pages and assets locally - Stack Overflow](https://stackoverflow.com/questions/9265172/how-can-i-scrape-a-website-and-store-all-pages-and-assets-locally)
- [Downloading an Entire Web Site with wget | Linux Journal](https://www.linuxjournal.com/content/downloading-entire-web-site-wget)
- [wget - Download a working local copy of a webpage - Stack Overflow](https://stackoverflow.com/questions/6348289/download-a-working-local-copy-of-a-webpage)
- [Rip a website via HTTP to download images, HTML and CSS - Super User](https://superuser.com/questions/130306/rip-a-website-via-http-to-download-images-html-and-css)
