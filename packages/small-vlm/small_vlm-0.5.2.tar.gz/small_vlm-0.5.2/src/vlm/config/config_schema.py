from dataclasses import dataclass, field

from hydra.core.config_store import ConfigStore
from omegaconf import MISSING  # pyright: ignore


@dataclass
class VisualEncoderConfig:
    name: str = MISSING
    hf_name: str = MISSING
    type: str = "hf_visual_encoder"
    hidden_size: int | None = None
    img_size: int | None = None
    patch_size: int | None = None
    output_layer: int | None = None
    use_cls_token: bool = False


@dataclass
class LLMConfig:
    name: str = MISSING
    hf_name: str = MISSING
    type: str = "hf_llm"
    hidden_size: int | None = None
    vocab_size: int | None = None
    max_seq_length: int | None = None
    image_token: str = "<image>"
    pad_token: str = "<pad>"
    system_token: str = "<|system|>"
    user_token: str = "<|user|>"
    assistant_token: str = "<|assistant|>"


@dataclass
class ConnectorConfig:
    name: str = MISSING
    type: str = MISSING
    mask_format: str = "2d"


@dataclass
class ModelConfig:
    name: str = MISSING
    visual_encoder: VisualEncoderConfig = field(default_factory=VisualEncoderConfig)
    llm: LLMConfig = field(default_factory=LLMConfig)
    connector: ConnectorConfig = field(default_factory=ConnectorConfig)


@dataclass
class DatasetConfig:
    name: str = MISSING
    hf_name: str | None = None
    json_path: str | None = None
    type: str = MISSING
    num_proc: int | None = 8
    num_workers: int = 4
    pin_memory: bool = True
    persistent_workers: bool = True


@dataclass
class UnfreezeConfig:
    train_visual_encoder: bool = True
    train_language_model: bool = True
    train_connector: bool = True


@dataclass
class LearningRateConfig:
    visual_encoder_learning_rate: float = 1e-4
    language_model_learning_rate: float = 1e-4
    connector_learning_rate: float = 1e-4
    default_lr: float = 1e-4


@dataclass
class WeightDecayConfig:
    visual_encoder_weight_decay: float = 0.0
    language_model_weight_decay: float = 0.0
    connector_weight_decay: float = 0.0


@dataclass
class SchedulerConfig:
    warmup_ratio: float = 0.0
    warmup_start_factor: float = 0.0
    min_lr_ratio: float = 0.0


@dataclass
class OptimizerConfig:
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_epsilon: float = 1e-8


@dataclass
class TrainerConfig:
    unfreeze: UnfreezeConfig = field(default_factory=UnfreezeConfig)
    learning_rate: LearningRateConfig = field(default_factory=LearningRateConfig)
    weight_decay: WeightDecayConfig = field(default_factory=WeightDecayConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    optimizer: OptimizerConfig = field(default_factory=OptimizerConfig)
    batch_size: int = 16
    ignore_index: int = -100
    default_root_dir: str = "."
    debug: bool = False
    experiment_name: str = "vlm_training"
    max_epochs: int = 30
    monitor_metric: str = "val_loss"
    monitor_mode: str = "min"
    early_stopping: bool = False
    patience: int = 5
    log_every_n_steps: int = 50
    val_check_interval: float = 0.5
    gradient_clip_val: float = 1.0
    accumulate_grad_batches: int = 1
    precision: str | None = None
    accelerator: str = "auto"
    devices: int | str = "auto"
    strategy: str = "auto"
    resume_from_checkpoint: bool = True
    checkpoint_path: str | None = None
    wandb_project_name: str = "vlm-training"
    log_model_to_wandb: bool = False
    save_every_n_epochs: int | None = None
    save_every_n_train_steps: int | None = None
    num_training_samples: int | None = None
    chat_template: str = "llava_plain"
    has_val_dataloader: bool = False
    load_optimizer_states: bool = True


@dataclass
class ModeConfig:
    is_training: bool = True


@dataclass
class InferenceConfig:
    checkpoint_path: str = MISSING
    num_inference_samples: int | None = None
    chat_template: str = "llava_plain"


@dataclass
class AppConfig:
    mode: ModeConfig = field(default_factory=ModeConfig)
    model: ModelConfig = field(default_factory=ModelConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    trainer: TrainerConfig = field(default_factory=TrainerConfig)
    inference: InferenceConfig = field(default_factory=InferenceConfig)


def register_configs() -> None:
    cs: ConfigStore = ConfigStore.instance()
    cs.store(name="cfg", node=AppConfig)
