"""
visual

contains constants for the visual of the frontend
"""

from frontend.agend_view import AgendView,Agend,AgendViewCreate
from frontend.activity_view import Activity,ActivityView
from frontend.main_view import MainView
from frontend.auth_page import AuthView,LoginView
from frontend.frontend_callbacks import *
from frontend.fonts import *
import tkinter as Tk
from tkinter import messagebox
import socket
from utils import set_json_data_to_send,get_json_data

class Application:
    
    def __init__(self,url,**kwargs):
        self._callbacks = kwargs
        self._url = url
        pass
    
    def config(self,**kwargs):
        if 'url' in kwargs.keys():
            self._url = kwargs['url']
            pass
        for key in kwargs.keys():
            if key == 'url': continue
            self._callbacks[key] = kwargs[key]
            pass
        pass
    
    def _build_client(self):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect(self._url)
        return client
    
    def _get_agends(self):
        try:
            client = self._build_client()
            data = {
                'order':Order.GET_AGENDS.value
            }
            json_data = set_json_data_to_send(data)
            client.sendall(json_data)
            json_response = client.recv(2**15)
            response = get_json_data(json_response)
            if response['status'] == Response.OK.value:
                agends = []
                for ag in response['agends']:
                    activitys = [Activity(act['description'],act['date']) for act in ag['activitys']]
                    a = Agend(ag['owner'],*activitys)
                    a.set_group(ag['groupName'])
                    agends.append(a)
                    pass
                return agends
            return []
        except Exception as ex:
            return []
        pass
    
    def run(self,agends=[]):
        def on_save_data_callback(agend,order,callback,**kwargs):
            if order == Order.EDIT_ACTIVITY.value:
                if self._callbacks['on_update_data_callback'](order=order,url=self._url,old=kwargs['old'],new=kwargs['new']):
                    callback()
                    pass
                else:
                    messagebox.showwarning('Connection Error',message='Error en el guardado de datos')
                    pass
                pass
            elif self._callbacks['on_save_data_callback'](agend=agend,order=order,url=self._url):
                callback()
                pass
            else:
                messagebox.showwarning('Connection Error',message='Error en el guardado de datos')
                pass
            pass
        
        def on_login_callback(username,password,callback):
            if self._callbacks['on_login_callback'](username,password,url=self._url):
                callback()
                if 'on_save_data_callback' in self._callbacks.keys():
                    MainView(agends,on_save_data_callback)
                    pass
                else:
                    MainView(agends)
                    pass
                pass
            else:
                messagebox.showwarning('Connection Error',message='Fallo al autenticarse')
                pass
            pass
        
        def on_create_account_callback(username,password,callback):
            if not self._callbacks['on_create_account_callback'](username,password,url=self._url):
                messagebox.showwarning('Connection Error',message='Fallo al crear la cuenta')
                pass
            callback()
            pass    
        
        agends += self._get_agends()

        if 'on_login_callback' in self._callbacks.keys():
            if 'on_create_account_callback' in self._callbacks.keys():
                AuthView(on_login_callback,on_create_account_callback)
                pass
            else:
                AuthView(on_login_callback,lambda username,password,callback: callback())
                pass
            pass
        else:
            AuthView(null_login,lambda username,password,callback: callback())
            pass
        pass
    
    pass

def null_login(username,password,callback):
    callback()
    MainView()
    pass