from sqlmodel import Session, SQLModel, select

from app.database import engine
from app.models import Hero, Mission, Team


def seed():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.exec(select(Team)).first():
            print("Database already seeded - nothing to do.")
            return

        avengers = Team(name="Avengers", headquarters="New York")
        xmen = Team(name="X-Men", headquarters="Westchester")
        sokovia = Mission(title="Battle of Sokovia")
        sentinels = Mission(title="Stop the Sentinels")

        session.add_all([
            Hero(name="Tony", age=45, secret_name="Iron Man", power="powered armor",
                 team=avengers, missions=[sokovia]),
            Hero(name="Natasha", age=35, secret_name="Black Widow", power="espionage",
                 team=avengers, missions=[sokovia]),
            Hero(name="Steve", age=105, secret_name="Captain America", power="super soldier",
                 team=avengers),
            Hero(name="Logan", age=150, secret_name="Wolverine", power="healing factor",
                 team=xmen, missions=[sentinels]),
            Hero(name="Jean", age=30, secret_name="Phoenix", power="telekinesis",
                 team=xmen, missions=[sentinels]),
            Hero(name="Peter", age=16, secret_name="Spider-Man", power="wall-crawling"),
        ])
        session.commit()
        print("Seeded 2 teams, 6 heroes, 2 missions.")


if __name__ == "__main__":
    seed()
