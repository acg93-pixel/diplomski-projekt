import json

with open('/home/ceja/Documents/projekt/config.json') as f:
    string = f.read()

dictionary = json.loads(string)

conf = type('test', (object,), {})()

conf.__dict__ = dictionary
