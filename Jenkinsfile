pipeline {
    agent any

    environment {
        // Load your Alpha Vantage API key from Jenkins credentials
        ALPHA_VANTAGE_API_KEY = credentials('API_KEY-jk')
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo '📥 Pulling latest Stock Market App code from GitHub...'
                git credentialsId: 'github-token', url: 'https://github.com/rakshanda/Stock-Market-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image for Stock Market App...'
                sh 'docker build -t stock-market-app:latest .'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo '🚀 Running Stock Market App container...'
                script {
                    // Remove old container if it exists
                    def containerId = sh(script: "docker ps -aq -f name=stock-market-container", returnStdout: true).trim()
                    if (containerId) {
                        echo '🧹 Removing existing container...'
                        sh "docker rm -f stock-market-container"
                    }

                    // Run new container with the API key as environment variable
                    echo '🟢 Starting new Stock Market App container on port 5000...'
                    sh """
                        docker run -d --name stock-market-container -p 5000:5000 \
                        -e ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY} \
                        stock-market-app:latest
                    """
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo '🔍 Verifying if container is running properly...'
                sh 'docker ps | grep stock-market-container'
            }
        }
    }

    post {
        success {
            echo '✅ Stock Market App deployed successfully!'
            sh 'docker images'
            sh 'docker ps -a'
        }
        failure {
            echo '❌ Deployment failed. Check logs above.'
        }
    }
}
