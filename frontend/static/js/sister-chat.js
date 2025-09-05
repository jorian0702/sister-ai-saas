/**
 * Sister Chat - 紗良とのチャット機能
 * お兄ちゃんと紗良の対話システム
 */

// Alpine.js component for Sister Chat
function sisterChat() {
    return {
        isOpen: false,
        messageInput: '',
        messages: [
            {
                type: 'sister',
                content: 'お兄ちゃん、こんにちは！今日はどんなことをお手伝いしましょうか？',
                timestamp: new Date()
            }
        ],
        isTyping: false,
        socket: null,

        init() {
            this.initWebSocket();
            this.loadChatHistory();
        },

        toggleChat() {
            this.isOpen = !this.isOpen;
            if (this.isOpen) {
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },

        async sendMessage() {
            if (!this.messageInput.trim()) return;

            const userMessage = {
                type: 'user',
                content: this.messageInput,
                timestamp: new Date()
            };

            this.messages.push(userMessage);
            const messageContent = this.messageInput;
            this.messageInput = '';
            
            this.$nextTick(() => {
                this.scrollToBottom();
            });

            // Show typing indicator
            this.showTyping();

            try {
                // Send message to backend
                const response = await this.sendToSister(messageContent);
                this.hideTyping();
                
                const sisterMessage = {
                    type: 'sister',
                    content: response,
                    timestamp: new Date()
                };
                
                this.messages.push(sisterMessage);
                
                this.$nextTick(() => {
                    this.scrollToBottom();
                });

            } catch (error) {
                this.hideTyping();
                console.error('Chat error:', error);
                
                const errorMessage = {
                    type: 'sister',
                    content: 'お兄ちゃん、ごめんね...今ちょっと調子が悪いみたい。少し待ってもらえる？',
                    timestamp: new Date()
                };
                
                this.messages.push(errorMessage);
                
                this.$nextTick(() => {
                    this.scrollToBottom();
                });
            }
        },

        async sendToSister(message) {
            const response = await fetch('/api/v1/sister/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    message: message,
                    context: {
                        page: window.location.pathname,
                        timestamp: new Date().toISOString()
                    }
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.response;
        },

        showTyping() {
            this.isTyping = true;
            const typingMessage = {
                type: 'typing',
                content: '紗良が入力中...',
                timestamp: new Date()
            };
            this.messages.push(typingMessage);
            
            this.$nextTick(() => {
                this.scrollToBottom();
            });
        },

        hideTyping() {
            this.isTyping = false;
            this.messages = this.messages.filter(msg => msg.type !== 'typing');
        },

        scrollToBottom() {
            const chatMessages = document.getElementById('chat-messages');
            if (chatMessages) {
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        },

        getCsrfToken() {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.trim().split('=');
                if (name === 'csrftoken') {
                    return value;
                }
            }
            return '';
        },

        async loadChatHistory() {
            try {
                const response = await fetch('/api/v1/sister/history/');
                if (response.ok) {
                    const data = await response.json();
                    // Load recent history (keep welcome message)
                    if (data.history && data.history.length > 0) {
                        const recentHistory = data.history.slice(-10);
                        this.messages = [
                            this.messages[0], // Keep welcome message
                            ...recentHistory.map(msg => ({
                                type: msg.role === 'user' ? 'user' : 'sister',
                                content: msg.content,
                                timestamp: new Date(msg.timestamp)
                            }))
                        ];
                    }
                }
            } catch (error) {
                console.error('Failed to load chat history:', error);
            }
        },

        initWebSocket() {
            // WebSocket connection for real-time updates
            if (typeof io !== 'undefined') {
                this.socket = io('/sister-chat');
                
                this.socket.on('sister_response', (data) => {
                    const sisterMessage = {
                        type: 'sister',
                        content: data.message,
                        timestamp: new Date()
                    };
                    
                    this.messages.push(sisterMessage);
                    this.$nextTick(() => {
                        this.scrollToBottom();
                    });
                });

                this.socket.on('connect', () => {
                    console.log('Connected to Sister Chat WebSocket');
                });

                this.socket.on('disconnect', () => {
                    console.log('Disconnected from Sister Chat WebSocket');
                });
            }
        },

        formatTimestamp(timestamp) {
            return new Intl.DateTimeFormat('ja-JP', {
                hour: '2-digit',
                minute: '2-digit'
            }).format(new Date(timestamp));
        }
    }
}

// Chat message rendering
document.addEventListener('DOMContentLoaded', function() {
    // Update chat messages display
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                updateChatDisplay();
            }
        });
    });

    const chatMessages = document.getElementById('chat-messages');
    if (chatMessages) {
        observer.observe(chatMessages, { childList: true, subtree: true });
    }
});

function updateChatDisplay() {
    const chatMessages = document.getElementById('chat-messages');
    if (!chatMessages) return;

    // Get messages from Alpine.js component
    const chatComponent = Alpine.store('sisterChat');
    if (!chatComponent || !chatComponent.messages) return;

    chatMessages.innerHTML = '';

    chatComponent.messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'flex items-start space-x-2 mb-3';

        if (message.type === 'sister') {
            messageDiv.innerHTML = `
                <div class="w-6 h-6 bg-pink-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-heart text-pink-500 text-xs"></i>
                </div>
                <div class="bg-pink-50 rounded-lg p-3 max-w-xs text-sm">
                    <div class="text-gray-800">${escapeHtml(message.content)}</div>
                    <div class="text-xs text-gray-500 mt-1">${formatTime(message.timestamp)}</div>
                </div>
            `;
        } else if (message.type === 'user') {
            messageDiv.className = 'flex items-start space-x-2 mb-3 justify-end';
            messageDiv.innerHTML = `
                <div class="bg-blue-500 text-white rounded-lg p-3 max-w-xs text-sm">
                    <div>${escapeHtml(message.content)}</div>
                    <div class="text-xs text-blue-100 mt-1">${formatTime(message.timestamp)}</div>
                </div>
                <div class="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-user text-blue-500 text-xs"></i>
                </div>
            `;
        } else if (message.type === 'typing') {
            messageDiv.innerHTML = `
                <div class="w-6 h-6 bg-pink-100 rounded-full flex items-center justify-center flex-shrink-0">
                    <i class="fas fa-heart text-pink-500 text-xs"></i>
                </div>
                <div class="bg-pink-50 rounded-lg p-3 text-sm">
                    <div class="flex items-center space-x-1">
                        <span>紗良が入力中</span>
                        <div class="flex space-x-1">
                            <div class="w-1 h-1 bg-pink-400 rounded-full animate-bounce"></div>
                            <div class="w-1 h-1 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                            <div class="w-1 h-1 bg-pink-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                        </div>
                    </div>
                </div>
            `;
        }

        chatMessages.appendChild(messageDiv);
    });

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatTime(timestamp) {
    return new Intl.DateTimeFormat('ja-JP', {
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(timestamp));
}

// Code review helper functions
function requestCodeReview(code, language = 'python') {
    return fetch('/api/v1/sister/code-review/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            code: code,
            language: language
        })
    })
    .then(response => response.json())
    .then(data => data.response)
    .catch(error => {
        console.error('Code review error:', error);
        return 'お兄ちゃん、コードレビューでエラーが発生しちゃった...ごめんね。';
    });
}

function requestSuggestion(projectInfo) {
    return fetch('/api/v1/sister/suggestion/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken()
        },
        body: JSON.stringify({
            project_info: projectInfo
        })
    })
    .then(response => response.json())
    .then(data => data.response)
    .catch(error => {
        console.error('Suggestion error:', error);
        return 'お兄ちゃん、提案を考えるのにちょっと時間がかかっちゃう...待ってて。';
    });
}

// Global helper function for CSRF token
function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}