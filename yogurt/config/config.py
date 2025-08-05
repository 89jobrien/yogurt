from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class LLMConfig(BaseModel):
    model_name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    stop_sequences: Optional[List[str]] = None


class YogurtSettings(BaseModel):
    log_level: str = "INFO"
    default_timeout: int = 120
    allowed_extensions: List[str] = Field(default_factory=list)
    allowed_filetypes: List[str] = Field(default_factory=list)
    log_level: str = Field(default="INFO")
    cache_enabled: bool = Field(default=True)
    cache_ttl_seconds: int = Field(default=300, ge=0)
    memory_enabled: bool = Field(default=True)
    memory_window: int = Field(default=10, ge=0)
    streaming_enabled: bool = Field(default=True)
    max_concurrent_requests: int = Field(default=10, ge=1)
    api_keys: Optional[Dict[str, str]] = None
    proxy: Optional[str] = None
    logging_format: str = Field(default="json")  # or "plain"
    use_advanced_parsers: bool = Field(default=False)
    plugin_directories: List[str] = Field(default_factory=list)
    enable_autonomous_agents: bool = Field(default=False)
    default_toolkits: List[str] = Field(default_factory=list)
    metrics_enabled: bool = Field(default=False)
    metrics_endpoint: Optional[str] = None
    security_policy: Optional[str] = None
    max_input_length: Optional[int] = Field(default=2048)
