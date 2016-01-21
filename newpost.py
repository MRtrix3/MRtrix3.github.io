#!/usr/bin/python
#
# Initialise new post for MRtrix website
# Author: Rami Tabbara
#

import sys, getopt, datetime, os

def usage():
    print ('''
usage: ./newpost.py [-t, --title] post_title [-a --author] post_author [c --categories] post_categories

OPTIONS:

  --title           directory where mrtrix source commands reside
  --author          github handle coressponding to author
  --categories      list of post categories (optional)

Example:
    
    ./newpost.py --title 'My awesome title' --author 'jdtournier' --categories 'awesome feature release'
''')


def main(argv):

    title = None
    author = None
    categories = ''
    
    now = datetime.datetime.now()
    timezone = "-0600" #Hard-wire for now
    date = now.strftime("%Y-%m-%d %H:%M:00") + " " + timezone    

    try:
        opts, args = getopt.getopt(argv, "t:a:c", ["title=", "author=", "categories="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-t", "--title"):
            title = arg
        elif opt in ("-a", "--author"):
            author = arg
        elif opt in ("-c", "--categories"):
            categories = arg

    if title is None or author is None:
        usage()
        exit(2)    


    dirn = "_posts/" + now.strftime("%Y/%m/")
    if not os.path.exists(dirn):
	    os.makedirs(dirn)

    filename = dirn + now.strftime("%Y-%m-%d") + "-" + title.replace(" ", "-").lower() + ".md"

    filecont = """---
layout: post
title: {}
author: {}
date: {}
categories: {}
---

Place your markdown content here! Uses [kramdown syntax](http://kramdown.gettalong.org/syntax.html).
Below are a few example features that you can incorporate into your post.

Remember to place any images used in `/images/posts` directory.

Code snippets (no highlighting):

~~~
def my_awesome_function():
    print 'My awesome function'
~~~

Code snippets (with language highlighting):

{{% highlight python %}}
def my_awesome_function():
    print 'My awesome function'
{{% endhighlight %}}

Math snippets (using LaTex syntax)

$$
\oint_{{C}} f(z) \, dz = 2 \pi i \sum Res(f, a_k)
$$

    """.format(title, author, date, categories)

    writer = open(filename, "w")
    writer.write(filecont)
    writer.close()
    print '\nNew post created at: ' + filename

if __name__ == "__main__":
    main(sys.argv[1:])
