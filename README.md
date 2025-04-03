# Python Web Application Template

A template for building robust web applications using Python and Flask.

## Features

- User authentication (register, login, logout)
- Role-based access control
- Database integration with SQLAlchemy ORM
- Responsive design with Bootstrap
- Blueprint-based application structure
- Error handling
- Testing framework
- Configurable port settings for all services

## Technology Stack

- **Backend**: Flask
- **Database**: SQLAlchemy with SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Testing**: pytest

## Project Structure

```
PythonWeb/
│
├── app/                      # Application package
│   ├── __init__.py           # Initialize Flask app
│   ├── models.py             # Database models
│   ├── auth/                 # Authentication blueprint
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── forms.py
│   ├── main/                 # Main blueprint
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── errors/               # Error handling blueprint
│   │   ├── __init__.py
│   │   └── handlers.py
│   ├── static/               # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── img/
│   └── templates/            # HTML templates
│       ├── base.html
│       ├── index.html
│       ├── about.html
│       ├── dashboard.html
│       ├── auth/
│       └── errors/
│
├── migrations/               # Database migrations
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_routes.py
│   └── test_models.py
│
├── venv/                     # Virtual environment
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-web-template.git
   cd python-web-template
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Configure environment variables:

   **Option 1: Using .env files (recommended)**

   The application supports different .env files for different environments and instances:

   ```
   # Copy the example files and modify as needed
   cp .env.example .env                # Base configuration
   cp .env.dev.example .env.dev        # Development instance
   cp .env.test.example .env.test      # Test instance
   ```

   **Option 2: Setting environment variables manually**

   ```
   # On Windows
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set FLASK_CONFIG=development
   set FLASK_INSTANCE=dev
   set SERVER_PORT=5000

   # On macOS/Linux
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export FLASK_CONFIG=development
   export FLASK_INSTANCE=dev
   export SERVER_PORT=5000
   ```

   See the `.env.example` file for all available configuration options.

5. Initialize the database:
   ```
   # Option 1: Using Flask-Migrate
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

   # Option 2: Using the initialization script
   python init_db.py
   ```

6. Run the application:
   ```
   # Run a single instance with default settings
   python run.py

   # Run with a specific port
   set SERVER_PORT=5000  # Windows
   export SERVER_PORT=5000  # macOS/Linux
   python run.py

   # Run with a specific instance name (will load .env.dev if it exists)
   set FLASK_INSTANCE=dev  # Windows
   export FLASK_INSTANCE=dev  # macOS/Linux
   python run.py
   ```

   The application will be available at http://localhost:5000 (or the configured port)

7. Running multiple instances concurrently:

   ### Using the provided scripts

   The project includes scripts to easily run multiple instances with different configurations:

   **Windows:**
   ```
   # Run both development and test instances
   run_instances.bat

   # Run with custom ports
   run_instances.bat --dev-port 5000 --test-port 5001

   # Run only one instance
   run_instances.bat --dev-only
   run_instances.bat --test-only
   run_instances.bat --custom-only --custom-port 5002

   # Show help
   run_instances.bat --help
   ```

   **macOS/Linux:**
   ```
   # Make the script executable
   chmod +x run_instances.sh

   # Run both development and test instances
   ./run_instances.sh

   # Run with custom ports
   ./run_instances.sh --dev-port 5000 --test-port 5001

   # Run only one instance
   ./run_instances.sh --dev-only
   ./run_instances.sh --test-only
   ./run_instances.sh --custom-only --custom-port 5002

   # Show help
   ./run_instances.sh --help
   ```

   ### Running manually with different terminal windows

   **Terminal 1 (Development instance):**
   ```
   # Windows
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set FLASK_CONFIG=development
   set FLASK_INSTANCE=dev
   set SERVER_PORT=5000
   python run.py

   # macOS/Linux
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export FLASK_CONFIG=development
   export FLASK_INSTANCE=dev
   export SERVER_PORT=5000
   python run.py
   ```

   **Terminal 2 (Testing instance):**
   ```
   # Windows
   set FLASK_APP=run.py
   set FLASK_ENV=development
   set FLASK_CONFIG=testing
   set FLASK_INSTANCE=test
   set SERVER_PORT=5001
   python run.py

   # macOS/Linux
   export FLASK_APP=run.py
   export FLASK_ENV=development
   export FLASK_CONFIG=testing
   export FLASK_INSTANCE=test
   export SERVER_PORT=5001
   python run.py
   ```

   The instances will be available at:
   - Development: http://localhost:5000
   - Testing: http://localhost:5001
   - Custom: http://localhost:5002 (if configured)

## Testing

Run tests using pytest:
```
pytest
```

## Development

This template follows a blueprint-based structure for better organization:

- `app/auth/`: Authentication-related routes and forms
- `app/main/`: Main application routes
- `app/errors/`: Error handling

## Port Configuration

This application uses a flexible port configuration system:

### Development Environment
- **Flask Development Server**: Port 5000 (configurable via `SERVER_PORT` or `DEV_SERVER_PORT`)
- **Database**:
  - SQLite (file-based, no port needed)
  - PostgreSQL: Port 5432 (configurable via `DB_PORT`)

### Testing Environment
- **Flask Test Server**: Port 5001 (configurable via `TEST_SERVER_PORT`)
- **Test Database**: SQLite (file-based, no port needed)

### Production Environment
- **WSGI Server** (Gunicorn/uWSGI): Port 8000 (configurable via `WSGI_SERVER_PORT` or `PROD_SERVER_PORT`)
- **Web Server**:
  - HTTP: Port 80 (configurable via `WEB_SERVER_HTTP_PORT`)
  - HTTPS: Port 443 (configurable via `WEB_SERVER_HTTPS_PORT`)
- **Database**: PostgreSQL on port 5432 (configurable via `DB_PORT`)

### Other Services
- **Mail Server**: Port 25, 587, or 465 (configurable via `MAIL_PORT`)
- **Redis** (for caching/sessions): Port 6379 (configurable via `REDIS_PORT`)

All port settings can be configured through environment variables or the `.env` file.

## Deployment

This application includes a complete deployment pipeline with Docker, Gunicorn, and Nginx.

### Local Deployment with Docker

1. Create a production environment file:
   ```
   cp .env.production.example .env.production
   ```

2. Edit the `.env.production` file with your settings

3. Generate SSL certificates for HTTPS:
   ```
   # On Linux/macOS
   chmod +x generate_ssl_certs.sh
   ./generate_ssl_certs.sh

   # On Windows
   ./generate_ssl_certs.ps1
   ```

4. Build and start the Docker containers:
   ```
   # On Linux/macOS
   chmod +x deploy.sh
   ./deploy.sh --env prod --build

   # On Windows
   ./deploy.ps1 -Env prod -Build
   ```

5. The application will be available at:
   - HTTP: http://localhost:80 (redirects to HTTPS)
   - HTTPS: https://localhost:443

### CI/CD Pipeline

The application includes a GitHub Actions workflow for CI/CD:

1. **Continuous Integration**:
   - Runs tests on every push and pull request
   - Performs linting checks

2. **Continuous Deployment**:
   - Builds a Docker image on successful merge to main/master
   - Pushes the image to Docker Hub
   - Deploys to the production server

### Manual Production Deployment

1. Set up a server with Docker and Docker Compose installed

2. Clone the repository and navigate to the project directory

3. Create a production environment file:
   ```
   cp .env.production.example .env.production
   ```

4. Edit the `.env.production` file with your production settings

5. Generate or install SSL certificates in `nginx/ssl/`

6. Deploy the application:
   ```
   # On Linux/macOS
   chmod +x deploy.sh
   ./deploy.sh --env prod --build --migrate

   # On Windows
   ./deploy.ps1 -Env prod -Build -Migrate
   ```

7. The application will be available at your server's domain or IP address

### Scaling

To scale the application horizontally:

1. Increase the number of web service replicas:
   ```
   docker-compose up -d --scale web=3
   ```

2. Ensure Nginx is configured to load balance between the instances

3. Consider using a managed database service for production

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Flask documentation
- SQLAlchemy documentation
- Bootstrap documentation
