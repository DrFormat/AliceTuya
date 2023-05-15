from uvicorn import workers


class UvicornWorker(workers.UvicornWorker):
    CONFIG_KWARGS = {"loop": "auto", "http": "auto", "forwarded_allow_ips": "*", "log_config": "logging.yaml"}
