# Django + ML Project

This repository contains a **simple, beginner‑friendly Django project** with a clear path toward adding **machine‑learning features later**.

The goal of this README is to help **any teammate** clone the repo and get a working Django server running **without prior context**.

---

## 🎯 Project Purpose

- Provide a **clean Django 5.2 (LTS)** starting point
- Use **Python 3.14** managed via **Miniconda**
- Keep the setup simple and reproducible
- Prepare the ground for adding ML (NumPy / scikit‑learn) later

At this stage, the project is **pure Django**. No ML code is required to run it.

---

## 🧰 Tech Stack

- **Python:** 3.14
- **Django:** 5.2 (LTS)
- **Environment management:** Conda (Miniconda)
- **ML libraries (installed but optional):** NumPy, SciPy, scikit‑learn, pandas

---

## 📦 Prerequisites

You need the following installed locally:

- **Git**
  [https://git-scm.com/](https://git-scm.com/)

- **Miniconda** (recommended) or Anaconda
  [https://www.anaconda.com/docs/getting-started/miniconda/install](https://www.anaconda.com/docs/getting-started/miniconda/install)

Verify installation:

```bash
git --version
conda --version
```

---

## 📁 Project Structure

```text
project-root/
├── backend/              # Django project (settings, URLs, ASGI/WSGI)
├── core/                 # Main Django app
├── ml/                   # ML code (empty / optional for now)
├── manage.py
├── environment.yml       # Conda environment definition
├── README.md
└── .gitignore
```

> 💡 You only need `backend/`, `core/`, and `manage.py` to run Django.

---

## 🐍 Environment Setup

### 1️⃣ Create the Conda environment

From the project root:

```bash
conda env create -f environment.yml
```

This installs:

- Python 3.14
- Django 5.2
- Scientific libraries (for future ML work)

### 2️⃣ Activate the environment

```bash
conda activate titanic_capstone_django-ml
```

### 3️⃣ Verify

```bash
python --version
django-admin --version
```

Expected:

- Python 3.14.x
- Django 5.2

---

## ▶️ Running the Django Project

Apply initial migrations:

```bash
python manage.py migrate
python manage.py import_passengers 
```

Start the development server:

```bash
python manage.py runserver
```

Open your browser:

```
http://127.0.0.1:8000/
```

You should see the Django welcome page.

---

## 🔌 Example Endpoint (Sanity Check)

This project includes a minimal endpoint to confirm everything works.

### View (`core/views.py`)

```python
from django.http import HttpResponse


def ping(request):
    return HttpResponse("pong")
```

### URL configuration (`core/urls.py`)

```python
from django.urls import path
from .views import ping

urlpatterns = [
    path("ping/", ping),
]
```

### Project URLs (`backend/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]
```

Test it in the browser:

```
http://127.0.0.1:8000/ping/
```

Expected response:

```
pong
```

---

## 📦 Dependency Management Rules

- Use **Conda** for all dependencies
- Do **not** install NumPy / SciPy / scikit‑learn with `pip`
- Update dependencies only via `environment.yml`

To apply changes:

```bash
conda env update -f environment.yml --prune
```

---

## 🧠 About the `ml/` Folder

The `ml/` folder is reserved for **future machine‑learning code**.

At this stage:

- It may be empty
- It is **not required** to run Django

When ML is added later:

- Models will be loaded lazily
- No ML code will run at Django startup

---

## 🧪 Common Issues

**Django commands fail**

- Make sure the Conda environment is activated

**Long Conda solve times**

- Ensure only `conda-forge` is used

---

## 📚 Common Commands

```bash
conda activate titanic_capstone_django-ml
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
```

---

## 🗺️ Next Steps

Planned improvements:

- Add Django REST Framework
- Add tests (pytest)
- Add ML inference endpoints
- Add Docker support

---

## 📝 License

Choose a license before publishing (MIT is common for learning projects).

---

Happy hacking 👋
