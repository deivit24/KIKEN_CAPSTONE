from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify


models = [
            {
            'id':1,
            'company':'Acorns',
            'name': 'Conservative',
            'JPST': 20,
            'ICSH': 20,
            'SHV': 20,
            'BIL': 20,
            'GBIL':20,
            },
        
          {   
              'id':2,
            'company':'Acorns',
            'name': 'Moderately Conservative',
            'VOO': 24,
           'VNQ': 4,
           'LQD': 30,
           'VB': 4,
           'SHY': 30,
           'VEA': 8,
        },

        {   'id':3,
            'company':'Acorns',
            'name': 'Moderate',
            'VOO': 29,
            'VWO': 6,
           'VNQ': 6,
           'LQD': 20,
           'VB': 10,
           'SHY': 20,
           'VEA': 12,
        },
  

            {
            'id':4,   
            'company':'Acorns',
            'name': 'Moderately Aggressive',
            'VOO': 38,
            'VWO': 4,
           'VNQ': 8,
           'LQD': 10,
           'VB': 14,
           'SHY': 10,
           'VEA': 16,
        },

        {   'id':5,
            'company':'Acorns',
            'name': 'Aggressive',
            'VOO': 40,
            'VWO': 10,
           'VNQ': 10,   
           'VB': 20,
           'VEA': 20,
        },
        

        {   'id':6,
            'company':'BlackRock',
            'name': '0/100  (Equity / Fixed Income %)',
            'LQD': 24,
            'IGSB': 12,
            'GOVT': 24,   
            'NEAR': 21,
            'SHYG': 9,
            'TLT':1,
            'EMB':5,
            'HYG':4,
        },

        {   'id':7,
            'company':'BlackRock',
            'name': '10/90  (Equity / Fixed Income %)',
            'IVV':5,
            'ESGU':2,
            'EFG':2,
            'USMV':2,
            'LQD': 24,
            'IGSB': 12,
            'GOVT': 18,   
            'NEAR': 19,
            'SHYG': 9,
            'TLT':1,
            'EMB':4,
            'HYG':2,
        },

        {   'id':8,
            'company':'BlackRock',
            'name': '20/80  (Equity / Fixed Income %)',
            'IVV':9,
            'ESGU':3,
            'EFG':2,
            'ESGE':3,
            'VLUE':2,
            'USMV':2,
            'LQD': 21,
            'IGSB': 12,
            'GOVT': 19,   
            'NEAR': 14,
            'SHYG': 9,
            'TLT':1,
            'EMB':3,
            
        },

        {   'id':9,
            'company':'BlackRock',
            'name': '30/70  (Equity / Fixed Income %)',
            'IVV':14,
            'ESGU':4,
            'EFG':3,
            'ESGE':4,
            'VLUE':2,
            'IXN':2,
            'USMV':2,
            'LQD': 17,
            'IGSB': 11,
            'GOVT': 18,   
            'NEAR': 12,
            'SHYG': 7,
            'TLT':1,
            'EMB':3,
            
        },
 ]






# shows a single todo item and lets you delete a todo item
class SingleModel(Resource):
    def get(self, id):
        model = [model for model in models if model['id'] == id]
        if len(model) == 0:
            abort(404)
        return jsonify({"models": model}) 

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class Models(Resource):
    def get(self):
        return jsonify({'models':models})

