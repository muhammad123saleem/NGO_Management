document.addEventListener("DOMContentLoaded", function () {
    const userSelect = document.getElementById("userSelect");
    const chatContainer = document.getElementById("chatContainer");
    const chatBox = document.getElementById("chatBox");
    const chatInput = document.getElementById("chatInput");
    const sendMessage = document.getElementById("sendMessage");

    userSelect.addEventListener("change", function () {
        const userId = userSelect.value;
        if (userId) {
            chatContainer.style.display = "block";
            loadMessages(userId);
        } else {
            chatContainer.style.display = "none";
        }
    });

    function loadMessages(userId) {
        fetch(`/messaging/admin/get-messages/${userId}/`)
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML = "";
            data.messages.forEach(msg => {
                const msgDiv = document.createElement("div");
                msgDiv.classList.add("message", msg.is_admin ? "admin-message" : "user-message");
                msgDiv.innerHTML = `<p><strong>${msg.is_admin ? "Admin" : "User"}:</strong> ${msg.message}</p>`;
                chatBox.appendChild(msgDiv);
            });
        });
    }

    sendMessage.addEventListener("click", function () {
        const userId = userSelect.value;
        const message = chatInput.value.trim();

        if (message) {
            fetch("/messaging/admin/send-message/", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ user_id: userId, message: message })
            })
            .then(response => response.json())
            .then(() => {
                loadMessages(userId);
                chatInput.value = "";
            });
        }
    });
});
