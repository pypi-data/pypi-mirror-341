from .server import serve


def main():
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to interact with RabbitMQ"
    )
    parser.add_argument("--rabbitmq-host", type=str, help="RabbitMQ host")
    parser.add_argument("--port", type=str, help="Port of the RabbitMQ host")
    parser.add_argument("--username", type=str, help="Username for the connection")
    parser.add_argument("--password", type=str, help="Password for the connection")
    parser.add_argument("--use-tls", type=bool, help="Is the connection amqps")
    parser.add_argument("--log-level", type=str, help="Log level, supports DEBUG|INFO|WARNING|ERROR, default to WARNING")

    args = parser.parse_args()
    asyncio.run(serve(
        rabbitmq_host=args.rabbitmq_host,
        port=args.port,
        username=args.username,
        password=args.password,
        use_tls=args.use_tls,
        log_level=args.log_level))


if __name__ == "__main__":
    main()
