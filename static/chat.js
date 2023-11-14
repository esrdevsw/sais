document.addEventListener('DOMContentLoaded', function () {
    const chatContainer = document.getElementById('chat');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const darkModeSwitch = document.getElementById('darkModeSwitch');

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    darkModeSwitch.addEventListener('change', function () {
        document.body.classList.toggle('dark-mode');
        chatContainer.classList.toggle('dark-mode');
        document.querySelectorAll('.message').forEach(msg => msg.classList.toggle('dark-mode'));
        userInput.classList.toggle('dark-mode');
        sendButton.classList.toggle('dark-mode');
    });

    async function sendToServer(userMessage) {
        try {
            const response = await fetch('/save_message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userMessage }),
            });

            if (response.ok) {
                const data = await response.json();
                appendMessage(data.message, false);
            } else {
                console.error('Error:', response.statusText);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function sendMessage() {
        const userMessage = userInput.value.trim();

        if (userMessage !== '') {
            appendMessage(`You: ${userMessage}`, true);
            userInput.value = '';

            sendToServer(userMessage);
        }
    }

    function appendMessage(message, isUser) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');

        if (isUser) {
            messageElement.classList.add('user-input');
        } else {
            messageElement.classList.add('ai-response');
        }

        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
