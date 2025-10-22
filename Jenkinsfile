pipeline {
    agent any

    environment {
        # 🔑 Inject your Alpha Vantage API key here (or use Jenkins credentials)
        ALPHA_VANTAGE_API_KEY = 'KNV8I6IPKC1LQ6YO'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "📥 Pulling latest Stock Market App code from GitHub..."
                git branch: 'main', url: 'https://github.com/rakshanda/Stock-Market-App.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image for Stock Market App..."
                sh '''
                    docker build -t stock-market-app:latest .
                '''
            }
        }

        stage('Cleanup Old Containers/Images') {
            steps {
                echo "🧹 Cleaning up old containers and images..."
                sh '''
                    if [ "$(docker ps -aq -f name=stock-market-container)" ]; then
                        docker rm -f stock-market-container
                    fi
                    docker image prune -f
                '''
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "🚀 Running Stock Market App container..."
                sh '''
                    echo "🟢 Starting container on port 5000..."
                    docker run -d \
                        --name stock-market-container \
                        -p 5000:5000 \
                        -e ALPHA_VANTAGE_API_KEY=${ALPHA_VANTAGE_API_KEY} \
                        stock-market-app:latest
                '''
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
