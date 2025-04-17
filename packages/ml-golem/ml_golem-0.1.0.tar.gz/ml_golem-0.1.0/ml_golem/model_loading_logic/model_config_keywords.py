from enum import Enum
class ModelConfigKeywords(Enum):
    MODEL_CLASS = 'model_class'
    TRAINING = 'training'
    INFERENCE = 'inference'
    EVALUATION = 'evaluation'
    ARCHITECTURE = 'architecture'
    VISUALIZATION = 'visualization'


    RESUME_EPOCH = 'resume_epoch'

    #TRAINING KEYWORDS
    EPOCHS = 'epochs'
    LEARNING_RATE = 'learning_rate'
    SAVE_EVERY = 'save_every'
    CAN_DISPLAY_EPOCH_PROGRESS = 'can_display_epoch_progress'

    DATASET = 'dataset'
    GROUND_TRUTH = 'ground_truth'
    DATATYPE = 'datatype'
    NUM_WORKERS = 'num_workers'
    BATCH_SIZE = 'batch_size'
    DATALOADER = 'dataloader'
    LOSS = 'loss'

    DATA_GEN_CONFIG = 'data_gen_config'
    IS_PRELOADED = 'is_preloaded'
    HAS_INDEX = 'has_index'