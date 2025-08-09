// Jenkinsfile

pipeline {
    agent any

    environment {
        // Replace 'ayush0077' with your actual Docker Hub username.
        DOCKER_IMAGE = "your-dockerhub-username/flask-app:${env.BUILD_NUMBER}"
        // This MUST match the ID of your Docker Hub credentials in Jenkins.
        DOCKER_REGISTRY_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {
        stage('Checkout') {
            steps {
                // Clones the repository to the Jenkins agent workspace.
                // This is automatically handled by the "Pipeline script from SCM" setting.
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
                    // Your Dockerfile's ENTRYPOINT is set to 'pytest test.py',
                    // so running the container executes the tests.
                    sh "docker run --rm ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Push Docker Image') {
            when {
                branch 'main' // Only push if changes are on the main branch
            }
            steps {
                script {
                    // Login to Docker Hub using stored Jenkins credentials
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_REGISTRY_CREDENTIALS, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \"$DOCKER_PASSWORD\" | docker login -u \"$DOCKER_USERNAME\" --password-stdin"
                    }
                    // Push the Docker image to the registry
                    echo "Pushing Docker image to registry..."
                    sh "docker push ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Deploy (Manual Trigger)') {
            // This stage demonstrates a manual deployment step.
            when {
                expression { env.BRANCH_NAME == 'main' }
            }
            steps {
                input message: 'Proceed with deployment to your RHEL 9 machine?', ok: 'Deploy'
                script {
                    echo "Attempting to deploy ${DOCKER_IMAGE}..."
                    // Stop any existing instance of the app (if any)
                    sh "docker stop flask_app_prod || true"
                    sh "docker rm flask_app_prod || true"
                    // Run the Flask application container, overriding the Dockerfile's ENTRYPOINT
                    sh "docker run -d -p 5000:5000 --name flask_app_prod --entrypoint python3 ${DOCKER_IMAGE} app.py"
                    echo "Application deployed. Access at http://192.168.29.134:5000"
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