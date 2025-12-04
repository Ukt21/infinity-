from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timedelta

engine = create_engine("sqlite:///database.sqlite", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # Telegram user_id
    language = Column(String, default="ru")  # ru / uz

    # Выбор моделей
    text_model = Column(String, default="chatgpt")      # chatgpt / claude / gemini / grok / llama
    image_model = Column(String, default="midjourney")  # midjourney / flux / sdxl / seedream / upscale

    # Подписка
    subscription = Column(String, default="free")       # free / premium / pro
    subscription_until = Column(DateTime, nullable=True)

    def has_subscription(self) -> bool:
        return (
            self.subscription != "free"
            and self.subscription_until is not None
            and self.subscription_until > datetime.utcnow()
        )


def init_db():
    Base.metadata.create_all(bind=engine)


def get_session():
    return SessionLocal()


def get_or_create_user(user_id: int) -> User:
    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    finally:
        db.close()


def update_language(user_id: int, lang: str):
    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.language = lang
            db.commit()
    finally:
        db.close()


def set_text_model(user_id: int, model: str):
    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.text_model = model
            db.commit()
    finally:
        db.close()


def set_image_model(user_id: int, model: str):
    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.image_model = model
            db.commit()
    finally:
        db.close()


def set_subscription(user_id: int, tier: str, days: int = 0):
    db = get_session()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            user = User(id=user_id)
            db.add(user)
            db.commit()
            db.refresh(user)

        user.subscription = tier
        if days > 0:
            user.subscription_until = datetime.utcnow() + timedelta(days=days)
        else:
            user.subscription_until = None

        db.commit()
    finally:
        db.close()

