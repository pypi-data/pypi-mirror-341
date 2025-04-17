from itertools import product
from omegaconf import OmegaConf
from file_golem import Config
import io
from enum import Enum
from ml_golem.model_loading_logic.config_class_instantiator import ConfigBasedClass
from ml_golem.datatypes import GridShellScript, GridSlurmScript, SlurmOutputStd, SlurmOutputErr
import pandas as pd


def _add_grid_search_args(parser,action_list):
    parser.add_argument('-gsn','--grid_search_name',type=str,default=None , help='Build a grid search object')
    parser.add_argument('-gsp','--grid_search_params', nargs='+', default=[], help='Build a grid search object')
    parser.add_argument('-ga','--grid_actions', nargs='+', default=[], help='Actions for the grid search to run per config')
    parser.add_argument('-ges','--grid_search_style', type=str, default=GridSearchExecutionStyle.NONE.value, help='How to execute the grid search')
    parser.add_argument('-gsc', '--grid_slurm_config', type=str, default=None, help='config to specify slurm parameters')
    action_list.append(lambda args: (GridSearchBuilder(args)() or True) if args.grid_search_name is not None else False)
    return parser, action_list

class GridSearchExecutionStyle(Enum):
    SEQUENTIAL = 'sequential'
    SLURM = 'slurm'
    NONE = 'none'

class GridSearchBuilder(ConfigBasedClass):
    def __init__(self,args):
        super().__init__(args)
        self.grid_search_name = args.grid_search_name
        self.grid_search_style = args.grid_search_style
        self.grid_search_params = args.grid_search_params
        self.grid_slurm_config = args.grid_slurm_config
        if len(self.grid_search_params) == 0:
            raise Exception('No grid search params provided')
        self.grid_actions = args.grid_actions
        self.parse_grid_params()
        self.config_list = []


    def __call__(self):
        print('Building grid search...')

        self.build_configs()

        if len(self.grid_actions) == 0:
            raise Exception('No grid actions provided')
        if self.grid_search_style == GridSearchExecutionStyle.SEQUENTIAL.value:
            self.build_and_execute_sequential_shell_script()
        elif self.grid_search_style == GridSearchExecutionStyle.SLURM.value:
            self.build_and_execute_slurm_script()

    def build_and_execute_slurm_script(self):
        slurm_script_file_name, total_array_length = self.build_slurm_script()
        command = f'sbatch -a 0-{total_array_length-1} ./{slurm_script_file_name}'
        self.data_io.run_system_command(command)


    def build_slurm_script(self):
        slurm_config = self.data_io.load_config(self.grid_slurm_config)

        script_buffer = io.StringIO()
        script_buffer.write(f'#!/bin/bash\n')
        
        partition = slurm_config.get('partition', 'a100')
        script_buffer.write(f'#SBATCH --partition={partition}\n')

        gpu = slurm_config.get('gpu', 0)
        script_buffer.write(f'#SBATCH --gres=gpu:{gpu}\n')

        cpu = slurm_config.get('cpu',1)
        script_buffer.write(f'#SBATCH -c {cpu}\n')

        time = slurm_config.get('time','1-00:00')
        script_buffer.write(f'#SBATCH -t {time}\n')

        memory = slurm_config.get('memory', '1G')
        script_buffer.write(f'#SBATCH --mem={memory}\n')

        data_args = {
            GridSlurmScript.CONFIG_NAME: self.global_config_name,
            GridSlurmScript.GRID_DIRECTORY: self.grid_search_name
        }

        slurm_output_directory = self.data_io.get_data_path(SlurmOutputStd,data_args = data_args)
        self.data_io.create_directory(slurm_output_directory)
        script_buffer.write(f'#SBATCH -o {slurm_output_directory}\n')

        slurm_error_directory = self.data_io.get_data_path(SlurmOutputErr,data_args = data_args)
        script_buffer.write(f'#SBATCH -e {slurm_error_directory}\n')
        script_buffer.write(f'eval "$(conda shell.bash hook)"\n')
        script_buffer.write(f'conda activate {self.data_io.system_config.base_conda_name}\n')


        grid_array_lengths = [len(array) for array in self.grid_arrays]
        for i in range(len(grid_array_lengths)):
            
            modulus= grid_array_lengths[i]
            divisor = 1
            for j in range(i + 1,len(grid_array_lengths)):
                divisor *= grid_array_lengths[j]

            script_buffer.write( f'i_{i}=$(( ($SLURM_ARRAY_TASK_ID / {divisor}) % {modulus} ))\n')

        config_file = self.data_io.get_data_path(Config, data_args={
            Config.CONFIG_NAME: self.global_config_name,
            Config.GRID_DIRECTORY: self.grid_search_name,
            Config.GRID_IDX: [f'${{i_{i}}}' for i in range(len(grid_array_lengths))],
        })
        for action_code in self.grid_actions:
            script_buffer.write(f'python main.py --{action_code} -c {config_file}\n')
            script_buffer.write(f'echo ""\n')

        total_array_length = 1
        for array_length in grid_array_lengths:
            total_array_length *= array_length

        return self._save_script_and_return_path(script_buffer,GridSlurmScript) ,total_array_length



    def parse_grid_params(self):
        self.grid_keys = []
        self.grid_arrays = []
        self.grid_dict= {}
        for param in sorted(self.grid_search_params):
            key, array = param.split('=')
            self.grid_keys.append(key)
            self.grid_arrays.append(array.split(','))

            self.grid_dict[key] = array.split(',')

    

    def config_info_iterator(self):
        for array_combo, grid_indices in zip(product(*self.grid_arrays), product(*[range(len(array)) for array in self.grid_arrays])):
            grid_args = dict(zip(self.grid_keys, array_combo))
            data_args = {
                Config.CONFIG_NAME: self.global_config_name,
                Config.GRID_DIRECTORY: self.grid_search_name,
                Config.GRID_IDX: grid_indices}
            yield data_args, grid_args


    def build_dataframe(self,evaluation_results):
        all_data = []
        for data_args, grid_args in self.config_info_iterator():
            data_sample = {}
            for key in grid_args.keys():
                data_sample[key] = grid_args[key]
            config_file = self.data_io.get_data_path(Config, data_args=data_args)

            config_evaluation = evaluation_results[config_file]

            for key in config_evaluation.keys():
                data_sample[key] = config_evaluation[key]
            all_data.append(data_sample)
        df = pd.DataFrame(all_data)
        return df


    def build_configs(self):
        for data_args, grid_args in self.config_info_iterator():
            override_config = OmegaConf.create({
                'defaults': [self.global_config_name],
            })
            for grid_key in grid_args:
                if grid_key == 'defaults':
                    override_config['defaults'] = [grid_args[grid_key]] + override_config['defaults']
                else: 
                    key_split = grid_key.split('.')
                    nested_config_condition = {}
                    current = nested_config_condition
                    for key in key_split[:-1]:  
                        current = current.setdefault(key, {}) 
                    current[key_split[-1]] = grid_args[grid_key] 

                    override_config = OmegaConf.merge(override_config, OmegaConf.create(nested_config_condition))

            data_args[Config.DATA]= override_config
            self.data_io.save_data(Config, data_args = data_args)
            config_file_name = self.data_io.get_data_path(Config, data_args = data_args)
            self.config_list.append(config_file_name)



    def build_configs_deprecated(self):
        for array_combo, grid_indices in zip(product(*self.grid_arrays), product(*[range(len(array)) for array in self.grid_arrays])):
            grid_args = dict(zip(self.grid_keys, array_combo))
            override_config = OmegaConf.create({
                'defaults': [self.global_config_name],
            })
            for grid_key in grid_args:
                if grid_key == 'defaults':
                    override_config['defaults'] = [grid_args[grid_key]] + override_config['defaults']
                else: 
                    key_split = grid_key.split('.')
                    nested_config_condition = {}
                    current = nested_config_condition
                    for key in key_split[:-1]:  
                        current = current.setdefault(key, {}) 
                    current[key_split[-1]] = grid_args[grid_key] 

                    override_config = OmegaConf.merge(override_config, OmegaConf.create(nested_config_condition))

            data_args = {
                Config.CONFIG_NAME: self.global_config_name,
                Config.GRID_DIRECTORY: self.grid_search_name,
                Config.GRID_IDX: grid_indices,
                Config.DATA: override_config}
            self.data_io.save_data(Config, data_args = data_args)
        

    def build_and_execute_sequential_shell_script(self):
        shell_script_file_name = self.build_shell_script()
        command = f'./{shell_script_file_name}'
        self.data_io.run_system_command(command)

    def build_shell_script(self):
        script_buffer = io.StringIO()
        script_buffer.write(f'#!/bin/bash\n')
        for config_file in self.config_list:
            for action_code in self.grid_actions:
                script_buffer.write(f'python main.py --{action_code} -c {config_file}\n')
                script_buffer.write(f'echo ""\n')
        return self._save_script_and_return_path(script_buffer,GridShellScript)
    
    def _save_script_and_return_path(self,script_buffer,script_class):
        script = script_buffer.getvalue()
        script_buffer.close()
        data_args = {
            script_class.CONFIG_NAME: self.global_config_name,
            script_class.GRID_DIRECTORY: self.grid_search_name,
            script_class.DATA: script}
        
        self.data_io.save_data(script_class, data_args = data_args)
        script_file_name = self.data_io.get_data_path(script_class, data_args = data_args)
        return script_file_name
