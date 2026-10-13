# Focus App
A personal productivity and focus-tracking web application built with Django.

# Features
- User registration and login
- Create and manage focus sessions
- Track time spent focusing
- View focus history
- Track daily focus goals
- Track focus streaks

# Tech Stack
- Python
- Django
- PostgreSQL
- HTML
- CSS
- JS *(countdown timer and sound for countdown over)*

# Project Status
In deployment phase

### Completed
- Custom user model
- User registration
- User login/logout
- Password change
- Password reset
- Authentication UI
- User goal
- Focus session
- Track completed sessions
- Focus history

# Setup

### Prerequisites
Before you begin, ensure you have Python 3.x and PostgreSQL installed and running on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/ubaidbnd/focus_app.git
cd focus_app
```

### 2. Set up a virtual environment
```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in your root project directory to securely manage your secrets (Integration in progress):
```env
SECRET_KEY=your_django_secret_key
DEBUG=True

# Database Configuration
DB_NAME=your_postgres_db_name
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Apply migrations and run
```bash
python manage.py migrate
python manage.py runserver
```
Open your browser and navigate to `http://127.0.0.1:8000/`.
