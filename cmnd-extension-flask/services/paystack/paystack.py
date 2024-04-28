import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()

class IPaystackService:
    def __init__(self):
        # paystack_live_secret_key = os.getenv('PAYSTACK_LIVE_SECRET_KEY')
        paystack_test_secret_key = os.getenv('PAYSTACK_TEST_SECRET_KEY')
        self.api_secret = paystack_test_secret_key

        if not self.api_secret:
            raise ValueError("PAYSTACK secret key environment variables are not set")

        self.config = {
            "headers": {
                "Authorization": f"Bearer {self.api_secret}",
                "Content-Type": "application/json",
                "cache-control": "no-cache",
            }
        }
        self.base_url = "https://api.paystack.co"
        self.percentage = 1.5 / 100  # 1.5%
        self.redirect_url = "https://standard.paystack.co/close"
        self.callback_url = "https://0e03-46-252-103-118.ngrok-free.app/payments/callback"

    def initialize(self, options):
        try:
            response = requests.post(
                f"{self.base_url}/transaction/initialize",
                json=options,
                headers=self.config["headers"],
            )
            response.raise_for_status()
            return response.json().get("data")
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to initialize transaction. Error: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def verify(self, ref, callback=None):
        try:
            response = requests.get(
                f"{self.base_url}/transaction/verify/{ref}",
                headers=self.config["headers"],
            )
            response.raise_for_status()
            data = response.json().get("data")
            if callback:
                callback(data)
            return data
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to verify transaction. Error: {str(e)}"
            logging.error(error_msg)
            raise Exception(error_msg)

    def get_amount(self, amount, percentage=None):
        percentage = percentage or self.percentage
        additional_fees = 10000 if amount > 250000 else 0
        fee = amount * percentage + additional_fees
        new_amount = amount - fee
        return new_amount


PaystackService = IPaystackService()