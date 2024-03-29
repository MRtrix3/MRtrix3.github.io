#!/usr/bin/env python
#
# Pull the latest MRtrix community announcements and blog posts
# and package them as blog posts to be pushed onto the website.
#
# Also updates the list of contributors from Github
#
# Authors: J-D Tournier and Rami Tabbara
#

import sys, getopt, json, requests, os, yaml, re, calendar

def usage():
    print ('''
usage: ./gen_blog.py [-a, --all]

OPTIONS:

  --all           specifies whether blog posts for all latest forum announcements and blog posts should be generated. By default we only fetch the latest forum post.
''')


def main(argv):

    # update contributors:
    site = 'https://api.github.com/'
    r = requests.get (site + 'repos/MRtrix3/mrtrix3/contributors')
    p = json.loads (r.text)
    try:
      with open('_data/frontpage/additional_contributors.txt') as extra_fd:
        for line in extra_fd:
          line = line.strip()
          if line:
            r = requests.get (site + 'users/' + line)
            p.append (json.loads (r.text))
    except:
      pass

    with open ('_data/frontpage/contributors.json', 'w') as fd:
      fd.write (json.dumps(p, indent=2, sort_keys=True))






    site = 'https://community.mrtrix.org'


    # update topic lists in wiki section:
    # wiki is category 12:
    r = requests.get (site + '/c/12/l/latest.json')
    p = json.loads (r.text)
    tags = set ([ tag for entry in p["topic_list"]["topics"] for tag in entry["tags"] ])
    with open ('_data/wiki_tags.csv', 'w') as f:
      f.write ('name\n')
      for tag in sorted(tags):
        f.write (tag + '\n')





    # update blog posts
    fetch_only_first = True

    try:
        opts, args = getopt.getopt(argv, "a", ["all"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--all"):
            fetch_only_first = False


    # 9 = Announcements
    # 11 = Blog
    for category in ['9', '11']:

        r = requests.get (site + '/c/{}/l/latest.json'.format(category))
        p = json.loads (r.text)

        with open (os.path.join('_data', 'authors.yml'), 'r') as f:
          author_list = yaml.load(f, Loader=yaml.SafeLoader)

        for x in (p['topic_list']['topics']):

            r = requests.get (site + '/t/' + str(x['id']) + '.json?include_raw=1')
            t = json.loads (r.text)
            post = t['post_stream']['posts'][0]
            discourse_id = x['id']
            author_handle = post['username']
            author_name = author_handle

            for author in author_list:
                # Match Discourse handle to GitHub handle (if it exists)
                if 'discourse' in author and author['discourse'] == author_handle:
                    author_name = author['name']
                    # Try to use GitHub handle if it exists
                    if 'github' in author:
                        author_handle = author['github']


            date = post['created_at'].replace('T', ' ').split('.')[0]
            date_simplified = date.split()[0]
            date_tokens = date_simplified.split('-')
            year = date_tokens[0]
            month = date_tokens[1]
            date_summary = calendar.month_abbr[int(month)] + ' ' + date_tokens[2] + ', ' + year

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
            post_content = re.sub(r"!\[([^|\]]+)[^\]]*\]\((/uploads/[^\)]*)\)",r"![\1](https://community.mrtrix.org\2)", post_content)

            post_content += '''

---

*[View comments on the community site](https://community.mrtrix.org/t/''' + str(discourse_id) + ')*\n'

            with open (filepath, 'wb') as f:
                blog_post = u"""---
layout: post
title: '{}'
author: '{}'
date: {}
categories:
summary: {}
---
{}
            """.format(t['title'], author_handle, date, 'posted by ' + author_name + ' on ' + date_summary, post_content)

                f.write (blog_post.encode('utf-8'))

                if fetch_only_first:
                    break









if __name__ == "__main__":
    main(sys.argv[1:])
