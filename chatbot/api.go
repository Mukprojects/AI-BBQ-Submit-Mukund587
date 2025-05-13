package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math/rand"
	"net/http"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

// RetellRequest represents a request to the Retell API
type RetellRequest struct {
	AgentID   string                 `json:"agent_id"`
	UserID    string                 `json:"user_id"`
	Message   string                 `json:"message"`
	Mode      string                 `json:"mode"`
	Context   map[string]interface{} `json:"context,omitempty"`
	Streaming bool                   `json:"streaming"`
}

// RetellResponse represents a response from the Retell API
type RetellResponse struct {
	ID             string                 `json:"id"`
	Response       string                 `json:"response"`
	Context        map[string]interface{} `json:"context,omitempty"`
	ConversationID string                 `json:"conversation_id"`
	Finished       bool                   `json:"finished"`
}

// WebCallRequest represents a request to create a web call
type WebCallRequest struct {
	AgentID    string                 `json:"agent_id"`
	UserID     string                 `json:"user_id"`
	Mode       string                 `json:"mode"`
	Context    map[string]interface{} `json:"context,omitempty"`
	WebhookURL string                 `json:"webhook_url,omitempty"`
}

// WebCallResponse represents a response from creating a web call
type WebCallResponse struct {
	AccessToken string `json:"access_token"`
	ExpiresAt   string `json:"expires_at"`
}

// StartChatbotRequest is the request for starting a chatbot session
type StartChatbotRequest struct {
	UserID  string `json:"user_id"`
	AgentID string `json:"agent_id,omitempty"`
}

// ChatMessageRequest is the request for sending a chat message
type ChatMessageRequest struct {
	ConversationID string                 `json:"conversation_id"`
	Message        string                 `json:"message"`
	Context        map[string]interface{} `json:"context,omitempty"`
}

// Define state types
type ConversationState string

const (
	StateGreeting     ConversationState = "greeting"
	StateCity         ConversationState = "city"
	StateOutlet       ConversationState = "outlet"
	StateReservation  ConversationState = "reservation"
	StateContact      ConversationState = "contact"
	StateConfirmation ConversationState = "confirmation"
	StateEnd          ConversationState = "end"
)

// StateFlowRequest represents a request for state-based conversation flow
type StateFlowRequest struct {
	UserID       string                 `json:"user_id"`
	CurrentState string                 `json:"current_state,omitempty"`
	Message      string                 `json:"message"`
	Context      map[string]interface{} `json:"context,omitempty"`
}

// StateFlowResponse represents a response from state-based conversation flow
type StateFlowResponse struct {
	NextState string                 `json:"next_state"`
	Response  string                 `json:"response"`
	Context   map[string]interface{} `json:"context,omitempty"`
	Finished  bool                   `json:"finished"`
}

// Global variables
var retellAPIKey string
var retellBaseURL = "https://api.retellai.com/v1"

// Initialize loads environment variables and sets up the module
func Initialize() {
	// Try to load .env from parent directory if not found in current directory
	err := godotenv.Load()
	if err != nil {
		// Try to load from parent directory
		parentEnvPath := filepath.Join("..", ".env")
		err = godotenv.Load(parentEnvPath)
		if err != nil {
			log.Println("Warning: .env file not found in current or parent directory, using environment variables")
		} else {
			log.Println("Loaded .env from parent directory")
		}
	} else {
		log.Println("Loaded .env from current directory")
	}

	// Get Retell API key from environment
	retellAPIKey = os.Getenv("RETELL_API_KEY")
	if retellAPIKey == "" {
		log.Println("Warning: RETELL_API_KEY is not set in environment")
	} else {
		log.Printf("RETELL_API_KEY is set: %s (length: %d)", maskAPIKey(retellAPIKey), len(retellAPIKey))
	}

	// Print the default agent ID for debugging
	defaultAgentID := os.Getenv("DEFAULT_AGENT_ID")
	if defaultAgentID == "" {
		log.Println("Warning: DEFAULT_AGENT_ID is not set in environment")
	} else {
		log.Printf("DEFAULT_AGENT_ID is set: %s", defaultAgentID)
	}

	log.Printf("Using Retell API base URL: %s", retellBaseURL)
}

// maskAPIKey returns a masked version of the API key for logging
func maskAPIKey(key string) string {
	if len(key) <= 8 {
		return "****"
	}
	return key[:4] + "..." + key[len(key)-4:]
}

// RegisterRoutes registers the chatbot API routes with Gin
func RegisterRoutes(router *gin.RouterGroup) {
	// Initialize environment
	Initialize()

	// Debug endpoint to check configuration
	router.GET("/debug", func(c *gin.Context) {
		debugInfo := map[string]interface{}{
			"retell_api_key_set": retellAPIKey != "",
			"default_agent_id":   os.Getenv("DEFAULT_AGENT_ID"),
			"webhook_url":        os.Getenv("WEBHOOK_URL"),
			"knowledge_base_id":  os.Getenv("KNOWLEDGE_BASE_ID"),
			"environment":        "production",
		}
		c.JSON(http.StatusOK, debugInfo)
	})

	// Regular endpoints
	router.POST("/chatbot/start", startChatbotHandler)
	router.POST("/chatbot/message", chatMessageHandler)
	router.POST("/chatbot/end", endChatbotHandler)
	router.POST("/chatbot/create-web-call", createWebCallHandler)

	// State-based conversation flow handler
	router.POST("/chatbot/state-flow", stateFlowHandler)
}

// startChatbotHandler handles requests to start a new chatbot conversation
func startChatbotHandler(c *gin.Context) {
	var req StartChatbotRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	// Use default agent ID if not provided
	agentID := req.AgentID
	if agentID == "" {
		// Get the default agent ID from environment
		agentID = os.Getenv("DEFAULT_AGENT_ID")
		if agentID == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Agent ID is required but DEFAULT_AGENT_ID is not set in environment"})
			return
		}
	}

	// Create conversation with Retell API (this is a simplified example)
	// In reality, we would use Retell's API to create a conversation
	conversationID := fmt.Sprintf("conv_%d", time.Now().Unix())

	c.JSON(http.StatusOK, gin.H{
		"conversation_id": conversationID,
		"agent_id":        agentID,
		"user_id":         req.UserID,
	})
}

// chatMessageHandler handles requests to send a message to the chatbot
func chatMessageHandler(c *gin.Context) {
	var req ChatMessageRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	if req.ConversationID == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "conversation_id is required"})
		return
	}

	if req.Message == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "message is required"})
		return
	}

	// First, try to use Retell API for message handling
	retellResponse, retellErr := callRetellAPI(req.Message, req.ConversationID)

	// If Retell API fails, fall back to local knowledge base
	if retellErr != nil {
		log.Printf("Retell API error: %v. Falling back to knowledge base API", retellErr)

		// Call the local knowledge base API
		kbResponse, kbErr := callKnowledgeBaseAPI(req.Message, req.ConversationID)
		if kbErr != nil {
			log.Printf("Knowledge base API error: %v", kbErr)
			c.JSON(http.StatusInternalServerError, gin.H{
				"error":        "Both Retell API and knowledge base API failed",
				"retell_error": retellErr.Error(),
				"kb_error":     kbErr.Error(),
			})
			return
		}

		// Return the knowledge base response
		c.JSON(http.StatusOK, gin.H{
			"response":        kbResponse.Response,
			"conversation_id": req.ConversationID,
			"source":          "knowledge_base",
			"finished":        kbResponse.Finished,
		})
		return
	}

	// Return the Retell API response
	c.JSON(http.StatusOK, gin.H{
		"response":        retellResponse.Response,
		"conversation_id": retellResponse.ConversationID,
		"context":         retellResponse.Context,
		"finished":        retellResponse.Finished,
	})
}

// callRetellAPI calls the Retell API with the given message and conversation ID
func callRetellAPI(message, conversationID string) (RetellResponse, error) {
	var response RetellResponse

	// Get the default agent ID from environment
	agentID := os.Getenv("DEFAULT_AGENT_ID")
	if agentID == "" {
		return response, fmt.Errorf("DEFAULT_AGENT_ID is not set in environment")
	}

	// Prepare the request to Retell API
	url := retellBaseURL + "/conversations"
	req := RetellRequest{
		AgentID:   agentID,
		UserID:    "user_" + conversationID,
		Message:   message,
		Mode:      "hybrid", // Use hybrid mode to allow for API modifications
		Streaming: false,
	}

	// Convert request to JSON
	jsonData, err := json.Marshal(req)
	if err != nil {
		return response, fmt.Errorf("error marshaling request: %v", err)
	}

	// Create HTTP request
	httpReq, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return response, fmt.Errorf("error creating request: %v", err)
	}

	// Set headers
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", "Bearer "+retellAPIKey)

	// Send request
	client := &http.Client{Timeout: 30 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		return response, fmt.Errorf("error sending request to Retell API: %v", err)
	}
	defer resp.Body.Close()

	// Read response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return response, fmt.Errorf("error reading response body: %v", err)
	}

	// Check for non-200 status code
	if resp.StatusCode != http.StatusOK {
		return response, fmt.Errorf("Retell API returned non-200 status code: %d, body: %s", resp.StatusCode, string(body))
	}

	// Parse response
	err = json.Unmarshal(body, &response)
	if err != nil {
		return response, fmt.Errorf("error parsing response body: %v", err)
	}

	return response, nil
}

// KBResponse represents a response from the knowledge base API
type KBResponse struct {
	Response       string `json:"response"`
	ConversationID string `json:"conversation_id"`
	Source         string `json:"source"`
	Finished       bool   `json:"finished"`
}

// callKnowledgeBaseAPI calls the local knowledge base API with the given message
func callKnowledgeBaseAPI(message, conversationID string) (KBResponse, error) {
	var response KBResponse

	// Prepare the request to the knowledge base API
	url := "http://localhost:8000/kb/conversation"
	reqBody := map[string]interface{}{
		"message":         message,
		"conversation_id": conversationID,
	}

	// Convert request to JSON
	jsonData, err := json.Marshal(reqBody)
	if err != nil {
		return response, fmt.Errorf("error marshaling request: %v", err)
	}

	// Create HTTP request
	httpReq, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		return response, fmt.Errorf("error creating request: %v", err)
	}

	// Set headers
	httpReq.Header.Set("Content-Type", "application/json")

	// Send request
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		return response, fmt.Errorf("error sending request to knowledge base API: %v", err)
	}
	defer resp.Body.Close()

	// Read response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return response, fmt.Errorf("error reading response body: %v", err)
	}

	// Check for non-200 status code
	if resp.StatusCode != http.StatusOK {
		return response, fmt.Errorf("knowledge base API returned non-200 status code: %d, body: %s", resp.StatusCode, string(body))
	}

	// Parse response
	err = json.Unmarshal(body, &response)
	if err != nil {
		return response, fmt.Errorf("error parsing response body: %v", err)
	}

	return response, nil
}

// endChatbotHandler handles requests to end a chatbot conversation
func endChatbotHandler(c *gin.Context) {
	var req struct {
		ConversationID string `json:"conversation_id"`
		Transcript     string `json:"transcript,omitempty"`
	}
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	// Log the conversation to our webhook API
	webhookURL := os.Getenv("WEBHOOK_URL")
	if webhookURL != "" {
		logData := map[string]interface{}{
			"modality":        "Chatbot",
			"conversation_id": req.ConversationID,
			"transcript":      req.Transcript,
		}

		// Convert log data to JSON
		logJSON, err := json.Marshal(logData)
		if err != nil {
			log.Printf("Failed to marshal log data: %v", err)
		} else {
			// Send log data to webhook
			_, err = http.Post(webhookURL+"/chatbot-log", "application/json", bytes.NewBuffer(logJSON))
			if err != nil {
				log.Printf("Failed to send log data to webhook: %v", err)
			}
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"status":  "success",
		"message": "Conversation ended",
	})
}

// createWebCallHandler creates a web call token for browser-based calls
func createWebCallHandler(c *gin.Context) {
	var req WebCallRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	// Get phone number from environment or use default
	twilioPhoneNumber := os.Getenv("TWILIO_PHONE_NUMBER")
	if twilioPhoneNumber == "" {
		twilioPhoneNumber = "+19787185545" // Default to the provided number
	}

	// Use default agent ID if not provided
	if req.AgentID == "" {
		req.AgentID = os.Getenv("DEFAULT_AGENT_ID")
		if req.AgentID == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Agent ID is required but DEFAULT_AGENT_ID is not set in environment"})
			return
		}
	}

	// Check if we're in direct Twilio mode or using Retell API
	useTwilioDirect := os.Getenv("USE_TWILIO_DIRECT") == "true"

	if useTwilioDirect {
		// Initialize Twilio direct call
		c.JSON(http.StatusOK, gin.H{
			"call_mode":    "twilio_direct",
			"phone_number": twilioPhoneNumber,
			"message":      "Please call the Barbeque Nation assistant at " + twilioPhoneNumber,
		})
		return
	}

	// Set mode to "phone" for Retell-based web calls
	if req.Mode == "" {
		req.Mode = "phone"
	}

	// Add the phone number to context
	if req.Context == nil {
		req.Context = make(map[string]interface{})
	}
	req.Context["phone_number"] = twilioPhoneNumber

	// Return a mock response for testing if we're in development mode
	// or if API credentials are missing
	if retellAPIKey == "your_retell_api_key_here" || retellAPIKey == "" || len(retellAPIKey) < 20 {
		log.Println("Using mock web call token because API key is missing or placeholder")
		c.JSON(http.StatusOK, gin.H{
			"call_mode":    "twilio_via_retell",
			"access_token": "mock_access_token_for_testing",
			"expires_at":   time.Now().Add(30 * time.Minute).Format(time.RFC3339),
			"phone_number": twilioPhoneNumber,
			"agent_id":     req.AgentID,
		})
		return
	}

	// Convert request to JSON for Retell API
	reqJSON, err := json.Marshal(req)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to marshal request: " + err.Error()})
		return
	}

	// For debugging - log the request
	log.Printf("Sending web call request to %s with agent ID %s", retellBaseURL+"/create-web-call", req.AgentID)

	// Create HTTP request - use batchCall endpoint if createWebCall fails
	httpReq, err := http.NewRequest("POST", retellBaseURL+"/create-web-call", bytes.NewBuffer(reqJSON))
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create request: " + err.Error()})
		return
	}

	// Set headers
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", "Bearer "+retellAPIKey)

	// Send request
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		log.Printf("Error connecting to Retell API: %v, trying fallback to batch call", err)
		// Fall back to batch call if create-web-call fails
		batchCallResp, batchErr := tryBatchCallEndpoint(req)
		if batchErr != nil {
			// Fall back to direct phone number as last resort
			c.JSON(http.StatusOK, gin.H{
				"call_mode":    "twilio_direct_fallback",
				"phone_number": twilioPhoneNumber,
				"message":      "Please call the Barbeque Nation assistant at " + twilioPhoneNumber,
				"error":        "Could not get Retell token: " + err.Error() + ", " + batchErr.Error(),
			})
			return
		}

		// Return Retell batch call response with phone number
		c.JSON(http.StatusOK, gin.H{
			"call_mode":    "twilio_via_retell",
			"access_token": batchCallResp.AccessToken,
			"expires_at":   batchCallResp.ExpiresAt,
			"phone_number": twilioPhoneNumber,
			"agent_id":     req.AgentID,
		})
		return
	}
	defer resp.Body.Close()

	// Read response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read response: " + err.Error()})
		return
	}

	// Check status code
	if resp.StatusCode != http.StatusOK {
		// Log the error for debugging
		log.Printf("Retell API error: Status %d, Response: %s", resp.StatusCode, string(body))

		// Try batch call instead
		log.Printf("Trying fallback to batch call endpoint")
		batchCallResp, batchErr := tryBatchCallEndpoint(req)
		if batchErr != nil {
			// Fall back to direct phone number as last resort
			c.JSON(http.StatusOK, gin.H{
				"call_mode":    "twilio_direct_fallback",
				"phone_number": twilioPhoneNumber,
				"message":      "Please call the Barbeque Nation assistant at " + twilioPhoneNumber,
				"error":        "API error: " + http.StatusText(resp.StatusCode),
			})
			return
		}

		// Return Retell batch call response with phone number
		c.JSON(http.StatusOK, gin.H{
			"call_mode":    "twilio_via_retell",
			"access_token": batchCallResp.AccessToken,
			"expires_at":   batchCallResp.ExpiresAt,
			"phone_number": twilioPhoneNumber,
			"agent_id":     req.AgentID,
		})
		return
	}

	// Parse response
	var webCallResp WebCallResponse
	err = json.Unmarshal(body, &webCallResp)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to parse response: " + err.Error()})
		return
	}

	// Return response with phone number
	c.JSON(http.StatusOK, gin.H{
		"call_mode":    "twilio_via_retell",
		"access_token": webCallResp.AccessToken,
		"expires_at":   webCallResp.ExpiresAt,
		"phone_number": twilioPhoneNumber,
		"agent_id":     req.AgentID,
	})
}

// tryBatchCallEndpoint attempts to use the batchCall endpoint as a fallback
func tryBatchCallEndpoint(req WebCallRequest) (WebCallResponse, error) {
	// Create batch call request
	batchReq := map[string]interface{}{
		"agent_id": req.AgentID,
		"user_id":  req.UserID,
		"mode":     "browser",
	}

	if req.Context != nil {
		batchReq["context"] = req.Context
	}

	// Convert request to JSON
	reqJSON, err := json.Marshal(batchReq)
	if err != nil {
		return WebCallResponse{}, err
	}

	// Create HTTP request to batchCall endpoint
	httpReq, err := http.NewRequest("POST", "https://dashboard.retellai.com/api/batchCall", bytes.NewBuffer(reqJSON))
	if err != nil {
		return WebCallResponse{}, err
	}

	// Set headers
	httpReq.Header.Set("Content-Type", "application/json")
	httpReq.Header.Set("Authorization", "Bearer "+retellAPIKey)

	// Send request
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(httpReq)
	if err != nil {
		return WebCallResponse{}, err
	}
	defer resp.Body.Close()

	// Read response body
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return WebCallResponse{}, err
	}

	// Check status code
	if resp.StatusCode != http.StatusOK {
		return WebCallResponse{}, fmt.Errorf("batch call API error: %d - %s", resp.StatusCode, string(body))
	}

	// Parse response to get access token
	var batchResp struct {
		AccessToken string `json:"access_token"`
		ExpiresAt   string `json:"expires_at"`
	}

	err = json.Unmarshal(body, &batchResp)
	if err != nil {
		return WebCallResponse{}, err
	}

	// Return in the format needed for WebCallResponse
	return WebCallResponse{
		AccessToken: batchResp.AccessToken,
		ExpiresAt:   batchResp.ExpiresAt,
	}, nil
}

// stateFlowHandler handles requests for state-based conversation flow
func stateFlowHandler(c *gin.Context) {
	var req StateFlowRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request: " + err.Error()})
		return
	}

	// Initialize context if not provided
	if req.Context == nil {
		req.Context = make(map[string]interface{})
	}

	// Determine current state
	currentState := ConversationState(req.CurrentState)
	if currentState == "" {
		currentState = StateGreeting
	}

	// Process state based on current state and user message
	var nextState ConversationState
	var response string
	var finished bool

	switch currentState {
	case StateGreeting:
		nextState, response = handleGreetingState(req.Message, req.Context)
	case StateCity:
		nextState, response = handleCityState(req.Message, req.Context)
	case StateOutlet:
		nextState, response = handleOutletState(req.Message, req.Context)
	case StateReservation:
		nextState, response = handleReservationState(req.Message, req.Context)
	case StateContact:
		nextState, response = handleContactState(req.Message, req.Context)
	case StateConfirmation:
		nextState, response, finished = handleConfirmationState(req.Message, req.Context)
	case StateEnd:
		nextState = StateEnd
		response = "Thank you for booking with Barbeque Nation. We look forward to serving you. Is there anything else I can help you with?"
		finished = true
	default:
		nextState = StateGreeting
		response = "Welcome to Barbeque Nation. How may I assist you today?"
	}

	c.JSON(http.StatusOK, StateFlowResponse{
		NextState: string(nextState),
		Response:  response,
		Context:   req.Context,
		Finished:  finished,
	})
}

// handleGreetingState handles the greeting state
func handleGreetingState(message string, context map[string]interface{}) (ConversationState, string) {
	// Check if the message mentions booking or reservation
	if strings.Contains(strings.ToLower(message), "book") ||
		strings.Contains(strings.ToLower(message), "reserv") {
		// If booking is mentioned, ask for city
		return StateCity, "Great! I can help you with a reservation. Which city would you like to book in - Delhi or Bangalore?"
	}

	// Check if the message mentions inquiry or information
	if strings.Contains(strings.ToLower(message), "info") ||
		strings.Contains(strings.ToLower(message), "know") ||
		strings.Contains(strings.ToLower(message), "detail") ||
		strings.Contains(strings.ToLower(message), "tell") {
		// If inquiry is mentioned, ask for city
		return StateCity, "I'd be happy to provide information about our outlets. Which city are you interested in - Delhi or Bangalore?"
	}

	// Check if city is already mentioned in the message
	if strings.Contains(strings.ToLower(message), "delhi") {
		context["city"] = "delhi"
		return StateOutlet, "Great! We have several outlets in Delhi. Which one are you interested in? We have outlets in Connaught Place, Vasant Kunj, and Janakpuri."
	}

	if strings.Contains(strings.ToLower(message), "bangalore") ||
		strings.Contains(strings.ToLower(message), "bengaluru") {
		context["city"] = "bangalore"
		return StateOutlet, "Great! We have several outlets in Bangalore. Which one are you interested in? We have outlets in Indiranagar, JP Nagar, Electronic City, and Koramangala."
	}

	// Default response
	return StateCity, "Welcome to Barbeque Nation! I can help you with bookings or information about our outlets. Which city are you interested in - Delhi or Bangalore?"
}

// handleCityState handles the city selection state
func handleCityState(message string, context map[string]interface{}) (ConversationState, string) {
	// Check if the message contains city information
	if strings.Contains(strings.ToLower(message), "delhi") {
		context["city"] = "delhi"
		return StateOutlet, "We have several outlets in Delhi. Which one are you interested in? We have outlets in Connaught Place, Vasant Kunj, and Janakpuri."
	}

	if strings.Contains(strings.ToLower(message), "bangalore") ||
		strings.Contains(strings.ToLower(message), "bengaluru") {
		context["city"] = "bangalore"
		return StateOutlet, "We have several outlets in Bangalore. Which one are you interested in? We have outlets in Indiranagar, JP Nagar, Electronic City, and Koramangala."
	}

	// If no city is mentioned, ask again
	return StateCity, "I'm sorry, I didn't catch which city you're interested in. We have outlets in Delhi and Bangalore. Which city would you like to select?"
}

// handleOutletState handles the outlet selection state
func handleOutletState(message string, context map[string]interface{}) (ConversationState, string) {
	city, _ := context["city"].(string)

	// Check if the message contains outlet information
	var outlet string

	// For Delhi
	if city == "delhi" {
		if strings.Contains(strings.ToLower(message), "connaught") ||
			strings.Contains(strings.ToLower(message), "cp") {
			outlet = "connaught_place"
			context["outlet"] = outlet
			return StateReservation, "Great choice! Connaught Place outlet is very popular. When would you like to make your reservation? Please let me know the date and time."
		}

		if strings.Contains(strings.ToLower(message), "vasant") {
			outlet = "vasant_kunj"
			context["outlet"] = outlet
			return StateReservation, "Excellent! Vasant Kunj outlet has a modern ambiance. When would you like to make your reservation? Please let me know the date and time."
		}

		if strings.Contains(strings.ToLower(message), "janakpuri") {
			outlet = "janakpuri"
			context["outlet"] = outlet
			return StateReservation, "Perfect! Janakpuri outlet is located in Unity Mall. When would you like to make your reservation? Please let me know the date and time."
		}
	}

	// For Bangalore
	if city == "bangalore" {
		if strings.Contains(strings.ToLower(message), "indiranagar") {
			outlet = "indiranagar"
			context["outlet"] = outlet
			return StateReservation, "Great choice! Indiranagar outlet is one of our most popular. When would you like to make your reservation? Please let me know the date and time."
		}

		if strings.Contains(strings.ToLower(message), "jp") ||
			strings.Contains(strings.ToLower(message), "jayanagar") {
			outlet = "jp_nagar"
			context["outlet"] = outlet
			return StateReservation, "Excellent! JP Nagar outlet is located on the 3rd floor. When would you like to make your reservation? Please let me know the date and time."
		}

		if strings.Contains(strings.ToLower(message), "electronic") {
			outlet = "electronic_city"
			context["outlet"] = outlet
			return StateReservation, "Perfect! Electronic City outlet is convenient for IT professionals. When would you like to make your reservation? Please let me know the date and time."
		}

		if strings.Contains(strings.ToLower(message), "koramangala") {
			outlet = "koramangala"
			context["outlet"] = outlet
			return StateReservation, "Great choice! Koramangala outlet is very popular. When would you like to make your reservation? Please let me know the date and time."
		}
	}

	// If no outlet is mentioned, ask again
	if city == "delhi" {
		return StateOutlet, "I'm sorry, I didn't catch which outlet you're interested in. In Delhi, we have outlets in Connaught Place, Vasant Kunj, and Janakpuri. Which one would you like to select?"
	} else if city == "bangalore" {
		return StateOutlet, "I'm sorry, I didn't catch which outlet you're interested in. In Bangalore, we have outlets in Indiranagar, JP Nagar, Electronic City, and Koramangala. Which one would you like to select?"
	} else {
		return StateCity, "Let's start by selecting a city. We have outlets in Delhi and Bangalore. Which city would you prefer?"
	}
}

// handleReservationState handles the reservation state
func handleReservationState(message string, context map[string]interface{}) (ConversationState, string) {
	// Check if the message contains date and time information

	// Simple parsing - in a real system, you'd use NLP for better date/time extraction
	hasDate := strings.Contains(strings.ToLower(message), "today") ||
		strings.Contains(strings.ToLower(message), "tomorrow") ||
		strings.Contains(strings.ToLower(message), "monday") ||
		strings.Contains(strings.ToLower(message), "tuesday") ||
		strings.Contains(strings.ToLower(message), "wednesday") ||
		strings.Contains(strings.ToLower(message), "thursday") ||
		strings.Contains(strings.ToLower(message), "friday") ||
		strings.Contains(strings.ToLower(message), "saturday") ||
		strings.Contains(strings.ToLower(message), "sunday")

	hasTime := strings.Contains(message, ":") ||
		strings.Contains(strings.ToLower(message), "am") ||
		strings.Contains(strings.ToLower(message), "pm") ||
		strings.Contains(strings.ToLower(message), "noon") ||
		strings.Contains(strings.ToLower(message), "night") ||
		strings.Contains(strings.ToLower(message), "evening") ||
		strings.Contains(strings.ToLower(message), "lunch") ||
		strings.Contains(strings.ToLower(message), "dinner")

	hasNumber := strings.Contains(message, "1") ||
		strings.Contains(message, "2") ||
		strings.Contains(message, "3") ||
		strings.Contains(message, "4") ||
		strings.Contains(message, "5") ||
		strings.Contains(message, "6") ||
		strings.Contains(message, "7") ||
		strings.Contains(message, "8") ||
		strings.Contains(message, "9")

	// Store the reservation details in context
	context["reservation_text"] = message

	if hasDate && hasTime {
		// Also try to extract party size
		if hasNumber {
			// This is a very basic extraction - a real system would use NLP
			context["party_size"] = extractNumber(message)
		} else {
			// Ask for party size
			return StateContact, "How many people will be dining? Please provide your contact number as well so we can confirm your reservation."
		}
		return StateContact, "Great! Could you please provide your contact number so we can confirm your reservation?"
	}

	// If missing date or time, ask again
	return StateReservation, "I need both a date and time for your reservation. For example, 'tomorrow at 7:30 PM' or 'Friday at noon'. When would you like to visit?"
}

// handleContactState handles the contact information state
func handleContactState(message string, context map[string]interface{}) (ConversationState, string) {
	// Check if the message contains a phone number
	hasPhoneNumber := containsPhoneNumber(message)

	if hasPhoneNumber {
		// Store the contact information in context
		context["contact"] = message

		// Move to confirmation state
		return StateConfirmation, formatConfirmationMessage(context)
	}

	// If no phone number is provided, ask again
	return StateContact, "I need your contact number to confirm the reservation. Please provide a valid phone number."
}

// handleConfirmationState handles the confirmation state
func handleConfirmationState(message string, context map[string]interface{}) (ConversationState, string, bool) {
	// Check if the message is a confirmation
	if strings.Contains(strings.ToLower(message), "yes") ||
		strings.Contains(strings.ToLower(message), "confirm") ||
		strings.Contains(strings.ToLower(message), "correct") ||
		strings.Contains(strings.ToLower(message), "right") {

		// Process the booking (in a real system, this would call a booking API)
		context["booking_confirmed"] = true
		context["booking_reference"] = "BBQ" + generateBookingReference()

		return StateEnd, "Your reservation has been confirmed! Your booking reference is " +
			context["booking_reference"].(string) +
			". We look forward to serving you. Is there anything else I can help you with?", true
	}

	if strings.Contains(strings.ToLower(message), "no") ||
		strings.Contains(strings.ToLower(message), "change") ||
		strings.Contains(strings.ToLower(message), "wrong") ||
		strings.Contains(strings.ToLower(message), "incorrect") {

		// Ask which information to change
		return StateCity, "I'll help you update your reservation. Let's start over. Which city would you like to book in - Delhi or Bangalore?", false
	}

	// If the response is unclear, ask for confirmation again
	return StateConfirmation, "I didn't catch that. Could you please confirm if the reservation details are correct? " +
		formatConfirmationMessage(context), false
}

// Helper function to extract a number from text
func extractNumber(text string) int {
	// This is a simplified version - a real implementation would be more robust
	words := strings.Fields(text)
	for _, word := range words {
		// Clean up word
		word = strings.Trim(word, ",.:;!?")

		// Try to parse as number
		num, err := strconv.Atoi(word)
		if err == nil {
			return num
		}

		// Check for number words
		switch strings.ToLower(word) {
		case "one":
			return 1
		case "two":
			return 2
		case "three":
			return 3
		case "four":
			return 4
		case "five":
			return 5
		case "six":
			return 6
		case "seven":
			return 7
		case "eight":
			return 8
		case "nine":
			return 9
		case "ten":
			return 10
		}
	}

	// Default to 2 if no number is found
	return 2
}

// Helper function to check if text contains a phone number
func containsPhoneNumber(text string) bool {
	// This is a simplified check - a real implementation would use regex
	digits := 0
	for _, char := range text {
		if char >= '0' && char <= '9' {
			digits++
		}
	}

	// If the text has at least 10 digits, assume it contains a phone number
	return digits >= 10
}

// Helper function to format the confirmation message
func formatConfirmationMessage(context map[string]interface{}) string {
	city, _ := context["city"].(string)
	outlet, _ := context["outlet"].(string)
	reservation, _ := context["reservation_text"].(string)
	contact, _ := context["contact"].(string)

	// Format the outlet name for display
	outletDisplay := strings.ReplaceAll(outlet, "_", " ")

	return fmt.Sprintf("Please confirm your reservation details: %s outlet in %s, %s. Contact: %s. Is this correct?",
		strings.Title(outletDisplay),
		strings.Title(city),
		reservation,
		contact)
}

// Helper function to generate a booking reference
func generateBookingReference() string {
	// Generate a random 6-digit booking reference
	rand.Seed(time.Now().UnixNano())
	return fmt.Sprintf("%06d", rand.Intn(1000000))
}
