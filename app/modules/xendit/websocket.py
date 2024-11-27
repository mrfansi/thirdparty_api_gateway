from typing import Dict, Any
from app.core.websocket import websocket_manager, ws_auth_required
import logging

logger = logging.getLogger(__name__)

@ws_auth_required
def handle_payment_subscribe(data):
    """Handle client subscription to payment updates"""
    payment_id = data.get('payment_id')
    if payment_id:
        room = f"xendit_payment_{payment_id}"
        join_room(room)
        emit('payment_subscribed', {'status': 'success', 'payment_id': payment_id})
        logger.info(f"Client subscribed to Xendit payment updates for payment_id: {payment_id}")
    else:
        emit('payment_subscribed', {'status': 'error', 'message': 'payment_id is required'})

@ws_auth_required
def handle_payment_unsubscribe(data):
    """Handle client unsubscription from payment updates"""
    payment_id = data.get('payment_id')
    if payment_id:
        room = f"xendit_payment_{payment_id}"
        leave_room(room)
        emit('payment_unsubscribed', {'status': 'success', 'payment_id': payment_id})
        logger.info(f"Client unsubscribed from Xendit payment updates for payment_id: {payment_id}")
    else:
        emit('payment_unsubscribed', {'status': 'error', 'message': 'payment_id is required'})

def init_xendit_websocket():
    """Initialize Xendit WebSocket handlers"""
    websocket_manager.register_handler('subscribe_xendit_payment', handle_payment_subscribe, namespace='/xendit')
    websocket_manager.register_handler('unsubscribe_xendit_payment', handle_payment_unsubscribe, namespace='/xendit')

async def notify_payment_update(payment_id: str, status: str, details: Dict[str, Any]):
    """Send payment update notification to subscribed clients"""
    room = f"xendit_payment_{payment_id}"
    websocket_manager.emit(
        'payment_update',
        {
            'payment_id': payment_id,
            'status': status,
            'details': details
        },
        room=room,
        namespace='/xendit'
    )
    logger.info(f"Xendit payment update notification sent for payment_id: {payment_id}")
