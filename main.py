# pyright:reportGeneralTypeIssues=false
# pyright:reportUnknownArgumentType=false
# pyright:reportUnknownVariableType=false
# pyright:reportRedeclaration=false

import typing as tp
import xwire
import sqlite3

# real dependency
@xwire.injectable
def db_string() -> str:
    return 'sqlite:///prod.db'

# real dependency
@xwire.injectable
def dbcnx(db_string: str) -> tp.Any:
    return sqlite3.connect(db_string)

# real dependency
@xwire.injectable
def users(dbcnx: tp.Any) -> list[str]:
    return list(f'{i} - {user}' for i, user in enumerate(dbcnx))


@xwire.injectable(environ='fake_users')
def users(users: list[str]) -> list[str]:
    return ['u1', 'u2', 'u3']

# fake dependency
@xwire.injectable(environ='fake_payments')
def users(_) -> dict[str, int]:
    return {
        'u1': 100,
        'u2': 200,
    }

# real dependency
@xwire.injectable
def payments(dbcnx: tp.Any) -> dict[str, int]:
    return {
        user: payment 
        for user, payment in dbcnx.execute(
            'SELECT user, sum(amount) FROM payments groyup by user'
            )
    }   

# ---------- Entry Point ----------
def render(users: list[str], payments: dict[str, int]):
    for user in users:
        print(f'The user {user} has {payments[user]} payments')


if __name__ == '__main__':
    xwire.run(render)


# Now, you can select which code will run based on the environment and dependencies
# python main.py --dependencies='fake_users, fake_payments'
# or
# python main.py --dependencies='fake_payments' 
