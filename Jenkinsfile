pipeline {
    options {
        // Add pipeline options here
    }
    
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
                script {
                    // Build and Push React Docker image
                    def reactTag = "maoravidan/projectapp:react-${env.BUILD_NUMBER}"
                    sh "docker build -t $reactTag ./test1"
                    sh "docker push $reactTag"

                    // Build and Push FastAPI Docker image
                    def fastapiTag = "maoravidan/projectapp:fastapi-${env.BUILD_NUMBER}"
                    sh "docker build -t $fastapiTag ./fast_api"
                    sh "docker push $fastapiTag"
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline post'
            cleanWs() // Cleanup Stage
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            notifyBuild('The build failed. Please check the build logs for details.')
        }
    }
}
