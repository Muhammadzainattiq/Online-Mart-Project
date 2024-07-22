import json
import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from sqlalchemy import select
from sqlmodel import Session
from app.db.db_connection import engine
from app.models.payment_models import Payment, PaymentStatus, PaymentUser, PaymentMethod
from app.utils import get_user_card_credentials, perform_payment, return_payment
from app.kafka.producer import KAFKA_PRODUCER, produce_message

async def consume_events(producer: AIOKafkaProducer):
    consumer = AIOKafkaConsumer(
        "user_payment_details_added",
        'order_processing',
        'order_returned',
        bootstrap_servers='broker:19092',
        group_id="payment_service_group",
        auto_offset_reset='earliest'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode('utf-8'))
            print("Event Consumed: ", event)
            await handle_event(event, producer)
    finally:
        await consumer.stop()

async def handle_event(event, producer: AIOKafkaProducer):
    event_type = event.get("event_type")
    if event_type == "order_processing":
        await handle_order_processing(event, producer)
    elif event_type == "order_returned":
        await handle_order_returned(event, producer)
    elif event_type == "user_payment_details_added":
        await handle_user_payment_details_added(event)

async def handle_order_processing(event, producer: AIOKafkaProducer):
    user_id = event.get("user_id")
    order_id = event.get("order_id")
    total_amount = event.get("total_amount")
    payment_method = event.get("payment_method")

    user_card_creds = await get_user_card_credentials(user_id)
    print("Here are the extracted user card credentials: ", user_card_creds)

    with Session(engine) as session:
        # Create a new payment record
        payment = Payment(
            order_id=order_id,
            user_id=user_id,
            amount=total_amount,
            status=PaymentStatus.PENDING,
            method=PaymentMethod(payment_method)
        )
        session.add(payment)
        session.commit()
        session.refresh(payment)

    if user_card_creds is not None:
        is_successful = await perform_payment(user_card_creds, total_amount)
        if is_successful:
            print("Payment successful")
            with Session(engine) as session:
                payment = session.get(Payment, payment.id)
                if payment:
                    payment.status = PaymentStatus.COMPLETED
                    session.add(payment)
                    session.commit()

            event_dict = {
                "event_type": "payment_successful",
                "user_id": user_id,
                "order_id": order_id,
                "total_amount": total_amount,
                "payment_method": payment_method
            }
            await produce_message("payment_successful", event_dict, producer)
        else:
            print("Payment failed")
            with Session(engine) as session:
                payment = session.get(Payment, payment.id)
                if payment:
                    payment.status = PaymentStatus.FAILED
                    session.add(payment)
                    session.commit()

            event_dict = {
                "event_type": "payment_failed",
                "user_id": user_id,
                "order_id": order_id,
                "total_amount": total_amount,
                "payment_method": payment_method
            }
            await produce_message("payment_failed", event_dict, producer)

async def handle_order_returned(event, producer: AIOKafkaProducer):
    user_id = event.get("user_id")
    order_id = event.get("order_id")
    total_amount = event.get("total_amount")
    payment_method = event.get("payment_method")

    user_card_creds = await get_user_card_credentials(user_id)

    if user_card_creds is not None:
        is_successful = await return_payment(user_card_creds, total_amount)
        if is_successful:
            print("Payment returned successfully")
            with Session(engine) as session:
                payment = session.exec(select(Payment).where(Payment.order_id == order_id)).first()
                if payment:
                    (payment,) = payment
                    payment_instance = session.get(Payment, payment.id)  # Get the instance to modify
                    payment_instance.status = PaymentStatus.RETURNED
                    session.add(payment_instance)
                    session.commit()

            event_dict = {
                "event_type": "payment_returned_successful",
                "user_id": user_id,
                "order_id": order_id,
                "total_amount": total_amount,
                "payment_method": payment_method
            }
            await produce_message("payment_returned_successful", event_dict, producer)

async def handle_user_payment_details_added(event):
    user_id = event.get("user_id")
    card_number = event.get("card_number")
    card_cvc = event.get("card_cvc")
    card_expiry = event.get("card_expiry")

    with Session(engine) as session:
        db_payment_user = PaymentUser(
            user_id=user_id,
            card_number=card_number,
            card_cvc=card_cvc,
            card_expiry=card_expiry
        )
        session.add(db_payment_user)
        session.commit()
        session.refresh(db_payment_user)
        print(f"Payment details added for user: {db_payment_user}")