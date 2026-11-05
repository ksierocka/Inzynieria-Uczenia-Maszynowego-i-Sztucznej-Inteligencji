from sqlalchemy import create_engine, select, update, delete, func
from sqlalchemy.orm import Session
from datetime import datetime
from models import Base, Experiment, DataPoint
import random

# Tworzenie połączenia z bazą SQLite
engine = create_engine("sqlite:///test.db", echo=True)

# Tworzenie zdefiniowanych tabel wraz z plikiem bazy danych 

# Base.metadata.create_all(engine)

with Session(engine) as session:

    # Dodanie 2 wierszy do tabeli Experiments

    experiment1 = Experiment(
        title="experiment_1",
        created_at=datetime.now(),
        type=1,
        finished=False
    )

    experiment2 = Experiment(
        title="experiment_2",
        created_at=datetime.now(),
        type=2,
        finished=True
    )

    # Dodanie 10 wierszy do tabeli DataPoints

    # data_points = [
    #     DataPoint(
    #         real_value=random.uniform(0, 100),
    #         target_value=random.uniform(0, 100)
    #     )
    #     for _ in range(10)
    # ]

    # Tworzenie 20 DataPoints - 10 dla jednego eksperymentu, 1- dla drugiego

    for _ in range(10):
        experiment1.data_points.append(DataPoint(
            real_value=round(random.uniform(0, 100), 2),
            target_value=round(random.uniform(0, 100), 2),
        ))

        experiment2.data_points.append(DataPoint(
            real_value=round(random.uniform(0, 100), 2),
            target_value=round(random.uniform(0, 100), 2),
        ))

    session.add_all([experiment1, experiment2])
    # session.add_all(data_points)

    # Pobranie danych i wyświetlanie informacji o nich 

    experiments = session.scalars(select(Experiment)).all()
    data_points = session.scalars(select(DataPoint)).all()

    for exp in experiments:
        print(exp.id, exp.title, exp.created_at, exp.type, exp.finished)

    for point in data_points:
        print(point.id, point.real_value, point.target_value)

    print(len(data_points))
    print(type(data_points[0]))
    print(data_points[0].real_value)
    print(data_points[0].target_value)

    # Aktualizacja wszystkich wierszy Experiment poprzez ustawienie finished na True

    stmt_update = update(Experiment).values(finished=True)
    session.execute(stmt_update)


    # Suma i średnia DataPoint dla każdego eksperymentu

    stmt_statistics = (
        select(
            Experiment.title,
            func.sum(DataPoint.real_value).label("sum_real"),
            func.avg(DataPoint.real_value).label("avg_real"),
            func.sum(DataPoint.target_value).label("sum_target"),
            func.avg(DataPoint.target_value).label("avg_target")
        )
        .join(Experiment.data_points)
        .group_by(Experiment.id)
    )

    results = session.execute(stmt_statistics).all()

    for row in results:
        print(f"\nEksperyment: {row.title}")
        print(f"Suma real_value: {row.sum_real:.2f}")
        print(f"Średnia real_value: {row.avg_real:.2f}")
        print(f"Suma target_value: {row.sum_target:.2f}")
        print(f"Średnia target_value: {row.avg_target:.2f}")


    # Usunięcie wszytkich wierszy z obu tabel 

    session.execute(delete(DataPoint))
    session.execute(delete(Experiment))
    session.commit()





