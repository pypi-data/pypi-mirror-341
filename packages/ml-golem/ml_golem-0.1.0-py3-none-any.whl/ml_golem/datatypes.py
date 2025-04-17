from file_golem import FileDatatypes,AbstractDatatype,FilePathEntries
from file_golem import Config

class ModelCheckpoint(AbstractDatatype):
    FILE_DATATYPE = FileDatatypes.TORCH
    EPOCH = 'epoch'
    RELATIVE_PATH_TUPLE = AbstractDatatype.RELATIVE_PATH_TUPLE + (
        'model_checkpoints',
        FilePathEntries.CONFIG_ENTRY,
        {FilePathEntries.DATA_ARG_ENTRY: EPOCH})
    


class TrainingLog(AbstractDatatype):
    FILE_DATATYPE = FileDatatypes.EMPTY
    RELATIVE_PATH_TUPLE = AbstractDatatype.RELATIVE_PATH_TUPLE + (
        'training_logs',
        FilePathEntries.CONFIG_ENTRY)



class EvaluationResults(AbstractDatatype):
    FILE_DATATYPE = FileDatatypes.JSON
    RELATIVE_PATH_TUPLE = AbstractDatatype.RELATIVE_PATH_TUPLE + (
        'evaluation_log',)





class GridShellScript(Config):
    FILE_DATATYPE = FileDatatypes.SHELL

    RELATIVE_PATH_TUPLE = Config.RELATIVE_PATH_TUPLE + ('grid_search',)
    
    @staticmethod
    def _grid_search_suffix(data_args):
        return (data_args[GridShellScript.GRID_DIRECTORY],)

    

class GridSlurmScript(Config):
    FILE_DATATYPE = FileDatatypes.SLURM_SCRIPT
    RELATIVE_PATH_TUPLE = Config.RELATIVE_PATH_TUPLE + ('slurm_search',)

    @staticmethod
    def _grid_search_suffix(data_args):
        return (data_args[GridSlurmScript.GRID_DIRECTORY],)
    

class AbstractSlurmOutput(AbstractDatatype):
    FILE_DATATYPE = None
    RELATIVE_PATH_TUPLE = AbstractDatatype.RELATIVE_PATH_TUPLE + ('slurm',
        {FilePathEntries.DATA_ARG_ENTRY: Config.GRID_DIRECTORY},
        '%j')
    

class SlurmOutputStd(AbstractSlurmOutput):
    FILE_DATATYPE = FileDatatypes.SLURM_OUTPUT_STD


class SlurmOutputErr(AbstractSlurmOutput):
    FILE_DATATYPE = FileDatatypes.SLURM_OUTPUT_ERR
