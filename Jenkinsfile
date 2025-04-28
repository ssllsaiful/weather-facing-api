// pipeline {
//     agent any

//     parameters {
//         string(name: 'DOCKER_IMAGE_VERSION', defaultValue: 'v0.0', description: 'Specify the Docker image version')
//     }

//     stages {
//         stage('Checkout') {
//             steps {
//                 script {
//                     echo "Checking out the latest code from GitHub..."
//                     git branch: 'main', url: 'https://github.com/ssllsaiful/weather-facing-api.git'
//                 }
//             }
//         }

//         stage('Build and Push Docker Image') {
//             steps {
//                 script {
//                     def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"

//                     echo "Building Docker image: ${dockerImageName}..."
//                     sh """
//                         docker build -t ${dockerImageName} .
//                     """
//                 }
//             }
//         }

//         stage('Deploy') {
//             steps {
//                 script {
//                     def dockerImageName = "weatherproject:${params.DOCKER_IMAGE_VERSION}"
//                     def composeFile = "/home/ubuntu/websites/weatherproject/docker-compose.yml"
                    
//                     echo "Tagging the built image as 'latest'..."
//                     sh "docker tag ${dockerImageName} weatherproject:latest"

//                     echo "Deploying using Docker Compose..."
//                     sh "docker compose -f ${composeFile} up -d"

//                     currentBuild.description = "Deployed version: ${dockerImageName}"
//                 }
//             }
//         }
//     }
// }



pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'ssllsaiful'
        DOCKERHUB_REPO = 'weatherproject'
        DOCKERHUB_PASSWORD = 'saiful1234'
        COMPOSE_FILE_PATH = '/home/ubuntu/websites/weatherproject/docker-compose.yml'
    }

    parameters {
        string(name: 'DOCKER_IMAGE_VERSION', defaultValue: '1.0.0', description: 'Specify the Docker image version (release tag)')
    }

    stages {

        stage('Checkout Code') {
            steps {
                script {
                    echo "Checking out code from GitHub..."
                    git branch: 'main', url: 'https://github.com/ssllsaiful/weather-facing-api.git'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${params.DOCKER_IMAGE_VERSION}"
                    echo "Building Docker image: ${imageTag}"

                    sh """
                        docker build --build-arg APP_VERSION=${params.DOCKER_IMAGE_VERSION} -t ${imageTag} .
                    """
                }
            }
        }

        stage('Push to DockerHub (Mocked)') {
            steps {
                script {
                    def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${params.DOCKER_IMAGE_VERSION}"

                    echo "Login to DockerHub (Mock)"
                    echo "docker login -u ${DOCKERHUB_USER} -p ${DOCKERHUB_PASSWORD}"

                    echo "Pushing Docker image to DockerHub (Mock): ${imageTag}"
                    echo "docker push ${imageTag}"
                }
            }
        }

        stage('Deploy with Docker Compose') {
            steps {
                script {
                    echo "Deploying with Docker Compose..."
                    sh """
                        docker compose -f ${COMPOSE_FILE_PATH} up -d
                    """
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo "Waiting 10 seconds for service to start..."
                    sleep(time:10, unit:"SECONDS")

                    echo "Checking if API is returning correct version..."
                    sh """
                        curl --fail http://weather.ideahubbd.com/api/hello | grep ${params.DOCKER_IMAGE_VERSION}
                    """
                }
            }
        }
    }
}
