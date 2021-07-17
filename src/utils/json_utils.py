def get_json_prop(json, *args):
    for x in args:
        if x in json:
            return json[x]
    return None