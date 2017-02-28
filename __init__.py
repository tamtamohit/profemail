from pymongo import MongoClient
import requests
from lxml import html
from elasticsearch import Elasticsearch

es = Elasticsearch()

# mongo_collection = MongoClient()['personal'].intership_research

def DOM(url):
    response = requests.get(url)
    return html.document_fromstring(response.text)

