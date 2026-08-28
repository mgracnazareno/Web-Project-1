## Documentation

For detailed information about the application’s architecture, workflow, database models, and relationships, see the [System Design Documentation](docs/SYSTEM-DESIGN.md).

## Project Management

Project tasks and development progress were organized using Trello.

🔗 [View the CareSchedule Trello Board](https://trello.com/b/0t3cjNv5/web-project-1)

---

## Installation and Local Setup

Follow these steps to run CareSchedule on your local computer.

### Prerequisites

Make sure the following software is installed:

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- A code editor such as PyCharm or Visual Studio Code

### 1. Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/mgracnazareno/Web-Project-1.git
```

Navigate to the project folder:

```bash
cd Web-Project-1
```

Then navigate to the folder containing `app.py`:

```bash
cd care-schedule/bp_app
```

> Adjust the path if your project structure is different.

### 2. Create a Virtual Environment

#### Windows PowerShell

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell prevents activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then try the activation command again.

#### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the Environment Variables

Create a file named `.env` in the same directory as `app.py`:

```env
SECRET_KEY=replace-with-your-own-secret-key
```

Generate a secure secret key with:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value and use it as the value of `SECRET_KEY`.

> Do not commit the `.env` file to GitHub.

### 5. Initialize the Database

Start the Flask shell:

```bash
python -m flask --app app shell
```

Inside the Flask shell, run:

```python
from models import db

db.create_all()
exit()
```

> Update the import statement if your `db` object is stored in a different file.

### 6. Run the Application

```bash
python -m flask --app app run --debug
```

Open the following address in your browser:

[http://127.0.0.1:5000](http://127.0.0.1:5000)

### 7. Create Test Accounts

Use the registration pages to create:

- A patient account
- A healthcare professional account

The demo accounts listed in this README are available on the deployed application. They may not exist in a newly created local database.

### Stop the Application

Press `Ctrl + C` in the terminal to stop the Flask server.

Deactivate the virtual environment:

```bash
deactivate
```

> The Flask development server is intended for local testing only and should not be used as a production server.

