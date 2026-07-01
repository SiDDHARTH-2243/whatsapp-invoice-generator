**Project Title: WhatsApp-to-PDF Invoice Engine

Architecture: Explain the data flow. (User WhatsApp -> Twilio Webhook -> Render Cloud Server -> Flask/Python Parsing -> FPDF2 Generation -> Twilio Media Response -> User WhatsApp).

Tech Stack: Python, Flask, FPDF2, Twilio API, Render, Gunicorn.

The Problem It Solves: "Small businesses need a zero-friction way to generate professional invoices directly from their phones without installing specialized software."

How to Test This Project
Join the Sandbox: Send the message join potatoes-hollow to the Twilio WhatsApp Sandbox number +14155238886.

Send an Invoice Request: Send a message in the following format:
Client: [Name] | Job: [Description] | Amount: [Value]

Receive the PDF: The system will process your request, generate a professional PDF invoice, and reply to your WhatsApp chat with the downloadable document.**
