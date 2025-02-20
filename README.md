# Digital Trading Platform

## Technology Choices

- **Backend Framework**: Django
    - Chosen for its robustness, scalability, and built-in admin interface.
- **Database**: SQLite
    - Used in the deployed version available
      at [https://nickmwangemi.pythonanywhere.com/](https://nickmwangemi.pythonanywhere.com/) due to the limitations of
      the free-tier on PythonAnywhere.
    - Can be replaced with PostgreSQL or MySQL for production.
- **API Framework**: Django REST Framework (DRF)
    - Used to create a RESTful API for the application, allowing for easy integration with other services.
- **Templating Engine**: Django Template Language
    - Used for rendering HTML dynamically.
- **WhatsApp Integration**: whatsapp-web.js
    - Used for sending WhatsApp notifications via a Node.js environment.

## Setup and Running the Application

### Prerequisites

- Python 3.6+
- Django 3.2+
- Node.js and npm for WhatsApp Integration

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

- The deployed version of the application is available
  at [https://nickmwangemi.pythonanywhere.com/](https://nickmwangemi.pythonanywhere.com/).
- Due to the limitations of the free-tier on PythonAnywhere, SQLite is used as the database.

### Running the WhatsApp Notification Service

### Prerequisites

- Node.js and npm installed

### Steps

1. **Navigate to the `whatsapp-notifier` directory:**
   ```bash
    cd whatsapp-notifier
   ```
2. **Install Dependencies:**
    ```bash
     npm install
    ```
3. **Set the Environment Variable:**
   Ensure that the `WHATSAPP_PHONE_NUMBER` environment variable is set with the recipient's phone number. You can set it
   in your terminal session or in a .env file.
   ```bash
    export WHATSAPP_PHONE_NUMBER=1234567890
   ```
4. **Run the Notification Service:**
    ```bash
   node notifier.js
   ```
5. **Scan the QR Code:**

Upon running the script, a QR code will be generated. Scan this QR code with your dedicated WhatsApp account to
authenticate.

### Known Limitations

- **Rate Limiting**: Be aware of WhatsApp's rate limits to avoid being blocked.
- **Dependency on WhatsApp Web**: The integration relies on WhatsApp Web, which requires manual QR code scanning for
  authentication.
- **Session Management**: Maintaining a session with WhatsApp Web can be challenging, requiring re-authentication if the
  session expires.
- **Compatibility**: The library may not be fully compatible with all WhatsApp features, especially after updates to the
  WhatsApp web interface.
- **Security Concerns**: Using unofficial APIs can pose security risks and may violate WhatsApp's terms of service.
- **Legal Considerations**: Automated messaging may have legal implications, especially for commercial use.
- **No Official Support**: As an unofficial API, there is no official support, relying instead on community and
  maintainer updates.
- **Performance Issues**: Handling a large volume of messages can lead to performance issues.
- **Limited to Personal Use**: Best suited for personal projects or testing due to WhatsApp's terms of service
  restrictions.

## Assumptions

- The application assumes that each item has a volume of 1 for the MVP.
- The WhatsApp integration is set up with a valid WhatsApp account and credentials.
- The system time is accurate for determining auction statuses.

## Features Not Fully Implemented

- **Payment Processing**: The settlement stage does not include actual payment processing.
- **Advanced Bidding Features**: Features like proxy bidding or bid increments are not implemented.
- **Previous Price and Volumes**: Simulated for extra credit but not fully integrated into the UI.

```
