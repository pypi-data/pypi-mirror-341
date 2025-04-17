from ml_golem.model_loading_logic.config_class_instantiator import ConfigBasedClass
from ml_golem.model_loading_logic.model_config_keywords import ModelConfigKeywords
from torch.utils.data import DataLoader
            
class DataLoadingBase(ConfigBasedClass):
    def _initialize_dataloader(self,args,subconfig_keys):
        config = self.data_io.fetch_subconfig(
            self.data_io.load_config(self.global_config_name),
            subconfig_keys=subconfig_keys)
        if ModelConfigKeywords.DATALOADER.value not in config:
            return None
        if ModelConfigKeywords.DATASET.value not in config:
            return None
            
        dataset = self.instantiate_config_based_class(args,subconfig_keys=subconfig_keys+[ModelConfigKeywords.DATASET.value])
        collate_fn = dataset.custom_collate_fn if hasattr(dataset,'custom_collate_fn') else None

        dataloader_config= self.data_io.fetch_subconfig(config,subconfig_keys=[ModelConfigKeywords.DATALOADER.value])
        dataloader = DataLoader(dataset,
            batch_size=dataloader_config[ModelConfigKeywords.BATCH_SIZE.value], 
            num_workers=dataloader_config[ModelConfigKeywords.NUM_WORKERS.value],
            collate_fn=collate_fn,
            shuffle=self._is_shuffle(), 
            pin_memory=True)
        return dataloader
    
    def _is_shuffle(self):
        return False