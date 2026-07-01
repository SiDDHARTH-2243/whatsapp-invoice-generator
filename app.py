from flask import Flask, request, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse
from invoice_generator import generate_invoice
import os

app = Flask(__name__)

# Create a folder to store PDFs so we can serve them to Twilio later
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

    # Hardcoded Ngrok URL. 
    # Critical Note: On the free tier, this URL changes every time you restart Ngrok.
    # If you close Ngrok tomorrow, you MUST update this variable with your new URL.
    # Automatically detects the current public URL (works on Ngrok OR Cloud Production)
    public_base_url = f"{request.scheme}://{request.host}"
    public_pdf_url = f"{public_base_url}/pdf/{filename}"
    public_pdf_url = f"{NGROK_BASE_URL}/pdf/{filename}"

    # Build the Twilio response with the media attachment
    resp = MessagingResponse()
    msg = resp.message(f"Invoice successfully generated for {client_name}.")
    msg.media(public_pdf_url) 
    
    return str(resp)

# 5. Route to serve the PDF to Twilio
@app.route("/pdf/<filename>")
def serve_pdf(filename):
    return send_from_directory(PDF_DIR, filename)

if __name__ == "__main__":
    # Running directly bypasses your Flask PATH error
    app.run(port=5000, debug=True, use_reloader=False)