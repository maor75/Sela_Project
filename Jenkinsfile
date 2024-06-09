pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: maven
                image: maven:alpine
                command:
                - cat
                tty: true
              - name: mongodb
                image: mongo:latest
                env:
                - name: MONGO_INITDB_ROOT_USERNAME
                  value: "root"
                - name: MONGO_INITDB_ROOT_PASSWORD
                  value: "maor"
                - name: MONGO_INITDB_DATABASE
                  value: "mydb"
                - name: HOST
                  value: "localhost"
              - name: python
                image: python:3.11-alpine
                command:
                - cat
                tty: true
            '''
        }
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Test FastAPI') {
            steps {
                container('python') {
                    sh '''
                    pip install pytest httpx
                    pytest ./fast_api/tests
                    '''
                }
            }
        }
        stage('Build and Push Docker Images') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        withDockerRegistry(credentialsId: 'docker-hub') {
                            // Build and Push React Docker image
                            sh "docker build -t maoravidan/projectapp:react${env.BUILD_NUMBER} ./test1"
                            sh "docker push maoravidan/projectapp:react${env.BUILD_NUMBER}"

                            // Build and Push FastAPI Docker image
                            sh "docker build -t maoravidan/projectapp:fastapi${env.BUILD_NUMBER} ./fast_api"
                            sh "docker push maoravidan/projectapp:fastapi${env.BUILD_NUMBER}"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline post'
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            emailext body: 'The build failed. Please check the build logs for details.',
                     subject: "Build failed: ${env.BUILD_NUMBER}",
                     to: 'avidanos75@gmail.com'
        }
    }
}
