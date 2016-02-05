#!/usr/bin/python

#
# Crawls through MRtrix commands source looking for inline references details
# Then, stores fetched YAML formatted document for use 
#

import sys, getopt, os, re, mmap
import subprocess
from random import randint
from time import sleep

 
def usage():
    print ('''
usage: ./mrtrix_publications_crawler.py [-c, --commands_dir] dir [-o --output_path]

OPTIONS:

  --commands_dir        directory where mrtrix source commands reside
  --output_path         output path of yaml publication list
''')


def main(argv):

    commands_dir = None
    output_path = None

    try:
        opts, args = getopt.getopt(argv, "c:o:", ["commands_dir=", "output_path="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--commands_dir"):
            commands_dir = arg
        elif opt in ("-o", "--output_path"):
            output_path = arg

    if commands_dir is None or output_path is None:
        usage()
        exit(2)

    crawl_commands(commands_dir, output_path)



def crawl_commands(commands_dir, output_path):
    
    output_file = open(output_path,'w')
    
    processed_titles = []    

    for command_file in os.listdir(commands_dir):
        command_path = os.path.join (commands_dir, command_file)
        if os.path.isfile(command_path):
            with open(command_path, 'r+') as f:
                # Map file to memory
                # Need this to perform regular expression matching on entire file 
                data = mmap.mmap(f.fileno(), 0)

                reg_exp = re.search(r'REFERENCES(?s)(.*)(ARGUMENTS)', data)
                if reg_exp is not None:
                    reference_comments = reg_exp.group(1).split(r'+')
                    for reference in reference_comments:
                        trimmed_ref = reference.replace('"', '')
                        if trimmed_ref.strip() != "":
                           output_file.write(convert_reference_data_to_yaml(trimmed_ref, processed_titles))
    output_file.close()

def convert_reference_data_to_yaml(reference_data, processed_titles):
    
    yaml_data = ''
    
    print reference_data    
    
    lines = reference_data.split(os.linesep)
    lines = [l for l in lines if not '*' in l and len(l.strip()) != 0]

    print lines
    
    line_len = len(lines)    

    if line_len >= 3:
        authors = lines[0].replace('// Internal', '').strip().replace("/\n", '')
        title = ''
        for line in lines[1:line_len-1]:
            title = title + re.sub('^\s+', '', line)
        title = title.strip().replace('.', '').replace('\n', '').replace('\t', '')
        
        if title in processed_titles:
            return ''
        else:            
            processed_titles.append(title)         

        journal = lines[line_len-1].strip().replace('Neuroimage', 'NeuroImage')
        year = re.search(r'\d{4}', journal).group(0)
        internal = '// Internal' in reference_data        
        yaml_data = '''
-  title: "{}"
   journal: "{}"
   year: {}
   authors: "{}"
   internal: {}
   url: "{}"
'''.format(title, journal, year, authors, internal, find_publication_link(title, authors))
    return yaml_data

def find_publication_link(title, authors):
    url = ''
    scholar_cmd = './scholar.py -c 1 --phrase "' + title + ' ' + authors + '"'
    
    try:
        process = subprocess.Popen(scholar_cmd, shell=True, stdout=subprocess.PIPE)
        pub_data = process.stdout.read().decode ('utf-8', 'ignore')
        url = re.search(r'URL\s*([^\n]*)\n', pub_data).group(1)
    except Exception:
        print 'Unable to find publication link for: {}'.format(title)

    return url


if __name__ == "__main__":
    main(sys.argv[1:])
