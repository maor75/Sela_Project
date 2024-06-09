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
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
              - name: node
                image: node:alpine
                command:
                - cat
                tty: true
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "maoravidan/projectapp"
    }
    
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Maven Version') {
            steps {
                container('maven') {
                    sh 'mvn -version'
                }
            }
        }
        stage('Test FastAPI') {
            steps {
                container('maven') {
                    // Ensure pytest is installed if not already in the container image
                    sh 'pip install pytest httpx'
                    // Run FastAPI tests
                    sh 'pytest ./fast_api/tests'
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
                            sh "docker build -t ${DOCKER_IMAGE}:react${env.BUILD_NUMBER} ./test1"
                            sh "docker push ${DOCKER_IMAGE}:react${env.BUILD_NUMBER}"

                            // Build and Push FastAPI Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER} ./fast_api"
                            sh "docker push ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER}"
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
}
