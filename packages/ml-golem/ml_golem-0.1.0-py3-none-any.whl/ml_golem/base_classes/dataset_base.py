import torch
from torch.utils.data import Dataset
from ml_golem.model_loading_logic.config_class_instantiator import ConfigBasedClass
from ml_golem.model_loading_logic.model_config_keywords import ModelConfigKeywords


class DatasetBase(ConfigBasedClass,Dataset):
    def __init__(self,args,subconfig_keys):
        super().__init__(args,subconfig_keys)
        self.datatype = self.data_io.fetch_class_from_config(config=self.config,subconfig_keys=[ModelConfigKeywords.DATATYPE.value])
        self.data_gen_config_name = self.config.get(ModelConfigKeywords.DATA_GEN_CONFIG.value, args.config_name) #BUGS AHOY!

        self.has_index = self.config.get(ModelConfigKeywords.HAS_INDEX.value,False)
        self.is_preloaded = self.config.get(ModelConfigKeywords.IS_PRELOADED.value, False)
        if self.is_preloaded:
            self.db = {}
            for i in range(len(self)):
                x = self._load_item(i)
                self.db[i] = x


    def __getitem__(self, idx):
        if self.is_preloaded:
            return self.db[idx]
        else:
            return self._load_item(idx)

    def _load_item(self,idx):
        data_item = self.data_io.load_data(self.datatype,data_args={
            self.datatype.IDX: idx,
            self.datatype.CONFIG_NAME: self.data_gen_config_name})
        
        if self.has_index:
            data_item[self.datatype.IDX] = torch.tensor(idx)
        return data_item
    
    def __len__(self):
        return self.data_io.get_datatype_length(self.datatype,data_args= {
            self.datatype.CONFIG_NAME: self.data_gen_config_name
        })