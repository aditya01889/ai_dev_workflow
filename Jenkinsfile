pipeline {
    agent any

    environment {
        DOCKER_RUN_CMD = 'docker run --env-file .env --rm'
    }

    stages {
        stage('Build Frontend') {
            steps {
                script {
                    sh 'docker-compose build frontend'
                }
            }
        }
        stage('Run Frontend') {
            steps {
                script {
                    sh 'docker-compose up -d frontend'
                }
            }
        }
        stage('Build Backend') {
            steps {
                script {
                    sh 'docker-compose build requirement_gathering_agent'
                    sh 'docker-compose build requirements_analysis_agent'
                    sh 'docker-compose build sprint_planning_agent'
                    sh 'docker-compose build approval_agent'
                    sh 'docker-compose build frontend_components_agent'
                    sh 'docker-compose build backend_microservices_agent'
                    sh 'docker-compose build database_schema_agent'
                    sh 'docker-compose build api_gateway_agent'
                    sh 'docker-compose build unit_testing_agent'
                    sh 'docker-compose build deployment_automation_agent'
                }
            }
        }
        stage('Run Backend') {
            steps {
                script {
                    sh 'docker-compose up -d requirement_gathering_agent'
                    sh 'docker-compose up -d requirements_analysis_agent'
                    sh 'docker-compose up -d sprint_planning_agent'
                    sh 'docker-compose up -d approval_agent'
                    sh 'docker-compose up -d frontend_components_agent'
                    sh 'docker-compose up -d backend_microservices_agent'
                    sh 'docker-compose up -d database_schema_agent'
                    sh 'docker-compose up -d api_gateway_agent'
                    sh 'docker-compose up -d unit_testing_agent'
                    sh 'docker-compose up -d deployment_automation_agent'
                }
            }
        }
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
