from sqlalchemy import create_engine, Integer, String, DateTime, Boolean, Float, select, update, delete, ForeignKey, Column, func, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from datetime import datetime


class Base(DeclarativeBase):
    pass

association_table = Table(
    "subject_experiment",
    Base.metadata,
    Column("subject_id", ForeignKey("Subject.id"), primary_key=True),
    Column("experiment_id", ForeignKey("Experiment.id"), primary_key=True)
)

# Tworzenie tabel Experiment i DataPoints

class Experiment(Base):
    __tablename__ = "Experiment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime)
    type: Mapped[int] = mapped_column(Integer)
    finished: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    # Relacja 1-do-wielu, by jeden Experiment posiadał wiele DataPoint'ów

    data_points = relationship("DataPoint", back_populates="experiment")

    # Relacja wiele-do-wielu z Subject
    subjects = relationship("Subject", secondary=association_table, back_populates="experiments")


class DataPoint(Base):
    __tablename__ = "DataPoint"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    real_value: Mapped[float] = mapped_column(Float)
    target_value: Mapped[float] = mapped_column(Float)

    # Relacja 1-do-wielu, by jeden Experiment posiadał wiele DataPoint'ów

    experiment_id = Column(Integer, ForeignKey("Experiment.id"))
    experiment = relationship("Experiment", back_populates="data_points")


# Tworzenie tabeli Subject

class Subject(Base):
    __tablename__ = "Subject"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    gdpr_accepted: Mapped[bool] = mapped_column(Boolean, default=False, server_default="0")

    # Relacja wiele-do-wielu z Experiment
    experiments = relationship("Experiment", secondary=association_table, back_populates="subjects")