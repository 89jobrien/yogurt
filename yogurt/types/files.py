from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any, List, Dict, Literal, TypeAlias, Union


FileID: TypeAlias = str
Timestamp: TypeAlias = datetime

# Common file extensions as type aliases
TextFileExtension: TypeAlias = Literal[".txt", ".md", ".csv", ".json"]
ImageFileExtension: TypeAlias = Literal[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
PDFFileExtension: TypeAlias = Literal[".pdf"]
AudioFileExtension: TypeAlias = Literal[".mp3", ".wav", ".ogg", ".flac"]
VideoFileExtension: TypeAlias = Literal[".mp4", ".mov", ".avi", ".mkv"]
YAMLFileExtension: TypeAlias = Literal[".yaml", ".yml"]
TOMLFileExtension: TypeAlias = Literal[".toml"]
CSVFileExtension: TypeAlias = Literal[".csv"]
XLSXFileExtension: TypeAlias = Literal[".xlsx", ".xls"]
HTMLFileExtension: TypeAlias = Literal[".html", ".htm"]
MarkdownFileExtension: TypeAlias = Literal[".md"]
JSONLFileExtension: TypeAlias = Literal[".jsonl"]
ParquetFileExtension: TypeAlias = Literal[".parquet"]
ZIPFileExtension: TypeAlias = Literal[".zip"]
BinaryFileExtension: TypeAlias = Literal[".bin"]
PythonFileExtension: TypeAlias = Literal[".py"]


# Generic file content representations
FileBytes: TypeAlias = bytes
FilePath: TypeAlias = str


class FileMetadata(BaseModel):
    filename: str
    filetype: str  # e.g., 'pdf', 'image', 'audio'
    extension: str
    size_bytes: Optional[int] = None
    extra: Dict[str, Any] = Field(default_factory=dict)


class TextFile(BaseModel):
    path: FilePath
    contents: str
    metadata: Optional[FileMetadata] = None


class ImageFile(BaseModel):
    path: FilePath
    content_bytes: FileBytes  # Raw bytes of the image
    metadata: Optional[FileMetadata] = None


class PDFFile(BaseModel):
    path: FilePath
    content_bytes: FileBytes
    num_pages: Optional[int] = None
    metadata: Optional[FileMetadata] = None


class AudioFile(BaseModel):
    path: FilePath
    content_bytes: FileBytes
    duration_seconds: Optional[float] = None
    metadata: Optional[FileMetadata] = None


class VideoFile(BaseModel):
    path: FilePath
    content_bytes: FileBytes
    duration_seconds: Optional[float] = None  # If known
    metadata: Optional[FileMetadata] = None


class YAMLFile(BaseModel):
    path: FilePath
    contents: Any  # Usually a dict or list after parsing YAML
    metadata: Optional[FileMetadata] = None


class TOMLFile(BaseModel):
    path: FilePath
    contents: Dict[str, Any]
    metadata: Optional[FileMetadata] = None


class CSVFile(BaseModel):
    path: FilePath
    rows: List[Dict[str, Any]] = Field(default_factory=list)  # Parsed rows
    metadata: Optional[FileMetadata] = None


class XLSXFile(BaseModel):
    path: FilePath
    sheets: Dict[str, List[Dict[str, Any]]] = Field(default_factory=dict)  # Sheet Name -> rows
    metadata: Optional[FileMetadata] = None


class HTMLFile(BaseModel):
    path: FilePath
    html: str
    metadata: Optional[FileMetadata] = None


class MarkdownFile(BaseModel):
    path: FilePath
    markdown: str
    metadata: Optional[FileMetadata] = None


class JSONLFile(BaseModel):
    path: FilePath
    lines: List[Dict[str, Any]] = Field(default_factory=list)
    metadata: Optional[FileMetadata] = None


class ParquetFile(BaseModel):
    path: FilePath
    records: Optional[List[Dict[str, Any]]] = None
    metadata: Optional[FileMetadata] = None


class ZIPFile(BaseModel):
    path: FilePath
    file_list: List[str] = Field(default_factory=list)
    metadata: Optional[FileMetadata] = None


class PythonFile(BaseModel):
    path: FilePath
    source: str
    metadata: Optional[FileMetadata] = None


class BinaryFile(BaseModel):
    path: FilePath
    content_bytes: FileBytes
    metadata: Optional[FileMetadata] = None


# Union types for convenience
AnyFile = Union[
    TextFile,
    ImageFile,
    PDFFile,
    AudioFile,
    VideoFile,
    YAMLFile,
    TOMLFile,
    CSVFile,
    XLSXFile,
    HTMLFile,
    MarkdownFile,
    JSONLFile,
    ParquetFile,
    ZIPFile,
    PythonFile,
    BinaryFile,
]

ConfigFile = Union[YAMLFile, TOMLFile]


# MIME type aliases for typing (expand as needed)
MimeType: TypeAlias = str  # e.g. "text/plain", "application/pdf", "image/png"
YAMLMimeType: TypeAlias = Literal["application/x-yaml", "text/yaml"]
TOMLMimeType: TypeAlias = Literal["application/toml", "text/toml"]

