pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Kingill/ckpool.git'
            }
        }

        stage('Build') {
            steps {
                sh 'echo "Build step (customize me)"'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Test step (customize me)"'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
        }
    }
}
