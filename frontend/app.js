document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const typingIndicator = document.getElementById('typing-indicator');
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = themeToggle.querySelector('i');
    
    // Server API endpoint
    const API_URL = 'http://127.0.0.1:5000/api/chat';

    // Scroll to bottom helper
    const scrollToBottom = () => {
        chatBox.scrollTo({
            top: chatBox.scrollHeight,
            behavior: 'smooth'
        });
    };

    // Format time
    const getTime = () => {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    // Append a message to the chat box
    const appendMessage = (sender, content, intent = null) => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        let contentHtml = '';
        
        // If it's a quote object (from bot)
        if (typeof content === 'object' && content !== null) {
            if (intent) {
                contentHtml += `<span class="intent-pill"><i class="fa-solid fa-tag"></i> ${intent}</span>`;
            }
            contentHtml += `
                <div class="quote-text">"${content.text}"</div>
                <div class="quote-author">— ${content.author}</div>
            `;
        } 
        // If it's a direct string (from user or simple bot response)
        else {
            if (sender === 'bot' && intent && intent !== 'greet') {
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

    // Show/Hide typing indicator
    const setTypingIndicator = (show) => {
        if (show) {
            typingIndicator.style.display = 'flex';
            scrollToBottom();
        } else {
            typingIndicator.style.display = 'none';
        }
    };

    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage('user', message);
        userInput.value = '';
        
        // Show typing indicator
        setTypingIndicator(true);

        try {
            // Call the Flask API
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Hide typing indicator
            setTypingIndicator(false);
            
            // Artificial small delay for realism
            setTimeout(() => {
                // If it's a quote payload
                if (data.quote_details) {
                    appendMessage('bot', {
                        text: data.quote_details.quote_text,
                        author: data.quote_details.author
                    }, data.intent);
                } else {
                    // If it's a simple text response
                    appendMessage('bot', data.response, data.intent);
                }
            }, 500);

        } catch (error) {
            console.error('Error fetching data:', error);
            setTypingIndicator(false);
            appendMessage('bot', "Sorry, I'm having trouble connecting to the server right now. Is the backend running?");
        }
    });

    // Theme Toggle Logic
    const toggleTheme = () => {
        const body = document.body;
        if (body.getAttribute('data-theme') === 'dark') {
            body.removeAttribute('data-theme');
            themeIcon.className = 'fa-solid fa-moon';
            localStorage.setItem('theme', 'light');
        } else {
            body.setAttribute('data-theme', 'dark');
            themeIcon.className = 'fa-solid fa-sun';
            localStorage.setItem('theme', 'dark');
        }
    };

    themeToggle.addEventListener('click', toggleTheme);

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fa-solid fa-sun';
    }
});
