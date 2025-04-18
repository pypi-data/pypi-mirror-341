import hashlib
import logging
import mimetypes
import os
import re
import shutil
import tempfile
import uuid
from typing import Union

import numpy as np
import soundfile as sf
from PIL import Image as PILImage

from .util import get_class

logger = logging.getLogger(f"{__name__.split('.')[0]}")
tag = "File"

VALID_CHAR = re.compile(r"^[a-zA-Z0-9_\-.]+$")
INVALID_CHAR = re.compile(r"[^a-zA-Z0-9_\-.]")


class File:
    tag = tag

    def __init__(
        self,
        path: str,
        name: str | None = None,
    ) -> None:
        self._path = os.path.abspath(path)
        self._id = self._hash()

        if not name:
            name = self._id
        elif not VALID_CHAR.match(name):
            e = ValueError(
                f"invalid file name: {name}; file name may only contain alphanumeric characters, dashes, underscores, and periods; proceeding with sanitized name"
            )
            logger.warning(f"{self.tag}: %s", e)
            name = INVALID_CHAR.sub("-", name)
        self._name = name
        self._ext = os.path.splitext(self._path)[-1]
        self._type = self._mimetype()
        self._stat = os.stat(self._path)  # os.path.getsize(self._path)
        self._url = None

    def _mimetype(self) -> str:
        return mimetypes.guess_type(self._path)[0] or "application/octet-stream"

    def _hash(self) -> str:  # do not truncate
        with open(self._path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def _mkcopy(self, dir) -> None:
        if not hasattr(self, "_tmp"):
            self._tmp = f"{dir}/files/{self._name}-{self._id}{self._ext}"
            shutil.copyfile(self._path, self._tmp)
            if hasattr(self, "_image"):
                os.remove(self._path)
            self._path = os.path.abspath(self._tmp)


class Image(File):
    tag = "Image"

    def __init__(
        self,
        data: Union[str, PILImage.Image, np.ndarray],
        caption: str | None = None,
    ) -> None:
        self._name = caption or f"{uuid.uuid4()}"
        self._id = f"{uuid.uuid4()}{uuid.uuid4()}".replace("-", "")
        self._ext = ".png"

        if isinstance(data, str):
            logger.debug(f"{self.tag}: used file")
            self._image = "file"  # self._image = PILImage.open(data)
            self._path = os.path.abspath(data)
        else:
            self._path = None
            if isinstance(data, PILImage.Image):
                logger.debug(f"{self.tag}: used PILImage")
                self._image = data
            else:
                class_name = get_class(data)
                if class_name.startswith("matplotlib."):
                    logger.debug(f"{self.tag}: attempted conversion from matplotlib")
                    self._image = make_compat_image_matplotlib(data)
                elif class_name.startswith("torch.") and (
                    "Tensor" in class_name or "Variable" in class_name
                ):
                    logger.debug(f"{self.tag}: attempted conversion from torch")
                    self._image = make_compat_image_torch(data)
                else:
                    logger.debug(f"{self.tag}: attempted conversion from array")
                    self._image = make_compat_image_numpy(data)

    def load(self, dir=None):
        if not self._path:
            if dir:
                self._tmp = f"{dir}/files/{self._name}-{self._id}{self._ext}"
                self._image.save(self._tmp, format=self._ext[1:])
                self._path = os.path.abspath(self._tmp)
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=self._ext) as tmp:
                    self._image.save(tmp.name, format=self._ext[1:])
                    self._path = os.path.abspath(tmp.name)

        super().__init__(path=self._path, name=self._name)
        if not self._type.startswith("image/"):
            logger.error(
                f"{self.tag}: proceeding with potentially incompatible mime type: {self._type}"
            )


class Audio(File):
    tag = "Audio"

    def __init__(
        self,
        data: Union[str, np.ndarray],
        rate: int | None = 48000,
        caption: str | None = None,
    ) -> None:
        self._name = caption or f"{uuid.uuid4()}"
        self._id = f"{uuid.uuid4()}{uuid.uuid4()}".replace("-", "")
        self._ext = ".wav"

        if isinstance(data, str):
            logger.debug(f"{self.tag}: used file")
            self._audio = "file"
            self._path = os.path.abspath(data)
        else:
            self._path = None
            if isinstance(data, np.ndarray):
                logger.debug(f"{self.tag}: used numpy array")
                self._audio = data
                self._rate = rate
            else:
                logger.critical(f"{self.tag}: unsupported data type: %s", type(data))

    def load(self, dir=None):
        if not self._path:
            if dir:
                self._tmp = f"{dir}/files/{self._name}-{self._id}{self._ext}"
                sf.write(file=self._tmp, data=self._audio, samplerate=self._rate)
                self._path = os.path.abspath(self._tmp)

        super().__init__(path=self._path, name=self._name)


def make_compat_image_matplotlib(val: any) -> any:
    # from matplotlib.spines import Spine # only required for is_frame_like workaround
    import matplotlib.pyplot as plt
    from matplotlib.figure import Figure

    if val == plt:
        val = val.gcf()
    elif not isinstance(val, Figure):
        if hasattr(val, "figure"):
            val = val.figure
            if not isinstance(val, Figure):
                e = ValueError(
                    "Invalid matplotlib object; must be a matplotlib.pyplot or matplotlib.figure.Figure object"
                )
                logger.critical(f"{tag}: Image conversion failed: %s", e)
                raise e

    from io import BytesIO

    buf = BytesIO()
    val.savefig(buf, format="png")
    image = PILImage.open(buf, formats=["PNG"])
    return image


def make_compat_image_torch(val: any) -> any:
    from torchvision.utils import make_grid

    if hasattr(val, "requires_grad") and val.requires_grad:
        val = val.detach()
    if hasattr(val, "dtype") and str(val.dtype).startswith("torch.uint8"):
        val = val.to(float)
    data = make_grid(val, normalize=True)
    image = PILImage.fromarray(
        data.mul(255).clamp(0, 255).byte().permute(1, 2, 0).cpu().numpy()
    )
    return image


def make_compat_image_numpy(val: any) -> any:
    import numpy as np

    if hasattr(val, "numpy"):
        val = val.numpy()
    if val.ndim > 2:
        val = val.squeeze()

    if np.min(val) < 0:
        val = (val - np.min(val)) / (np.max(val) - np.min(val))
    if np.max(val) <= 1:
        val = (val * 255).astype(np.int32)
    val.clip(0, 255).astype(np.uint8)

    image = PILImage.fromarray(val, mode="RGBA" if val.shape[-1] == 4 else "RGB")
    return image
