from django.core.management.base import BaseCommand
from db_researchers.models import Researcher
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX dbc: <http://dbpedia.org/resource/Category:>
    SELECT DISTINCT ?researcher
    WHERE {
    ?researcher dct:subject dbc:Database_researchers.
    }
    """
)

class Command(BaseCommand):
    help = "Inserts RDF data into the database"

    def handle(self, *args, **kwargs):
        try:
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

                Researcher.objects.create(name=name, description=desc)
                print(f"{count}/{length}")
                count+=1
            self.stdout.write(self.style.SUCCESS('Data fetched and inserted successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))
        