pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                git url: 'https://github.com/Kingill/ckpool.git', branch: 'main', credentialsId: 'github-pat-ckpool'
                sh 'ls'
            }
        }
    }
}
