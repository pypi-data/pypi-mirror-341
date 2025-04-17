from ml_golem.base_classes.dataloading_base import DataLoadingBase
from ml_golem.model_loading_logic.model_config_keywords import ModelConfigKeywords
from ml_golem.datatypes import EvaluationResults




class ModelEvaluation(DataLoadingBase):


    def __init__(self,args,subconfig_keys):
        super().__init__(args,subconfig_keys)
        self.dataloader= self._initialize_dataloader(args,
            subconfig_keys = self.subconfig_keys)
        if ModelConfigKeywords.GROUND_TRUTH.value in self.config:
            self.ground_truth_dataloader = self._initialize_dataloader(args,
                subconfig_keys = self.subconfig_keys + [ModelConfigKeywords.GROUND_TRUTH.value])
    def __call__(self):
        raise Exception('Not Implemented')
    

    def save_to_dataframe(self,evaluation_results):

        self.data_io.atomic_operation(EvaluationResults,
            data_args={}, 
            atomic_function = self.combine_data_in_dataframe, 
            new_data = evaluation_results)


        # data_args = {}
        # if self.data_io.is_file_present(EvaluationResults,data_args = data_args):
        #     df = self.data_io.load_data(EvaluationResults,data_args = data_args)
        # else:
        #     df = {}
        
        # if self.global_config_name in df:
        #     old_results = df[self.global_config_name]
        #     df[self.global_config_name] = {**old_results, **evaluation_results}
        # else:
        #     df[self.global_config_name] = evaluation_results
        
        # data_args[EvaluationResults.DATA] = df

        # self.data_io.save_data(EvaluationResults,data_args = data_args)


    def combine_data_in_dataframe(self,df,evaluation_results):
        if self.global_config_name in df:
            old_results = df[self.global_config_name]
            df[self.global_config_name] = {**old_results, **evaluation_results}
        else:
            df[self.global_config_name] = evaluation_results
        return df
        
        #data_args[EvaluationResults.DATA] = df
        
        


