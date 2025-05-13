package main

import (
	"log"
	"os"
	"path/filepath"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	// Load .env file if it exists
	err := godotenv.Load()
	if err != nil {
		log.Println("Warning: .env file not found, using environment variables")
	}

	// Create Gin router
	router := gin.Default()

	// Set up CORS
	router.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		AllowCredentials: true,
	}))

	// Static files
	router.Static("/static", "./chatbot/static")

	// API routes
	api := router.Group("/api")
	{
		// Register chatbot routes directly (since we're in the same package now)
		RegisterRoutes(api)
	}

	// Root route redirects to static index.html
	router.GET("/", func(c *gin.Context) {
		c.Redirect(302, "/static/index.html")
	})

	// Get port from environment variable or use default
	port := os.Getenv("GO_PORT")
	if port == "" {
		port = "8080"
	}

	// Start server
	log.Printf("Starting server on port %s", port)
	router.Run(":" + port)
}

// createStaticDir creates the static directory structure if it doesn't exist
func createStaticDir() {
	// Path to static directories
	paths := []string{
		"./chatbot/static",
		"./chatbot/static/css",
		"./chatbot/static/js",
		"./chatbot/static/img",
	}

	// Create each directory
	for _, path := range paths {
		if _, err := os.Stat(path); os.IsNotExist(err) {
			os.MkdirAll(path, os.ModePerm)
		}
	}

	// Create placeholder logo image if it doesn't exist
	logoPath := filepath.Join("./chatbot/static/img", "bbq-logo.png")
	if _, err := os.Stat(logoPath); os.IsNotExist(err) {
		// This would typically be a real logo, but for demo purposes
		// we'll just create an empty file as a placeholder
		file, err := os.Create(logoPath)
		if err != nil {
			log.Printf("Warning: Could not create placeholder logo: %v", err)
		}
		file.Close()
	}
}
