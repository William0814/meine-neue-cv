# 🧠 Engineer William – CV Web App

A web application built with **Flask**, **MySQL**, and a clean **HTML/CSS/JS** frontend to showcase my **professional résumé** in a dynamic, multilingual, and scalable way. Deployed locally (WSL/Ubuntu) and prepared for cloud deployment.

---

## 🚀 Key Features

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML5, CSS3, JavaScript
- **i18n:** Tolgee-driven translations
- **Email:** SendGrid API for contact form
- **Clean structure:** Classes, persistence layer, templates, and static assets
- **Security basics:** `.env` variables, input validation & sanitization

---

## 🧰 Tech Stack

| Technology | Purpose |
|-----------|---------|
| 🐍 **Flask** | Python web framework |
| 🐬 **MySQL** | Relational database |
| 🧩 **Jinja2** | HTML templating |
| 🌐 **Tolgee** | Internationalization (i18n) |
| ✉️ **SendGrid** | Email delivery |
| 🗂️ **WSL/Ubuntu** | Local dev environment |
| 🔐 **python-dotenv** | Environment variables |

---

## 🏗️ Project Structure (as-is)

> This mirrors the repository view you shared so anyone can navigate quickly.

```text
MEINE-NEUE-CV/
├─ classes/
│  ├─ __pycache__/
│  ├─ emailSender.py
│  ├─ mailTasks.py
│  └─ tolgge.py
├─ percistence/
│  ├─ __pycache__/
│  └─ form.py
├─ static/assets/
│  ├─ apk/
│  ├─ css/
│  ├─ icons/
│  ├─ images/
│  ├─ js/
│  ├─ json/
│  ├─ pdf/
│  ├─ sass/
│  └─ webfonts/
├─ templates/
│  ├─ aboutMe.html
│  ├─ experience.html
│  ├─ index.html
│  └─ studies.html


