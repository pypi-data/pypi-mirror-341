from .utils.prepare_model import download, prepare_offline_models, prepare_online_models
from .utils.benchmark import (
    benchmark_vad,
    benchmark_asr,
    benchmark_pipeline,
    benchmark_loader,
)
from jsonargparse import CLI


commands = {
    "prepare": {
        "offline": prepare_offline_models,
        "online": prepare_online_models,
    },
    "download": download,
    "benchmark": {
        "vad": benchmark_vad,
        "asr": benchmark_asr,
        "pipeline": benchmark_pipeline,
        "loader": benchmark_loader,
        "_help": "benchmark",
    },
}


def run():
    """命令行"""
    CLI(components=commands)


if __name__ == "__main__":
    run()
