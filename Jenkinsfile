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
                    docker rm -f playwright-tests || true

                    docker run --name playwright-tests --ipc=host \
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
            sh '''
                docker cp playwright-tests:/app/allure-results ./allure-results || true
                docker cp playwright-tests:/app/test-results ./test-results || true
                docker rm -f playwright-tests || true
            '''

            archiveArtifacts artifacts: 'test-results/**/*',
                             allowEmptyArchive: true

            allure([
                includeProperties: false,
                results: [[path: 'allure-results']]
            ])

            echo 'Pipeline finished'
        }
    }
}