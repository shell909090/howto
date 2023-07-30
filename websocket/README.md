# websocket example and test

The purpose of this project is to demonstrate the usage of websocket, and test how it works.

# requirement

* ws
* socket.io
* socket.io-client

# run

1. To run ws server: `nodejs ws-srv.js`.
2. To run ws client: `nodejs ws-cli.js`.
3. To run socketio server: `nodejs socketio-srv.js`.
4. To run socketio client: `nodejs socketio-cli.js`.

`ws-{srv/cli}` can't cooperate with `socketio-{srv/cli}`. socketio will do a lot of extra work than websocket.

# pcaps

Two pcap files inside. One for socketio and one for ws.

# reference

1. [ws: a Node.js WebSocket library](https://github.com/websockets/ws)
2. [socket.io](https://github.com/socketio/socket.io)
3. [WebSocket协议完整解析](https://zhuanlan.zhihu.com/p/407711596)
