from ml_golem.base_classes.model_io_base import ModelIOBase
from ml_golem.model_loading_logic.model_config_keywords import ModelConfigKeywords
import torch.nn as nn
class ModelInference(ModelIOBase):
    def __init__(self,args,config):
        super().__init__(args,config)
        self.output_datatype = self.data_io.fetch_class_from_config(config_name= self.global_config_name,
                subconfig_keys = [ModelConfigKeywords.EVALUATION.value,
                                  ModelConfigKeywords.DATASET.value,
                                  ModelConfigKeywords.DATATYPE.value],
                is_required=False)

        if isinstance(self.model, nn.Module):
            self.device = next(self.model.parameters()).device
            self.model = self.model.to(self.device)
            self.model.eval()

    def __call__(self):

        if self.dataloader is None:
            results = self.make_inference(self.model)
            self.save_results(results, self.model)
        else:
            for input_data in self.dataloader:
                results = self.make_inference(self.model,input_data)
                self.save_results(results,self.model,input_data)


    def make_inference(self,model,input_data=None):
        if input_data is None:
            output = model()
        else:
            output = model(input_data)
        return output
    
    def save_results(self,output,model,input_data=None):
        raise Exception('Not Implemented')