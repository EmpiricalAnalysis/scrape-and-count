## Scrape and Count

This utility runs with the command `python scrape_and_count/main.py get-word-count`.

If you want to get the count from a dynamic webpage where JavaScript has been loaded, make sure to install geckodriver on your system, then issue the command `python scrape_and_count/main.py get-word-count --dynamic True`.

You can also change the default url (Wikipedia's python page) to one of your choice. To do so, use the command `python scrape_and_count/main.py get-word-count --url https://google.com`.
