from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import cgi
import sqlite3
import os
import json

SQL_DROP_MSG = "DROP TABLE messages;"
SQL_CREATE_MSG =    "CREATE TABLE IF NOT EXISTS messages( " + \
                        "receiver TEXT " +              "NOT NULL, " + \
                        "sender TEXT " +                "NOT NULL, " + \
                        "value TEXT " +                 "NOT NULL " + \
                    ");"
PORT_NUM = 8000


def connect(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

    return connection


def drop(conn):
    cur = conn.cursor()
    cur.execute(SQL_DROP_MSG)


def create(conn):
    cur = conn.cursor()
    cur.execute(SQL_CREATE_MSG)


conn = connect( os.path.join( os.getcwd(), "storage.db" ) )
drop(conn)
create(conn)


class GP(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()


    def do_HEAD(self):
        self._set_headers()


    def do_GET(self):
        self._set_headers()
        params = parse_qs(self.path[2:])

        # Get messages
        print( "RETRIEVING" )
        name = params['user'][0]
        rows = self.select(name)
        print(name,rows)
        messages = []
        for row in rows:
            messages.append( {'sender': row[1], 'value': row[2]} )
        jsonObj = {'response': {'user': name, 'messages': messages} }
        print( json.dumps(jsonObj, indent=3) )
        print( json.loads( json.dumps(jsonObj, indent=3) ) )
        self.wfile.write( json.dumps(jsonObj, indent=3).encode() )


    def do_POST(self):
        self._set_headers()
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Parse the POST request
        receiver = form.getvalue("receiver")
        sender = form.getvalue("sender")
        message = form.getvalue("message")

        # Insert into DB
        print( "INSERTING" )
        self.insert( receiver, sender, message )


    def insert(self, receiver, sender, message):
        cur = conn.cursor()
        cur.execute("INSERT INTO messages(receiver,sender,value) VALUES(?,?,?)", (receiver,sender,message) )
        conn.commit()


    def select(self, name):
        cur = conn.cursor()
        cur.execute("SELECT * FROM messages WHERE receiver=?", (name,) )
        rows = cur.fetchall()
        return rows


def run(server_class=HTTPServer, handler_class=GP, port=PORT_NUM):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print( 'Server running at localhost:' + str(PORT_NUM) + '...' )
    httpd.serve_forever()

run()