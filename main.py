import eventlet
import socketio
import ast

sio = socketio.Server()
application = app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

world = {'image': ['ffffff'] * (256 * 256)}

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    sio.emit('snapshot', ''.join(world['image']), room=sid)

@sio.event
def paint(sid, data):
    sio.emit("paint", data)

    dict = ast.literal_eval(str(data))
    touches = dict['t']

    for touch in touches:
        c = touch['c']
        i = touch['y'] * 256 + touch['x']

        world['image'][i] = c


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 44127)), app)
