document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const serverSelect = document.getElementById("server-select");
    const connectButton = document.getElementById("connect-button");
    const connectionStatus = document.getElementById("connection-status");

    const appendMessage = (sender, message) => {
        const messageElement = document.createElement("div");
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    const connectToServer = async () => {
        const serverUrl = serverSelect.value;
        connectionStatus.textContent = "Connecting...";
        sendButton.disabled = true;

        try {
            const response = await fetch("/connect", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ server_url: serverUrl }),
            });

            if (response.ok) {
                const data = await response.json();
                connectionStatus.textContent = `Connected to ${serverUrl}`;
                appendMessage("System", data.message);
                sendButton.disabled = false;
            } else {
                const errorData = await response.json();
                connectionStatus.textContent = "Connection failed.";
                appendMessage("Error", errorData.error || "An unknown error occurred.");
            }
        } catch (error) {
            connectionStatus.textContent = "Connection failed.";
            appendMessage("Error", "Could not connect to the server.");
        }
    };

    const sendMessage = async () => {
        const message = chatInput.value.trim();
        if (message) {
            appendMessage("You", message);
            chatInput.value = "";

            try {
                const response = await fetch("/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ message }),
                });

                if (response.ok) {
                    const data = await response.json();
                    appendMessage("Server", data.response.replace(/\n/g, '<br>'));
                } else {
                    const errorData = await response.json();
                    appendMessage("Error", errorData.error || "An unknown error occurred.");
                }
            } catch (error) {
                appendMessage("Error", "Could not connect to the server.");
            }
        }
    };

    connectButton.addEventListener("click", connectToServer);
    sendButton.addEventListener("click", sendMessage);
    chatInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter" && !sendButton.disabled) {
            sendMessage();
        }
    });

    appendMessage("System", "Welcome to the MCP Chat Client! Please select a server and connect.");
});
