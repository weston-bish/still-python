# MIT License
# Static site builder python script

import sys
import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import markdown #markdown.markdown(text)

# Global Variables
WEBSITE_URL = "https://www.westonbishop.com"

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

homepage_list = []



# Function Definitions
# Copies static assets such as images and stylesheet.
def copyAssets():
    print( "Copying static assets..." )

    # copy images
    shutil.copytree( Path( IMG_DIR, PUBLIC_DIR ))

    # copy stylesheet
    shutil.copy( Path( INCLUDE_DIR + "style.css", PUBLIC_DIR))

# Builds the posts
def buildPosts():
    dir_path = Path( POSTS_DIR )

    for item in dir_path.iterdir():
        if item.is_file():
            with open(item, 'r') as file:
                for line in file:
                    clean_line = line.strip()
                    if clean_line:
                        data_elements = clean_line.split(':')
                        if data_elements[0] == "title":
                            title = data_elements[1]
                        if data_elements[0] == "date":
                            date = data_elements[1]
            
            base = Path(item).stem
            outpath = PUBLIC_DIR + "posts/" + base + ".html"
            post_body = markdown.markdown(item)

            with open(outpath, 'wb') as outfile:
                with open(HEADER, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

                outfile.write(post_body)

                with open(FOOTER, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

            homepage_list.append("<li><span class='post-date'>" + date + "</span> - <a href='posts/" + base + ".html'>$title</a></li>")

            url = WEBSITE_URL + "/posts/" + "base.html"
            newpost = Post(title, date, url, post_body)

# Constructs the homepage
def buildIndex():

    print("Building homepage...")    

    homepage_list.sort()

    # Optional: include index.html in content/ to get a block on homepage for welcome text.
    intro_html = ""
    index_path = CONTENT_DIR + "index.md"

    if os.path.isfile(index_path):
        intro_html = markdown.markdown(index_path)

    outpath = PUBLIC_DIR + "index.html"

    with open(outpath, 'wb') as outfile:
        with open(HEADER, 'rb') as infile:
            shutil.copyfileobj(infile, outfile)

        outfile.write(intro_html + "</main><main><h1>Bulletin</h1><ul>")

        for item in homepage_list:
            outfile.write("<h1>Bulletin</h1><ul>" + item + "</ul>")

        with open(FOOTER, 'rb') as infile:
            shutil.copyfileobj(infile, outfile)

# Constructs the other pages besides posts and homepage
def buildChildren():
    dir_path = Path( CONTENT_DIR )

    for item in dir_path.iterdir():
        if item.is_file():
            base = Path(item).stem
            outpath = PUBLIC_DIR + base + ".html"
            content_body = markdown.markdown(item)

            with open(outpath, 'wb') as outfile:
                with open(HEADER, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

                outfile.write(content_body)

                with open(FOOTER, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)


# Constructs the homepage
def main():
    shutil.rmtree( Path( PUBLIC_DIR ))
    os.mkdir( PUBLIC_DIR + "posts" )

    copyAssets()
    buildPosts()
    buildIndex()
    buildChildren()

    print( "Done! All pages are in " + PUBLIC_DIR )

if __name__ == "__main__":
    main()











