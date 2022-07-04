import json

with open("objects.json", 'r') as f:
    print (json.loads(f.read()))
