stage('Build') {
    steps {
        script {
            if (fileExists('autogen.sh')) {
                sh './autogen.sh && ./configure && make'
            } else {
                echo 'No build script found'
            }
        }
    }
}
