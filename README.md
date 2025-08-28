# xwire

Smart, recursive Inversion of Control for Python.

xwire is a **lightweight, function-first dependency injection framework** designed to let you focus on your **real application logic**, not on wiring dependencies. Declare what you need, and xwire handles the rest.

---

## Features

- **Autowiring & Recursive Resolution**  
  Dependencies are automatically discovered and resolved recursively based on function parameters.

- **Minimalistic & Pythonic**  
  No heavy container boilerplate, no annotations required. Just `@injectable` for providers.

- **Environment-Aware**  
  Configure injectables with environments (`environ="test"`) to easily switch contexts.

- **Composable & Flexible**  
  Supports both built-in injectables and optional explicit injection (`@inject`) when needed.

- **Framework-Agnostic**  
  Works with plain functions, making it easy to integrate into any Python project.

---

## Installation

xwire is **currently under development**. To install locally for development:

```bash
uv pip install -e .
```


## Basic Usage

Define your dependencies using `@injectable`. xwire will automatically resolve them based on function parameters.

```python

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

```


## How it Works

xwire lets you focus on your application logic while it handles dependency wiring automatically.  

Imagine your app depends on several external services, such as a database, an API, or a payment system. Normally, testing your functions would require connecting to these services—but often you just want to run your code with **fake or simplified implementations**.

With xwire, you can define **environment-specific injectables** and selectively choose which implementations to use when running your application. This makes testing and development safe, fast, and flexible.

For example, to run your app using fake users and fake payments:

```bash
python main.py --dependencies='fake_users,fake_payments'
``` 


xwire automatically **resolves** the dependencies for you, so you don't need to worry about it.


If you are deploying to production, you can:

```bash
python main.py --dependencies='prod'
```


## TODOs

### Core Framework
- [ ] Improve recursive dependency resolution for nested callables
- [ ] Handle class-based injectables alongside function-based ones
- [ ] Add better error messages when a dependency cannot be resolved
- [ ] Support optional dependencies with default fallback values
- [ ] Implement lifecycle management (singleton vs new instance per injection)

### Environment & Configuration
- [ ] Enhance `--dependencies` parsing (support spaces, different separators)
- [ ] Support multiple environments at once (`test`, `dev`, `prod`)
- [ ] Add config file support for environment selection
- [ ] Allow dynamic runtime switching of environment

### CLI & Developer Experience
- [ ] Provide a CLI command to list all registered injectables and their environments
- [ ] Add verbose/debug mode for seeing dependency resolution steps
- [ ] Include helpful warnings for overridden dependencies

### Testing & QA
- [ ] Write unit tests for `injectable` decorator
- [ ] Write integration tests for `run()` with multiple environments
- [ ] Test edge cases: circular dependencies, missing injectables

### Documentation & Examples
- [ ] Expand README with more usage patterns
- [ ] Add visual diagrams for dependency resolution
- [ ] Include real-world examples (e.g., API client, caching layer)
- [ ] Create a tutorial for new users showing environment switching

### Optional / Advanced
- [ ] Support asynchronous dependencies (`async def`)
- [ ] Add type-based resolution (resolve by return type in addition to parameter name)
- [ ] Implement dependency scoping (request/session/global)
- [ ] Provide automatic mocking for testing environments
