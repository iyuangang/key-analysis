import click
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models
from .auth import get_password_hash
import uuid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("username")
@click.argument("password")
@click.option("--email", default=None)
@click.option("--full-name", default=None)
def create_user(username: str, password: str, email: str = None, full_name: str = None):
    """创建新用户"""
    db = next(get_db())

    # 检查用户是否已存在
    if db.query(models.User).filter(models.User.username == username).first():
        click.echo(f"用户 {username} 已存在")
        return

    # 创建新用户
    user = models.User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=get_password_hash(password),
    )

    db.add(user)
    db.commit()
    click.echo(f"用户 {username} 创建成功")


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    cli()
