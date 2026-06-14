// Jenkins declarative pipeline for the CI/CD mini project.
// Each stage maps to something you would otherwise do by hand:
//   Checkout     -> git clone / git pull
//   Build        -> create a virtualenv and install dependencies
//   Test         -> run the unit tests
//   Docker Build -> package the app into a Docker image
//
// The whole point of CI/CD is that Jenkins does these steps for you,
// automatically and identically, every time code changes.

pipeline {
    agent any

    environment {
        IMAGE_NAME = 'cicd-mini-project'
        IMAGE_TAG  = "${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Stage 1: Getting the source code'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Stage 2: Installing dependencies into a virtualenv'
                dir('app') {
                    sh '''
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Stage 3: Running the unit tests'
                dir('app') {
                    sh '''
                        . venv/bin/activate
                        pytest -v --junitxml=test-results.xml
                    '''
                }
            }
            post {
                always {
                    // Publishes the test report in the Jenkins UI.
                    // Requires the JUnit plugin (included in the suggested plugins).
                    junit 'app/test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Stage 4: Building the Docker image'
                dir('app') {
                    sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
                }
                sh 'docker images | grep ${IMAGE_NAME}'
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded. Built image ${IMAGE_NAME}:${IMAGE_TAG}"
        }
        failure {
            echo 'Pipeline failed. Scroll up and read the first red error in the log.'
        }
        always {
            echo 'Pipeline finished.'
        }
    }
}
