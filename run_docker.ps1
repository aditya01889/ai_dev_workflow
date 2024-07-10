# Build Docker Images
docker build -t requirement_gathering_agent ./requirement_gathering_agent
docker build -t requirements_analysis_agent ./requirements_analysis_agent
docker build -t sprint_planning_agent ./sprint_planning_agent
docker build -t approval_agent ./approval_agent
docker build -t frontend_components_agent ./frontend_components_agent
docker build -t backend_microservices_agent ./backend_microservices_agent
docker build -t database_schema_agent ./database_schema_agent
docker build -t api_gateway_agent ./api_gateway_agent
docker build -t unit_testing_agent ./unit_testing_agent
docker build -t deployment_automation_agent ./deployment_automation_agent

# Run Docker Containers
docker run --env-file .env --name requirement_gathering_agent -d requirement_gathering_agent
docker run --env-file .env --name requirements_analysis_agent -d requirements_analysis_agent
docker run --env-file .env --name sprint_planning_agent -d sprint_planning_agent
docker run --env-file .env --name approval_agent -d approval_agent
docker run --env-file .env --name frontend_components_agent -d frontend_components_agent
docker run --env-file .env --name backend_microservices_agent -d backend_microservices_agent
docker run --env-file .env --name database_schema_agent -d database_schema_agent
docker run --env-file .env --name api_gateway_agent -d api_gateway_agent
docker run --env-file .env --name unit_testing_agent -d unit_testing_agent
docker run --env-file .env --name deployment_automation_agent -d deployment_automation_agent

# Start Logstash
cd logging
logstash -f logstash.conf