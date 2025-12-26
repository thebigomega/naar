const socket = io();

const form = document.getElementById('chat-form');
const messageInput = document.getElementById('message');
const nameInput = document.getElementById('name');
const messagesList = document.getElementById('messages');

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMessage(message) {
  const li = document.createElement('li');
  li.innerHTML = `
    <div class="meta">
      <span class="name">${message.name || 'Anonymous'}</span>
      <span class="time">${formatTime(message.timestamp)}</span>
    </div>
    <p>${message.text}</p>
  `;
  messagesList.appendChild(li);
  messagesList.scrollTop = messagesList.scrollHeight;
}

socket.on('history', (history) => {
  messagesList.innerHTML = '';
  history.forEach(addMessage);
});

socket.on('message', addMessage);

form.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = messageInput.value.trim();
  const name = nameInput.value.trim();

  if (!text) return;

  socket.emit('message', { name, text });
  messageInput.value = '';
  messageInput.focus();
});
