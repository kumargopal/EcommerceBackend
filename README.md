# Django E-commerce Backend

This project is a backend implementation for an e-commerce platform built using Django Rest Framework (DRF). It includes functionalities for authentication, products, shopping cart, and orders, along with an admin interface. The project uses Docker and Docker Compose for containerization and Swagger UI for API documentation.

## Features

- User and admin authentication (including Google OAuth and OTP-based login)
- Product management
- Shopping cart functionality
- Order processing
- API documentation with Swagger UI

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/kumargopal/EcommerceBackend.git
    cd EcommerceBackend
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:

    Create a `.env` file in the root directory and add the following environment variables:

    ```env
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    MYSQL_DATABASE=ecommerce
    MYSQL_USER=root
    MYSQL_PASSWORD=password
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    EMAIL_HOST_USER=your-email@gmail.com
    EMAIL_HOST_PASSWORD=your-email-password
    DEFAULT_FROM_EMAIL=your-email@gmail.com
    GOOGLE_CLIENT_ID=your-google-client-id
    GOOGLE_CLIENT_SECRET=your-google-client-secret
    EMAIL_CONFIRM_REDIRECT_BASE_URL=http://localhost:3000/email/confirm/
    PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL=http://localhost:3000/password-reset/confirm/
    ```

## Running the Project

### Using Docker

1. Build and start the containers:

    ```bash
    docker-compose up --build
    ```

2. Apply migrations and create a superuser:

    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    ```

3. Access the application at `http://localhost:8000`.

### Without Docker

1. Apply migrations:

    ```bash
    python manage.py migrate
    ```

2. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

3. Run the development server:

    ```bash
    python manage.py runserver
    ```

4. Access the application at `http://localhost:8000`.

