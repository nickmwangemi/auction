const { Client } = require('whatsapp-web.js');
const express = require('express');
const bodyParser = require('body-parser');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(bodyParser.json());

// Initialize the WhatsApp client.
const client = new Client();

// Display QR code for authentication.
client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Scan the QR code above with your dedicated WhatsApp account.');
});

client.on('ready', () => {
    console.log('WhatsApp client is ready!');
});

client.initialize();

// HTTP endpoint to receive auction notifications from Django.
app.post('/notify', async (req, res) => {
    const { auction_number, title, winning_bid, winning_user } = req.body;

    // Compose the message.
    let message = `Auction Notification:\nAuction Number: ${auction_number}\n${title}\nWinning Bid: ${winning_bid}`;
    if (winning_user && winning_user.trim() !== "") {
        message += `\nWinner: ${winning_user}`;
    } else {
        message += `\nNo bids were placed.`;
    }

    // Read phone number from environment variable.
    const phoneNumber = process.env.WHATSAPP_PHONE_NUMBER;
    if (!phoneNumber) {
        console.error("Environment variable WHATSAPP_PHONE_NUMBER is not set.");
        return res.status(500).json({ error: 'WhatsApp phone number not configured' });
    }

    // whatsapp-web.js expects the chat ID in this format.
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

// Start the Express server.
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`WhatsApp notification service running on port ${PORT}`);
});
