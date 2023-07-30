'use strict';

import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 5300 });

wss.on('connection', (ws) => {
  ws.on('message', async (arg) => {
    console.log('recved: %s %s', arg, typeof arg);
    await new Promise((resolve) => {
      setTimeout(resolve, 1000);
    });
    ws.send(arg+'1');
  });
});
