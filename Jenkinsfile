pipeline {
    agent any
    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Kingill/ckpool.git', branch: 'main'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'sudo apt-get update && sudo apt-get install -y build-essential yasm autoconf automake libtool'
            }
    }
}
