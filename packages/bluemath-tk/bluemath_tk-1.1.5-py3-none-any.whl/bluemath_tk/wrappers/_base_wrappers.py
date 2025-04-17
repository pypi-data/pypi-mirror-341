import copy
import itertools
import os
import os.path as op
import subprocess
import threading
from queue import Queue
from typing import List, Union

import numpy as np
import pandas as pd
import xarray as xr
from jinja2 import Environment, FileSystemLoader

from ..core.models import BlueMathModel
from ._utils_wrappers import copy_files, write_array_in_file

sbatch_file_example = """
#!/bin/bash
#SBATCH --job-name=your_job_name  # Job name
#SBATCH --partition=geocean       # Standard output and error log
#SBATCH --mem=4gb                 # Memory per node in GB (see also --mem-per-cpu)

case_dir=$(ls | awk "NR == $SLURM_ARRAY_TASK_ID")
yourLauncher.sh --case-dir $case_dir > $case_dir/wrapper_out.log 2> $case_dir/wrapper_error.log
"""


class BaseModelWrapper(BlueMathModel):
    """
    Base class for numerical models wrappers.

    Attributes
    ----------
    templates_dir : str
        The directory where the templates are stored.
    metamodel_parameters : dict
        The parameters to be used in the templates.
    fixed_parameters : dict
        The fixed parameters for the model.
    output_dir : str
        The directory where the output files will be saved.
    env : Environment
        The Jinja2 environment.
    templates_name : List[str]
        The names of the templates.
    cases_dirs : List[str]
        The list with cases directories.
    cases_context : List[dict]
        The list with cases context.
    thread : threading.Thread
        The thread for background execution.
    status_queue : Queue
        The queue to update the status.
    sbatch_file_example : str
        The example sbatch file.

    Methods
    -------
    _check_parameters_type -> None
        Check if the parameters have the correct type.
    _exec_bash_commands -> None
        Execute bash commands.
    list_available_launchers -> dict
        List the available launchers.
    list_default_parameters -> pd.DataFrame
        List the default parameters.
    set_cases_dirs_from_output_dir -> None
        Set the cases directories from the output directory.
    write_array_in_file -> None
        Write an array in a file.
    copy_files -> None
        Copy file(s) from source to destination.
    render_file_from_template -> None
        Render a file from a template.
    create_cases_context_one_by_one -> List[dict]
        Create an array of dictionaries with the combinations of values from the
        input dictionary, one by one.
    create_cases_context_all_combinations -> List[dict]
        Create an array of dictionaries with each possible combination of values
        from the input dictionary.
    build_case -> None
        Build the input files for a case.
    prebuild_case -> None
        Build the input dir and context for a case.
    build_cases -> None
        Create the cases folders and render the input files.
    run_case -> None
        Run the case based on the launcher specified.
    run_cases -> None
        Run the cases based on the launcher specified.
        Parallel execution is optional.
        Cases to run can be specified.
    run_cases_bulk -> None
        Run the cases based on the launcher specified.
    postprocess_case -> None
        Postprocess the model output for a specific case.
    join_postprocessed_files -> xr.Dataset
        Join the postprocessed files.
    postprocess_cases -> Union[xr.Dataset, List[xr.Dataset]]
        Postprocess the model output.
    """

    sbatch_file_example = sbatch_file_example

    def __init__(
        self,
        templates_dir: str,
        metamodel_parameters: dict,
        fixed_parameters: dict,
        output_dir: str,
        templates_name: List[str] = "all",
        default_parameters: dict = None,
    ) -> None:
        """
        Initialize the BaseModelWrapper.
        """

        super().__init__()
        if default_parameters is not None:
            fixed_parameters = self._check_parameters_type(
                default_parameters=default_parameters,
                metamodel_parameters=metamodel_parameters,
                fixed_parameters=fixed_parameters,
            )
        self.templates_dir = templates_dir
        self.metamodel_parameters = metamodel_parameters
        self.fixed_parameters = fixed_parameters
        self.output_dir = output_dir
        self._env = Environment(loader=FileSystemLoader(self.templates_dir))
        if templates_name == "all":
            self.logger.info(
                f"Templates name is 'all', so all templates in {self.templates_dir} will be used."
            )
            self.templates_name = self.env.list_templates()
            self.logger.info(f"Templates names: {self.templates_name}")
        else:
            self.templates_name = templates_name
        self.cases_dirs: List[str] = []
        self.cases_context: List[dict] = []
        self.thread: threading.Thread = None
        self.status_queue: Queue = None

    @property
    def env(self) -> Environment:
        return self._env

    def _check_parameters_type(
        self,
        default_parameters: dict,
        metamodel_parameters: dict,
        fixed_parameters: dict,
    ) -> None:
        """
        Check if the parameters have the correct type.
        This functions checks if the parameters in the metamodel_parameters have the
        correct type according to the default_parameters.
        Then, it updates the fixed_parameters with the default_parameters values.

        Raises
        ------
        ValueError
            If a parameter has the wrong type.
        """

        for metamodel_param, param_value in metamodel_parameters.items():
            if metamodel_param not in default_parameters:
                self.logger.warning(
                    f"Parameter {metamodel_param} is not in the default_parameters"
                )
            else:
                if isinstance(param_value, (list, np.ndarray)) and all(
                    isinstance(item, default_parameters[metamodel_param]["type"])
                    for item in param_value
                ):
                    self.logger.info(
                        f"Parameter {metamodel_param} has the correct type: {default_parameters[metamodel_param]}"
                    )
                else:
                    raise ValueError(
                        f"Parameter {metamodel_param} has the wrong type: {default_parameters[metamodel_param]}"
                    )
        for default_param, param_info in default_parameters.items():
            if (
                default_param not in fixed_parameters
                and param_info.get("value") is not None
            ):
                fixed_parameters[default_param] = param_info.get("value")

        return fixed_parameters

    def _exec_bash_commands(
        self, str_cmd: str, out_file: str = None, err_file: str = None, cwd: str = None
    ) -> None:
        """
        Execute bash commands.

        Parameters
        ----------
        str_cmd : str
            The bash command.
        out_file : str, optional
            The name of the output file. If None, the output will be printed in the terminal.
            Default is None.
        err_file : str, optional
            The name of the error file. If None, the error will be printed in the terminal.
            Default is None.
        cwd : str, optional
            The current working directory. Default is None.
        """

        _stdout = None
        _stderr = None

        if out_file:
            _stdout = open(out_file, "w")
        if err_file:
            _stderr = open(err_file, "w")

        try:
            _s = subprocess.run(
                str_cmd,
                shell=True,
                stdout=_stdout,
                stderr=_stderr,
                cwd=cwd,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error running command: {str_cmd}")
            self.logger.error(f"Error: {e}")

        if out_file:
            _stdout.flush()
            _stdout.close()
        if err_file:
            _stderr.flush()
            _stderr.close()

    def list_available_launchers(self) -> dict:
        """
        List the available launchers.

        Returns
        -------
        dict
            A list with the available launchers.
        """

        if hasattr(self, "available_launchers"):
            return self.available_launchers
        else:
            raise AttributeError("The attribute available_launchers is not defined.")

    def list_default_parameters(self) -> pd.DataFrame:
        """
        List the default parameters.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the default parameters.
        """

        if hasattr(self, "default_parameters"):
            return pd.DataFrame(self.default_parameters)
        else:
            raise AttributeError(
                "The attribute default_parameters is not defined in the child class."
            )

    def set_cases_dirs_from_output_dir(self) -> None:
        """
        Set the cases directories from the output directory.
        """

        if self.cases_dirs:
            self.logger.warning("Cases directories already set... resetting.")

        self.cases_dirs = sorted(
            [
                op.join(self.output_dir, case_dir)
                for case_dir in os.listdir(self.output_dir)
                if op.isdir(op.join(self.output_dir, case_dir))
            ]
        )

        self.logger.info(f"Cases directories set from {self.output_dir}.")

    def write_array_in_file(self, array: np.ndarray, filename: str) -> None:
        """
        Write an array in a file.

        Parameters
        ----------
        array : np.ndarray
            The array to be written. Can be 1D or 2D.
        filename : str
            The name of the file.
        """

        write_array_in_file(array=array, filename=filename)

    def copy_files(self, src: str, dst: str) -> None:
        """
        Copy file(s) from source to destination.

        Parameters
        ----------
        src : str
            The source file.
        dst : str
            The destination file.
        """

        copy_files(src=src, dst=dst)

    def render_file_from_template(
        self, template_name: str, context: dict, output_filename: str = None
    ) -> None:
        """
        Render a file from a template.

        Parameters
        ----------
        template_name : str
            The name of the template file.
        context : dict
            The context to be used in the template.
        output_filename : str, optional
            The name of the output file. If None, it will be saved in the output
            directory with the same name as the template.
            Default is None.
        """

        template = self.env.get_template(name=template_name)
        rendered_content = template.render(context)
        if output_filename is None:
            output_filename = op.join(self.output_dir, template_name)
        with open(output_filename, "w") as f:
            f.write(rendered_content)

    def create_cases_context_one_by_one(self) -> List[dict]:
        """
        Create an array of dictionaries with the combinations of values from the
        input dictionary, one by one.

        Returns
        -------
        List[dict]
            A list of dictionaries, each representing a unique combination of
            parameter values.
        """

        num_cases = len(next(iter(self.metamodel_parameters.values())))
        array_of_contexts = []
        for param, values in self.metamodel_parameters.items():
            if len(values) != num_cases:
                raise ValueError(
                    f"All parameters must have the same number of values in one_by_one mode, check {param}"
                )

        for case_num in range(num_cases):
            case_context = {
                param: values[case_num]
                for param, values in self.metamodel_parameters.items()
            }
            array_of_contexts.append(case_context)

        return array_of_contexts

    def create_cases_context_all_combinations(self) -> List[dict]:
        """
        Create an array of dictionaries with each possible combination of values
        from the input dictionary.

        Returns
        -------
        List[dict]
            A list of dictionaries, each representing a unique combination of
            parameter values.
        """

        keys = self.metamodel_parameters.keys()
        values = self.metamodel_parameters.values()
        combinations = itertools.product(*values)

        array_of_contexts = [
            dict(zip(keys, combination)) for combination in combinations
        ]

        return array_of_contexts

    def build_case(
        self,
        case_context: dict,
        case_dir: str,
    ) -> None:
        """
        Build the input files for a case.

        Parameters
        ----------
        case_context : dict
            The case context.
        case_dir : str
            The case directory.
        """

        pass

    def prebuild_case(
        self,
        case_num: dict,
        case_context: str,
        cases_name_format: callable,
    ) -> None:
        """
        Build the input dir and context for a case.

        Parameters
        ----------
        case_num : int
            The case number.
        case_context : dict
            The case context.
        """

        case_context["case_num"] = case_num
        case_dir = op.join(self.output_dir, cases_name_format(case_context))
        self.cases_dirs.append(case_dir)
        os.makedirs(case_dir, exist_ok=True)
        case_context.update(self.fixed_parameters)
        self.build_case(
            case_context=case_context,
            case_dir=case_dir,
        )
        for template_name in self.templates_name:
            self.render_file_from_template(
                template_name=template_name,
                context=case_context,
                output_filename=op.join(case_dir, template_name),
            )

    def build_cases(
        self,
        mode: str = "one_by_one",
        cases_to_build: List[int] = None,
        cases_name_format: callable = lambda ctx: f"{ctx.get('case_num'):04}",
        num_workers: int = None,
    ) -> None:
        """
        Create the cases folders and render the input files.

        Parameters
        ----------
        mode : str, optional
            The mode to create the cases. Can be "all_combinations" or "one_by_one".
            Default is "one_by_one".
        cases_to_build : List[int], optional
            The list with the cases to build. Default is None.
        cases_name_format : callable, optional
            The function to format the case name. Default is a lambda function
            that formats the case number with leading zeros.
        num_workers : int, optional
            The number of parallel workers. Default is None.

        Raises
        ------
        ValueError
            If the mode is not valid.
        """

        if num_workers is None:
            num_workers = self.num_workers

        if mode == "all_combinations":
            self.cases_context = self.create_cases_context_all_combinations()
        elif mode == "one_by_one":
            self.cases_context = self.create_cases_context_one_by_one()
        else:
            raise ValueError(f"Invalid mode to create cases: {mode}")

        if cases_to_build is not None:
            self.cases_context = [self.cases_context[i] for i in cases_to_build]
        else:
            cases_to_build = list(range(len(self.cases_context)))

        if num_workers > 1:
            self.logger.debug(
                f"Building cases in parallel. Number of workers: {num_workers}."
            )
            _results = self.parallel_execute(
                func=self.prebuild_case,
                items=zip(cases_to_build, self.cases_context),
                num_workers=num_workers,
                cases_name_format=cases_name_format,
            )
        else:
            self.logger.debug("Building cases sequentially.")
            for case_num, case_context in zip(cases_to_build, self.cases_context):
                self.prebuild_case(
                    case_num=case_num,
                    case_context=case_context,
                    cases_name_format=cases_name_format,
                )

        self.logger.info(
            f"{len(self.cases_dirs)} cases created in {mode} mode and saved in {self.output_dir}"
        )

        # Save an example sbatch file in the output directory
        with open(f"{self.output_dir}/sbatch_example.sh", "w") as file:
            file.write(self.sbatch_file_example)
        self.logger.info(f"SBATCH example file generated in {self.output_dir}")

    def run_case(
        self,
        case_dir: str,
        launcher: str,
        output_log_file: str = "wrapper_out.log",
        error_log_file: str = "wrapper_error.log",
    ) -> None:
        """
        Run the case based on the launcher specified.

        Parameters
        ----------
        case_dir : str
            The case directory.
        launcher : str
            The launcher to run the case.
        output_log_file : str, optional
            The name of the output log file. Default is "wrapper_out.log".
        error_log_file : str, optional
            The name of the error log file. Default is "wrapper_error.log".
        """

        # Get launcher command from the available launchers
        launcher = self.list_available_launchers().get(launcher, launcher)

        # Run the case in the case directory
        self.logger.info(f"Running case in {case_dir} with launcher={launcher}.")
        output_log_file = op.join(case_dir, output_log_file)
        error_log_file = op.join(case_dir, error_log_file)
        self._exec_bash_commands(
            str_cmd=launcher,
            out_file=output_log_file,
            err_file=error_log_file,
            cwd=case_dir,
        )

    def run_cases(
        self,
        launcher: str,
        cases_to_run: List[int] = None,
        num_workers: int = None,
    ) -> None:
        """
        Run the cases based on the launcher specified.
        Cases to run can be specified.
        Parallel execution is optional by modifying the num_workers parameter.

        Parameters
        ----------
        launcher : str
            The launcher to run the cases.
        cases_to_run : List[int], optional
            The list with the cases to run. Default is None.
        num_workers : int, optional
            The number of parallel workers. Default is None.
        """

        if num_workers is None:
            num_workers = self.num_workers

        # Get launcher command from the available launchers
        launcher = self.list_available_launchers().get(launcher, launcher)

        if cases_to_run is not None:
            self.logger.warning(
                f"Cases to run was specified, so just {cases_to_run} will be run."
            )
            cases_dir_to_run = [self.cases_dirs[case] for case in cases_to_run]
        else:
            cases_dir_to_run = copy.deepcopy(self.cases_dirs)

        if num_workers > 1:
            self.logger.debug(
                f"Running cases in parallel with launcher={launcher}. Number of workers: {num_workers}."
            )
            _results = self.parallel_execute(
                func=self.run_case,
                items=cases_dir_to_run,
                num_workers=num_workers,
                launcher=launcher,
            )
        else:
            self.logger.debug(f"Running cases sequentially with launcher={launcher}.")
            for case_dir in cases_dir_to_run:
                try:
                    self.run_case(
                        case_dir=case_dir,
                        launcher=launcher,
                    )
                except Exception as exc:
                    self.logger.error(
                        f"Job for {case_dir} generated an exception: {exc}."
                    )

        self.logger.info("All cases executed.")

    def _run_cases_with_status(
        self,
        launcher: str,
        cases_to_run: List[int],
        num_workers: int,
        status_queue: Queue,
    ) -> None:
        """
        Run the cases and update the status queue.

        Parameters
        ----------
        launcher : str
            The launcher to run the cases.
        cases_to_run : List[int]
            The list with the cases to run.
        num_workers : int
            The number of parallel workers.
        status_queue : Queue
            The queue to update the status.
        """

        try:
            self.run_cases(launcher, cases_to_run, num_workers)
            status_queue.put("Completed")
        except Exception as e:
            status_queue.put(f"Error: {e}")

    def run_cases_in_background(
        self,
        launcher: str,
        cases_to_run: List[int] = None,
        num_workers: int = None,
    ) -> None:
        """
        Run the cases in the background based on the launcher specified.
        Cases to run can be specified.
        Parallel execution is optional by modifying the num_workers parameter.

        Parameters
        ----------
        launcher : str
            The launcher to run the cases.
        cases_to_run : List[int], optional
            The list with the cases to run. Default is None.
        num_workers : int, optional
            The number of parallel workers. Default is None.
        """

        if num_workers is None:
            num_workers = self.num_workers

        self.status_queue = Queue()
        self.thread = threading.Thread(
            target=self._run_cases_with_status,
            args=(launcher, cases_to_run, num_workers, self.status_queue),
        )
        self.thread.start()

    def get_thread_status(self) -> str:
        """
        Get the status of the background thread.

        Returns
        -------
        str
            The status of the background thread.
        """

        if self.thread is None:
            return "Not started"
        elif self.thread.is_alive():
            return "Running"
        else:
            return self.status_queue.get()

    def run_cases_bulk(
        self,
        launcher: str,
    ) -> None:
        """
        Run the cases based on the launcher specified.

        Parameters
        ----------
        launcher : str
            The launcher to run the cases.
        """

        self.logger.info(f"Running cases with launcher={launcher}.")
        self._exec_bash_commands(str_cmd=launcher, cwd=self.output_dir)

    def monitor_cases(self) -> None:
        """
        Return the status of the cases.
        """

        raise NotImplementedError("The method monitor_cases must be implemented.")

    def postprocess_case(self, case_num: int, case_dir: str) -> None:
        """
        Postprocess the model output.

        Parameters
        ----------
        case_num : int
            The case number.
        case_dir : str
            The case directory.
        """

        raise NotImplementedError("The method postprocess_case must be implemented.")

    def join_postprocessed_files(
        self, postprocessed_files: List[xr.Dataset]
    ) -> xr.Dataset:
        """
        Join the postprocessed files.

        Parameters
        ----------
        postprocessed_files : List[xr.Dataset]
            The list with the postprocessed files.
        """

        raise NotImplementedError(
            "The method join_postprocessed_files must be implemented."
        )

    def postprocess_cases(
        self,
        cases_to_postprocess: List[int] = None,
        write_output_nc: bool = True,
        clean_after: bool = False,
        force: bool = False,
        **kwargs,
    ) -> Union[xr.Dataset, List[xr.Dataset]]:
        """
        Postprocess the model output.
        All extra keyword arguments will be passed to the postprocess_case method.

        Parameters
        ----------
        cases_to_postprocess : List[int], optional
            The list with the cases to postprocess. Default is None.
        write_output_nc : bool, optional
            Write the output postprocessed file. Default is True.
        clean_after : bool, optional
            Clean the cases directories after postprocessing. Default is False.
        force : bool, optional
            Force the postprocessing. Default is False.
        **kwargs
            Additional keyword arguments to be passed to the postprocess_case method.

        Returns
        -------
        xr.Dataset or List[xr.Dataset]
            The postprocessed file or the list with the postprocessed files.
        """

        if force:
            kwargs["force"] = force

        output_postprocessed_file_path = op.join(
            self.output_dir, "output_postprocessed.nc"
        )
        if op.exists(output_postprocessed_file_path) and not force:
            self.logger.warning(
                "Output postprocessed file already exists. Skipping postprocessing."
            )
            return xr.open_dataset(output_postprocessed_file_path)

        if not self.cases_dirs:
            self.logger.warning(
                "Cases directories are not set and will be searched from the output directory."
            )
            self.set_cases_dirs_from_output_dir()

        if cases_to_postprocess is not None:
            self.logger.warning(
                f"Cases to postprocess was specified, so just {cases_to_postprocess} will be postprocessed."
            )
            self.logger.warning(
                "Remember you can just use postprocess_case method to postprocess a single case."
            )
            cases_dir_to_postprocess = [
                self.cases_dirs[case] for case in cases_to_postprocess
            ]
        else:
            cases_to_postprocess = list(range(len(self.cases_dirs)))
            cases_dir_to_postprocess = copy.deepcopy(self.cases_dirs)

        postprocessed_files = []
        for case_num, case_dir in zip(cases_to_postprocess, cases_dir_to_postprocess):
            try:
                postprocessed_file = self.postprocess_case(
                    case_num=case_num, case_dir=case_dir, **kwargs
                )
                postprocessed_files.append(postprocessed_file)
            except Exception as e:
                self.logger.error(
                    f"Output not postprocessed for case {case_num}. Error: {e}."
                )

        try:
            output_postprocessed = self.join_postprocessed_files(
                postprocessed_files=postprocessed_files
            )
            if write_output_nc:
                self.logger.info(
                    f"Writing output postprocessed file to {output_postprocessed_file_path}."
                )
                output_postprocessed.to_netcdf(output_postprocessed_file_path)
            if clean_after:
                self.logger.warning("Cleaning up all cases dirs.")
                # self._exec_bash_commands(
                #     str_cmd=f"rm -rf {self.output_dir}/*/*", cwd=self.output_dir
                # )
                self.logger.info("Clean up completed.")
            return output_postprocessed

        except NotImplementedError as exc:
            self.logger.error(f"Error joining postprocessed files: {exc}")
            return postprocessed_files
