#python filename.py -i <inout.owl> -o <output.obo>
#python owl-obo.py -i dron.owl -o output1.obo
# Import libraries
import json
import xml.etree.ElementTree as ET
# import argparse
from argparse import RawTextHelpFormatter
# read variable from config file
with open('config.json', 'r') as c:
    config = json.load(c)
    ID_PREFIX_LIST=list(config['Params'].values())
    print(ID_PREFIX_LIST)
    ONT_PREFIX_LIST=list(config['Ontologies'].values())
    print(ONT_PREFIX_LIST)    

# Arg parser function to get input and output paths
def argument_parser():

    parser = argparse.ArgumentParser(
        description=__doc__,
        # prog='owl_obo.py',
        formatter_class=RawTextHelpFormatter
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_file_path",
        required=True,
        help="a path to the input file."
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file_path",
        required=True,
        help="a path to the out file."
    )
    args = parser.parse_args()
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path
    return input_file_path,output_file_path

#read owl filesn and return the dictionary of IDs and Labels
def read_owl_file(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()
    items=[]
    item={}
    existid=0
#itterte in the owl file
    for child in root:
        if child.tag=='{http://www.w3.org/2002/07/owl#}Class':
            item= {}
            existid=0
            for second_child in child:
                Flag=0
                for prefix_ in ID_PREFIX_LIST:
                    for ontology in ONT_PREFIX_LIST:
                        print(f'{{{ontology}}}'+ prefix_)
                        if second_child.tag == f'{{{ontology}}}'+ prefix_:
                            item['id:'+str(prefix_.split("_")[0])]= second_child.text
                            print(item['id:'+str(prefix_.split("_")[0])])
                            existid=1
                        elif second_child.tag == '{http://www.w3.org/2000/01/rdf-schema#}label' and existid:
                            item['name']= second_child.text
                            Flag=1
                            existid=0
                if Flag:
                    items.append(item)
    return items

#generate the output file from the list of dictionaries produced by read_owl_file function
def obo_output(list_,outputfile):
    file_=open(outputfile,'w')
    for item_ in list_:
        file_.write('Term:[term]\n')
        for key, value in item_.items():
            file_.write('{}:{}\n'.format(key,value))
        file_.write("\n")

# calling all required functions
def main():
    input_file_path,output_file_path = argument_parser()
    final_list=read_owl_file(input_file_path)
    obo_output(final_list,output_file_path)

if __name__=="__main__":
    main()
