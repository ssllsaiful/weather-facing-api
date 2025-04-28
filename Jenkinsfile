
pipeline {
    agent any

    environment {
        DOCKERHUB_USER = 'ssllsaiful'
        DOCKERHUB_REPO = 'weatherproject'
        DOCKERHUB_PASSWORD = 'saiful1234'
        COMPOSE_FILE_PATH = '/home/ubuntu/websites/weatherproject/docker-compose.yml'
    }

    stages {

        stage('Checkout Code') {
            steps {
                script {
                    echo "Checking out code from GitHub..."
                    git branch: 'main', url: 'https://github.com/ssllsaiful/weather-fetch-api.git'
                    sh """
                        git fetch --tags --force --prune
                    """
                }
            }
        }


        stage('Get Latest Git Tag') {
            steps {
                script {
                    echo "Fetching latest Git Tag..."
                    sh "git fetch --tags"
                    env.DOCKER_IMAGE_VERSION = sh(script: "git tag --sort=-creatordate | head -n 1", returnStdout: true).trim()
                    echo "Detected Latest Release Tag: ${env.DOCKER_IMAGE_VERSION}"
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${env.DOCKER_IMAGE_VERSION}"
                    echo "Building Docker image: ${imageTag}"
                    sh """
                        docker build -t ${imageTag} .
                    """
                }
            }
        }

        // stage('Push to DockerHub') {
        //     steps {
        //         script {
        //             def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${env.DOCKER_IMAGE_VERSION}"
        //             sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USER} --password-stdin"
        //             sh "docker push ${imageTag}"
        //         }
        //     }
        // }


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

        stage('Version Check') {
            steps {
                script {
                    echo "Waiting 10 seconds for service to start..."
                    sleep(time:10, unit:"SECONDS")

                    echo "Checking if API is returning correct version..."

                    def response = sh(script: "curl --fail https://weather.ideahubbd.com/api/hello", returnStdout: true).trim()
                    echo "API Response: ${response}"

                    def version = sh(script: "echo '${response}' | jq -r '.version'", returnStdout: true).trim()

                    if (version != env.DOCKER_IMAGE_VERSION) {
                        error "Version check : version mismatch (expected: ${env.DOCKER_IMAGE_VERSION}, found: ${version})"
                    }
                }
                script {
                    currentBuild.description = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${env.DOCKER_IMAGE_VERSION}"
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

