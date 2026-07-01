from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from invoice_generator import generate_invoice
import os

app = Flask(__name__)

# Create a folder to store PDFs
PDF_DIR = "static_pdfs"
os.makedirs(PDF_DIR, exist_ok=True)

@app.route("/webhook", methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"Incoming WhatsApp message: {incoming_msg}")

    try:
        parts = incoming_msg.split('|')
        client_name = parts[0].split(':')[1].strip()
        job_desc = parts[1].split(':')[1].strip()
        amount = parts[2].split(':')[1].strip()
    except Exception as e:
        print(f"Parsing failed: {e}")
        resp = MessagingResponse()
        resp.message("Invalid format. Use -> Client: Name | Job: Task | Amount: 000")
        return str(resp)

    filename = f"invoice_{client_name.replace(' ', '')}.pdf"
    filepath = os.path.join(PDF_DIR, filename)
    generate_invoice(client_name, job_desc, amount, output_path=filepath)

    # Bulletproof Production URL
    RENDER_BASE_URL = "https://whatsapp-invoice-generator-bvzh.onrender.com"
    public_pdf_url = f"{RENDER_BASE_URL}/pdf/{filename}"

    # Build the Twilio response with the media attachment
    resp = MessagingResponse()
    msg = resp.message(f"Invoice successfully generated for {client_name}.")
    msg.media(public_pdf_url) 
    
    return str(resp)

@app.route("/pdf/<filename>")
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename)

if __name__ == "__main__":
    app.run(port=5000, debug=True, use_reloader=False)loader=False)
