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

- The deployed version of the application is available at [https://nickmwangemi.pythonanywhere.com/](https://nickmwangemi.pythonanywhere.com/).
- Due to the limitations of the free-tier on PythonAnywhere, SQLite is used as the database.

### WhatsApp Integration Setup

1. **Install Node.js and npm**:
   - Follow the instructions on the [official Node.js website](https://nodejs.org/) to install Node.js and npm.

2. **Install whatsapp-web.js**:
   ```bash
   npm install whatsapp-web.js qrcode-terminal express body-parser nodemon
   ```

3. **Set Up WhatsApp Notification Script**:
   - Create a new directory for your Node.js project and initialize it:
     ```bash
     mkdir whatsapp-notifier
     cd whatsapp-notifier
     npm init -y
     ```
   - Create a script (e.g., `notifier.js`) to handle WhatsApp notifications:
     ```javascript
     const { Client } = require('whatsapp-web.js');
     const express = require('express');
     const bodyParser = require('body-parser');
     const qrcode = require('qrcode-terminal');

     const app = express();
     app.use(bodyParser.json());

     const client = new Client();

     client.on('qr', (qr) => {
         qrcode.generate(qr, { small: true });
         console.log('Scan the QR code above with your dedicated WhatsApp account.');
     });

     client.on('ready', () => {
         console.log('WhatsApp client is ready!');
     });

     client.initialize();

     app.post('/notify', async (req, res) => {
         const { auction_number, title, winning_bid, winning_user } = req.body;
         let message = `Auction Notification:\nAuction Number: ${auction_number}\n${title}\nWinning Bid: ${winning_bid}`;
         if (winning_user && winning_user.trim() !== "") {
             message += `\nWinner: ${winning_user}`;
         } else {
             message += `\nNo bids were placed.`;
         }

         const phoneNumber = process.env.WHATSAPP_PHONE_NUMBER;
         if (!phoneNumber) {
             console.error("Environment variable WHATSAPP_PHONE_NUMBER is not set.");
             return res.status(500).json({ error: 'WhatsApp phone number not configured' });
         }

         const chatId = `${phoneNumber}@c.us`;

         try {
             await client.sendMessage(chatId, message);
             console.log(`Notification sent for auction ${auction_number}`);
             res.status(200).json({ status: 'Message sent' });
         } catch (error) {
             console.error('Error sending WhatsApp message:', error);
             res.status(500).json({ error: 'Failed to send message' });
         }
     });

     const PORT = process.env.PORT || 3000;
     app.listen(PORT, () => {
         console.log(`WhatsApp notification service running on port ${PORT}`);
     });
     ```

4. **Run the WhatsApp Notification Script**:
   ```bash
   nodemon notifier.js
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

- **whatsapp-web.js**: A JavaScript library for interacting with WhatsApp Web.

### Setup Instructions

1. **Install Node.js and npm**: Ensure you have Node.js and npm installed.
2. **Install whatsapp-web.js**: Use npm to install the library.
3. **Create and Run the Script**: Set up a script to send WhatsApp messages using the library.
4. **Environment Variables**: Ensure that the `WHATSAPP_PHONE_NUMBER` environment variable is set with the recipient's phone number.


### Known Limitations

- **Rate Limiting**: Be aware of WhatsApp's rate limits to avoid being blocked.
- **Dependency on WhatsApp Web**: The integration relies on WhatsApp Web, which requires manual QR code scanning for authentication.
- **Session Management**: Maintaining a session with WhatsApp Web can be challenging, requiring re-authentication if the session expires.
- **Compatibility**: The library may not be fully compatible with all WhatsApp features, especially after updates to the WhatsApp web interface.
- **Security Concerns**: Using unofficial APIs can pose security risks and may violate WhatsApp's terms of service.
- **Legal Considerations**: Automated messaging may have legal implications, especially for commercial use.
- **No Official Support**: As an unofficial API, there is no official support, relying instead on community and maintainer updates.
- **Performance Issues**: Handling a large volume of messages can lead to performance issues.
- **Limited to Personal Use**: Best suited for personal projects or testing due to WhatsApp's terms of service restrictions.

```