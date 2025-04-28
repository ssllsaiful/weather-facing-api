
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

        stage('Get Release Version') {
            steps {
                script {
                    echo "Extracting release tag from webhook payload..."
                    
                    def payload = readJSON text: env.GITHUB_EVENT_PAYLOAD
                    def releaseTag = payload.release.tag_name
                    
                    if (!releaseTag) {
                        error "No release tag found in payload!"
                    }
                    
                    env.DOCKER_IMAGE_VERSION = releaseTag
                    echo "Detected Release Tag: ${env.DOCKER_IMAGE_VERSION}"
                }
            }
        }

        stage('Checkout Code') {
            steps {
                script {
                    echo "Checking out code from GitHub..."
                    git branch: 'main', url: 'https://github.com/ssllsaiful/weather-fetch-api.git'
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
