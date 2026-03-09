document.addEventListener('DOMContentLoaded', () => {

    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const typingIndicator = document.getElementById('typing-indicator');
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');

    // Backend API
    const API_URL = "http://127.0.0.1:5000/api/chat";

    const scrollToBottom = () => {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: "smooth"
        });
    };

    const getTime = () => {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    };

    const appendMessage = (sender, content, intent = null) => {

        const messageDiv = document.createElement("div");
        messageDiv.className = `message ${sender}`;

        let contentHtml = "";

        if (typeof content === "object" && content !== null) {

            if (intent) {
                contentHtml += `<span class="intent-pill"><i class="fa-solid fa-tag"></i> ${intent}</span>`;
            }

            contentHtml += `
                <div class="quote-text">"${content.text}"</div>
                <div class="quote-author">— ${content.author}</div>
            `;

        } else {

            if (sender === "bot" && intent && intent !== "greet") {
                contentHtml += `<span class="intent-pill"><i class="fa-solid fa-tag"></i> ${intent}</span>`;
            }

            contentHtml += `<p>${content}</p>`;
        }

        messageDiv.innerHTML = `
            <div class="message-content">
                ${contentHtml}
            </div>
            <span class="message-time">${getTime()}</span>
        `;

        chatBox.appendChild(messageDiv);
        scrollToBottom();
    };

    const setTypingIndicator = (show) => {
        typingIndicator.style.display = show ? "flex" : "none";
        scrollToBottom();
    };

    chatForm.addEventListener("submit", async (e) => {

        e.preventDefault();

        const message = userInput.value.trim();
        if (!message) return;

        appendMessage("user", message);
        userInput.value = "";

        setTypingIndicator(true);

        try {

            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message })
            });

            console.log("API Response Status:", response.status);

            const data = await response.json();

            console.log("API Response Data:", data);

            setTypingIndicator(false);

            setTimeout(() => {

                if (data.quote_details) {

                    appendMessage("bot", {
                        text: data.quote_details.quote_text,
                        author: data.quote_details.author
                    }, data.intent);

                } else if (data.response) {

                    appendMessage("bot", data.response, data.intent);

                } else {

                    appendMessage("bot", "Sorry, I couldn't understand that.");
                }

            }, 500);

        } catch (error) {

            console.error("API Connection Error:", error);

            setTypingIndicator(false);

            appendMessage(
                "bot",
                "⚠️ Unable to connect to the server. Please make sure the backend is running on port 5000."
            );
        }

    });

    // Theme Toggle
    const toggleTheme = () => {

        const body = document.body;

        if (body.getAttribute("data-theme") === "dark") {
            body.removeAttribute("data-theme");
            themeIcon.className = "fa-solid fa-moon";
            localStorage.setItem("theme", "light");
        } else {
            body.setAttribute("data-theme", "dark");
            themeIcon.className = "fa-solid fa-sun";
            localStorage.setItem("theme", "dark");
        }

    };

    themeToggle.addEventListener("click", toggleTheme);

    const savedTheme = localStorage.getItem("theme");

    if (
        savedTheme === "dark" ||
        (!savedTheme &&
            window.matchMedia("(prefers-color-scheme: dark)").matches)
    ) {
        document.body.setAttribute("data-theme", "dark");
        themeIcon.className = "fa-solid fa-sun";
    }

});