# MIT License
# Static site builder python script

import sys
import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import markdown #markdown.markdown(text)
import xml.etree.ElementTree as ET
from datetime import datetime

# Global Variables
WEBSITE_URL = "https://www.westonbishop.com"
WEBSITE_TITLE = "WestonBishop.com"
GENERATE_RSS = True
FEED_LENGTH = 10

CONTENT_DIR = "content/"
POSTS_DIR = CONTENT_DIR + "posts"
INCLUDE_DIR = "include/"
PUBLIC_DIR = "public/"
IMG_DIR = INCLUDE_DIR + "img"

HEADER = INCLUDE_DIR + "header.html"
FOOTER = INCLUDE_DIR + "footer.html"

@dataclass
class Post:
    title: str
    date: str
    url: str
    description: str

postsList = []
homepage_list = []



# Function Definitions
# Copies static assets such as images and stylesheet.
def copyAssets():

    print( "Copying static assets..." )

    # copy images
    shutil.copytree( Path( IMG_DIR ), PUBLIC_DIR + "img" )

    # copy stylesheet
    shutil.copy( Path( INCLUDE_DIR + "style.css"), PUBLIC_DIR)

# Builds the posts
def buildPosts():

    content = ""
    dir_path = Path( POSTS_DIR )

    for item in dir_path.iterdir():
        print(item)

        if item.is_file():

            with open(item, 'r') as file:
                content = file.read()

            lines = content.splitlines()

            for line in lines:
                clean_line = line.strip()
                if clean_line:
                    data_elements = clean_line.split(': ')
                    if data_elements[0] == "title":
                        title = data_elements[1]
                        print( "Found post: " + title )
                    if data_elements[0] == "date":
                        date = data_elements[1]
        
            base = Path(item).stem
            outpath = PUBLIC_DIR + "posts/" + base + ".html"
            post_body = markdown.markdown(content)

            with open(outpath, 'w') as outfile:
                with open(HEADER, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)

                outfile.write(post_body)

                with open(FOOTER, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)

            homepage_list.append("<li><span class='post-date'>" + date + "</span> - <a href='posts/" + base + ".html'>" + title + "</a></li>")

            url = WEBSITE_URL + "/posts/" + base + ".html"
            newpost = Post(title, date, url, post_body)
            postsList.append(newpost)

# Constructs the homepage
def buildIndex():

    print("Building homepage...")    

    homepage_list.sort()

    # Optional: include index.html in content/ to get a block on homepage for welcome text.
    intro_html = ""
    index_path = CONTENT_DIR + "index.md"

    if os.path.isfile(index_path):
        with open(index_path, 'r') as file:
            content = file.read()
            intro_html = markdown.markdown(content)

    outpath = PUBLIC_DIR + "index.html"

    with open(outpath, 'w') as outfile:
        with open(HEADER, 'r') as infile:
            shutil.copyfileobj(infile, outfile)

        outfile.write(intro_html + "<h1>Posts</h1><ul>\n")

        for item in homepage_list:
            outfile.write(item + "\n")

        outfile.write("</ul>")

        with open(FOOTER, 'r') as infile:
            shutil.copyfileobj(infile, outfile)

# Constructs the other pages besides posts and homepage
def buildChildren():

    print("Building other pages...")

    dir_path = Path( CONTENT_DIR )

    for item in dir_path.iterdir():

        if item.is_file():
            base = Path(item).stem

            if base == "index":
                break

            outpath = PUBLIC_DIR + base + ".html"

            with open(item, 'r') as file:
                content = file.read()
                content_body = markdown.markdown(content)

            with open(outpath, 'w') as outfile:
                with open(HEADER, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)

                outfile.write(content_body)

                with open(FOOTER, 'r') as infile:
                    shutil.copyfileobj(infile, outfile)

# Builds RSS feed and puts it in feed.xml
def buildFeed():

    sorted_posts = sorted(postsList, key=lambda x: x.date)

    rss = ET.Element('rss', version='2.0')
    channel = ET.SubElement(rss, 'channel')

    ET.SubElement(channel, 'title').text = WEBSITE_TITLE
    ET.SubElement(channel, 'link').text = WEBSITE_URL
    ET.SubElement(channel, 'description').text = WEBSITE_TITLE
    ET.SubElement(channel, 'lastBuildDate').text = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')

    i = FEED_LENGTH
    for post in sorted_posts:
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = post.title
        ET.SubElement(item, 'link').text = post.url
        ET.SubElement(item, 'description').text = post.description

        dt = datetime.strptime(post.date, "%Y-%m-%d")
        ET.SubElement(item, 'pubDate').text = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

        i = i - 1
        if i == 0:
            break

    feed = ET.tostring(rss, encoding='utf-8', xml_declaration=True).decode('utf-8')

    with open(PUBLIC_DIR + 'feed.xml', 'w') as outfile:
        outfile.write(feed)

# main
def main():

    shutil.rmtree( Path( PUBLIC_DIR ), ignore_errors=True )
    os.makedirs( PUBLIC_DIR + "posts" )

    copyAssets()
    buildPosts()
    buildIndex()
    buildChildren()

    if GENERATE_RSS:
        buildFeed()

    print( "Done! All pages are in " + PUBLIC_DIR )

if __name__ == "__main__":
    main()











