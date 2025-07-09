pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/hoangnhobe/Web.git'
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
