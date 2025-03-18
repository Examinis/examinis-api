# Examinis

## Installation for develop

1. **Clone the repository:**
   ```bash
   git clone git@github.com:paulosys/Examinis.git
   cd Examinis
   ```

2. **Install Poetry:**
   - Windows:
      ```bash
      (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
      ```

3. **Start Poetry:**
   ```bash
   poetry install
   poetry shell
   ```
   
4. **Start the containers:**
   ```bash
   docker compose up --build -d
   ```

### Running and Stopping the Application

* **Start the containers:**
   ```bash
   docker-compose up --build -d
   ```

* **Stop the containers:**
   ```bash
   docker-compose stop
   ```

## Before commit changes
### Branch creation
Whenever you change the code, switch to the develop branch and pull from the develop source. Then create a branch with the OpenProject task number and a small identification. Example: `12345_new_module`
```bash
$ git checkout develop
$ git pull origin develop
$ git checkout -b 12345_new_module
```
### Checking code
```bash
$ task lint
```
