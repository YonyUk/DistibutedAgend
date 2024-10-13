import socket
from utils import get_json_data,set_json_data_to_send
from frontend.frontend_callbacks import Response,Order
from backend.backend_functions import *
from hashlib import sha384

class Server:

    def __init__(self,host,port,listen=1):
        self._host,self._port = host,port
        self._server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self._server.bind((host,port))
        self._server.listen(listen)
        self._buffer_size = 1024
        self._database = start_database('Database')
        pass
    
    def buffer_size(self,value=None):
        if not value:
            return self._buffer_size
        if not type(value) == int:
            raise Exception('Value most be an integer')
        self._buffer_size = value
        return value
    
    def run(self):
        while True:
            conn,_ = self._server.accept()
            json_data = conn.recv(self._buffer_size)
            data = get_json_data(json_data)
            response = self.handle_data(data)
            json_response = set_json_data_to_send(response)
            conn.sendall(json_response)
            conn.close()
            pass
        pass
    
    def handle_data(self,data):
        
        requests = {
            Order.LOGIN.value:self._handle_login_request,
            Order.CREATE_ACCOUNT.value:self._handle_create_account_request,
            Order.ADD.value:self._handle_add_agend_request,
            Order.EDIT.value:self._handle_edit_agend_request,
            Order.GET_AGENDS.value:self._handle_get_agends_request,
            Order.EDIT_ACTIVITY.value:self._handle_edit_activity_request
        }
                
        if not 'order' in data.keys() or not data['order'] in requests.keys():
            return { 'status':Response.BAD_REQUEST.value }
        
        return requests[data['order']](**data)
        
    def _get_activity_id(self,activity):
        description = activity['description']
        date = activity['date']
        key = f'{date}<--->{description}'
        hasher = sha384()
        hasher.update(bytes(key,'utf-8'))
        return hasher.hexdigest()
    
    def _handle_login_request(self,**request):
        if not 'username' in request.keys() or not 'password' in request.keys():
            return {'status':Response.BAD_REQUEST}
        self._database.connect()
        self._database.open()
        data = self._database.selectFieldsFrom(
            'Users',
            'username',
            'password',
            username=request['username'],
            password=request['password']
        )
        self._database.close()
        self._database.disconnect()
        return {'status':Response.OK.value} if len(data) > 0 else {'status':Response.WRONG.value}

    def _handle_create_account_request(self,**request):
        if not 'username' in request.keys() or not 'password' in request.keys():
            return {'status':Response.BAD_REQUEST.value}
        self._database.connect()
        self._database.open()
        self._database.insertInto('Users',(request['username'],request['password']))
        self._database.close()
        self._database.disconnect()
        return {'status':Response.OK.value}
    
    def _handle_add_agend_request(self,**request):
        if 'agend' in request.keys():
            agend = request['agend']
            activitys = agend['activitys']
            self._database.connect()
            self._database.open()
            self._database.insertInto('Agends',(agend['owner'],agend['group']))
            for act in activitys:
                Id = self._get_activity_id(act)
                count = self._database.count('Activitys','Id',Id=Id)
                if count == 0:
                    self._database.insertInto('Activitys',(Id,act['description'],act['date']))
                    pass
                self._database.insertInto('AgendActivitys',(agend['owner'],Id))
                pass
            self._database.close()
            self._database.disconnect()
            return {'status':Response.OK.value}
        return {'status':Response.WRONG.value}
            
    def _handle_edit_agend_request(self,**request):
        if 'agend' in request.keys():
            agend = request['agend']
            activitys = agend['activitys']
            self._database.connect()
            self._database.open()
            count = self._database.count('Agends','owner',owner=agend['owner'])
            if count == 0:
                return {'status':Response.WRONG.value}
            agend_ = self._database.selectFrom('Agends',owner=agend['owner'])[0]
            if not agend['group'] == agend_['groupName']:
                self._database.updateTable('Agends',('groupName',agend['group']),owner=agend['owner'])
                pass
            for act in activitys:
                Id = self._get_activity_id(act)
                count = self._database.count('Activitys','Id',Id=Id)
                if count == 0:
                    self._database.insertInto('Activitys',(Id,act['description'],act['date']))
                    pass
                else:
                    self._database.updateTable('Activitys',('description',act['description']),('date',act['date']),Id=Id)
                    pass
                count = self._database.selectFieldsFrom('AgendActivitys','owner','Id',owner=agend['owner'],Id=Id)
                if len(count) == 0:
                    self._database.insertInto('AgendActivitys',(agend['owner'],Id))
                    pass
                pass
            self._database.close()
            self._database.disconnect()
            return {'status':Response.OK.value}
        return {'status':Response.WRONG.value}
    
    def _handle_get_agends_request(self,**request):
        self._database.connect()
        self._database.open()
        agends = self._database.selectFrom('Agends')
        agends_ = []
        for ag in agends:
            activitys = self._database.selectFieldsFrom('AgendActivitys','Id',owner=ag['owner'])
            activitys = [self._database.selectFrom('Activitys',Id=act['Id'])[0] for act in activitys]
            agends_.append({
                'owner':ag['owner'],
                'groupName':ag['groupName'],
                'activitys':activitys
            })
            pass
        self._database.close()
        self._database.disconnect()
        return {'status':Response.OK.value,'agends':agends_}
    
    def _handle_edit_activity_request(self,**request):
        self._database.connect()
        self._database.open()
        old = request['old']
        new = request['new']
        Id = self._get_activity_id(old)
        self._database.updateTable('Activitys',('description',new['description']),('date',new['date']),Id=Id)
        self._database.close()
        self._database.disconnect()
        return {'status':Response.OK.value}
    
    pass
