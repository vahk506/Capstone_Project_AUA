from datetime import datetime
from models import db  # use Flask-SQLAlchemy's db, not declarative_base()
from zoneinfo import ZoneInfo  # ✅ built-in from Python 3.9+


class AssistantConversation(db.Model):
    __tablename__ = "assistant_conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)
    booking_id = db.Column(db.Integer, nullable=True)
    subject = db.Column(db.String(255))
    sender_email = db.Column(db.String(255))
    conversation_id = db.Column(db.String(255))
    attributes = db.Column(db.JSON)
    clean_attributes = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))
    updated_at = db.Column( db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")), onupdate=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))

    threads = db.relationship("AssistantConversationThread", back_populates="conversation", cascade="all, delete-orphan")
    messages = db.relationship("AssistantConversationMessage", back_populates="conversation", cascade="all, delete-orphan")


class AssistantConversationThread(db.Model):
    __tablename__ = "assistant_conversation_threads"

    id = db.Column(db.Integer, primary_key=True)
    assistant_conversation_id = db.Column(db.Integer, db.ForeignKey("assistant_conversations.id"), nullable=False)
    thread_id = db.Column(db.String(255))
    thread_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))
    updated_at = db.Column( db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")), onupdate=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))

    conversation = db.relationship("AssistantConversation", back_populates="threads")


class AssistantConversationMessage(db.Model):
    __tablename__ = "assistant_conversation_messages"

    id = db.Column(db.Integer, primary_key=True)
    assistant_conversation_id = db.Column(db.Integer, db.ForeignKey("assistant_conversations.id"), nullable=False)
    message_id = db.Column(db.String(255))
    received_at = db.Column(db.DateTime)
    mail_body = db.Column(db.Text)
    reply_mail = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))
    updated_at = db.Column( db.DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Yerevan")), onupdate=lambda: datetime.now(ZoneInfo("Asia/Yerevan")))

    conversation = db.relationship("AssistantConversation", back_populates="messages")
