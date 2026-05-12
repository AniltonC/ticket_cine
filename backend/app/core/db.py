from sqlmodel import Session, create_engine, select
from app.core.config import settings
from app import crud
from app.models import User, UserCreate

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))

# Garante que todos os models estão importados antes de inicializar o banco
# Caso contrário, o SQLModel pode falhar ao inicializar relacionamentos

def init_db(session: Session) -> None:
    # Tabelas criadas via Alembic migrations — não use create_all em produção
    # Para desenvolvimento sem migrations, descomente:
    # from sqlmodel import SQLModel
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)