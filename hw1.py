# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 16:41:25 2017

@author: kevin
"""
from pymongo import MongoClient
from pprint import pprint
mongodb = MongoClient() 
hw1DB = mongodb.hw1DB

models = hw1DB.models
papers = hw1DB.papers

#insert models
import json

with open('modelcollection.json') as json_data:
    mc = json.load(json_data)
    
models.insert(mc)
#insert papers
with open('papercollection.json') as json_data:
    pc = json.load(json_data)

papers.insert(pc)

#Q: How many models are there?
models.count()#1114

#Q:
for doc in models.find({'_id': 87284}):
    pprint(doc.keys())

len(models.find().distinct('celltypes'))
#118

#Find the list of model ids for models that contain a Hippocampus CA3 pyramidal cell
for doc in models.find({'celltypes': 'Hippocampus CA3 pyramidal cell'}, {'_id':1}):
    pprint(doc)

#What other cells appear in models with a Hippocampus CA3 pyramidal cell? Sort them in alphabetical order. How many such cells are there?    
otherCells = []
for doc in models.find({'celltypes': 'Hippocampus CA3 pyramidal cell'}, {'celltypes':1, '_id':0}):
    doc['celltypes'].remove('Hippocampus CA3 pyramidal cell')
    for celltype in doc['celltypes']:#this is nasty, maybe a more elegant way?
        otherCells.append(celltype)
otherCells = sorted(list(set(otherCells)))
#print otherCells
len(otherCells)
#len(models.find({'celltypes': 'Hippocampus CA3 pyramidal cell'}, {'celltypes':1, '_id':0}).distinct('celltypes'))
#maybe [item for sublist in l for item in sublist]

pipeline = [
    {'$unwind': '$celltypes'},
    {'$group' : 
        {'_id' : '$celltypes', 'num_models' : 
                {'$sum' : 1}
        }
    }, 
    {'$project': 
            {'celltypes':1, 'num_models':1}
    },
    { "$sort": { "num_models": -1 } }]
for doc in (models.aggregate(pipeline)):
    pprint (doc)

pipeline = [{'$lookup': 
                {'from' : 'models',
                 'localField' : '_id',
                 'foreignField' : 'references',
                 'as' : 'cellmodels'}},
            {'$unwind': '$cellmodels'},
             {'$match':
                 {'authors' : 'Migliore M', 'cellmodels.celltypes' : 'Hippocampus CA3 pyramidal cell'}},
            {'$project': 
                {'cellmodels.title':1, '_id' : 0}} 
             ]
             
for doc in (papers.aggregate(pipeline)):
    pprint (doc)


pipeline = [{'$lookup': 
                {'from' : 'models',
                 'localField' : '_id',
                 'foreignField' : 'references',
                 'as' : 'cellmodels'}},
            {'$unwind': '$cellmodels'},
             {'$match':
                 {'cellmodels.celltypes' : 'Hippocampus CA3 pyramidal cell'}},
            {'$project': 
                {'authors':1, '_id' : 0, 'cellmodels.celltypes':1}} 
             ]
             
for doc in (papers.aggregate(pipeline)):
    pprint (doc)

#WTF?
pipeline = [{'$unwind': '$references'},
{'$lookup': 
                {'from' : 'papers',
                 'localField' : 'references',
                 'foreignField' : '_id',
                 'as' : 'cellpapers'}},
            
             ]
             
for doc in (models.aggregate(pipeline)):
    pprint (doc)
temp = []

models.update_many({'celltypes':'Hippocampus CA1 pyramidal cell'},
              {'$set':
                  {'celltypes':'Hippocampus CA1 pyramidal neuron'}})

papers.insert_one(    {
        "missing_references": "all done", 
        "doi": "10.1111/j.1549-8719.2001.tb00156.x", 
        "title": "Simulating the spread of memes through the use of 4chan.", 
        "journal": "4chan.org", 
        "year": "2017", 
        "month": "Feb", 
        "volume": "2", 
        "first_page": "1", 
        "last_page": "999", 
        "references": [
            4461, 
        ], 
        "pubmed_id": "11296851", 
        "authors": [
            "Crane GJ", 
            "Hines ML", 
            "Neild TO"
        ], 
        "_id": 5432112345, 
        "type": "M"
    })

models.insert_one({
                  'name': 'Hippocampus MEME Cell',
                  'channels': ['Rare_PePe', 'Salt_Bae', 'How_Bout_Dat?', 'Cash_Me_Outside'],
                  'transmitters': ['NO', 'Glutamate'],
                  'average dendrite length': 4586,
                  'references' : [5432112345, 3860]
              })

for doc in models.find({'name':'Hippocampus MEME Cell'}):
    print doc

pipeline = [{'$lookup': 
                {'from' : 'models',
                 'localField' : '_id',
                 'foreignField' : 'references',
                 'as' : 'cellmodels'}},
            {'$unwind': '$cellmodels'},
             {'$match':
                 {'_id' : 5432112345}},
            {'$project': 
                {'authors':1, '_id' : 0, 'cellmodels.celltypes':1}} 
             ]
for doc in papers.aggregate(pipeline):
    print doc