document.addEventListener("DOMContentLoaded", function () {
    const sendButton = document.getElementById("sendMessage");
    const chatInput = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    function loadMessages() {
        fetch("/messaging/get-messages/")
            .then(response => response.json())
            .then(data => {
                chatBox.innerHTML = "";
                data.messages.forEach(msg => {
                    chatBox.innerHTML += `<p><strong>${msg.is_admin ? "Admin" : "You"}:</strong> ${msg.message}</p>`;
                });
            });
    }

    sendButton.addEventListener("click", function () {
        fetch("/messaging/send-message/", {
            method: "POST",
            body: new URLSearchParams({ "message": chatInput.value })
        })
        .then(response => response.json())
        .then(() => loadMessages());

        chatInput.value = "";
    });

    setInterval(loadMessages, 5000);
});
