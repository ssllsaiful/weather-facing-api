pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE_VERSION', defaultValue: 'v0.0', description: 'Specify the Docker image version')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo "Checking out the latest code from GitHub..."
                    git branch: 'main', url: 'https://github.com/ssllsaiful/weather-facing-api.git'
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"

                    echo "Building Docker image: ${dockerImageName}..."
                    sh """
                        docker build -t ${dockerImageName} .
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"
                    def composeFile = "/home/ubuntu/websites/weatherproject/docker-compose.yml"
                    
                    echo "Tagging the built image as 'latest'..."
                    sh "docker tag ${dockerImageName} weatherproject:latest"

                    echo "Deploying using Docker Compose..."
                    sh "docker compose -f ${composeFile} up -d"

                    currentBuild.description = "Deployed version: ${dockerImageName}"
                }
            }
        }
    }
}
