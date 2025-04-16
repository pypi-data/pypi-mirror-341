import shutil
import sys
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Tuple

import uuid
import click
from loguru import logger
import pandas as pd
import os

from rnadvisor.enums.list_dockers import SERVICES, SERVICES_DICT

from rnadvisor.enums.list_dockers import ALL, ALL_METRICS, ALL_SF

import subprocess
from importlib.resources import files


from rnadvisor.predict_abstract import PredictAbstract
from rnadvisor.utils.utils import TqdmCompatibleHandler


@dataclass
class RNAdvisorCLI:
    native_path: Optional[str]
    pred_dir: str
    out_path: Optional[str]
    out_time_path: Optional[str]
    scores: List[str]
    sort_by: Optional[str]
    params: Optional[Dict[str, Any]]
    tmp_dir_out: Optional[str] = None
    tmp_dir_out_times: Optional[str] = None

    def __post_init__(self):
        self.check_docker()
        self.clean_prev_results()
        self.check_init_paths(self.native_path, self.pred_dir)
        self.scores = self.check_scores(self.scores)
        self._init_logger()
        self.volumes = self.add_volumes()

    def check_docker(self):
        """
        Check if docker-compose is installed
        """
        if shutil.which("docker") is None:
            raise RuntimeError("Docker is not installed or not in PATH.")
        try:
            subprocess.run(
                ["docker", "compose", "version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Docker Compose is not available: {e.stderr.decode().strip()}")

    def find_docker_compose_cmd(self):
        if shutil.which("docker") and self._has_subcommand("compose"):
            return ["docker", "compose"]
        elif shutil.which("docker-compose"):
            return ["docker-compose"]
        else:
            raise RuntimeError("Neither 'docker compose' nor 'docker-compose' is available.")

    def _has_subcommand(self, subcommand):
        try:
            subprocess.run(["docker", subcommand, "version"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception:
            return False

    def add_volumes(self) -> Dict[str, str]:
        """
        Return a dict mapping host absolute paths to container paths.
        """
        volumes = {}

        def bind_path(host_path: str, container_path: str):
            if host_path:
                abs_host = os.path.abspath(host_path)
                volumes[abs_host] = container_path

        bind_path(self.native_path, "/data/native.pdb")
        bind_path(self.pred_dir, "/data/preds")
        bind_path(self.tmp_dir_out, "/app/tmp/results")
        bind_path(self.tmp_dir_out_times, "/app/tmp/results_time")

        return volumes

    def clean_prev_results(self):
        """
        Remove the previous results if they exist.
        """
        shutil.rmtree(self.tmp_dir_out, ignore_errors=True)
        shutil.rmtree(self.tmp_dir_out_times, ignore_errors=True)

    def _init_logger(self, verbose: bool = True):
        logger.remove()
        logger.add(
            sys.stderr,
            level="DEBUG" if verbose else "INFO",
            filter=lambda record: record["level"].name != "INFO",
            colorize=True,
            backtrace=True,
            diagnose=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

        logger.add(
            TqdmCompatibleHandler(),
            level="INFO",
            filter=lambda record: record["level"].name == "INFO",
            colorize=True,
            backtrace=True,
            diagnose=True,
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )

    def check_scores(self, scores: List[str]) -> List[str]:
        """
        Check the given metrics/scoring functions to use.
        :param scores: list of metrics/scoring functions to use, or keywords like "ALL", "METRICS", "SF"
        :return: list of valid metrics/scoring functions that can be used
        """
        expanded_scores = []
        for score in scores:
            score_lower = score.lower()
            if score_lower == "all":
                expanded_scores.extend(ALL)
            elif score_lower == "metrics":
                expanded_scores.extend(ALL_METRICS)
            elif score_lower == "sf":
                expanded_scores.extend(ALL_SF)
            else:
                expanded_scores.append(score_lower)
        # Make the list unique and filter valid scores
        unique_scores = list(set(expanded_scores))
        return [score for score in unique_scores if score in SERVICES]

    def check_init_paths(self, native_path: Optional[str], pred_dir: Optional[str]):
        """
        Check the different paths depending if there is a native path or not
        :param native_path: path to a native structure. If None, it will only compute scoring functions.
        :param pred_dir: path to a directory or single RNA `.pdb` file.
        """
        if native_path is None and pred_dir is None:
            msg = "Either native_path or pred_dir must be provided."
            logger.warning(msg)
            raise ValueError(msg)
        elif native_path is not None and pred_dir is None:
            logger.info(f"No prediction directory provided. Using native path: {native_path}")
        elif native_path is not None and pred_dir is not None:
            if os.path.isfile(pred_dir):
                logger.info(f"Using prediction file: {pred_dir}")
                return None
            if not os.path.isdir(pred_dir):
                raise ValueError(f"Prediction directory {pred_dir} is not a valid file or directory.")
            logger.info(f"Using native path: {native_path} and prediction directory: {pred_dir}")
        elif native_path is None and pred_dir is not None:
            if not (os.path.isdir(pred_dir) or os.path.isfile(pred_dir)):
                raise ValueError(
                    f"Prediction directory {pred_dir} is not a valid file or directory.")
            logger.info(f"Using prediction directory: {pred_dir}")

    def get_services(self) -> Dict:
        """
        Get the different docker services to run
        :return: a dictionary of services
        """
        services = {}
        for key in self.scores:
            service = SERVICES_DICT[key]
            # No out_path here because it is set in tmp dir
            service["args"].update({
                "--native_path": "/data/native.pdb" if self.native_path is not None else "",
                "--pred_dir": "/data/preds" if self.pred_dir is not None else "",
                "--params": self.params if self.params is not None else "",
                "--out_path": f"/app/tmp/results/{key}.csv" if self.tmp_dir_out is not None else "",
                "--out_time_path": f"/app/tmp/results_time/{key}.csv" if self.tmp_dir_out_times is not None else "",
            })
            services[key] = service
        return services

    def get_cmd(self, service: str) -> List:
        """
        Return the docker command to launch, set the name of the image and the volumes
        :param service: name of the metric/scoring function
        :return: a list of arguments for the command
        """
        dc_path = str(files("rnadvisor").joinpath("docker-compose.slim.yaml"))
        dc = self.find_docker_compose_cmd()
        cmd = dc + ["-f", dc_path, "run", "--rm"]
               # '--user', f"{os.getuid()}:{os.getgid()}"]
        for key, val in self.volumes.items():
            if val is not None:
                cmd += ["-v", f"{key}:{val}"]
        cmd+= [service]
        return cmd

    def run_services(self, services: Dict) -> List:
        """
        Return the different docker images to run
        :param services: a dictionary of services with the different arguments
        """
        processes = []
        for service, config in services.items():
            cmd = self.get_cmd(service)
            for key, val in config["args"].items():
                cmd += [key, val]
            cmd+=["--quiet"]
            process = subprocess.Popen(cmd)
            processes.append((service, process))
        return processes

    def wait_services(self, processes: List):
        """
        Run and wait for the different docker images to finish
        :param processes: a list of processes to wait for
        """
        for service, process in processes:
            ret_code = process.wait()
            if ret_code == 0:
                logger.info(f"✅ {service} completed successfully ✅")
            else:
                logger.info(f"❌ {service} exited with error code {ret_code} ❌")

    def merge_dfs(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Merge all the predicted dataframes into a single dataframe
        :return: the merged dataframes with all the scores
        """
        df_scores, df_times = None, None
        try:
            csvs = [os.path.join(self.tmp_dir_out, name) for name in os.listdir(self.tmp_dir_out) if name.endswith(".csv")]
            csvs_times = [os.path.join(self.tmp_dir_out_times, name) for name in os.listdir(self.tmp_dir_out_times) if name.endswith(".csv")]
            df_scores = pd.concat([pd.read_csv(f, index_col=0) for f in csvs], axis=1)
            df_times = pd.concat([pd.read_csv(f, index_col=0) for f in csvs_times], axis=1)
        except (PermissionError, FileNotFoundError) as e:
            logger.warning("No scores or times found. Returning empty dataframes.")
        shutil.rmtree(self.tmp_dir_out_times, ignore_errors=True)
        shutil.rmtree(self.tmp_dir_out, ignore_errors=True)
        return df_scores, df_times

    def save_dfs(self, df: pd.DataFrame, df_times: pd.DataFrame, out_path: Optional[str], out_time_path: Optional[str]):
        """
        Save the output dictionary into dataframes
        :param df: predicted scores
        :param df_times: time for each RNA
        :param out_path: path where to save the predictions
        :param out_time_path: path where to save the times for each prediction
        """
        out_path, out_time_path = PredictAbstract.init_out_path(out_path, out_time_path)
        logger.info(f"Saving predictions to {out_path}")
        if df is None:
            logger.warning("No scores found")
            return None
        df.to_csv(out_path, index=True)
        logger.info(f"Saving time to {out_time_path}")
        df_times.to_csv(out_time_path, index=True)

    def predict(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Run the predictions for the different metrics/scoring functions
        :return:
        """
        services = self.get_services()
        processes = self.run_services(services)
        self.wait_services(processes)
        df, df_times = self.merge_dfs()
        self.save_dfs(df, df_times, self.out_path, self.out_time_path)
        return df, df_times

@click.command()
@click.option("--native_path", type=str, default=None, help="Path to the native structure.")
@click.option("--pred_dir", type=str, required=True, help="Path to the prediction directory.")
@click.option("--out_path", type=str, default=None, help="Path to save the results.")
@click.option("--out_time_path", type=str, default=None, help="Path to save the time results.")
@click.option( "--scores", type=str, default="lociparse", help="Comma-separated list of scores to compute.",
    callback=lambda ctx, param, value: value.split(",")
)
@click.option("--sort_by", type=str, default=None, help="Sort by a specific score.")
@click.option("--params", type=str, default=None, help="Additional parameters for scoring functions.")
def main(native_path, pred_dir, out_path, out_time_path, scores, sort_by, params):
    """
    Main function to run the RNAdvisor CLI
    :param native_path: path to the native structure.
    :param pred_dir: path to the prediction directory.
    :param out_path: path to save the results.
    :param out_time_path: path to save the time results.
    :param scores: list of scores to compute.
    :param sort_by: sort by a specific score.
    :param params: additional parameters for scoring functions.
    """
    tmp_dir = "/tmp/rnadvisor"
    unique_id = uuid.uuid4().hex[:8]
    out_dir = os.path.join(tmp_dir, f"run_{unique_id}")
    os.makedirs(out_dir, exist_ok=True)
    out_dir_scores = os.path.join(out_dir, "scores")
    out_dir_times = os.path.join(out_dir, "times")
    os.makedirs(out_dir_scores, exist_ok=True)
    os.makedirs(out_dir_times, exist_ok=True)
    rnadvisor_cli = RNAdvisorCLI(
        native_path=native_path,
        pred_dir=pred_dir,
        out_path=out_path,
        out_time_path=out_time_path,
        scores=list(scores),
        sort_by=sort_by,
        params=params,
        tmp_dir_out=out_dir_scores,
        tmp_dir_out_times=out_dir_times,
    )
    rnadvisor_cli.predict()
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir, ignore_errors=True)
