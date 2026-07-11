# 📚 LibManage

> A robust Library Management System built with Django, featuring custom user roles, book inventory management, and an automated borrowing and fine calculation system.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Django](https://img.shields.io/badge/django-4.0%2B-green.svg)

## 📖 About The Project

**LibManage** is a comprehensive backend system for managing library operations. It implements role-based access control, distinguishing between standard users and authors, and fully handles the lifecycle of book borrowing, returning, and fine tracking.

### 🏗️ Project Structure
The project is divided into the main configuration and two core applications:
* **`libmange/`**: The core project settings and routing directory.
* **`library/`**: Handles the core library logistics (Books, Tags, Borrows, and Fines).
* **`user/`**: Manages custom user authentication and role profiles.

### ✨ Key Features

**User & Access Management**
* **Custom Authentication:** Secure signup, login, and profile management.
* **Role-Based Permissions:** Users can register as standard borrowers or 'Authors'. 
* **Author Privileges:** Users with an Author profile are granted permissions to create tags, add new books, update book details, and delete books from the catalog.

**Book & Inventory System**
* **Catalog Management:** Books are tracked by Title, Author, Description, and Tags.
* **Inventory Tracking:** The system automatically tracks `total_copies` and dynamically updates `available_copies` as books are checked in and out.
* **Tagging System:** Books can be categorized using a flexible Many-to-Many tagging system.

**Borrowing & Fine Logistics**
* **Checkout System:** Users can borrow books with a specified due date, instantly decrementing available inventory.
* **Automated Returns:** Returning a book automatically restores library inventory and flags the record as returned.
* **Fine Calculation:** Automatically calculates overdue fines based on the due date and actual return date at a rate of $1 per day.
* **Borrow History:** Users can view their active and past borrows, while staff can view the global borrow list.

## 🛠️ Built With

* **Framework:** [Django](https://www.djangoproject.com/)
* **Language:** Python
* **Database:** SQLite (Default) / PostgreSQL / MySQL
* **Frontend:** HTML/CSS (Django Templates)

## 🚀 Getting Started

Follow these instructions to get a local copy of the project up and running on your machine.

### Prerequisites

* Python 3.8 or higher
* pip (Python package installer)

### Installation

1. **Clone the repository**
   ```sh
   git clone [https://github.com/m4shaikh/LibManage.git](https://github.com/m4shaikh/LibManage.git)
