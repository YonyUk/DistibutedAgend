import socket
import json
from utils import set_json_data_to_send,get_json_data
from enum import Enum

class Order(Enum):
    LOGIN = 0
    CREATE_ACCOUNT = 1
    EDIT = 2
    ADD = 3
    GET_AGENDS = 4
    GET_ACTIVITYS = 5
    EDIT_ACTIVITY = 6
    DELETE_ACTIVITY = 7
    pass

class Response(Enum):
    OK = 0
    WRONG = 1
    BAD_REQUEST = 2
    pass

def login_callback(username,password,**kwargs):
    client = None
    if 'url' in kwargs.keys():
        host,port = kwargs['url']
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        data = {
            'order':Order.LOGIN.value,
            'username':username,
            'password':password
        }
        json_data = set_json_data_to_send(data)
        client.sendall(json_data)
        json_response = client.recv(1024)
        response = get_json_data(json_response)
        if response['status'] == Response.OK.value:
            return True
        return False
    return True

def edit_activity_callback(**kwargs):
    client = None
    if 'url' in kwargs.keys() and 'order' in kwargs.keys():
        host,port = kwargs['url']
        order = kwargs['order']
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        old = {
            'description':kwargs['old'].description,
            'date':kwargs['old'].date
        }
        new = {
            'description':kwargs['new'].description,
            'date':kwargs['new'].date
        }
        data = {
            'order':order,
            'new':new,
            'old':old
        }
        json_data = set_json_data_to_send(data)
        client.sendall(json_data)
        json_response = client.recv(1024)
        response = get_json_data(json_response)
        if response['status'] == Response.OK.value:
            return True
        return False
    return True

def create_account_callback(username,password,**kwargs):
    client = None
    if 'url' in kwargs.keys():
        host,port = kwargs['url']
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        data = {
            'order':Order.CREATE_ACCOUNT.value,
            'username':username,
            'password':password
        }
        json_data = set_json_data_to_send(data)
        client.sendall(json_data)
        json_response = client.recv(1024)
        response = get_json_data(json_response)
        if response['status'] == Response.OK.value:
            return True
        return False
    return True

def save_data_callback(**kwargs):
    client = None
    if 'url' in kwargs.keys() and 'order' in kwargs.keys():
        host,port = kwargs['url']
        order = kwargs['order']
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((host,port))
        agend = kwargs['agend']
        activitys = agend.activitys
        activitys_ = [{'date':act.date,'description':act.description} for act in activitys]
        agend_ = {
            'owner':agend.owner,
            'group':agend.group,
            'activitys':activitys_
        }
        data = {
            'order':order,
            'agend':agend_
        }
        json_data = set_json_data_to_send(data)
        client.sendall(json_data)
        json_response = client.recv(1024)
        response = get_json_data(json_response)
        if response['status'] == Response.OK.value:
            return True
        return False
    return True