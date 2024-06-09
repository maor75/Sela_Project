pipeline {
    agent {
        kubernetes {
            yaml '''
            apiVersion: v1
            kind: Pod
            spec:
              containers:
              - name: dind
                image: docker:20.10.9
                command: ["dockerd", "--host=unix:///var/run/docker.sock"]
                securityContext:
                  privileged: true
                volumeMounts:
                - name: docker-socket
                  mountPath: /var/run/docker.sock
              - name: maven
                image: maven:alpine
                command:
                - cat
                tty: true
              - name: python
                image: python:3.9-alpine
                command:
                - cat
                tty: true
              - name: ez-docker-helm-build
                image: ezezeasy/ez-docker-helm-build:1.41
                imagePullPolicy: Always
                securityContext:
                  privileged: true
            volumes:
            - name: docker-socket
              hostPath:
                path: /var/run/docker.sock
            '''
        }
    }

    environment {
         DOCKER_IMAGE = "maoravidan/projectapp"
    }

    stages {
        stage('Wait for MongoDB') {
            steps {
                container('python') {
                    script {
                        sh 'while ! nc -z mongodb.default.svc.cluster.local 27017; do echo "Waiting for MongoDB..."; sleep 1; done; echo "MongoDB is running!"'
                    }
                }
            }
        }

        stage('Build and Run Python Container') {
            steps {
                container('ez-docker-helm-build') {
                    script {
                        // Build Python Docker image
                        sh "docker build -t ${DOCKER_IMAGE}:backend ./fast_api"

                        // Run Python Docker container
                        sh "docker run -d --name python-container ${DOCKER_IMAGE}:backend"
                    }
                }
            }
        }

        stage('Run Tests in Python Container') {
            steps {
                script {
                    // Execute config-test.py script within the Python container
                    sh "docker exec python-container python3 config-test.py > test_logs.txt"
                }
            }
        }

        stage('Echo Logs') {
            steps {
                script {
                    // Echo the logs
                    sh "cat test_logs.txt"
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
                            // Build and Push Maven Docker image
                            sh "docker build -t ${DOCKER_IMAGE}:react1 ./test1"
                            sh "docker push ${DOCKER_IMAGE}:react1"
                            sh "docker push ${DOCKER_IMAGE}:backend"
                        }
                    }
                }
            }
        }
    }

    post {
        always {
            emailext(
                to: 'edmonp173@gmail.com',
                subject: "Jenkins Build: ${currentBuild.fullDisplayName}",
                body: """<p>Build ${currentBuild.fullDisplayName} completed with status ${currentBuild.result}.</p>
                         <p>Check console output at ${env.BUILD_URL} to view the results.</p>"""
            )
        }
    }
}
