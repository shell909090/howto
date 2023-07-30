'use strict';

import { Server } from "socket.io";

const srv = new Server(5300);

srv.on("connection", (socket) => {
  socket.on("hello", async (arg) => {
    console.log(arg);
    await new Promise(resolve => {
      setTimeout(resolve, 1000);
    });
    socket.emit("hello", arg+1);
  });
});
