from pathlib import Path
from typing import Literal


DEFAULT_CACHE_DIR = Path.home() / ".cache" / "fasr" / "checkpoints"  # 默认缓存目录


def prepare_offline_models(cache_dir: str | Path = DEFAULT_CACHE_DIR):
    """Prepare offline models for building pipeline"""
    from modelscope import snapshot_download

    models = [
        "iic/punc_ct-transformer_zh-cn-common-vocab272727-pytorch",
        "iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "iic/SenseVoiceSmall",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def prepare_online_models(cache_dir: str | Path = DEFAULT_CACHE_DIR):
    """
    Prepare online models for building pipeline
    """
    from modelscope import snapshot_download

    models = [
        "iic/SenseVoiceSmall",
        "iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online",
    ]
    for model in models:
        snapshot_download(model_id=model, cache_dir=cache_dir)


def download(
    repo_id: str,
    revision: str = None,
    cache_dir: str | Path = DEFAULT_CACHE_DIR,
    endpoint: Literal["modelscope", "huggingface", "hf-mirror"] = "modelscope",
) -> None:
    """Download model from modelscope"""
    cache_dir = Path(cache_dir)
    if endpoint == "hf-mirror":
        from huggingface_hub import snapshot_download

        _ = snapshot_download(
            repo_id=repo_id,
            local_dir=cache_dir / repo_id,
            revision=revision,
            local_dir_use_symlinks=False,
            endpoint="https://hf-mirror.com",
        )
    if endpoint == "huggingface":
        from huggingface_hub import snapshot_download

        _ = snapshot_download(
            repo_id=repo_id,
            local_dir=cache_dir / repo_id,
            revision=revision,
            local_dir_use_symlinks=False,
        )

    elif endpoint == "modelscope":
        from modelscope import snapshot_download

        _ = snapshot_download(model_id=repo_id, cache_dir=cache_dir, revision=revision)
