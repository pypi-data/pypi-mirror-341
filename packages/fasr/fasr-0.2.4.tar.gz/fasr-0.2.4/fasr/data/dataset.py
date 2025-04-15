from .audio import Audio, Waveform, AudioList
from litdata import StreamingDataset, StreamingDataLoader
from typing import List, Dict


class AudioDataset(StreamingDataset):
    def __getitem__(self, index):
        item: Dict | List = super().__getitem__(index)
        if isinstance(item, dict):
            url = item.get("url", None)
            sample_rate = item.get("sample_rate", None) or item.get("sr", None)
            data = item.get("data", None)
            waveform = Waveform(data=data, sample_rate=sample_rate)
            audio = Audio(url=url).append_channel()
            audio[0].waveform = waveform
            text = item.get("text", None)
            audio[0].text = text
            audio.sample_rate = sample_rate
            return audio
        elif isinstance(item, list):
            audio_list = AudioList()
            for item in item:
                url = item.get("url", None)
                sample_rate = item.get("sample_rate", None) or item.get("sr", None)
                data = item.get("data", None)
                waveform = Waveform(data=data, sample_rate=sample_rate)
                audio = Audio(url=url).append_channel()
                audio[0].waveform = waveform
                text = item.get("text", None)
                audio[0].text = text
                audio.sample_rate = sample_rate
                audio_list.append(audio)
            return audio_list
        else:
            raise ValueError(f"Unsupported item type: {type(item)}")


def collate_to_audio_list(batch: List[Audio]):
    return AudioList(batch)


class AudioDatasetLoader(StreamingDataLoader):
    def __init__(
        self,
        dataset_dir: str,
        batch_size: int = 1,
        num_workers: int = 0,
        profile_batches: bool | int = False,
        profile_skip_batches: int = 0,
        profile_dir: str | None = None,
        prefetch_factor: int | None = None,
        shuffle: bool | None = None,
        drop_last: bool | None = None,
    ):
        super().__init__(
            dataset=AudioDataset(input_dir=dataset_dir),
            collate_fn=collate_to_audio_list,
            batch_size=batch_size,
            num_workers=num_workers,
            profile_batches=profile_batches,
            profile_skip_batches=profile_skip_batches,
            profile_dir=profile_dir,
            prefetch_factor=prefetch_factor,
            shuffle=shuffle,
            drop_last=drop_last,
        )
