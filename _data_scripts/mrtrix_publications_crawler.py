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
                           output_file.write(convert_reference_data_to_yaml(trimmed_ref))
    output_file.close()

def convert_reference_data_to_yaml(reference_data):
    
    yaml_data = ''
    
    print reference_data    
    
    lines = reference_data.split(os.linesep)
    lines = [l for l in lines if not '*' in l and len(l.strip()) != 0]

    print lines
    
    if len(lines) == 3:
        authors = lines[0].replace('// Internal', '').strip().replace("/\n", '')
        title = lines[1].strip().replace('.', '').replace('\n', '')
        journal = lines[2].strip().replace('Neuroimage', 'NeuroImage')
        year = re.search(r'\d{4}', journal).group(0)
        internal = '// Internal' in reference_data        
        yaml_data = '''
-  title: "{}"
   journal: "{}"
   year: {}
   authors: "{}"
   internal: {}
'''.format(title, journal, year, authors, internal)
    return yaml_data

if __name__ == "__main__":
    main(sys.argv[1:])
