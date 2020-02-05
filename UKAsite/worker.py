from rq import Connection, Worker
from dataplot.server import app, queue,conn

if __name__ == "__main__":
    with app.server.app_context():
        with Connection(conn):
            w = Worker([queue])
            w.work()
