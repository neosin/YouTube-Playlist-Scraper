import re
import urllib.request
import urllib.error
import sys
import os


def crawl(playlist_url, out):
    """Crawls a playlist URL and outputs found links"""
    list_id = ""
    scraped_urls = []

    # Check if the playlist link contains the 'list' element
    if 'list=' in playlist_url:
        regex = r"[^&?]*?list=([^&?]*)"
        list_id = re.findall(regex, playlist_url)[0]
        if list_id == "":
            print("List parameter was empty")
            sys.exit(1)
    else:
        print('YouTube URL must contain the "list=" parameter')
        sys.exit(1)

    scraping_url = "https://youtube.com/playlist?list=" + list_id

    # Get content from page and filter through to get what we want
    with urllib.request.urlopen(urllib.request.Request(scraping_url)) as response:
        web_links = re.findall(re.compile(
            r'watch\?v=[^&]*\&list=' + list_id), str(response.read().decode("unicode_escape")))
    if web_links:
        for i in web_links:
            if '&' in str(i):
                scraped_urls.append('https://www.youtube.com/' +
                                    str(i)[:(str(i).index('&'))])

        scraped_urls = list(set(scraped_urls))
        for i, j in enumerate(scraped_urls):
            print(j + '\n')

        if out:
            output_file = open(out, 'w')
            # Output to console and file
            for i, j in enumerate(scraped_urls):
                output_file.write(j + '\n')
            output_file.close()

        sys.exit(0)
    else:
        print('No videos found.')
        sys.exit(1)


def print_usage():
    """Prints the usage to console"""
    print('USAGE: ' + os.path.basename(__file__) + ' [url] [output]')


ARG_LEN = len(sys.argv)

if ARG_LEN < 2 or ARG_LEN > 3:
    print_usage()
    sys.exit(1)
else:
    url = sys.argv[1]
    if ARG_LEN == 2:
        crawl(url, "")
    elif ARG_LEN == 3:
        crawl(url, sys.argv[2])
    else:
        print_usage()
        sys.exit(1)
