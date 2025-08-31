# School Database Project: E-commerce System

This project is a Django-based e-commerce application developed for a school database course. It demonstrates the implementation of a complete web store, with a strong focus on advanced PostgreSQL database features such as stored procedures, views, triggers, cursors, and performance optimization with indexes and window functions.

## Features

- **User Authentication**: Separate login and registration for customers and employees.
- **Role-Based Access**: Distinct views and permissions for administrators (employees) and regular customers.
- **Product Management**: Full CRUD (Create, Read, Update, Delete) functionality for products. Products are categorized (Mobile, PC Component, Home Appliance) with specific attributes for each category.
- **Provider Management**: CRUD operations for product suppliers.
- **Shopping Cart**: Customers can add, view, and remove products from their cart.
- **Ordering System**: Customers can place orders from their cart.
- **Sales & Order Management**: Administrators can view all orders, confirm them, and generate sales reports.
- **User History**: Tracks user actions, such as placing an order.
- **Data Population**: Includes scripts to populate the database with fake data for testing purposes.

## Technology Stack

- **Backend**: Django
- **Database**: PostgreSQL
- **Frontend**: Django Template Language, HTML, CSS, JavaScript

## Database Schema

The database is designed to support a typical e-commerce workflow, with tables for users, products, orders, and more.

| Table Name | Description |
| :--- | :--- |
| `proveedor` | Stores supplier information. |
| `proveedor_telef` | Stores phone numbers for suppliers. |
| `producto` | Base table for all products. |
| `componente_pc` | Inherits from `producto`, for PC components. |
| `movil` | Inherits from `producto`, for mobile devices with specific attributes. |
| `equipo_hogar` | Inherits from `producto`, for home appliances. |
| `usuario` | Base table for all users (customers and employees). |
| `cliente` | Inherits from `usuario`, represents customers. |
| `trabajador` | Inherits from `usuario`, represents employees/administrators. |
| `cliente_producto`| Manages the items in a customer's shopping cart. |
| `pedido` | Stores customer order information. |
| `pedido_producto` | Maps products to specific orders. |
| `confirmaciones` | Stores order confirmations made by employees. |
| `info_ventas` | Stores sales information generated from confirmed orders. |
| `perfil_usuario` | Stores additional user profile information. |
| `productos_vacios`| Tracks products that are out of stock. |
| `historial_usuario`| Logs actions performed by users. |

An Entity-Relationship diagram is available in the `Diagrama sin título.drawio` file.

## Advanced Database Features

This project heavily utilizes database-level logic to ensure data integrity and performance.

### Views
- `proveedor_telefono`: Aggregates phone numbers for each provider.
- `listar_productos`: Lists all products, ordered by ID.
- `listar_producto_detalle`: Provides a detailed view of products, joining with category-specific tables.
- `carrito`: A simple view for the `cliente_producto` table.
- `listar_pedidos`: Joins `pedido`, `cliente`, and `producto` tables for a comprehensive order view.
- `listar_confirmaciones`: Shows detailed confirmation information, joining with orders and employees.
- `listar_ventas`: Generates a sales report, including total profit for each sale.
- `total_productos`: A view to count the total number of products.

### Stored Functions & Procedures
The application's business logic is largely encapsulated in PostgreSQL functions, which are executed from the Django backend.
- **CRUD Operations**: Functions like `insertar_proveedor`, `add_producto`, `actualizar_producto`, and `eliminar_producto` handle all data manipulation.
- **User Management**: `login`, `registrar_cliente`, and `add_trabajador` manage user authentication and creation.
- **E-commerce Logic**: `adicionar_al_carrito`, `obtener_carrito`, `add_un_pedido`, and `crear_confirmacion` handle the core shopping and checkout workflow.

### Performance Optimizations
- **Indexes**: `idx_nombre` and `idx_categoria` are created on the `producto` table to accelerate searching and filtering operations.
- **Window Functions**:
  - `suma_acumulativa_carrito` uses `OVER()` to calculate a running total of prices in the shopping cart.
  - `productos_mas_vendidos` uses `RANK()` to efficiently rank products by sales volume.
- **Common Table Expressions (CTEs)**:
  - `productos_x_categorias` and `ganancia_promedio` use the `WITH` clause to improve query readability and structure.

### Triggers
- `verificar_stock_vacio`: Automatically adds a product to the `productos_vacios` table when its stock reaches zero.
- `registrar_pedido`: Inserts a record into the `historial_usuario` table every time a new order is created.

### Cursors
- `aumentar_precios` and `disminuir_precios`: Use cursors to iterate through all products and apply a bulk price increase or decrease.

## Project Structure

- `project/`: Main Django project configuration (`settings.py`, `urls.py`).
- `app_prod/`: Handles all logic related to products, providers, orders, cart, and sales.
- `app_user/`: Manages user registration, login, and roles (client vs. employee).
- `app_user_profile/`: Manages user profile details.
- `static/`: Contains all static assets (CSS, JS, images).
- `*.sql`: SQL files defining the database schema, views, functions, and other features.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    ```
2.  **Set up the Database:**
    - Install PostgreSQL.
    - Create a new database named `tienda`.
    - Run the `tienda.sql` script to create the initial tables.
3.  **Configure Django:**
    - Update the database connection settings in `project/settings.py` with your PostgreSQL credentials.
4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run Migrations:**
    The database schema, views, functions, and triggers are created automatically when the Django application starts (as defined in the `apps.py` file of each app). However, you should run migrations to create Django's built-in tables.
    ```bash
    python manage.py migrate
    ```
6.  **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

## Data Population (Optional)

The application includes views to populate the database with sample data using the Faker library. Once you have an admin user, access the `/extras/` URL to find options for populating products, clients, employees, providers, and orders.
