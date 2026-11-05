pipeline {

    agent any

    triggers {
        pollSCM('H/5 * * * *')
    }

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
        stage('Smoke Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'reqres-api-key', variable: 'REQRES_API_KEY')
                ]) {
                    sh '''
                        docker run --rm --ipc=host \
                        -e API_BASE_URL=https://jsonplaceholder.typicode.com \
                        -e REQRES_BASE_URL=https://reqres.in/api/ \
                        -e REQRES_API_KEY=$REQRES_API_KEY \
                        playwright-test-framework \
                        pytest -m smoke -v --browser chromium
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                withCredentials([
                    string(credentialsId: 'reqres-api-key', variable: 'REQRES_API_KEY')
                ]) {
                    sh '''
                        docker rm -f playwright-tests || true

                        docker run --name playwright-tests --ipc=host \
                        -e API_BASE_URL=https://jsonplaceholder.typicode.com \
                        -e REQRES_BASE_URL=https://reqres.in/api/ \
                        -e REQRES_API_KEY=$REQRES_API_KEY \
                        playwright-test-framework \
                        pytest -m regression -n auto \
                        --browser chromium \
                        --browser firefox \
                        --browser webkit
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                rm -rf test-results

                docker cp playwright-tests:/app/allure-results ./allure-results || true
                docker cp playwright-tests:/app/test-results ./test-results 2>/dev/null || true
                docker rm -f playwright-tests || true
            '''

            script {
                if (fileExists('test-results')) {
                    archiveArtifacts artifacts: 'test-results/**/*',
                                     allowEmptyArchive: true
                } else {
                    echo 'No Playwright failure artifacts to archive'
                }
            }

            allure([
                includeProperties: false,
                results: [[path: 'allure-results']]
            ])

            echo 'Pipeline finished'
        }
    }
}