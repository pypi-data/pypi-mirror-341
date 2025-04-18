# zmprinter_sdk/__init__.py
from .core import LabelPrinterSDK
from .config import PrinterConfig, LabelConfig
from .elements import (
    LabelElement,
    TextElement,
    BarcodeElement,
    ImageElement,
    RFIDElement,
    ShapeElement,
)
from .enums import (
    PrinterStyle,
    BarcodeType,
    RFIDEncoderType,
    RFIDDataBlock,
    RFIDDataType,
)
from .utils import get_logger, setup_file_logging
# from .exceptions import (
#     ZMPrinterError,
#     ZMPrinterImportError,
#     ZMPrinterConnectionError,
#     ZMPrinterCommandError,
#     ZMPrinterLSFError,
#     ZMPrinterRFIDError,
# )

# 设置包级别的 logger
logger = get_logger("zmprinter")

# Optional: Define __all__ for explicit export control
__all__ = [
    "LabelPrinterSDK",
    "PrinterConfig",
    "LabelConfig",
    "LabelElement",
    "TextElement",
    "BarcodeElement",
    "ImageElement",
    "RFIDElement",
    "ShapeElement",
    "PrinterStyle",
    "BarcodeType",
    "RFIDEncoderType",
    "RFIDDataBlock",
    "RFIDDataType",
    "get_logger",
    "setup_file_logging",
    "logger",
    # "ZMPrinterError",
    # "ZMPrinterImportError",
    # "ZMPrinterConnectionError",
    # "ZMPrinterCommandError",
    # "ZMPrinterLSFError",
    # "ZMPrinterRFIDError",
]

__version__ = "0.1.0"
