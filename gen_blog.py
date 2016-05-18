#!/usr/bin/env python
#
# Pull the latest MRtrix community announcements and
# package them as blog posts to be pushed onto the website.
#
# Authors: J-D Tournier and Rami Tabbara
# 

import sys, getopt, json, requests, os

def usage():
    print ('''
usage: ./gen_blog.py [-a, --all]

OPTIONS:

  --all           specifies whether blog posts for all latest forum announcements should be generated. By default we only fetch the latest forum post.
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

    r = requests.get (site + '/c/9/l/latest.json')
    p = json.loads (r.text)

    for x in (p['topic_list']['topics']): 
        if x['pinned']:
            continue

        r = requests.get (site + '/t/' + str(x['id']) + '.json')
        t = json.loads (r.text)
        post = t['post_stream']['posts'][0]
        discourse_id = x['id']
        
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

        # Blog post already exists so skip generation
        if os.path.exists(filepath):
            continue

        print ('generating "' + filepath + '"...')
        with open (filepath, 'w') as f:
            f.write ("""---
layout: post
title: {}
author: {}
date: {}
categories:
discourse_id: {}
---
{}
            """.format(t['title'], post['username'], date, str(discourse_id), post['cooked']))

            if fetch_only_first:
                return

if __name__ == "__main__":
    main(sys.argv[1:])
