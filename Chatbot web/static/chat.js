document.getElementById('send-button').addEventListener('click', sendMessage);

function sendMessage() {
    let userInput = document.getElementById('user-input');
    let message = userInput.value.trim();
    
    if (message === "") return;

    appendMessage('user', message);
    userInput.value = '';

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        appendMessage('bot', data.reply);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function appendMessage(sender, message) {
    let messageElement = document.createElement('div');
    messageElement.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
    
    let messageContent = document.createElement('div');
    messageContent.classList.add('message-content');
    messageContent.textContent = message;
    
    messageElement.appendChild(messageContent);
    document.getElementById('chat-messages').appendChild(messageElement);
    messageElement.scrollIntoView({ behavior: 'smooth' });
}