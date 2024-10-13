import json

def insert_ordered(item,array):
    if len(array) == 1:
        if array[0].ID > item.ID:
            return [item] + array
        return array + [item]
    pos = len(array) // 2
    if array[pos].ID > item.ID:
        return insert_ordered(item,array[:pos]) + array[pos:]
    return array[:pos] + insert_ordered(item,array[pos:])

def get_json_data(data):
    if type(data) == bytes: return json.loads(data.decode())
    return json.loads(data)

def set_json_data_to_send(data,encoding='utf-8'):
    return bytes(json.dumps(data),encoding)