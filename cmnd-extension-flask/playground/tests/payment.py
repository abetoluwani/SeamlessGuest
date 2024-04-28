from services.paystack.paystack import PaystackService
import json

# Example usage:
def initialize_payment():
    try:
        initialize_response = PaystackService.initialize({"amount": 5000, "email": "example@example.com"})
        print("Initialize Response:", initialize_response)
    except Exception as e:
        print("Error:", e)

def verifyPayment():
    try:
        verify_response = PaystackService.verify('j8uzadg7qo')
        print("Verify Response:", verify_response)
    except Exception as e:
        print("Error:", e)