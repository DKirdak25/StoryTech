function loadMessages() {
    fetch("/chat/fetch/")
        .then(res => res.json())
        .then(data => {
            let html = "";

            data.messages.forEach(msg => {
                if (msg.sender === "user") {
                    html += `
                        <div class="user-msg">
                            <div class="bubble">${msg.text}</div>
                        </div>
                    `;
                } else {
                    html += `
                        <div class="admin-msg">
                            <div class="bubble">${msg.text}</div>
                        </div>
                    `;
                }
            });

            let container = document.getElementById("messages");
            container.innerHTML = html;
            container.scrollTop = container.scrollHeight;
        });
}

// Auto-refresh every 2 seconds
setInterval(loadMessages, 2000);
loadMessages();

document.getElementById("chatForm").addEventListener("submit", function(e) {
    e.preventDefault();

    let input = document.getElementById("msgInput");

    fetch("/chat/send/", {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        },
        body: new URLSearchParams({
            "text": input.value
        })
    })
    .then(() => {
        input.value = "";
        loadMessages();
    });
});