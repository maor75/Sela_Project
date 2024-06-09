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
                  value: "edmon"
                - name: MONGO_INITDB_DATABASE
                  value: "mydb"
                - name: HOST
                  value: "localhost"
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "edmonp173/project_app"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Wait for MongoDB') {
            steps {
                container('maven') {
                    script {
                        def maxTries = 30
                        def waitTime = 10
                        for (int i = 0; i < maxTries; i++) {
                            def mongoRunning = sh(script: 'nc -z localhost 27017', returnStatus: true) == 0
                            if (mongoRunning) {
                                echo 'MongoDB is running!'
                                break
                            }
                            echo 'Waiting for MongoDB to start...'
                            sleep waitTime
                        }
                        if (!mongoRunning) {
                            error 'MongoDB did not start in time'
                        }
                    }
                }
            }
        }

        stage('maven version') {
            steps {
                container('maven') {
                    sh 'mvn -version'
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
                        withDockerRegistry(credentialsId: 'dockerhub') {
                            // Build and Push Maven Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:react1 ./test1"
                            sh "docker push ${DOCKER_IMAGE}:react1"

                            // Build and Push FastAPI Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:backend ./fast_api"
                            sh "docker push ${DOCKER_IMAGE}:backend"
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
                     to: 'edmonp173@gmail.com'
        }
    }
}
