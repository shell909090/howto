'use strict';

import WebSocket from 'ws';

const ws = new WebSocket('ws://127.0.0.1:5300/');

ws.on('message', async arg => {
  console.log('recved: %s', arg);
  await new Promise((resolve) => {
    setTimeout(resolve, 1000);
  });
  ws.send(arg+'1');
});

ws.on('open', () => {
  ws.send('0');
});
