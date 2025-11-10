pipeline {
    agent any

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
        timestamps()
    }

    parameters {
        choice(
            name: 'LEGACY_VERSION',
            choices: [
                'ACEest_Fitness.py',
                'ACEest_Fitness-V1.1.py',
                'ACEest_Fitness-V1.2.py',
                'ACEest_Fitness-V1.2.1.py',
                'ACEest_Fitness-V1.2.2.py',
                'ACEest_Fitness-V1.2.3.py',
                'ACEest_Fitness-V1.3.py'
            ],
            description: 'Desktop release file to package from versions/.'
        )
        string(name: 'RELEASE_VERSION', defaultValue: 'v2.0.0', description: 'Semantic version for this pipeline run.')
        string(name: 'DOCKER_REPOSITORY', defaultValue: 'docker.io/YOUR_DOCKER_ID/aceest-fitness', description: 'Fully-qualified image repository (registry/namespace/name).')
        choice(
            name: 'DEPLOY_STRATEGY',
            choices: ['base', 'blue-green', 'canary', 'rolling', 'shadow', 'ab'],
            description: 'Kubernetes manifest to apply from k8s/.'
        )
        booleanParam(name: 'PUSH_IMAGE', defaultValue: true, description: 'Push the image to DOCKER_REPOSITORY after build.')
        booleanParam(name: 'DEPLOY_TO_K8S', defaultValue: false, description: 'Apply the selected Kubernetes manifest (requires kubeconfig credentials).')
    }

    environment {
        APP_NAME = 'aceest-fitness'
        PYTHON = 'python3'
        VENV_DIR = '.venv'
        DIST_DIR = 'dist'
        IMAGE_URI = "${params.DOCKER_REPOSITORY}:${params.RELEASE_VERSION}"
        K8S_NAMESPACE = 'aceest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git status -sb || true'
            }
        }

        stage('Setup Python & Dependencies') {
            steps {
                sh '''
                    ${PYTHON} -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest -q --maxfail=1 --disable-warnings --cov=app --cov-report=xml --junitxml=junit.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'junit.xml'
                    archiveArtifacts artifacts: 'coverage.xml', onlyIfSuccessful: false
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQubeServer') {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        sonar-scanner \
                          -Dsonar.projectVersion=${RELEASE_VERSION}
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 10, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_URI} ."
            }
        }

        stage('Push Docker Image') {
            when { expression { return params.PUSH_IMAGE } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKERHUB_USER', passwordVariable: 'DOCKERHUB_TOKEN')]) {
                    sh '''
                        echo "${DOCKERHUB_TOKEN}" | docker login --username "${DOCKERHUB_USER}" --password-stdin $(echo ${DOCKER_REPOSITORY} | cut -d/ -f1)
                        docker push ${IMAGE_URI}
                    '''
                }
            }
        }

        stage('Package Legacy Desktop Version') {
            steps {
                sh '''
                    mkdir -p ${DIST_DIR}/legacy
                    cp versions/${LEGACY_VERSION} ${DIST_DIR}/legacy/${LEGACY_VERSION}
                    tar -czf ${DIST_DIR}/legacy-${LEGACY_VERSION%.py}-${RELEASE_VERSION}.tar.gz -C ${DIST_DIR}/legacy ${LEGACY_VERSION}
                '''
                archiveArtifacts artifacts: "${DIST_DIR}/legacy-*.tar.gz", onlyIfSuccessful: true
            }
        }

        stage('Deploy to Kubernetes') {
            when { expression { return params.DEPLOY_TO_K8S } }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl config use-context "$(kubectl config current-context)"
                        kubectl apply -f k8s/${DEPLOY_STRATEGY}.yaml
                        kubectl get deployments -n ${K8S_NAMESPACE}
                        kubectl get pods -o wide -n ${K8S_NAMESPACE}
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout || true'
            cleanWs deleteDirs: true, disableDeferredWipeout: true
        }
    }
}
