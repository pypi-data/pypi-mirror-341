from ml_golem.model_loading_logic.config_class_instantiator import ConfigBasedClass
from ml_golem.model_loading_logic.model_config_keywords import ModelConfigKeywords
from ml_golem.datatypes import ModelCheckpoint, TrainingLog
from file_golem import FilePathEntries

class ModelAction(ConfigBasedClass):
    def train(self,args):
        self._call_subconf_action(args,[ModelConfigKeywords.TRAINING.value],'Training')

    def inference(self,args):
        self._call_subconf_action(args,[ModelConfigKeywords.INFERENCE.value],'Inference')

    def evaluate(self,args):
        self._call_subconf_action(args,[ModelConfigKeywords.EVALUATION.value],'Evaluation')

    def visualize(self,args):
        self._call_subconf_action(args,args.visualization_type.split('.') + [ModelConfigKeywords.VISUALIZATION.value],'Visualization')


    def wipe(self):
        print(f'Wipe: {self.global_config_name}')
        print('WARNING: YOU PROBABLY DONT WANT TO CALL WIPE')
        self.data_io.delete_data(ModelCheckpoint,data_args = {
            ModelCheckpoint.CONFIG_NAME: self.global_config_name,
            ModelCheckpoint.EPOCH:FilePathEntries.OPEN_ENTRY
        })

        self.data_io.delete_data(TrainingLog,data_args = {
            TrainingLog.CONFIG_NAME: self.global_config_name,
        })

    def _call_subconf_action(self,args,subconfig_keys,action_name):
        print(f'{action_name}: {self.global_config_name}')
        action_model = self.instantiate_config_based_class(args,subconfig_keys =subconfig_keys)
        action_model()