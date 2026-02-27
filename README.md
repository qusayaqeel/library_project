# Library Project 📚

This project is an online bookstore web application, built using the powerful **Django** framework for the backend, and **HTML, CSS, JavaScript** for the frontend design.

## Key Features ✨
- Display a list of available books categorized into groups (Categories).
- Add, edit, and delete books from the admin panel.
- A fully integrated Admin Panel to manage the website easily.
- Upload images for book covers and user profile pictures.
- User authentication system (users can borrow or purchase books depending on the settings).

## Prerequisites 🛠️
Before running the project, make sure you have the following installed on your machine:
- **Python** (version 3.10 or newer is recommended).
- **pip** (Python package installer).
- A virtual environment setup using either `venv` or `conda`.

## Setup and Running the Project 🚀

### 1. Set up the Virtual Environment
It is always recommended to isolate project dependencies using a virtual environment. If you are using `conda` (which is highly recommended for this project), run:
```bash
conda create --name libraryenv python=3.10
conda activate libraryenv
```
Or if you are using the standard `venv`:
```bash
python -m venv venv
venv\Scripts\activate   # For Windows
```

### 2. Install Requirements
The project includes a `requirements.txt` file containing the essential libraries (like Django and Pillow for image processing). Install them by running:
```bash
pip install -r requirements.txt
```

### 3. Setup the Database (Migrations)
The project uses the default `db.sqlite3` database for local development. To create and initialize the necessary tables (such as users and books):
```bash
python manage.py migrate
```

### 4. Create a Superuser
To create an admin account to manage the site (add books and categories):
```bash
python manage.py createsuperuser
```
You will be prompted to enter a username, email address, and password.

### 5. Run the Local Server
Now that everything is set up, you can run the project using the following command:
```bash
python manage.py runserver
```

## Important Links 🌐
After starting the server, you can visit the following links in your browser:
- **Main Website:** `http://127.0.0.1:8000/`
- **Admin Panel:** `http://127.0.0.1:8000/admin/`

---
*Designed and developed by Qusay*
