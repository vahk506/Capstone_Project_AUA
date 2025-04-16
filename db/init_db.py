import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# ✅ Load environment variables from .env
load_dotenv()

from flask import Flask
from models import db
from models.model import AssistantConversation
from models.model import AssistantConversationThread
from models.model import AssistantConversationMessage

# ✅ Setup Flask app with config from .env
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getenv('DATABASE_PATH')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    print("🔧 Creating tables...")
    db.create_all()
    print("✅ Tables created.")

    # Insert sample conversation
    conversation = AssistantConversation(
        user_id=1,
        booking_id=None,
        subject="Test Subject",
        sender_email="user@example.com",
        conversation_id="openai-123456",
        attributes={"intent": "booking"},
        clean_attributes={"intent": "booking"},
    )
    db.session.add(conversation)
    db.session.commit()
    print(f"✅ Inserted Conversation ID: {conversation.id}")

    # Insert related thread
    thread = AssistantConversationThread(
        assistant_conversation_id=conversation.id,
        thread_id="thread-openai-xyz",
        thread_type="openai",
    )
    db.session.add(thread)
    db.session.commit()
    print(f"✅ Inserted Thread ID: {thread.id}")

    # Insert related message
    message = AssistantConversationMessage(
        assistant_conversation_id=conversation.id,
        message_id="msg-openai-abc",
        received_at=datetime.utcnow(),
        mail_body="Hi, I want to book a room.",
        reply_mail="Sure, I can help with that!"
    )
    db.session.add(message)
    db.session.commit()
    print(f"✅ Inserted Message ID: {message.id}")
