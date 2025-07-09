pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git url: 'https://github.com/hoangnhobe/Web.git', branch: 'main'

            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }
}
