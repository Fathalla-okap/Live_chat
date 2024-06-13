document.addEventListener('DOMContentLoaded', (event) => {
    const socket = io();

    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message');
    const sendButton = document.getElementById('send-button');
    const onlineUsersElement = document.getElementById('online-users');
    const totalVisitorsElement = document.getElementById('total-visitors');

    let userId;

    socket.on('assign_user_id', (id) => {
        userId = id;
    });

    socket.on('load_messages', (messages) => {
        messages.forEach((msg, index) => displayMessage(msg, index));
    });

    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message) {
            socket.send(message);
            messageInput.value = '';
        }
    });

    socket.on('message', (msg) => {
        const index = document.getElementsByClassName('message').length;
        displayMessage(msg, index);
    });

    socket.on('update_online_users', (onlineUsers) => {
        onlineUsersElement.textContent = `Online Users: ${onlineUsers}`;
    });

    socket.on('update_total_visitors', (totalVisitors) => {
        totalVisitorsElement.textContent = `Total Visitors: ${totalVisitors}`;
    });

    function displayMessage(msg, index) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `<strong>${msg.user}:</strong> ${msg.text}<span class="timestamp">${new Date().toLocaleTimeString()}</span>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
