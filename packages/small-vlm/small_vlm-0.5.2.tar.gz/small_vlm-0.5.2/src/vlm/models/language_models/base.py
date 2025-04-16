import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import cast, override

import torch
import torch.nn as nn
from transformers.configuration_utils import PretrainedConfig
from transformers.modeling_utils import PreTrainedModel
from transformers.tokenization_utils import PreTrainedTokenizer

from ...config.config_schema import LLMConfig

log: logging.Logger = logging.getLogger(name=__name__)


@dataclass
class TokenConfig:
    """Special token configuration"""

    image_token: str = "<image>"
    pad_token: str = "<pad>"
    system_token: str = "<|system|>"
    user_token: str = "<|user|>"
    assistant_token: str = "<|assistant|>"
    image_token_id: int | None = None
    pad_token_id: int | None = None
    system_token_id: int | None = None
    user_token_id: int | None = None
    assistant_token_id: int | None = None


@dataclass
class LanguageModelConfig:
    hidden_size: int | None = None
    vocab_size: int | None = None
    max_seq_length: int | None = None


class LanguageModel(nn.Module, ABC):
    def __init__(self, config: LLMConfig) -> None:
        super().__init__()
        self.config: LLMConfig = config
        self.name: str = self.config.name
        self.hf_name: str = self.config.hf_name
        self.model_type: str = self.config.type

        # model config
        self.model_config: LanguageModelConfig = LanguageModelConfig(
            hidden_size=getattr(self.config, "hidden_size", None),
            vocab_size=getattr(self.config, "vocab_size", None),
            max_seq_length=getattr(self.config, "max_seq_length", None),
        )

        # token config
        self.token_config: TokenConfig = TokenConfig(
            image_token=getattr(self.config, "image_token", "<image>"),
            pad_token=getattr(self.config, "pad_token", "<pad>"),
            system_token=getattr(self.config, "system_token", "<|system|>"),
            user_token=getattr(self.config, "user_token", "<|user|>"),
            assistant_token=getattr(self.config, "assistant_token", "<|assistant|>"),
        )

        self._initialize_components()

    # initialize all components
    def initialize_components(self) -> None:
        self._language_model: PreTrainedModel = self._build_language_model()
        self._embeddings: nn.Module = self._build_embedding_layer()
        self.language_model.resize_token_embeddings(len(self.tokenizer))

    # only initialize components needed for dataset processing
    def _initialize_components(self) -> None:
        self._tokenizer: PreTrainedTokenizer = self._build_tokenizer()
        self._hf_config: PretrainedConfig = self._build_hf_config()

        self._add_special_tokens()

        self.verify_config()

    def _add_special_tokens(self) -> None:
        """Adds special tokens to the tokenizer if they don't exist."""
        special_tokens_to_add = [
            (self.token_config.image_token, "image_token_id", "additional_special_tokens"),
            (self.token_config.pad_token, "pad_token_id", "pad_token"),
            (self.token_config.system_token, "system_token_id", "additional_special_tokens"),
            (self.token_config.user_token, "user_token_id", "additional_special_tokens"),
            (self.token_config.assistant_token, "assistant_token_id", "additional_special_tokens"),
        ]

        for token, token_id_attr, token_type in special_tokens_to_add:
            self._add_or_get_special_token(
                token=token,
                token_id_attr=token_id_attr,
                token_type=token_type,
            )

    def _add_or_get_special_token(self, token: str, token_id_attr: str, token_type: str) -> None:
        """Checks if a special token exists, adds it if not, and sets the token ID."""
        token_id = self.tokenizer.convert_tokens_to_ids(token)
        if token_id != self.tokenizer.unk_token_id:
            log.info(f"Token '{token}' exists in tokenizer, ID: {token_id}")
            setattr(self.token_config, token_id_attr, cast(int, token_id))
        else:
            log.info(f"Token '{token}' does not exist in tokenizer, adding it")
            new_token_id = self._add_special_token(token=token, token_type=token_type)
            setattr(self.token_config, token_id_attr, new_token_id)

    def _add_special_token(self, token: str, token_type: str) -> int:
        log.info(f"Adding {token_type}: {token}")

        if token_type == "pad_token":
            self.tokenizer.add_special_tokens({"pad_token": token})
        else:
            # Use a list for additional_special_tokens as per transformers documentation
            self.tokenizer.add_special_tokens({token_type: [token]})  # pyright: ignore

        token_id: int = cast(int, self.tokenizer.convert_tokens_to_ids(token))
        return token_id

    @property
    def tokenizer(self) -> PreTrainedTokenizer:
        return self._tokenizer

    @property
    def language_model(self) -> PreTrainedModel:
        return self._language_model

    @property
    def hf_config(self) -> PretrainedConfig:
        return self._hf_config

    @property
    def hidden_size(self) -> int:
        return cast(int, self.model_config.hidden_size)

    @hidden_size.setter
    def hidden_size(self, value: int) -> None:
        self.model_config.hidden_size = value

    @property
    def vocab_size(self) -> int:
        return cast(int, self.model_config.vocab_size)

    @vocab_size.setter
    def vocab_size(self, value: int) -> None:
        self.model_config.vocab_size = value

    @property
    def max_seq_length(self) -> int:
        return cast(int, self.model_config.max_seq_length)

    @max_seq_length.setter
    def max_seq_length(self, value: int) -> None:
        self.model_config.max_seq_length = value

    @property
    def embeddings(self) -> nn.Module:
        return self._embeddings

    @property
    def image_token_id(self) -> int:
        return cast(int, self.token_config.image_token_id)

    @property
    def pad_token_id(self) -> int:
        return cast(int, self.token_config.pad_token_id)

    @abstractmethod
    def _build_embedding_layer(self) -> nn.Module:
        pass

    @abstractmethod
    def _build_tokenizer(self) -> PreTrainedTokenizer:
        pass

    @abstractmethod
    def _build_language_model(self) -> PreTrainedModel:
        pass

    @abstractmethod
    def _build_hf_config(self) -> PretrainedConfig:
        pass

    @abstractmethod
    @override
    def forward(
        self,
        input_ids: torch.Tensor | None = None,
        inputs_embeds: torch.Tensor | None = None,
        attention_mask: torch.Tensor | None = None,
    ) -> torch.Tensor:
        pass

    def verify_config(self) -> None:
        config_pairs = [
            ("hidden_size", self.get_config("hidden_size"), self.hidden_size),
            ("vocab_size", self.get_config("vocab_size"), self.vocab_size),
            ("max_seq_length", self.get_config("max_position_embeddings"), self.max_seq_length),
        ]

        for key, model_value, config_value in config_pairs:
            self._verify_param_match(key, model_value, config_value)

    def _verify_param_match(
        self, key: str, model_value: int | str | None, config_value: int | str | None
    ) -> None:
        capitalized_key = key.capitalize()

        if model_value is None and config_value is None:
            log.warning(f"{capitalized_key} not found in config for {self.name}")
        elif model_value is not None and config_value is None:
            setattr(self, key, int(model_value))
            if hasattr(self.config, key):
                setattr(self.config, key, int(model_value))
            log.info(f"{capitalized_key} not found in config, using hf config: {model_value}")
        elif model_value is None and config_value is not None:
            log.warning(f"{capitalized_key} not found in hf config for {self.name}")
        elif model_value is not None and config_value is not None:
            if model_value != config_value:
                error_msg = f"{capitalized_key} mismatch: hf config: {model_value} != config: {config_value}"
                log.error(error_msg)
                raise ValueError(error_msg)
            else:
                log.info(
                    f"{capitalized_key} verified: hf config: {model_value} == config: {config_value}"
                )

    def get_config(self, key: str) -> int | str | None:
        return getattr(self.hf_config, key, None)
