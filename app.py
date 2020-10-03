#Autor Francisco Pulice Rojas 8-929-988
#Conexion a la BD utilizando framework web Tornado
import tornado.ioloop
import tornado.web
import sqlite3
import asyncio
from datetime import datetime


now = datetime.now()
dt = now.strftime("%Y-%m-%d %H:%M:%S")
#conexion a la BD a traves del archivo testdb.sqlite
def _execute(query):
        dbPath = './testdb.sqlite'
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()
        try:
                print("Conexion a Base de Datos Establecida")
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                connection.commit()

        except Exception:
                raise
        connection.close()
        return result

class Main(tornado.web.RequestHandler):
    def get(self):
        self.write("Main")


class AddDistrict(tornado.web.RequestHandler):
    def get(self):
        self.render('templates/index.html')
    #funcion post para ingresar a la base de datos a traves de el query
    def post(self):
        distrito = self.get_argument('distrito')
        query = ''' insert into districts (province_id, name,created_at,updated_at) values (%d, '%s', '%s', '%s') ''' %(5,distrito,str(dt),str(dt));
        _execute(query)
        print("Ingresado con exito")

 #arreglo de rutas web               
app = tornado.web.Application([
    (r"/",Main),
    (r'/css/(.*)', tornado.web.StaticFileHandler, {'path':'./static/css'}),
    (r"/create",AddDistrict),
], debug=True)

if __name__ == "__main__":
     #Linea para ejecutar tornado en windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.listen(8080)
    print("port: 8080 on")
    tornado.ioloop.IOLoop.instance().start()