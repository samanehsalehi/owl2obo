import rdflib
from rdflib import Graph, Namespace

# Define the namespaces used in your RDF data
rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
oboInOwl = Namespace("http://www.geneontology.org/formats/oboInOwl#")
owl = Namespace("http://www.w3.org/2002/07/owl#")

# Load the RDF/XML file
g = Graph()
g.parse("go.owl") 

query = """
 SELECT ?id ?label ?synonym ?dbXref ?isa  ?someValuesFrom
 WHERE {
   ?class rdf:type owl:Class .
   ?class oboInOwl:id ?id ;
          rdfs:label ?label .
   OPTIONAL {
     ?class oboInOwl:hasExactSynonym ?synonym .}
   OPTIONAL {
     ?class oboInOwl:hasDbXref ?dbXref .}
   OPTIONAL {
     ?class rdfs:subClassOf ?isa .}
   OPTIONAL {
    ?class rdfs:subClassOf[
      rdf:type owl:Restriction ;
      owl:onProperty ?property ;
      owl:someValuesFrom ?someValuesFrom ].
    }
    }"""
print('**************')
# Execute the SPARQL query
results = g.query(query)
obo_str = ""
last_id = ""
last_syn = ""
last_xref = ""
last_isa = ""
resource_id = 'first try'
# Process the query results
finalstr = ''
last_term = 0
# for line_number, row in enumerate(results):
#   print(row)
for line_number, row in enumerate(results):
  print("get to results")
  resource_id = row.id.toPython()
  if resource_id != last_id:
    label = row.label.toPython()
    obo_str += f"[Term]\nid: {resource_id}\nlabel: {label}\n"
    last_term = line_number
    if row.dbXref is not None:
      xref = row.dbXref.toPython()
      obo_str = obo_str + f"xref: {xref}\n"
      last_xref = xref
    if row.synonym is not None:
      syn = row.synonym.toPython()
      obo_str = obo_str + f"synonym: {syn}\n"
      last_syn = syn
    if row.isa is not None:
      is_a = row.isa.toPython()
      if is_a.startswith("http://purl.obolibrary.org/obo/"):
        _, go_part = is_a.rsplit("/", 1)
        obo_str = obo_str + f"is_a: {go_part}\n"
        last_isa = go_part
  if last_id == resource_id:
    if row.dbXref is not None:
      xref = row.dbXref.toPython()
      if last_xref != xref:
        obo_str = obo_str + f"xref: {xref}\n"
        last_xref = xref
    if row.synonym is not None:
      if last_syn != row.synonym.toPython():
        syn = row.synonym.toPython()
        obo_str = obo_str + f"synonym:{syn}\n"
        last_syn = syn
    # if row.isa is not None:
    #   is_a = row.isa.toPython()
    #   if is_a.startswith("http://purl.obolibrary.org/obo/"):
    #     _, go_part = is_a.rsplit("/", 1)
    #     if last_isa != go_part:
    #       lines = obo_str.splitlines()
    #       print(len(lines))
    #       for line_n in range(last_term,len(lines)-1):
    #         is_a_found = False
    #         line = lines[line_n]
    #         print(line)
    #         if go_part in line:
    #           is_a_found= True 
    #           print('foun:', go_part)
    #           print(last_term)
    #           break
    #         else:
    #           print('notequal')
    #       if is_a_found == False:
    #         obo_str = obo_str + f"is_a: {go_part}\n"
    #     else:
    #       pass
  last_id = resource_id 
  print(resource_id)
with open('resultowltoobordflib.obo','w') as f:
  f.write(obo_str)