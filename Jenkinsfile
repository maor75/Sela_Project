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
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
              - name: tester
                image: curlimages/curl:latest
                command:
                - cat
                tty: true
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "maoravidan/projectapp"
        MONGO_URI = "mongodb://root:maor@localhost:27017/mydb"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
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

        stage('Start MongoDB') {
            steps {
                container('mongodb') {
                    script {
                        // Wait for MongoDB to be ready
                        def retries = 90
                        while (retries > 0) {
                            try {
                                sh '''
                                mongo --username root --password maor --eval "db.stats()"
                                '''
                                break
                            } catch (Exception e) {
                                echo 'Waiting for MongoDB to be ready...'
                                sleep 5
                                retries--
                            }
                        }
                        if (retries == 0) {
                            error 'MongoDB did not start in time'
                        }
                    }
                }
            }
        }

        stage('Deploy API and Run Tests') {
            steps {
                container('tester') {
                    script {
                        // Deploy API container
                        sh '''
                        docker run -d -p 8000:8000 --name fastapi_container ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER}
                        '''

                        // Wait for API to be ready
                        def retries = 60
                        while (retries > 0) {
                            try {
                                sh '''
                                curl -s -o /dev/null http://localhost:8000
                                '''
                                break
                            } catch (Exception e) {
                                echo 'Waiting for API to be ready...'
                                sleep 5
                                retries--
                            }
                        }
                        if (retries == 0) {
                            error 'API did not start in time'
                        }

                        // Check if the API root endpoint is accessible
                        sh '''
                        echo "Testing root endpoint"
                        STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/)
                        if [ $STATUS_CODE -ne 200 ]; then
                            echo "Root endpoint failed with status code: $STATUS_CODE"
                            exit 1
                        fi
                        '''
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
