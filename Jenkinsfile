
// pipeline {
//     agent any

//     environment {
//         DOCKERHUB_USER = 'ssllsaiful'
//         DOCKERHUB_REPO = 'weatherproject'
//         DOCKERHUB_PASSWORD = 'saiful1234'
//         COMPOSE_FILE_PATH = '/home/ubuntu/websites/weatherproject/docker-compose.yml'
//     }

//     parameters {
//         string(name: 'DOCKER_IMAGE_VERSION', defaultValue: '1.0.0', description: 'Specify the Docker image version (release tag)')
//     }

//     stages {

//         stage('Checkout Code') {
//             steps {
//                 script {
//                     echo "Checking out code from GitHub..."
//                     git branch: 'main', url: 'https://github.com/ssllsaiful/weather-fetch-api.git'
//                 }
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 script {
//                     def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${params.DOCKER_IMAGE_VERSION}"
//                     echo "Building Docker image: ${imageTag}"

//                     sh """
//                         docker build -t ${imageTag} .
//                     """
//                 }
//             }
//         }

//         stage('Push to DockerHub') {
//             steps {
//                 script {
//                     def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${params.DOCKER_IMAGE_VERSION}"

//                     // Actual Docker login (instead of echo)
//                     echo "Logging in to DockerHub..."
//                     sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USER} --password-stdin"

//                     echo "Pushing Docker image to DockerHub: ${imageTag}"
//                     sh "docker push ${imageTag}"
//                 }
//             }
//         }

//         stage('Deploy with Docker Compose') {
//             steps {
//                 script {
//                     echo "Deploying with Docker Compose..."
//                     sh """
//                         docker compose -f ${COMPOSE_FILE_PATH} up -d
//                     """
//                 }
//             }
//         }

//         stage('Health Check') {
//             steps {
//                 script {
//                     echo "Waiting 10 seconds for service to start..."
//                     sleep(time:10, unit:"SECONDS")

//                     echo "Checking if API is returning correct version..."


//                     def response = sh(script: "curl --fail https://weather.ideahubbd.com/api/hello", returnStdout: true).trim()
//                     echo "API Response: ${response}"

//                     def version = sh(script: "echo '${response}' | jq -r '.version'", returnStdout: true).trim()

//                     if (version != "${params.DOCKER_IMAGE_VERSION}") {
//                         error "Health check failed: version mismatch (expected: ${params.DOCKER_IMAGE_VERSION}, found: ${version})"
//                     }
//                 }
//             }
//         }
//     }

//     post {
//         failure {
//             echo "Build or Deployment failed!"
//         }
//         success {
//             echo "Deployment Successful!"
//         }
//     }
// }




// stage('Push to DockerHub') {
//     steps {
//         script {
//             def imageTag = "${DOCKERHUB_USER}/${DOCKERHUB_REPO}:${env.DOCKER_IMAGE_VERSION}"
//             sh "echo ${DOCKERHUB_PASSWORD} | docker login -u ${DOCKERHUB_USER} --password-stdin"
//             sh "docker push ${imageTag}"
//         }
//     }
// }


/////////////////

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
                    //test -push my test
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

                    if (version != env.DOCKER_IMAGE_VERSION) {
                        error "Health check failed: version mismatch (expected: ${env.DOCKER_IMAGE_VERSION}, found: ${version})"
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

//
