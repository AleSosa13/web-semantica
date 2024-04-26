from django.shortcuts import render
from .models import Researcher
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

def db_researcher_view(request):
    researchers = Researcher.objects.order_by('name')
    return render(request, 'researcher_list.html', {'researchers': researchers, "field": "Database Researchers"})

def researcher_types(request):
    types = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?field
        WHERE {
        ?field skos:broader dbc:Computer_scientists_by_field_of_research.
        }
        """
    )

    ret = sparql.queryAndConvert()
    length = len(ret["results"]["bindings"])
    count = 1

    for r in ret["results"]["bindings"]:
        if "researchers" in r["field"]["value"]:
            g = Graph().parse(r["field"]["value"])
            for subj, pred, obj in g:
                if "rdf-schema#label" in pred:
                    if "researchers" in obj: types.append(obj.value.replace(" ", "_"))
            print(f"{count}/{length}")
        count+=1
    return render(request, 'researcher_types.html', {'types': types})

def researcher_type(request, type):
    researchers = []
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setReturnFormat(JSON)

    sparql.setQuery("""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX dbc: <http://dbpedia.org/resource/Category:>
        SELECT DISTINCT ?researcher
        WHERE {
        ?researcher dct:subject dbc:"""+type+""".
        }
        LIMIT 10
        """
    )
    ret = sparql.queryAndConvert()
    length = len(ret["results"]["bindings"])
    count = 1

    for r in ret["results"]["bindings"]:
        g = Graph().parse(r["researcher"]["value"])
        name = ""
        desc = ""
        
        # Iterate over triples and save English labels
        for subj, pred, obj in g:
            if "rdf-schema#label" in pred:
                if obj.language == 'en': name = obj
            elif "ontology/abstract" in pred:
                if obj.language == 'en': desc = obj
        researchers.append(Researcher(name=name, description=desc))
        print(f"{count}/{length}")
        count+=1
    return render(request, 'researcher_list.html', {'researchers': researchers, "field": type.replace("_", " ").title()})
