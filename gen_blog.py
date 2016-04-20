#!/usr/bin/env python

import json, requests, shutil, os

site = 'http://community.mrtrix.org'

shutil.rmtree ('_posts', ignore_errors=True)
os.mkdir ('_posts')


r = requests.get (site + '/c/9/l/latest.json')
p = json.loads (r.text)

for x in (p['topic_list']['topics']): 
  if not x['pinned']:
    r = requests.get (site + '/t/' + str(x['id']) + '.json')
    t = json.loads (r.text)
    post = t['post_stream']['posts'][0]
    date = post['created_at'].replace('T', ' ').split('.')[0]
    filename = '_posts/' + date.split()[0] + '-' + t['slug'] + '.md'
    print ('generating "' + filename + '"...')
    with open (filename, 'w') as f:
      f.write ('''---
layout: post
title: ''' + t['title'] + '''
author: ''' + post['username'] + '''
date: ''' + date + '''
categories:
---
''' + post['cooked'])






