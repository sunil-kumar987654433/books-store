from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String, Integer, Column, Boolean, DateTime, text, func
from datetime import datetime, date, timedelta, timezone
import uuid
from typing import Optional, List
import sqlalchemy.dialects.postgresql as pg
from src.books import models


class User(SQLModel, table=True):
    __tablename__ = "auth_users"
    # __table_args__ = {"schema": "auth"}

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            unique=True,
            primary_key=True,
            server_default=text("gen_random_uuid()")
        ),
        default_factory=uuid.uuid4
    )
    username: str = Field(description="username of user", nullable=True, index=True)
    email: str = Field(description="email of user", unique=True, index=True)
    first_name: str = Field(
        default=None,
        description="first name of user", 
        sa_column=Column(
            pg.VARCHAR,
                nullable=True
            )
    )
    last_name: str = Field(
        default=None,
        description="last name of user",
          sa_column=Column(
              pg.VARCHAR,
                nullable=True
            )
    )
    is_verfied: bool =  Field(
        default=False,

    )
    is_active: bool=  Field(
            default=True
        )
    password_hash: str = Field(exclude=True, nullable=True)               
    is_admin: bool =  Field(
            default=False
        )
    is_superuser: bool =  Field(
            default=False
        )
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(),
            nullable=False
        )
    )
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR, default='user',
            nullable=False
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    books: List['models.Book'] = Relationship(back_populates='user', sa_relationship_kwargs={"lazy": 'selectin'})


    
    def __repr__(self):
        return f"<User (email: {self.email})>"