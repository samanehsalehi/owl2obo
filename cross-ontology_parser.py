# import liberaries
import re
import argparse
from argparse import *
# get input and output file from cmd line
def argument_parser():
    parser = argparse.ArgumentParser(prog='parser')
    parser.add_argument("-i", "--input", required=True, dest="input_file",
                        help="input of parser")
    parser.add_argument("-o", "--output", required=True, dest="output_file", default='0', type=str,
                           help="output of parser")
    args = parser.parse_args()
    infile = args.input_file
    outfile = args.output_file
    return infile, outfile
# function to open an ontology file
def open_file(input_file):
    with open (input_file) as file_name:
        lines=file_name.readlines()
    return lines
# find terms location in lines
def terms_loc(lines):
    terms_locations = []
    # lines = open_file(input_file)
    for i in range(len(lines)):
        if '[Term]' in lines[i]:
            terms_locations.append(i)
    lastTerm = terms_locations[-1]+2
    print(lastTerm)
    for nextbraket in range(lastTerm, len(lines)-1):
        print(nextbraket)
        if lines[nextbraket].startswith('['):
            # print(nextbraket)
            terms_locations.append(nextbraket)
            break
    for nextbraket in range(lastTerm, len(lines)-1):
        no_next_bracket=[]
        if lines[nextbraket].startswith('['):
            no_next_bracket.append(nextbraket)
            break
    if not no_next_bracket:
        print('********')
        print(no_next_bracket)
        terms_locations.append(len(lines)-1)
    print(terms_locations[-1])
    # print(len(terms_locations))
    return terms_locations
# generate output file
def output(lines,terms_locations, ouput_file):
    length = len(terms_locations)
    with open(ouput_file, 'w') as out:
        for num in range(len(terms_locations)-1):
            current_node = terms_locations[num]
            counter = terms_locations[num]
            next_node = terms_locations[num+1]
            while(counter<next_node):
                counter = counter +1
                if 'xref:' in lines[counter]:
                        x = re.sub(r'^id:\s','',lines[current_node+1].strip()) + '-' + re.sub(r'^name:\s','',lines[current_node+2].replace('\n','|'))
                        out.write(x)
                        out.write(lines[counter].replace(': ','|'))
                if 'is_a:' in lines[counter]:
                    x = re.sub(r'^id:\s','',lines[current_node+1].strip()) + '-' + re.sub(r'^name:\s','',lines[current_node+2].replace('\n','|'))
                    out.write(x)
                    out.write(lines[counter].replace(': ','|'))
    return out

def main():
    # call functions
    input_file, ouput_file = argument_parser()
    lines = open_file(input_file)
    terms1_loc = terms_loc(lines)
    output(lines,terms1_loc,ouput_file)
if __name__=="__main__":
    main()





