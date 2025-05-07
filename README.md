# Pawsome Pet Products - E-commerce Platform

This is a fully functional e-commerce platform for selling pet products built using the Django framework. It includes a wide range of features for both users and administrators.

## Features
**User Side:**

-   User sign-up and login (with OTP and social login).
-   Browse and view product details (including images, price, reviews, stock).
-   User profile management (details, addresses, orders).
-   Shopping cart functionality.
-   Checkout process with address selection and Cash on Delivery.
-   Order history and cancellation.
-   Payment gateway integration (Razorpay).
-   Search and category filtering.
-   Wishlist.
-   Wallet.

**Admin Side:**

-   Admin login.
-   User management (list, block/unblock).
-   Category management (add, edit, delete).
-   Product management (add, edit, delete, multiple images).
-   Order management (list, change status, cancel).
-   Stock management display.
-   Sales reports (daily, weekly, yearly, custom).
-   Admin dashboard with key metrics.

## Technologies Used

-   **Django:** The primary web framework.
-   **Python:** The programming language.
-   **HTML, CSS, JavaScript, Bootstrap:** For frontend development.
-   **Database:** PostgreSQL
-

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/bithulmb/ecommerce-project.git
    cd ecommerce-project/pawsomepetproducts
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set environment variables (see .env.sample):**
    ```bash
    cp .env.sample .env
    ```

5.  **Apply migrations:**    
    -   Run migrations:
        ```bash
        python manage.py migrate
        ```

6.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the application:** 
    Open your web browser and navigate to `http://127.0.0.1:8000/`.



