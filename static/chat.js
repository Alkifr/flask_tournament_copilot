var socket = io();
var room = "{{ room.id }}";
var username = "{{ current_user.email }}";

socket.emit('join', {'room': room, 'username': username});

socket.on('message', function(data) {
    var messages = document.getElementById('messages');
    var message = document.createElement('div');
    message.textContent = data;
    messages.appendChild(message);
});

function sendMessage() {
    var messageInput = document.getElementById('message');
    var message = messageInput.value;
    socket.emit('message', {'room': room, 'username': username, 'message': message});
    messageInput.value = '';
}
