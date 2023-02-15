import json

def jsonify_list(object):
    object = [dict(item) for item in object]
    return json.dumps(object)






