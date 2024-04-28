from flask import Flask, request, jsonify, abort, Blueprint, redirect
from services.properties.properties import PropertyService
from services.paystack.paystack import PaystackService

# Create Flask app instance
app = Blueprint('payments', __name__)

@app.route("/callback", methods=['GET'])
def transaction_callback():
    reference = request.args.get('reference')
    if not reference:
        abort(400, description="Invalid request: 'reference' parameter is required")

    try:
        # Verify payment with Paystack
        payment = PaystackService.verify(reference)

        # Check payment status
        if payment['status'] != "success":
            return jsonify({ 'error': f"Transaction {payment.status}", 'payment': payment }), 403
        
        metadata = payment['metadata']
        id = metadata['room_number']
        email = metadata['email']

        print(metadata)
        property = PropertyService.get_by_id(id)


        print(id, email, property)
        if property['available'] == False:
            return jsonify({ 'error': "Property is not Available", 'transaction': payment }), 403

        newPurchase = PropertyService.purchase(id, email)
        print('<<=', newPurchase , '<<=')
        return redirect(PaystackService.redirect_url)

    except Exception as e:
        print(e)
        abort(500, description=str(e))


# payments/callback?ref=121323123 /GET query string -> ref

# {'id': 3748450718, 'domain': 'test', 'status': 'success', 'reference': 'j8uzadg7qo', 'receipt_number': None, 'amount': 5000, 'message': None, 'gateway_response': 'Successful', 'paid_at': '2024-04-27T21:06:23.000Z', 'created_at': '2024-04-27T21:05:43.000Z', 'channel': 'card', 'currency': 'NGN', 'ip_address': '46.252.103.118', 'metadata': '', 'log': {'start_time': 1714251979, 'time_spent': 4, 'attempts': 1, 'errors': 0, 'success': True, 'mobile': False, 'input': [], 'history': [{'type': 'action', 'message': 'Attempted to pay with card', 'time': 4}, {'type': 'success', 'message': 'Successfully paid with card', 'time': 4}]}, 'fees': 75, 'fees_split': None, 'authorization': {'authorization_code': 'AUTH_om7c7egt4m', 'bin': '408408', 'last4': '4081', 'exp_month': '12', 'exp_year': '2030', 'channel': 'card', 'card_type': 'visa ', 'bank': 'TEST BANK', 'country_code': 'NG', 'brand': 'visa', 'reusable': True, 'signature': 'SIG_Mzl7gU6JFaNRm6TB3hDL', 'account_name': None}, 'customer': {'id': 166477808, 'first_name': None, 'last_name': None, 'email': 'example@example.com', 'customer_code': 'CUS_agrm6gmghlpg00m', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': None, 'split': {}, 'order_id': None, 'paidAt': '2024-04-27T21:06:23.000Z', 'createdAt': '2024-04-27T21:05:43.000Z', 'requested_amount': 5000, 'pos_transaction_data': None, 'source': None, 'fees_breakdown': None, 'connect': None, 'transaction_date': '2024-04-27T21:05:43.000Z', 'plan_object': {}, 'subaccount': {}}