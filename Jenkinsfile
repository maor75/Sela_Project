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
                ports:
                - containerPort: 27017
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
            '''
        }
    }

    environment {
        DOCKER_IMAGE = "maoravidan/projectapp"
        MONGO_HOST = "mongodb"
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

        stage('Build Docker Images') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        sh "docker build -t ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER} ./fast_api"
                        sh "docker build -t ${DOCKER_IMAGE}:react${env.BUILD_NUMBER} ./test1"
                    }
                }
            }
        }

        stage('Run FastAPI Tests') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Ensure pytest can locate tests
                        sh "docker run --network host --rm -v \$(pwd)/fast_api:/app -w /app ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER} pytest --junitxml=test-results.xml --maxfail=1 --disable-warnings"
                    }
                }
            }
            post {
                always {
                    // Archive test results
                    junit 'fast_api/test-results.xml'
                }
                failure {
                    script {
                        currentBuild.result = 'FAILURE'
                    }
                }
            }
        }

        stage('Push Docker Images') {
            when {
                branch 'main'
            }
            steps {
                container('ez-docker-helm-build') {
                    script {
                        withDockerRegistry(credentialsId: 'docker-hub') {
                            sh "docker push ${DOCKER_IMAGE}:fastapi${env.BUILD_NUMBER}"
                            sh "docker push ${DOCKER_IMAGE}:react${env.BUILD_NUMBER}"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline post'
            script {
                sh 'rm -rf *' // Alternative cleanup if cleanWs is not available
            }
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            emailext body: 'The build failed. Please check the build logs for details.',
                     subject: "Build failed: ${env.BUILD_NUMBER}",
                     to: 'avidanos75@gmail.com',
                     attachLog: true,
                     compressLog: true
        }
    }
}
