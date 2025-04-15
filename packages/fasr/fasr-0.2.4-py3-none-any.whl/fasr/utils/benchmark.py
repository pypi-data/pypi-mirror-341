from pathlib import Path
import time
from loguru import logger
from tqdm import trange
from fasr import AudioList
from typing import Literal


def check_input_and_load(input: str) -> AudioList:
    """检查输入文件是否存在.

    Args:
        input (str): 输入文件路径.
    """
    if not Path(input).exists():
        raise FileNotFoundError(f"{input} not found")
    if Path(input).is_dir():
        files = [
            str(p) for p in Path(input).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
        audios = AudioList.from_urls(files)
    else:
        if Path(input).suffix == ".al":
            audios = AudioList.load_binary(input)
        elif Path(input).suffix == ".txt":
            with open(input, "r") as f:
                urls = f.readlines()
                urls = [url.strip() for url in urls]
                audios = AudioList.from_urls(urls)
    return audios


def benchmark_pipeline(
    input: str,
    batch_size: int = 2,
    num_threads: int = 2,
    batch_size_s: int = 100,
    num_samples: int | None = None,
    asr_model: str = "paraformer",
    vad_model: str = "fsmn",
    punc_model: str = "ct_transformer",
    compile: bool = False,
):
    """对比测试fasr与funasr pipeline(load -> vad -> asr -> punc)的性能.

    Args:
        input (str): 测试文件，格式可以为一行为一个url的txt文件可以为AudioList保存格式.
        batch_size (int, optional): 批处理大小. Defaults to 2.
        batch_size_s (int, optional): asr模型的批处理大小. Defaults to 100.
        num_threads (int, optional): 并行处理的工作线程数. Defaults to 2.
        num_samples (int, optional): 采样数量. Defaults to 100.
        asr_model (str, optional): asr模型. Defaults to "paraformer".
        vad_model (str, optional): vad模型. Defaults to "fsmn".
        punc_model (str, optional): 标点模型. Defaults to "ct_transformer".
    """
    from fasr import AudioPipeline

    audios = check_input_and_load(input)
    audios = audios.load(num_workers=4)
    duration = audios.duration_s
    if num_samples:
        audios = audios[:num_samples]
    asr = (
        AudioPipeline()
        .add_pipe(
            "detector",
            num_threads=num_threads,
            compile=compile,
            model=vad_model,
            batch_size=batch_size,
        )
        .add_pipe(
            "recognizer",
            model=asr_model,
            batch_size_s=batch_size_s,
            batch_size=batch_size,
        )
        .add_pipe("sentencizer", model=punc_model, batch_size=batch_size)
    )

    def run_pipeline(urls):
        start = time.perf_counter()
        _ = asr.run(urls, verbose=True)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    # warm up
    logger.info("warm up")
    _ = run_pipeline(audios[0:2])

    # benchmark
    logger.info("benchmark")
    pipeline_took = run_pipeline(audios)
    # 所有通道的总时长
    logger.info(f"duration: {round(duration, 2)} seconds")
    logger.info(
        f"pipeline: took {pipeline_took} seconds, speedup: {round(duration / pipeline_took, 2)}"
    )


def benchmark_vad(
    urls: str,
    model: str = "fsmn",
    batch_size: int = 2,
    num_threads: int = 2,
    num_samples: int | None = None,
):
    """对比测试fasr与funasr pipeline(load -> vad)的性能.

    Args:
        urls (str): url文件路径.
        batch_size (int, optional): 批处理大小. Defaults to 2.
        num_threads (int, optional): 并行处理的工作线程数. Defaults to 2.
        num_samples (int, optional): 采样数量. Defaults to 100.
        model_dir (str, optional): 语音检测模型目录. Defaults to "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch".
    """
    from fasr.data import Audio, AudioList
    from fasr.components import VoiceDetector

    vad = VoiceDetector().setup(model=model, num_threads=num_threads)

    if not Path(urls).exists():
        raise FileNotFoundError(f"{urls} not found")
    if Path(urls).is_dir():
        urls = [
            str(p) for p in Path(urls).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
    else:
        with open(urls, "r") as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]
    if num_samples:
        urls = urls[:num_samples]

    audios = AudioList[Audio]()
    duration = 0
    for idx in range(0, len(urls), batch_size):
        batch_urls = urls[idx : idx + batch_size]
        batch_audios = AudioList.from_urls(urls=batch_urls, load=True, num_workers=4)
        for audio in batch_audios:
            duration += audio.duration * len(audio.channels)
        audios.extend(batch_audios)

    def run_vad(audios: AudioList[Audio]) -> float:
        start = time.perf_counter()
        for i in trange(0, len(audios), batch_size):
            _audios = audios[i : i + batch_size]
            _audios = vad.predict(_audios)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    # warm up
    logger.info("warm up")
    _ = run_vad(audios[0:1])

    # benchmark
    fasr_took = run_vad(audios)
    logger.info(f"All channels duration: {round(duration, 2)} seconds")
    logger.info(
        f"{model}: took {fasr_took} seconds, speedup: {round(duration / fasr_took, 2)}"
    )


def benchmark_asr(
    urls: str,
    model: str = "paraformer",
    batch_size: int = 2,
    num_threads: int = 1,
    num_samples: int | None = None,
):
    """测试asr推理性能.

    Args:
        urls (str): url文件路径.
        batch_size (int, optional): 批处理大小. Defaults to 2.
        num_threads (int, optional): 并行处理的工作线程数. Defaults to 2.
        num_samples (int, optional): 采样数量. Defaults to 100.
        model_dir (str, optional): 语音检测模型目录. Defaults to "checkpoints/iic/speech_fsmn_vad_zh-cn-16k-common-pytorch".
    """
    from fasr.data import Audio, AudioList
    from fasr.components import SpeechRecognizer, AudioLoaderV2

    asr = SpeechRecognizer().setup(model=model, num_threads=num_threads)
    loader = AudioLoaderV2()

    if not Path(urls).exists():
        raise FileNotFoundError(f"{urls} not found")
    if Path(urls).is_dir():
        urls = [
            str(p) for p in Path(urls).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
    else:
        with open(urls, "r") as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]
    if num_samples:
        urls = urls[:num_samples]

    audios = AudioList[Audio]()
    duration = 0
    for idx in range(0, len(urls), batch_size):
        batch_urls = urls[idx : idx + batch_size]
        batch_audios = AudioList.from_urls(urls=batch_urls)
        batch_audios = loader.predict(batch_audios)
        for audio in batch_audios:
            duration += audio.duration * len(audio.channels)
        audios.extend(batch_audios)

    def run_asr(audios: AudioList[Audio]) -> float:
        start = time.perf_counter()
        for i in trange(0, len(audios), batch_size):
            _audios = audios[i : i + batch_size]
            _audios = asr.predict(_audios)
        end = time.perf_counter()
        took = round(end - start, 2)
        return took

    # warm up
    logger.info("warm up")
    _ = run_asr(audios[0:1])

    # benchmark
    fasr_took = run_asr(audios)
    logger.info(f"All channels duration: {round(duration, 2)} seconds")
    logger.info(
        f"{model}: took {fasr_took} seconds, speedup: {round(duration / fasr_took, 2)}"
    )


def benchmark_loader(
    urls: str,
    loader: Literal["loader.v1", "loader.v2"] = "loader.v1",
    num_threads: int = 1,
):
    """测试fasr的loader性能.

    Args:
        loader (Literal["loader.v1", "loader.v2"]): loader版本.
    """
    from fasr.config import registry

    if loader == "loader.v1":
        loader = registry.components.get(loader)(num_threads=num_threads)
    else:
        loader = registry.components.get(loader)()

    if not Path(urls).exists():
        raise FileNotFoundError(f"{urls} not found")
    if Path(urls).is_dir():
        urls = [
            str(p) for p in Path(urls).iterdir() if p.is_file() and p.suffix == ".wav"
        ]
    else:
        with open(urls, "r") as f:
            urls = f.readlines()
        urls = [url.strip() for url in urls]

    # warm up
    _ = urls[:5] | loader

    # benchmark
    start = time.perf_counter()
    audios = urls | loader
    end = time.perf_counter()
    took = round(end - start, 2)
    duration = audios.duration_s
    logger.info(f"took {took} seconds, speedup: {round(duration / took, 2)}")
