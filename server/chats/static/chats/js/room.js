const roomName = JSON.parse(document.getElementById('room-name').textContent);
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxNzc0MTE3LCJpYXQiOjE2ODkxODIxMTcsImp0aSI6IjFmYWQwYmQ3MzVlMDRkZTA4NzJkMzdjNjg4ODlkYTRkIiwidXNlcl9pZCI6IjU0OGQzYmYyLTRhMmQtNGU5Mi1hYzM5LTE0Y2EyNDIzNjk0YiJ9._-8PDsXD0UCU1H-7nHf5R9dwFWdMtOHoAcC6ZmCmJk4";

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat?token=' + token
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.text + '\n');
};
chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const text = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'text': text
    }));
    messageInputDom.value = '';
};