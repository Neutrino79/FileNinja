# 🗂️ File Ninja

---

File Ninja is a comprehensive and user-centric open-source platform designed to manage PDF files and other digital documents efficiently. It provides advanced functionalities like file conversion, compression, splitting, merging, and AI-powered summarization.

> [!NOTE]\
> We have used `postgresSQL` as a database you can use any other also but `postgresSQL` is recommended

## 🎯 Objectives

- **User-Friendly Interface:** Create an intuitive, accessible platform for all users.
- **Comprehensive File Manipulation:** Convert, compress, split, and merge PDF files seamlessly.
- **Advanced AI Technologies:** Summarize lengthy documents using AI algorithms.
- **Open-Source Commitment:** Promote transparency and community-driven development.
- **Robust Security:** Implement strong encryption and data protection policies.

## 🛠️ Requirements

- **Backend:** Python, Django Framework
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** MongoDB or another suitable NoSQL database

## 📦 Prerequisites

1. **Python 3.x**  
   Ensure Python is installed on your system. Download from [here](https://www.python.org/downloads/).

2. **Node.js**  
   Required for managing frontend dependencies. Download from [here](https://nodejs.org/).

3. **MongoDB**  
   A NoSQL database for storing data. Download from [here](https://www.mongodb.com/try/download/community).

## 🚀 Steps to Get and Install the Project

1. **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/file-ninja.git
    cd file-ninja
    ```

2. **Backend Setup**

    - Create and activate a virtual environment:

      ```bash
      python -m venv venv
      source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
      ```

    - Install backend dependencies:

      ```bash
      pip install -r requirements.txt
      ```

    - Set up the database:

      ```bash
      python manage.py migrate
      ```

    - Run the backend server:

      ```bash
      python manage.py runserver
      ```

3. **Access the Application**

   Open your web browser and navigate to `http://localhost:8000` to access File Ninja.

---

Thank you for using File Ninja! We hope it simplifies your document management tasks.
