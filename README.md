# Inventory Management API (Capstone Project)

This is my Backend Capstone project for ALX.  
It is a Django REST Framework-based **Inventory Management API**.

---

## Features (Completed so far)
- **Inventory CRUD**: Create, read, update, and delete inventory items.
- **Transactions**: Track inflow (`IN`) and outflow (`OUT`) of stock via transactions.
- **Automatic Stock Updates**: Item quantities are updated automatically using **Django signals** after each transaction.
- **Validation**: Prevents outflow transactions when requested quantity exceeds available stock.
- **Admin Panel**: Manage inventory items and transactions directly through Django Admin.
- **REST API Endpoints**:
  - `/api/inventory/items/` → Manage inventory items.
  - `/api/inventory/transactions/` → Record inflow/outflow transactions.
- **Data Serialization**: Using Django REST Framework serializers.
- **Clean URL Routing**: Dedicated `inventory/urls.py` and project-level routing setup.

---

## Features (Planned Next)
- **User Authentication (JWT)**
- **Role-based Permissions** (Admin, Manager, Staff)
- **Reporting**
  - Low-stock alerts
  - Transaction history
- **Unit Tests & Integration Tests**

---

## Setup

1. Clone repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

