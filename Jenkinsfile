// Jenkinsfile

pipeline {
    agent any

    environment {
        // Replace 'your-dockerhub-username' with your actual Docker Hub username.
        DOCKER_IMAGE = "your-dockerhub-username/flask-app:${env.BUILD_NUMBER}"
        // This MUST match the ID of your Docker Hub credentials in Jenkins.
        DOCKER_REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/AC-Gitenvir/CI-CD-Pipelining.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image ${DOCKER_IMAGE}..."
                    sh "docker build -t ${DOCKER_IMAGE} ."
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    echo "Running unit tests inside the Docker container..."
                    sh "docker run --rm ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Push Docker Image') {
            // This stage will now run every time, without a conditional.
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_REGISTRY_CREDENTIALS, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \"$DOCKER_PASSWORD\" | docker login -u \"$DOCKER_USERNAME\" --password-stdin"
                    }
                    echo "Pushing Docker image to registry..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy (Manual Trigger)') {
            // This stage will now run every time, without a conditional.
            steps {
                input message: 'Proceed with deployment to your RHEL 9 machine?', ok: 'Deploy'
                script {
                    echo "Attempting to deploy ${DOCKER_IMAGE}..."
                    sh "docker stop flask_app_prod || true"
                    sh "docker rm flask_app_prod || true"
                    sh "docker run -d -p 5000:5000 --name flask_app_prod --entrypoint python3 ${DOCKER_IMAGE} app.py"
                    echo "Application deployed. Access at http://YOUR_RHEL_IP_ADDRESS:5000"
                }
            }
            post {
                success {
                    echo 'Deployment successful!'
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline finished."
        }
        success {
            echo "Pipeline executed successfully!"
        }
        failure {
            echo "Pipeline failed! Check logs for details."
        }
    }
}