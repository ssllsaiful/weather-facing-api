pipeline {
    agent any

    parameters {
        string(name: 'DOCKER_IMAGE_VERSION', defaultValue: 'V0.0', description: 'Specify the Docker image version')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    git branch: 'main', url: 'https://github.com/ssllsaiful/weather-facing-api.git'
                    // check out the branch last update
                }
            }
        }

        stage('Build and Push Docker Image') {
            steps {
                script {
                    def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"
                    sh "docker build -t ${dockerImageName} -f /home/ubuntu/websites/weatherproject/Dockerfile ."

                }
            }
        }


        stage('Deploy') {
            steps {
                script {
                    def composeFile = "/home/ubuntu/websites/weatherproject/docker-compose.yml"
                    def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"
                    sh """
                    docker tag ${s} weatherproject:latest
                    docker compose -f ${composeFile} up -d
                    """
                    currentBuild.description = "${dockerImageName}"
                 }
            }
         }
        
    }
}



