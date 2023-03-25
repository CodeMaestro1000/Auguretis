import pika, json, logging
from utils import OAuthSerializer
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from core.settings import AMPQ_URL
from schemas import UserCreate
from db.repository import create_new_user, get_user_by_email, get_user_by_username
from db.database import Base
from routes.login import login_for_access_token, get_current_user_from_token
from core.settings import SQLALCHEMY_DATABASE_URL
from fastapi import HTTPException


logging.basicConfig(level=logging.INFO)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine) # create tables

params = pika.URLParameters(AMPQ_URL)

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main')

def callback(channel, method, properties: pika.BasicProperties, body):
    logging.info('========= Recieved in main ============')
    body = json.loads(body)
    response = ''
    if properties.content_type == "user create":
        try:
            user = UserCreate(**body)
            with Session(engine) as db:
                create_new_user(user, db)
            logging.info(f"{user.username} added to database....")
            response = "Success"
        except IntegrityError:
            logging.info(f"Create unsuccessful: User with {user.username} already exists....")
            response = "Failure: User Already exists"
        
        except Exception as e:
            response = f"Failure: {e}"

    elif properties.content_type == "login":
        try:
            form = OAuthSerializer(body['username'], body['password'])
            with Session(engine) as db:
                response = login_for_access_token(form, db)
                response = response['access_token']
                logging.info(f"{form.username} login successful....")
        except HTTPException:
            logging.info(f"Login failure: Invalid credentials")
            response = "Incorrect email/password"

    elif properties.content_type == "validate login":
        try:
            with Session(engine) as db:
                user = get_current_user_from_token(body, db) # body is a string representing token
                response = f"{user.username} logged in"
        except HTTPException:
            response = "No user logged in"
        logging.info(f"Login validation...")

    elif properties.content_type == "validate email":
        try:
            with Session(engine) as db:
                user =  get_user_by_email(db, body)
                if user is None:
                    response = "not found"
                else:
                    response = "exists"
        except HTTPException:
            response = "Something went wrong"
        logging.info(f"Email validation...")
    
    elif properties.content_type == "validate username":
        try:
            with Session(engine) as db:
                user =  get_user_by_username(db, body)
                if user is None:
                    response = "not found"
                else:
                    response = "exists"
        except HTTPException:
            response = "Something went wrong"
        logging.info(f"Username validation...")

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id = properties.correlation_id),
        body=response
    )
    
    channel.basic_ack(delivery_tag=method.delivery_tag)


# channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='main', on_message_callback=callback)

logging.info('Started Consuming')

channel.start_consuming()

channel.close()