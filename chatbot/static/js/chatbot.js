/**
 * Barbeque Nation Chatbot
 * This script handles the chatbot interface and functionality.
 */

// Configuration
const API_BASE_URL = '/api'; // Will be the endpoint for our server
let conversationId = null;
let retellWebClient = null;

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const startVoiceCallButton = document.getElementById('start-voice-call');
const endCallButton = document.getElementById('end-call-btn');
const callStatus = document.getElementById('call-status');
const statusMessage = document.getElementById('status-message');
const callModal = new bootstrap.Modal(document.getElementById('callModal'), {
    backdrop: 'static'
});

// Initialize the chatbot
document.addEventListener('DOMContentLoaded', () => {
    // Add initial bot message
    addBotMessage("Hello! Welcome to Barbeque Nation. I'm your virtual assistant. How can I help you today?");
    
    // Start a new conversation
    startConversation();
    
    // Add event listeners
    setupEventListeners();
    
    // Update status for troubleshooting
    statusMessage.innerHTML = `Debug: API Base URL: ${API_BASE_URL}<br>Using Retell SDK: ${typeof RetellWebClient !== 'undefined' ? 'Yes' : 'No'}`;
});

// Set up event listeners
function setupEventListeners() {
    // Send message when the send button is clicked
    sendButton.addEventListener('click', sendMessage);
    
    // Send message when Enter key is pressed in the input field
    userInput.addEventListener('keypress', event => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
    
    // Start voice call when the button is clicked
    startVoiceCallButton.addEventListener('click', startVoiceCall);
    
    // End call when the button is clicked
    endCallButton.addEventListener('click', endVoiceCall);
}

// Start a new conversation
async function startConversation() {
    try {
        const userId = 'user_' + Math.random().toString(36).substring(2, 15);
        
        addBotMessage("Attempting to connect to server...");
        
        const response = await fetch(`${API_BASE_URL}/chatbot/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: userId
            })
        });
        
        const data = await response.json();
        
        if (data.conversation_id) {
            conversationId = data.conversation_id;
            statusMessage.textContent = `Connected (Conversation ID: ${conversationId})`;
            addBotMessage("Connected successfully! How can I help you today?");
        } else {
            statusMessage.textContent = 'Error: Could not start conversation';
            addBotMessage("Error: Couldn't start a conversation. Response: " + JSON.stringify(data));
        }
    } catch (error) {
        console.error('Error starting conversation:', error);
        statusMessage.textContent = 'Error: Could not connect to the server';
        addBotMessage(`Connection error: ${error.message}. Please check if the server is running.`);
    }
}

// Send a message to the chatbot
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (message === '') {
        return;
    }
    
    // Clear the input field
    userInput.value = '';
    
    // Add user message to the chat
    addUserMessage(message);
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        if (!conversationId) {
            removeTypingIndicator();
            addBotMessage("Error: No active conversation. Trying to reconnect...");
            startConversation();
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/chatbot/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                message: message
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator();
        
        if (data.response) {
            // Add bot response to the chat
            addBotMessage(data.response);
        } else if (data.error) {
            // Show specific error message with details if available
            let errorMsg = `Error from server: ${data.error}`;
            
            if (data.api_response) {
                try {
                    // Try to parse the API response for more details
                    const apiError = JSON.parse(data.api_response);
                    if (apiError && apiError.message) {
                        errorMsg += `\n\nAPI Error: ${apiError.message}`;
                    }
                } catch (e) {
                    // Just use the raw response if parsing fails
                    errorMsg += `\n\nAPI Response: ${data.api_response}`;
                }
            }
            
            addBotMessage(errorMsg);
            
            // Show debugging information in status
            if (data.request_url) {
                statusMessage.innerHTML = `Debug: Error connecting to ${data.request_url}<br>Status: ${data.status_code || 'Unknown'}`;
            }
        } else {
            // Show error message
            addBotMessage("I'm sorry, I'm having trouble understanding. Could you try again?");
        }
    } catch (error) {
        console.error('Error sending message:', error);
        
        // Remove typing indicator
        removeTypingIndicator();
        
        // Show detailed error message
        addBotMessage(`I'm sorry, there was an error processing your request: ${error.message}. Please try again later.`);
    }
}

// Add a user message to the chat
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'user-message');
    messageElement.textContent = message;
    
    // Add timestamp
    const timeElement = document.createElement('span');
    timeElement.classList.add('message-time');
    timeElement.textContent = getCurrentTime();
    messageElement.appendChild(timeElement);
    
    chatMessages.appendChild(messageElement);
    
    // Scroll to the bottom
    scrollToBottom();
}

// Add a bot message to the chat
function addBotMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'bot-message');
    messageElement.textContent = message;
    
    // Add timestamp
    const timeElement = document.createElement('span');
    timeElement.classList.add('message-time');
    timeElement.textContent = getCurrentTime();
    messageElement.appendChild(timeElement);
    
    chatMessages.appendChild(messageElement);
    
    // Scroll to the bottom
    scrollToBottom();
}

// Show the typing indicator
function showTypingIndicator() {
    const typingElement = document.createElement('div');
    typingElement.classList.add('typing-indicator');
    typingElement.id = 'typing-indicator';
    
    // Add dots
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        typingElement.appendChild(dot);
    }
    
    chatMessages.appendChild(typingElement);
    
    // Scroll to the bottom
    scrollToBottom();
}

// Remove the typing indicator
function removeTypingIndicator() {
    const typingElement = document.getElementById('typing-indicator');
    if (typingElement) {
        typingElement.remove();
    }
}

// Scroll the chat to the bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Get the current time in HH:MM format
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Start a voice call
async function startVoiceCall() {
    try {
        // Show the call modal
        callModal.show();
        
        // Update status
        callStatus.textContent = 'Connecting to agent...';
        
        // Get web call token
        const response = await fetch(`${API_BASE_URL}/chatbot/create-web-call`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_id: 'web_user_' + Math.random().toString(36).substring(2, 15)
            })
        });
        
        const data = await response.json();
        
        // Clear any previous error details
        const callDetails = document.getElementById('call-details');
        if (callDetails) {
            callDetails.innerHTML = '';
        }
        
        // Handle different call modes
        if (data.call_mode === 'twilio_direct' || data.call_mode === 'twilio_direct_fallback') {
            // Show phone number to call
            callStatus.textContent = 'Please call this number:';
            
            const phoneElement = document.createElement('div');
            phoneElement.className = 'phone-number';
            phoneElement.innerHTML = `<a href="tel:${data.phone_number}" class="btn btn-success btn-lg mt-3 mb-3">
                <i class="bi bi-telephone"></i> ${data.phone_number}</a>
                <div class="small text-muted mt-2">${data.message || 'Call this number to speak with BBQ Nation assistant'}</div>`;
            callDetails.appendChild(phoneElement);
            
            // Update UI
            endCallButton.disabled = true;
            endCallButton.textContent = 'Close';
            
            return;
        }
        
        // Continue with RetellWebClient for other modes
        if (!data.access_token) {
            const errorMsg = data.error || 'Unknown error';
            let detailedError = errorMsg;
            
            // Try to extract more detailed error information
            if (data.api_response) {
                try {
                    // Try to parse the API response for more details
                    const apiError = JSON.parse(data.api_response);
                    if (apiError && apiError.message) {
                        detailedError += `: ${apiError.message}`;
                        
                        // Check for common error patterns
                        if (apiError.message.includes("Agent not found")) {
                            detailedError += "\n\nPlease check if the Agent ID is correct in your .env file.";
                        } else if (apiError.message.includes("unauthorized") || apiError.message.includes("Invalid token")) {
                            detailedError += "\n\nPlease check if your Retell API key is correct and not expired.";
                        }
                    }
                } catch (e) {
                    // Just use the raw response if parsing fails
                    detailedError += `: ${data.api_response}`;
                    
                    // Check for common error patterns in raw response
                    if (data.api_response.includes("404")) {
                        detailedError += "\n\nPlease check if the API endpoint URL is correct.";
                    } else if (data.api_response.includes("403") || data.api_response.includes("401")) {
                        detailedError += "\n\nPlease verify your API credentials.";
                    }
                }
            }
            
            if (data.debugging_info) {
                detailedError += `\n\nDebugging info: ${JSON.stringify(data.debugging_info)}`;
            }
            
            // If we have a phone number as fallback, display it
            if (data.phone_number) {
                callStatus.textContent = 'Web call failed. Please call this number:';
                
                const phoneElement = document.createElement('div');
                phoneElement.className = 'phone-number';
                phoneElement.innerHTML = `<a href="tel:${data.phone_number}" class="btn btn-success btn-lg mt-3 mb-3">
                    <i class="bi bi-telephone"></i> ${data.phone_number}</a>
                    <div class="small text-muted mt-2">Call this number to speak with BBQ Nation assistant</div>`;
                callDetails.appendChild(phoneElement);
                
                // Add error details below the phone number
                const errorDetails = document.createElement('div');
                errorDetails.classList.add('error-details', 'mt-3');
                errorDetails.textContent = detailedError;
                callDetails.appendChild(errorDetails);
            } else {
                // No phone number fallback, just show error
                callStatus.textContent = `Error: Could not start call`;
                
                // Add detailed error to a separate element for readability
                const errorDetails = document.createElement('div');
                errorDetails.classList.add('error-details');
                errorDetails.textContent = detailedError;
                callDetails.appendChild(errorDetails);
            }
            
            console.error('Voice call error:', data);
            return;
        }
        
        // Display alternate phone number if provided
        if (data.phone_number) {
            const phoneElement = document.createElement('div');
            phoneElement.className = 'alternate-phone small text-muted mt-2 mb-2';
            phoneElement.innerHTML = `Alternatively, you can call: <a href="tel:${data.phone_number}">${data.phone_number}</a>`;
            callDetails.appendChild(phoneElement);
        }
        
        // Initialize Retell client
        if (typeof RetellWebClient === 'undefined') {
            callStatus.textContent = 'Error: Retell SDK not loaded';
            console.error('RetellWebClient is not defined - SDK may not be loaded');
            
            // If we have a phone number as fallback, display it
            if (data.phone_number) {
                const phoneElement = document.createElement('div');
                phoneElement.className = 'phone-number';
                phoneElement.innerHTML = `<a href="tel:${data.phone_number}" class="btn btn-success btn-lg mt-3">
                    <i class="bi bi-telephone"></i> ${data.phone_number}</a>
                    <div class="small text-muted mt-2">Call this number to speak with BBQ Nation assistant</div>`;
                callDetails.appendChild(phoneElement);
            }
            
            return;
        }
        
        retellWebClient = new RetellWebClient();
        
        // Set up event handlers
        retellWebClient.on('call_started', () => {
            callStatus.textContent = 'Connected to agent';
            endCallButton.disabled = false;
            // Clear any error details that might be showing
            if (callDetails) {
                callDetails.innerHTML = '';
                
                // Still show the alternative phone number if available
                if (data.phone_number) {
                    const phoneElement = document.createElement('div');
                    phoneElement.className = 'alternate-phone small text-muted mt-2';
                    phoneElement.innerHTML = `Alternatively, you can call: <a href="tel:${data.phone_number}">${data.phone_number}</a>`;
                    callDetails.appendChild(phoneElement);
                }
            }
        });
        
        retellWebClient.on('call_ended', () => {
            callStatus.textContent = 'Call ended';
            endCallButton.disabled = true;
            setTimeout(() => callModal.hide(), 2000);
            retellWebClient = null;
        });
        
        retellWebClient.on('agent_speech_started', () => {
            callStatus.textContent = 'Agent is speaking...';
        });
        
        retellWebClient.on('agent_speech_ended', () => {
            callStatus.textContent = 'Agent is listening...';
        });
        
        retellWebClient.on('error', (error) => {
            console.error('Retell error:', error);
            callStatus.textContent = 'Error: ' + error.message;
            
            // Add more details for specific errors
            const errorDetails = document.createElement('div');
            errorDetails.classList.add('error-details');
            
            if (error.message.includes("audio") || error.message.includes("microphone")) {
                errorDetails.textContent = "Please ensure your microphone is connected and you've granted permission to use it.";
            } else if (error.message.includes("network") || error.message.includes("connection")) {
                errorDetails.textContent = "Please check your internet connection and try again.";
            } else {
                errorDetails.textContent = "An error occurred with the voice call. Please try again later.";
            }
            
            callDetails.appendChild(errorDetails);
            
            // Show alternate phone number if available
            if (data.phone_number) {
                const phoneElement = document.createElement('div');
                phoneElement.className = 'phone-number mt-3';
                phoneElement.innerHTML = `<p>Alternatively, you can call:</p>
                    <a href="tel:${data.phone_number}" class="btn btn-success">
                    <i class="bi bi-telephone"></i> ${data.phone_number}</a>`;
                callDetails.appendChild(phoneElement);
            }
        });
        
        // Start the call
        console.log('Starting call with access token:', data.access_token.substring(0, 10) + "...");
        await retellWebClient.startCall({
            accessToken: data.access_token
        });
        
    } catch (error) {
        console.error('Error starting voice call:', error);
        callStatus.textContent = `Error: Could not start call`;
        
        // Add detailed error to a separate element for readability
        const errorDetails = document.createElement('div');
        errorDetails.classList.add('error-details');
        errorDetails.textContent = error.message || "Unknown error";
        
        if (error.message && error.message.includes("Failed to fetch")) {
            errorDetails.textContent += "\n\nPlease check if the server is running and accessible.";
        }
        
        document.getElementById('call-details').appendChild(errorDetails);
    }
}

// End the voice call
function endVoiceCall() {
    if (retellWebClient) {
        retellWebClient.endCall();
        callStatus.textContent = 'Ending call...';
        endCallButton.disabled = true;
    }
} 