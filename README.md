# AI Development Workflow

This project sets up a workflow for developing AI applications using Docker containers and a CI/CD pipeline with Jenkins. It includes logging and monitoring using Logstash, Kibana, Prometheus, and Grafana.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/ai_dev_workflow.git
    cd ai_dev_workflow
    ```

2. Create a `.env` file in the project root with your environment variables:
    ```plaintext
    OPENAI_API_KEY=your-openai-api-key
    ```

3. Run the Docker Compose setup:
    - For Unix-based systems:
        ```sh
        ./run_all.sh
        ```
    - For Windows PowerShell:
        ```powershell
        ./run_all.ps1
        ```

## Project Structure

- `requirement_gathering_agent/`: Code for the requirement gathering agent.
- `requirements_analysis_agent/`: Code for the requirements analysis agent.
- `sprint_planning_agent/`: Code for the sprint planning agent.
- `approval_agent/`: Code for the approval agent.
- `frontend_components_agent/`: Code for the frontend components agent.
- `backend_microservices_agent/`: Code for the backend microservices agent.
- `database_schema_agent/`: Code for the database schema agent.
- `api_gateway_agent/`: Code for the API gateway agent.
- `unit_testing_agent/`: Code for the unit testing agent.
- `deployment_automation_agent/`: Code for the deployment automation agent.
- `logging/`: Configuration for Logstash.
- `kibana/`: Configuration for Kibana.
- `prometheus/`: Configuration for Prometheus.
- `grafana/`: Configuration for Grafana.
- `jenkins/`: Configuration for Jenkins.

## License

This project is licensed under the MIT License.
