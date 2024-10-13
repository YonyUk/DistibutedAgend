# Iniciar frontend

```python
from frontend import *

app = Application((url)
# sustituye 'url' por la direccion a la que te vayas a conectar
# Ej: url = 'localhost',8000
app.config(on_login_callback=login_callback)
app.config(on_create_account_callback=create_account_callback)
app.config(on_save_data_callback=save_data_callback)
app.config(on_update_data_callback=edit_activity_callback)
app.run()
```

# Iniciar backend

```python
from backend import *

server = Server('localhost',8000)
server.run()
```
