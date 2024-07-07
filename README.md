# erc20-standard-detector

### About
This project is a service for managing status ERC20 standart.
Service works with init data in database

Service for:
- analyze existing contracts in database
  - is erc20 (True/False)
  - status
    - WAITS PROCESSING
    - PROCESSING
    - PROCESSED
    - FAILED
- update fields of contract

## Configuration
Configuration is stored in `.env`, for examples see `.default.env`

## Installing on a local machine
This project requires python 3.11. Python virtual environment should be installed and activated.
 Dependencies are managed by [poetry](https://python-poetry.org/) with requirements stored in `pyproject.toml`.

Install requirements:

```bash
make install
```

RUN:
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

make run
```
