pipeline {
    agent any

    stages {
        stage('Requirement Gathering') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm requirement_gathering_agent'
                }
            }
        }
        stage('Requirements Analysis') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm requirements_analysis_agent'
                }
            }
        }
        stage('Sprint Planning') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm sprint_planning_agent'
                }
            }
        }
        stage('Approval') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm approval_agent'
                }
            }
        }
        stage('Frontend Components') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm frontend_components_agent'
                }
            }
        }
        stage('Backend Microservices') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm backend_microservices_agent'
                }
            }
        }
        stage('Database Schema') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm database_schema_agent'
                }
            }
        }
        stage('API Gateway') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm api_gateway_agent'
                }
            }
        }
        stage('Unit Testing') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm unit_testing_agent'
                }
            }
        }
        stage('Deployment') {
            steps {
                script {
                    sh 'docker run --env-file .env --rm deployment_automation_agent'
                }
            }
        }
    }
}
