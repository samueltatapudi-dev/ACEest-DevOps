pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t aceest:${BUILD_NUMBER} .'
            }
        }
        stage('Push') {
            steps {
                sh 'docker tag aceest:${BUILD_NUMBER} samueltatapudi/aceest:${BUILD_NUMBER}'
                sh 'docker push samueltatapudi/aceest:${BUILD_NUMBER}'
            }
        }
        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/'
            }
        }
    }
}
