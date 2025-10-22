pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Pulling latest Stock Market App code from GitHub..."
                git credentialsId: 'github-token', branch: 'main', url: 'https://github.com/rakshanda/Stock-Market-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image for Stock Market App..."
                sh 'docker build -t stock-market-app:latest ./app'
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "🚀 Running Stock Market App container..."
                script {
                    // Clean up existing container if it exists
                    sh '''
                        if [ "$(docker ps -aq -f name=stock-market-container)" ]; then
                            echo "🧹 Removing existing container..."
                            docker rm -f stock-market-container
                        fi
                    '''

                    // Start new container with port mapping
                    sh '''
                        echo "🟢 Starting new Stock Market App container on port 5000..."
                        docker run -d --name stock-market-container -p 5000:5000 stock-market-app:latest
                    '''
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                echo "🔍 Verifying if container is running properly..."
                sh '''
                    docker ps | grep stock-market-container || (echo "❌ Container not running!" && exit 1)
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Stock Market App deployed successfully!"
            sh 'docker images'
            sh 'docker ps -a'
        }
        failure {
            echo "❌ Deployment failed. Please check Jenkins logs."
            sh 'docker ps -a'
        }
    }
}
