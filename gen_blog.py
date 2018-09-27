#!/usr/bin/env python2
#
# Pull the latest MRtrix community announcements and blog posts
# and package them as blog posts to be pushed onto the website.
#
# Authors: J-D Tournier and Rami Tabbara
#

import sys, getopt, json, requests, os, yaml, re

def usage():
    print ('''
usage: ./gen_blog.py [-a, --all]

OPTIONS:

  --all           specifies whether blog posts for all latest forum announcements and blog posts should be generated. By default we only fetch the latest forum post.
''')


def main(argv):

    fetch_only_first = True

    try:
        opts, args = getopt.getopt(argv, "a", ["all"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--all"):
            fetch_only_first = False

    site = 'http://community.mrtrix.org'

    # 9 = Announcements
    # 11 = Blog
    for category in ['9', '11']:

        r = requests.get (site + '/c/{}/l/latest.json'.format(category))
        p = json.loads (r.text)

        author_list = yaml.load(file(os.path.join('_data', 'authors.yml'), 'r'))

        for x in (p['topic_list']['topics']):

            r = requests.get (site + '/t/' + str(x['id']) + '.json?include_raw=1')
            t = json.loads (r.text)
            post = t['post_stream']['posts'][0]
            discourse_id = x['id']
            author_handle = post['username']

            for author in author_list:
                # Match Discourse handle to GitHub handle (if it exists)
                if 'discourse' in author and author['discourse'] == author_handle:
                    # Try to use GitHub handle if it exists
                    if 'github' in author:
                        author_handle = author['github']


            date = post['created_at'].replace('T', ' ').split('.')[0]
            date_simplified = date.split()[0]
            date_tokens = date_simplified.split('-')
            year = date_tokens[0]
            month = date_tokens[1]

            year_path = os.path.join('_posts', year)
            month_path = os.path.join(year_path, month)
            filepath = os.path.join(month_path, date_simplified + '-' + t['slug'] + '.md')

            if not os.path.exists(year_path):
                os.makedirs(year_path)

            if not os.path.exists(month_path):
                os.makedirs(month_path)

            print ('generating "' + filepath + '"...')

            post_content = post['raw']

            # Fix-up local image links (if they exist)
            post_content = re.sub(r"!\[(.*)\]\((/uploads/.*)\)",r"![\1](http://community.mrtrix.org\2)", post_content)

            with open (filepath, 'w') as f:
                blog_post = u"""---
layout: post
title: '{}'
author: '{}'
date: {}
categories:
discourse_id: {}
---
{}
            """.format(t['title'], author_handle, date, str(discourse_id), post_content)

                f.write (blog_post.encode('utf-8'))

                if fetch_only_first:
                    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
