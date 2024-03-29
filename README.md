# 📗 Table of Contents

- [📖 About the Project](#about-project)
  - [🛠 Built With](#built-with)
    - [Tech Stack](#tech-stack)
    - [Key Features](#key-features)
- [💻 Getting Started](#getting-started)
  - [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Install](#install)
  - [Usage](#usage)
- [👥 Authors](#authors)
- [🔭 Future Features](#future-features)
- [⭐️ Show your support](#support)
- [🙏 Acknowledgements](#acknowledgements)
- [📝 License](#license)

<!-- PROJECT DESCRIPTION -->

# 📖 [Vendor-Management-System] <a name="about-project"></a>

> This is a Vendor Management System built with Django and Django Rest Framework. It is a REST API that allows users to create, read, update and delete Vendors and their Purchase Orders. It also keeps track of the Historical Performance of the Vendors.



## 🛠 Built With <a name="built-with"></a>

### Tech Stack <a name="tech-stack"></a>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="#">Python</a></li>
    <li><a href="#">Django</a></li>
    <li><a href="#">Django Rest Framework</a></li>
  </ul>
</details>

<details>
  <summary>Database</summary>
  <ul>
    <li><a href="#">PostgreSQL</a></li>
    <li><a href="#">Psycopg2</a></li>
  </ul>
</details>


<!-- Features -->

### Key Features <a name="key-features"></a>

- **[Objects-oriented]**
- **[Token-Authentication]**
- **[CRUD]**
- **[Test-Driven-Development]**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## 💻 Getting Started <a name="getting-started"></a>

To get a local copy up and running, follow these steps.

### Prerequisites

In order to run this project you need:

<ul>
    <li>Python</li>
    <li>Django</li>
    <li>Django Rest Framework</li>
    <li>PostgreSQL</li>
    <li>Psycopg2</li>
</ul>

### Setup

Clone this repository to your desired folder:

Example commands:
```bash
cd my-folder
git clone https://github.com/Rishi-Mishra0704/vendor-management
```
### Database Setup

1. **Create a PostgreSQL Database:**
   - Set up a PostgreSQL database and make a note of the database name, username, and password.

2. **Update `settings.py`:**
   - Open the `settings.py` file in your Django project.

3. **Add Database Configuration:**
   - Locate the `DATABASES` section in `settings.py` and update it with the following code:

     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your-db-name',
             'USER': 'your-username',
             'PASSWORD': 'your-password',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

   - Replace `'your-db-name'`, `'your-username'`, and `'your-password'` with your actual database credentials.

Now your Django project is configured to use the PostgreSQL database you've set up.


### Install

1. Create a virtual environment and activate it:
   - For Windows:
     ```powershell
     python -m venv env
     & desired_folder/env/Scripts/Activate.ps1
     ```

   - For Linux and Mac:
     ```bash
     python -m venv env
     source env/bin/activate
     ```

   Ensure that you have the necessary execution permissions on the activation script.

2. Install the dependencies:
```bash
   pip install -r requirement.txt
 ```
 
3. Run the following commands to create the Models in database :
```bash
python manage.py makemigrations
python manage.py migrate
```
### Usage

To run the project, execute the following command:

```bash
cd desired-folder/vendor-management/vendorManagement
 python manage.py runserver
 ```

<h1>Watch the video demo for more understanding the usage.</h1>

### 🚀<a name="Video-Demo" href = "https://drive.google.com/file/d/1I8PSeIjY0iiphBC-70fNTq_mfgLRk8eT/view?usp=sharing">Video Demo</a>

### Testing
To run the tests, execute the following command:

To run all the tests:
```bash
 python manage.py test
 ```

To run a specific test:
```bash
 python manage.py test vendorApi
 ```
 
```bash
python manage.py test PurchaseApi
 ```

```bash
python manage.py test historyApi
```



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- AUTHORS -->

## 👥 Authors <a name="authors"></a>

👤 **Rishi_Mishra**

- GitHub: [@githubhandle](https://github.com/Rishi-Mishra0704)
- Twitter: [@twitterhandle](https://twitter.com/RishiMi31357764)
- LinkedIn: [LinkedIn](https://www.linkedin.com/in/rrmishra/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- SUPPORT -->

## ⭐️ Show your support <a name="support"></a>

> Show your support by giving a ⭐️ if you like this project!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGEMENTS -->

## 🙏 Acknowledgments <a name="acknowledgements"></a>

I would like to thank Fatmug Design for giving me the opportunity to work on this project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## 📝 License <a name="license"></a>

This project is [MIT](./LICENSE) licensed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
