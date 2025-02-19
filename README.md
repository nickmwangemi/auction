# Digital Trading Platform

## Technology Choices

- **Backend Framework**: Django
  - Chosen for its robustness, scalability, and built-in admin interface.
- **Database**: SQLite
  - Used in the deployed version available at [https://nickmwangemi.pythonanywhere.com/](https://nickmwangemi.pythonanywhere.com/) due to the limitations of the free-tier on PythonAnywhere.
  - Can be replaced with PostgreSQL or MySQL for production.
- **API Framework**: Django REST Framework (DRF)
  - Used to create a RESTful API for the application, allowing for easy integration with other services.
- **Templating Engine**: Django Template Language
  - Used for rendering HTML dynamically.
- **WhatsApp Integration**: Yowsup Library
  - Used for sending WhatsApp notifications.

## Setup and Running the Application

### Prerequisites

- Python 3.6+
- Django 3.2+
- Yowsup Library for WhatsApp Integration

### Steps

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:nickmwangemi/auction.git
   cd auction
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the Application**:
   - Open your web browser and go to `http://127.0.0.1:8000/`.

### Deployed Version

- The deployed version of the application is available at [https://nickmwangemi.pythonanywhere.com/](https://nickmwangemi.pythonanywhere.com/).
- Due to the limitations of the free-tier on PythonAnywhere, SQLite is used as the database.

### WhatsApp Integration Setup

1. **Install Yowsup**:
   ```bash
   pip install yowsup2
   ```

2. **Configure WhatsApp Credentials**:
   - Add your WhatsApp credentials (phone number and password) in the script.

3. **Run the WhatsApp Notification Script**:
   ```bash
   python whatsapp_notification.py
   ```

## Assumptions

- The application assumes that each item has a volume of 1 for the MVP.
- The WhatsApp integration is set up with a valid WhatsApp account and credentials.
- The system time is accurate for determining auction statuses.

## Features Not Fully Implemented

- **Payment Processing**: The settlement stage does not include actual payment processing.
- **Advanced Bidding Features**: Features like proxy bidding or bid increments are not implemented.
- **Previous Price and Volumes**: Simulated for extra credit but not fully integrated into the UI.

## WhatsApp Integration Details

### Library Used

- **Yowsup**: A Python library for interacting with WhatsApp.

### Setup Instructions

1. **Register with Yowsup**: Follow the Yowsup documentation to register your phone number.
2. **Configure Credentials**: Update the script with your WhatsApp phone number and password.
3. **Run the Script**: Execute the script to send notifications.

### Known Limitations

- **Rate Limiting**: Be aware of WhatsApp's rate limits to avoid being blocked.
- **Dependency on Yowsup**: The integration relies on Yowsup, which may have its own limitations and dependencies.
