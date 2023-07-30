import { io } from "socket.io-client";

const socket = io("ws://localhost:5300");

socket.on("hello", async (arg) => {
  console.log(arg);
  await new Promise((resolve) => {
    setTimeout(resolve, 1000);
  });
  socket.emit("hello", arg+1);
});

socket.emit("hello", 0);
