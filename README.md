# Online Store Project with Django

## Overview

This project is an Online Store built using Django, featuring various key components and technologies:

- **JWT Token Authentication**: Authentication in this project is managed using JSON Web Tokens (JWT) for secure user sessions.

- **Django REST Framework (DRF)**: The project utilizes DRF to create robust APIs for managing products, user profiles, orders, and comments.

- **Caching with Redis**: Redis is employed for caching, enhancing performance by storing frequently accessed data.

- **Celery for Asynchronous Tasks**: Celery, a distributed task queue, is used to handle asynchronous tasks like sending emails, updating product inventory, and more.

## Features

- **Product Management**: Admins can add, edit, and categorize products, while users can browse and search for products.

- **User Profiles**: Each user has a profile page that displays order history and relevant details.

- **Search Functionality**: Users can search for products using keywords, with results displayed on a dedicated search page.

- **Comments and Reviews**: Users can leave comments and reviews on products, contributing to product discussions.

- **JWT Token-Based Authentication**: Users are authenticated using JWT tokens, providing secure access to their profiles and order history.

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Abbas-moradi/The-final-project.git
    cd The-final-project
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up database and apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Start the Celery worker for asynchronous tasks:

    ```bash
    celery -A OnlineShop worker --loglevel=info
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Usage

- Access the admin panel at `/admin` to manage products, categories, and users.

- Use the provided API endpoints for product listing, user profiles, order creation, and commenting.

- Customize the frontend templates in the `templates` directory to match your store's design.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit pull requests for new features, bug fixes, or improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides an overview of my project, how to install it, how to use it, and contributions from the open source community. 