pipeline {
    agent any

    environment {
        DOCKER_RUN_CMD = 'docker run --env-file .env --rm'
    }

    stages {
        stage('Requirement Gathering') {
            steps {
                script {
                    runDocker('requirement_gathering_agent')
                }
            }
        }
        stage('Requirements Analysis') {
            steps {
                script {
                    runDocker('requirements_analysis_agent')
                }
            }
        }
        stage('Sprint Planning') {
            steps {
                script {
                    runDocker('sprint_planning_agent')
                }
            }
        }
        stage('Approval') {
            steps {
                script {
                    runDocker('approval_agent')
                }
            }
        }
        stage('Frontend Components') {
            steps {
                script {
                    runDocker('frontend_components_agent')
                }
            }
        }
        stage('Backend Microservices') {
            steps {
                script {
                    runDocker('backend_microservices_agent')
                }
            }
        }
        stage('Database Schema') {
            steps {
                script {
                    runDocker('database_schema_agent')
                }
            }
        }
        stage('API Gateway') {
            steps {
                script {
                    runDocker('api_gateway_agent')
                }
            }
        }
        stage('Unit Testing') {
            steps {
                script {
                    runDocker('unit_testing_agent')
                }
            }
        }
        stage('Deployment') {
            steps {
                script {
                    runDocker('deployment_automation_agent')
                }
            }
        }
    }
}

def runDocker(agentName) {
    try {
        sh "${DOCKER_RUN_CMD} ${agentName}"
    } catch (Exception e) {
        error "Failed to run ${agentName}: ${e.message}"
    }
}
