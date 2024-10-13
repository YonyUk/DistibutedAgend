"""
main view

here's defined the main view page
"""

import tkinter as Tk
from frontend import auth_page,agend_view,activity_view
from frontend.activity_view import Activity
from frontend.agend_view import Agend,AgendView,AgendViewCreate
from frontend.fonts import *
from frontend.frontend_callbacks import Order,Response

size= '1200x600'

class AgendItem:
    
    def __init__(self,master,agend,root=None,on_save_data_callback=None):
        self._root = root
        self._master = master
        self._agend = agend
        self._on_save_data_callback = on_save_data_callback
        self._frame = Tk.Canvas(master,relief='solid',width=500,borderwidth=2,bg=rgb_to_hex(100,100,100))
        self._owner_label = Tk.Label(self._frame,text=self._agend.owner,font=AUTH_FONT,bg=rgb_to_hex(100,100,100),fg='white')
        self._agend_group = Tk.Label(self._frame,text=self._agend.group,font=AUTH_FONT,bg=rgb_to_hex(100,100,100),fg='white')
        self._activity_counter_label = Tk.Label(self._frame,text=f'Actividades programadas: {len(agend.activitys)}',font=AUTH_FONT,bg=rgb_to_hex(100,100,100),fg='white')
        self._controls_frame = Tk.Canvas(self._frame,bg=rgb_to_hex(100,100,100))
        self._edit_btn = Tk.Button(self._controls_frame,text='Edit',command=lambda : self._edit(),font=AUTH_FONT,bg=rgb_to_hex(100,100,100),fg='white')
        self._delet_btn = Tk.Button(self._controls_frame,text='Delete',command=self.destroy,bg=rgb_to_hex(100,100,100),fg='white',font=AUTH_FONT)
        self._show()
        pass
    
    def _show(self):
        self._frame.pack(side='top',padx=5,pady=5,expand=True,fill='x')
        self._owner_label.pack(side='top',padx=300,pady=10)
        self._agend_group.pack(side='top',padx=300,pady=10)
        self._activity_counter_label.pack(side='top',padx=300,pady=10)
        self._controls_frame.pack(side='bottom',padx=10,pady=20)
        self._edit_btn.pack(side='left',padx=15,pady=10)
        self._delet_btn.pack(side='right',padx=15,pady=10)
        pass
    
    def _edit(self,**kwargs):
        
        def update(**kwargs):
            if self._on_save_data_callback:
                order = Order.EDIT.value
                if 'action' in kwargs.keys():
                    order = kwargs['action']
                    pass
                if order == Order.EDIT_ACTIVITY.value:
                    self._on_save_data_callback(self._agend,order,lambda : print('OK'),old=kwargs['old'],new=kwargs['new'])
                    pass
                else:
                    self._on_save_data_callback(self._agend,Order.EDIT.value,lambda : print('OK'))
                    pass
                self._activity_counter_label.config(text=f'Actividades programadas: {len(self._agend.activitys)}')
                self._agend_group.config(text=self._agend.group)
                pass
            else:
                self._activity_counter_label.config(text=f'Actividades programadas: {len(self._agend.activitys)}')
                self._agend_group.config(text=self._agend.group)
                pass
            return True
                
        self._root.withdraw()
        AgendView(self._agend,update,self._root,update)
        pass
    
    def destroy(self):
        self._frame.destroy()
        pass
    
    pass

class MainView(Tk.Tk):
    
    """
    agends: list(Agend)
    on_save_data_callback: func(Agend,str,callback) -> bool (debe retornar true si el guardado de datos fue exitoso)
    """
    
    def __init__(self,agends=[],on_save_data_callback=None,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._on_save_data_callback = on_save_data_callback
        self._center_win()
        self.title('Agends')
        self._Frame = Tk.Canvas(self,width=500,height=500,bg=rgb_to_hex(100,100,200))
        self._Frame.pack(side='left',padx=5,pady=5,expand=True,fill='both')
        self._ScrollBar = Tk.Scrollbar(self,orient='vertical',command=self._Frame.yview)
        self._ScrollBar.pack(side='right',fill='y')
        self._Frame.configure(yscrollcommand=self._ScrollBar.set)
        self._View = Tk.Frame(self._Frame,bg=rgb_to_hex(100,100,200))
        self._Frame.create_window((600,0),window=self._View,anchor='nw')
        self._agends = agends
        set_agend_list(self._View,agends,self,on_save_data_callback)
        self._View.update_idletasks()
        self._Frame.configure(scrollregion=self._Frame.bbox('all'))
        self._add_agend_btn = Tk.Button(self,text='Add',font=AUTH_FONT,bg=rgb_to_hex(100,100,100),fg='white',command=lambda : self._add_agend())
        self._add_agend_btn.pack(side='bottom',pady=10,padx=10)
        self.config(bg=rgb_to_hex(100,100,200))
        self.mainloop()
        pass

    def _center_win(self):
        win_width,win_height = self.winfo_screenwidth(),self.winfo_screenheight()
        width,height = int(size.split('x')[0]),int(size.split('x')[0])
        x,y = win_width // 2 - width // 2,win_height // 2 - height // 2
        self.geometry(f'{size}+{x}+{y}')
        pass

    def _add_agend(self):
        
        def update(agend):
            if self._on_save_data_callback:
                self._on_save_data_callback(agend,Order.ADD.value,lambda : print('OK'))
                self._agends.append(agend)
                AgendItem(self._View,agend,self,self._on_save_data_callback)
                self._View.update_idletasks()
                self._Frame.configure(scrollregion=self._Frame.bbox('all'))
                pass
            else:
                self._agends.append(agend)
                AgendItem(self._View,agend,self,self._on_save_data_callback)
                self._View.update_idletasks()
                self._Frame.configure(scrollregion=self._Frame.bbox('all'))
                pass
            pass
        
        self.withdraw()
        AgendViewCreate(lambda agend: update(agend),self)
        pass
    
    pass

def set_agend_list(master,agends,root=None,on_save_data_callback=None):
    return [AgendItem(master,agend,root,on_save_data_callback) for agend in agends]