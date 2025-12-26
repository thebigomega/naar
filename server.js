const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer);

const messages = [];

app.use(express.static('public'));

io.on('connection', (socket) => {
  socket.emit('history', messages);

  socket.on('message', (message) => {
    const trimmedName = (message.name || 'Anonymous').trim() || 'Anonymous';
    const trimmedText = (message.text || '').trim();

    if (!trimmedText) {
      return;
    }

    const messagePayload = {
      id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
      name: trimmedName,
      text: trimmedText,
      timestamp: Date.now()
    };

    messages.push(messagePayload);
    if (messages.length > 100) {
      messages.shift();
    }

    io.emit('message', messagePayload);
  });
});

const port = process.env.PORT || 3000;
httpServer.listen(port, () => {
  console.log(`Chat server listening on http://localhost:${port}`);
});
