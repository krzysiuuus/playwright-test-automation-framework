pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t playwright-test-framework .'
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker run --rm --ipc=host \
                    playwright-test-framework \
                    pytest -n auto \
                    --browser chromium \
                    --browser firefox \
                    --browser webkit
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}