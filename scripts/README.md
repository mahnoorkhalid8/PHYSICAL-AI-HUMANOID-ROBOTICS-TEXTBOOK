# Project Scripts

This folder contains helpful scripts for setting up and running the Physical AI Humanoid Robotics Textbook project.

## Available Scripts

### `setup.sh` / `setup.bat`
- Sets up the project by installing both frontend and backend dependencies
- Checks for required tools (Node.js, Python)
- Provides instructions for completing the setup

### `dev-start.sh` / `dev-start.bat`
- Starts both the backend and frontend servers for development
- For Unix systems: runs both servers in the same terminal
- For Windows: opens separate command windows for each server

## Usage

### On Unix/Linux/Mac:
```bash
# Make scripts executable
chmod +x scripts/*.sh

# Run setup
./scripts/setup.sh

# Start development servers
./scripts/dev-start.sh
```

### On Windows:
```cmd
# Run setup
scripts\setup.bat

# Start development servers
scripts\dev-start.bat
```

## Notes

- Make sure you have Python 3.11+, Node.js 18+, and the required services (Qdrant, Postgres) running before starting
- The `.env.local` file should be properly configured with your API keys and service endpoints
- For production deployment, use the appropriate deployment commands for your hosting platform (e.g., Vercel)