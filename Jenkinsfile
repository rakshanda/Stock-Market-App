pipeline {
    agent any

    environment {
        IMAGE_NAME = "stock-market-tracker"
        CONTAINER_NAME = "stock-tracker-container"
        AWS_REGION = "us-east-1"
        TF_DIR = "terraform"
        ANSIBLE_DIR = "ansible"
        APP_DIR = "app"
        MONITORING_DIR = "monitoring"
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Cloning repository..."
                git branch: 'main', url: 'https://github.com/rakshanda/Stock-Market-App.git'
            }
        }

        stage('Provision Infrastructure with Terraform') {
            steps {
                echo "🏗️ Provisioning AWS infrastructure..."
                dir("${TF_DIR}") {
                    sh '''
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "🐳 Building Docker image for the application..."
                dir("${APP_DIR}") {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Configure and Deploy with Ansible') {
            steps {
                echo "⚙️ Configuring EC2 instance and deploying app using Ansible..."
                dir("${ANSIBLE_DIR}") {
                    sh '''
                        ansible-playbook -i inventory.ini playbook.yml
                    '''
                }
            }
        }

        stage('Start Monitoring Stack') {
            steps {
                echo "📊 Deploying Prometheus and Grafana..."
                dir("${MONITORING_DIR}") {
                    // Assume Docker Compose is used for monitoring stack
                    sh 'docker-compose up -d'
                }
            }
        }

    }

    post {
        success {
            echo "✅ Deployment completed successfully!"
            sh 'docker images'
            sh 'docker ps -a'
        }
        failure {
            echo "❌ Deployment failed. Please check logs."
            sh 'docker ps -a || true'
        }
    }
}
