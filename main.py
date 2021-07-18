import socketio
import ast
from gevent import pywsgi

sio = socketio.Server(async_mode='gevent')
application = app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

world = {'image': 'f' * (6 * 256 * 256)}

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('snapshot', world['image'], room=sid)

@sio.event
def paint(sid, data):
    sio.emit("paint", data)

    dict = ast.literal_eval(str(data))
    touches = dict['t']

    for touch in touches:
        c = touch['c']
        i = (touch['y'] * 256 + touch['x']) * 6

        world['image'] = world['image'][:i] + c + world['image'][i + 6:]


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    pywsgi.WSGIServer(('', 44127), app).serve_forever()
