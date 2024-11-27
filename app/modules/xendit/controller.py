from flask import Blueprint, request, jsonify
from .schemas import (
    CustomerRequest, PaymentMethodRequest, PaymentRequest,
    PaymentMethodResponse, PaymentResponse
)
from .use_cases import XenditUseCase
from .websocket import notify_payment_update
from app.core.third_party import ThirdPartyAPIException

bp = Blueprint('xendit', __name__)
xendit_use_case = None

def init_use_case():
    global xendit_use_case
    if xendit_use_case is None:
        xendit_use_case = XenditUseCase()

@bp.before_app_request
def before_request():
    init_use_case()

# Customer Routes
@bp.route('/customers', methods=['POST'])
async def create_customer():
    try:
        customer_data = CustomerRequest(**request.json)
        result = await xendit_use_case.create_customer(customer_data)
        return jsonify(result), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/customers/<customer_id>', methods=['GET'])
async def get_customer(customer_id: str):
    try:
        result = await xendit_use_case.get_customer(customer_id)
        return jsonify(result), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# Payment Method Routes
@bp.route('/payment-methods', methods=['POST'])
async def create_payment_method():
    try:
        payment_method_data = PaymentMethodRequest(**request.json)
        result = await xendit_use_case.create_payment_method(payment_method_data)
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payment-methods/<payment_method_id>', methods=['GET'])
async def get_payment_method(payment_method_id: str):
    try:
        result = await xendit_use_case.get_payment_method(payment_method_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payment-methods/<payment_method_id>', methods=['PATCH'])
async def update_payment_method(payment_method_id: str):
    try:
        result = await xendit_use_case.update_payment_method(payment_method_id, request.json)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payment-methods', methods=['GET'])
async def list_payment_methods():
    try:
        result = await xendit_use_case.list_payment_methods(request.args.to_dict())
        return jsonify([method.dict() for method in result]), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payment-methods/<payment_method_id>/expire', methods=['POST'])
async def expire_payment_method(payment_method_id: str):
    try:
        result = await xendit_use_case.expire_payment_method(payment_method_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# Payment Routes
@bp.route('/payments', methods=['POST'])
async def create_payment():
    try:
        payment_data = PaymentRequest(**request.json)
        result = await xendit_use_case.create_payment(payment_data)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payments/<payment_id>', methods=['GET'])
async def get_payment(payment_id: str):
    try:
        result = await xendit_use_case.get_payment(payment_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/payments', methods=['GET'])
async def list_payments():
    try:
        result = await xendit_use_case.list_payments(request.args.to_dict())
        return jsonify([payment.dict() for payment in result]), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# Card Payment Routes
@bp.route('/card-payments', methods=['POST'])
async def create_card_payment():
    try:
        result = await xendit_use_case.create_card_payment(request.json)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/card-payments/<payment_id>/capture', methods=['POST'])
async def capture_card_payment(payment_id: str):
    try:
        result = await xendit_use_case.capture_card_payment(payment_id, request.json)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/card-payments/<payment_id>/refund', methods=['POST'])
async def refund_card_payment(payment_id: str):
    try:
        result = await xendit_use_case.refund_card_payment(payment_id, request.json)
        await notify_payment_update(result)
        return jsonify(result), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# eWallet Routes
@bp.route('/ewallet-charges', methods=['POST'])
async def create_ewallet_charge():
    try:
        result = await xendit_use_case.create_ewallet_charge(request.json)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/ewallet-charges/<charge_id>', methods=['GET'])
async def get_ewallet_charge_status(charge_id: str):
    try:
        result = await xendit_use_case.get_ewallet_charge_status(charge_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# QR Code Routes
@bp.route('/qr-codes', methods=['POST'])
async def create_qr_code():
    try:
        result = await xendit_use_case.create_qr_code(request.json)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/qr-codes/<qr_code_id>', methods=['GET'])
async def get_qr_code_status(qr_code_id: str):
    try:
        result = await xendit_use_case.get_qr_code_status(qr_code_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

# Over-the-Counter Routes
@bp.route('/otc-payments', methods=['POST'])
async def create_otc_payment():
    try:
        result = await xendit_use_case.create_otc_payment(request.json)
        await notify_payment_update(result.dict())
        return jsonify(result.dict()), 201
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/otc-payments/<payment_id>', methods=['GET'])
async def get_otc_payment_status(payment_id: str):
    try:
        result = await xendit_use_case.get_otc_payment_status(payment_id)
        return jsonify(result.dict()), 200
    except ThirdPartyAPIException as e:
        return jsonify({'error': str(e)}), 400
