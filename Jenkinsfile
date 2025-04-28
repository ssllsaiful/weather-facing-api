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
                        docker build -t ${imageTag} .
                    """
                }
            }
        }

        stage('Push to DockerHub') {
            steps {
                script {
                    def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${params.DOCKER_IMAGE_VERSION}"

                    // Actual Docker login (instead of echo)
                    echo "Logging in to DockerHub..."
                    sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USER} --password-stdin"

                    echo "Pushing Docker image to DockerHub: ${imageTag}"
                    sh "docker push ${imageTag}"
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


                    def response = sh(script: "curl --fail https://weather.ideahubbd.com/api/hello", returnStdout: true).trim()
                    echo "API Response: ${response}"

                    def version = sh(script: "echo '${response}' | jq -r '.version'", returnStdout: true).trim()

                    if (version != "${params.DOCKER_IMAGE_VERSION}") {
                        error "Health check failed: version mismatch (expected: ${params.DOCKER_IMAGE_VERSION}, found: ${version})"
                    }
                }
            }
        }
    }

    post {
        failure {
            echo "Build or Deployment failed!"
        }
        success {
            echo "Deployment Successful!"
        }
    }
}
