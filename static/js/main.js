document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io();

    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message');
    const sendButton = document.getElementById('send-button');

    let userId;

    socket.on('assign_user_id', (id) => {
        userId = id;
    });

    socket.on('load_messages', (messages) => {
        chatBox.innerHTML = ''; // Clear chat box before loading messages
        messages.forEach(msg => displayMessage(msg));
    });

    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message) {
            socket.emit('message', message);
            messageInput.value = '';
        }
    });

    socket.on('message', (msg) => {
        displayMessage(msg);
    });

    function displayMessage(msg) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `<strong>${msg.user}:</strong> ${msg.text} <span class="timestamp">${msg.timestamp}</span>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
