from .base import StreamVADModel
from funasr import AutoModel
from fasr.config import registry
from fasr.data import Waveform, AudioSpan
from typing_extensions import Self
from typing import Dict, Iterable
from pathlib import Path
import numpy as np


DEFAULT_CHECKPOINT_DIR = Path(__file__).parent.parent.parent / "asset" / "fsmn-vad"


@registry.stream_vad_models.register("stream_fsmn")
class FSMNForStreamVAD(StreamVADModel):
    fsmn: AutoModel | None = None
    chunk_size_ms: int = 100
    sample_rate: int = 16000

    def detect_chunk(
        self,
        waveform: Waveform,
        is_last: bool,
        state: Dict,
    ) -> Iterable[AudioSpan]:
        """Detect voice activity in the given chunk of waveform.

        Args:
            waveform (Waveform): The chunk of waveform to detect voice activity in.
            is_last (bool): Indicates if the chunk is the last chunk of the audio.
            state (Dict): The state of the model, which includes buffer, cache, offset, is_detected, and audio_waveform.

        Notes:
            - The function processes the waveform in chunks of size `self.chunk_size`.
            - If the sample rate of the input waveform does not match `self.sample_rate`, it will be resampled.
            - The function maintains a buffer to handle waveform chunks and updates the state accordingly.
            - Voice activity detection is performed using the FSMN model, and detected segments are yielded as AudioSpan objects.
            - If `is_last` is True and there is remaining data in the buffer, it processes the final chunk.

        Yields:
            AudioSpan: Detected voice activity spans, each represented as an AudioSpan object.
        """
        if waveform.sample_rate != self.sample_rate:
            waveform = waveform.resample(self.sample_rate)
        buffer: Waveform = state.get(
            "buffer",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        buffer = buffer.append(waveform)
        audio_waveform: Waveform = state.get(
            "audio_waveform",
            Waveform(data=np.array([], dtype=np.float32), sample_rate=self.sample_rate),
        )
        audio_waveform = audio_waveform.append(waveform=waveform)
        cache = state.get("cache", {})
        offset = state.get("offset", 0)
        is_detected = state.get("is_detected", False)

        while len(buffer) >= self.chunk_size:
            chunk_waveform = buffer[: self.chunk_size]
            buffer = buffer[self.chunk_size :]
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            segments = self.fsmn.generate(
                input=data,
                fs=sample_rate,
                chunk_size=self.chunk_size_ms,
                is_final=False,
                cache=cache,
            )[0]["value"]

            if len(segments) > 0:
                for segment in segments:
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=False,
                        )

                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=True,
                        )

                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=True,
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        is_last=False,
                    )

            offset += len(data)

        if is_last and 0 < len(buffer) < self.chunk_size:
            chunk_waveform = buffer
            buffer = Waveform(data=np.array([]), sample_rate=self.sample_rate)
            data = chunk_waveform.data
            sample_rate = chunk_waveform.sample_rate
            segments = self.fsmn.generate(
                input=data,
                fs=sample_rate,
                is_final=True,
                cache=cache,
            )[0]["value"]

            if len(segments) > 0:
                for segment in segments:
                    start, end = segment
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * sample_rate // 1000
                        end_idx = len(data) + offset
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=False,
                        )

                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=True,
                        )

                    if start != -1 and end != -1:
                        is_detected = False
                        start_idx = start * sample_rate // 1000
                        end_idx = end * sample_rate // 1000
                        segment_waveform = audio_waveform[start_idx:end_idx]
                        yield AudioSpan(
                            start_ms=start,
                            end_ms=end,
                            waveform=segment_waveform,
                            sample_rate=sample_rate,
                            is_last=True,
                        )
            else:
                if is_detected:
                    yield AudioSpan(
                        start_ms=-1,
                        end_ms=-1,
                        waveform=waveform,
                        sample_rate=sample_rate,
                        is_last=False,
                    )

            offset += len(data)

        state.update(
            {
                "buffer": buffer,
                "cache": cache,
                "offset": offset,
                "is_detected": is_detected,
                "audio_waveform": audio_waveform,
            }
        )

    def reset(self):
        pass

    def from_checkpoint(
        self, disable_update: bool = True, disable_pbar: bool = True, *args, **kwargs
    ) -> Self:
        checkpoint_dir = DEFAULT_CHECKPOINT_DIR
        self.fsmn = AutoModel(
            model=str(checkpoint_dir),
            disable_update=disable_update,
            disable_pbar=disable_pbar,
        )
        return self

    @property
    def chunk_size(self) -> int:
        return self.chunk_size_ms * self.sample_rate // 1000
