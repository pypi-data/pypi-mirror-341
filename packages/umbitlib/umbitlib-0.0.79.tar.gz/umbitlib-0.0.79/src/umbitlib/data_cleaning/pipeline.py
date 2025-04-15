import time
import pandas as pd

class DataCleaningPipeline:
    def __init__(self, verbose=False, continue_on_error=False, log_file=None):
        """
        Create a data cleaning pipeline.
        
        Args:
            verbose (bool): If True, print steps during execution.
            continue_on_error (bool): If True, continue even if a step fails.
            log_file (str): Optional path to log execution details to a file.
        """
        self.steps = []
        self.verbose = verbose
        self.continue_on_error = continue_on_error
        self.log_file = log_file

    def add_step(self, name, function, **kwargs):  
        """
        Add a step with keyword arguments as parameters.
        """
        self.steps.append({'name': name, 'function': function, 'kwargs': kwargs})

    def remove_step(self, name):
        self.steps = [step for step in self.steps if step['name'] != name]

    def clear_steps(self):
        self.steps = []

    def reorder_steps(self, new_order):
        """
        Reorder the steps based on a list of step names.
        
        Args:
            new_order (list): A list of step names in the desired order.
        
        Raises:
            ValueError: If any name in new_order does not exist in current steps.
        """
        name_to_step = {step['name']: step for step in self.steps}

        if set(new_order) != set(name_to_step.keys()):
            raise ValueError("New order must contain exactly the same step names as existing steps.")

        self.steps = [name_to_step[name] for name in new_order]

    def list_steps(self):
        return [step['name'] for step in self.steps]

    def _log(self, message):
        if self.verbose:
            print(message)
        if self.log_file:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')

    def execute(self, df):
        results = []
        current_df = df.copy()

        for step in self.steps:
            step_name = step['name']
            func = step['function']
            kwargs = step.get('kwargs', {})
            before_shape = current_df.shape
            start_time = time.time()

            self._log(f"Running step: {step_name}")

            try:
                current_df = func(current_df, **kwargs)
                after_shape = current_df.shape
                elapsed = round(time.time() - start_time, 4)

                result = {
                    'step': step_name,
                    'status': 'success',
                    'rows_before': before_shape[0],
                    'rows_after': after_shape[0],
                    'cols_before': before_shape[1],
                    'cols_after': after_shape[1],
                    'rows_affected': before_shape[0] - after_shape[0],
                    'cols_affected': before_shape[1] - after_shape[1],
                    'duration_sec': elapsed
                }

                results.append(result)
                self._log(f"✅ {step_name} succeeded in {elapsed}s")

            except Exception as e:
                elapsed = round(time.time() - start_time, 4)
                result = {
                    'step': step_name,
                    'status': 'failed',
                    'error': str(e),
                    'duration_sec': elapsed
                }

                results.append(result)
                self._log(f"❌ {step_name} failed: {e}")

                if not self.continue_on_error:
                    break

        return current_df, results