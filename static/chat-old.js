// chat.js

// JavaScript function to send a message
function sendMessage() {
    const userMessage = document.getElementById("user-input").value;

    // Check if the user message is not empty before sending
    if (userMessage.trim() !== "") {
        appendMessage(userMessage, true);
        document.getElementById("user-input").value = "";

        // Send the message to the server to store in the database
        sendToServer(userMessage);
    }
}

// JavaScript function to display a message in the chat container
function appendMessage(message, isUser) {
    const chatContainer = document.getElementById("chat");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");

    if (isUser) {
        messageElement.classList.add("user-input");
    } else {
        messageElement.classList.add("ai-response");
    }

    messageElement.textContent = message;
    chatContainer.appendChild(messageElement);
}

// Function to send a message when Enter key is pressed
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

// Add event listener for the Enter key press
document.getElementById("user-input").addEventListener("keypress", handleKeyPress);
document.getElementById("send-button").addEventListener("click", sendMessage);

// Function to send the user's message to the server
function sendToServer(userMessage) {
    // You should implement the server communication here
    // Send the 'userMessage' to the server for database insertion and response retrieval

    fetch("/save_message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display the AI response in the chat
                appendMessage(data.message, false);
            } else {
                // Handle insertion failure if needed
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}
