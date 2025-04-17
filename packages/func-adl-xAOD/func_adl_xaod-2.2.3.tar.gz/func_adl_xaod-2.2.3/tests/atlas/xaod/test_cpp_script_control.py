# Tests that will make sure the runner.sh script can do everything it is supposed to do,
# as we are now asking a fair amount from it.
import ast
import os
import tempfile
from collections import namedtuple
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, List, Optional

import pytest
from func_adl import EventDataset
from func_adl_xAOD.atlas.xaod.executor import atlas_xaod_executor

from .config import local_path, run_long_running_tests

pytestmark = run_long_running_tests

ExecutorInfo = namedtuple("ExecutorInfo", "main_script output_filename")


class hash_event_dataset(EventDataset):
    def __init__(self, output_dir: Path):
        super().__init__()
        self._dir = output_dir

    async def execute_result_async(self, a: ast.AST, title: str) -> Any:
        if self._dir.exists():
            self._dir.mkdir(parents=True, exist_ok=True)
        exe = atlas_xaod_executor()
        f_spec = exe.write_cpp_files(exe.apply_ast_transformations(a), self._dir)
        return ExecutorInfo(f_spec.main_script, f_spec.result_rep.filename)


@pytest.fixture()
def cache_directory():
    "Return a directory that can be deleted when the test is done"
    with tempfile.TemporaryDirectory() as d_temp:
        yield Path(d_temp)


def generate_test_jet_fetch(cache_dir: Path):
    """
    Generate an expression and C++ files, etc., that contains code for a valid C++ run
    """
    return (
        hash_event_dataset(cache_dir)
        .SelectMany(lambda e: e.Jets("AntiKt4EMTopoJets"))
        .Select(lambda j: j.pt() / 1000.0)
        .value()
    )


def generate_test_jet_fetch_bad(cache_dir: Path):
    """
    Generate an expression and C++ files, etc., that contains code for a valid C++ run
    """
    return (
        hash_event_dataset(cache_dir)
        .SelectMany(lambda e: e.Jets("AntiKt4EMTopoJets"))
        .Select(lambda j: j.ptt() / 1000.0)
        .value()
    )


class docker_run_error(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


class docker_runner:
    def __init__(self, name: str, results_dir):
        self._name = name
        self.results_dir = results_dir

    def compile(self, info):
        "Run the script as a compile"

        results_dir = tempfile.TemporaryDirectory()
        self.exec(
            f"cd /home/atlas; chmod +x /scripts/{info.main_script}; /scripts/{info.main_script} -c"
        )
        return results_dir

    def exec(self, cmd: str, docker_cmd_modifier: str = ""):
        "Pass a command to the container to run"

        docker_cmd = (
            f'docker exec {self._name} {docker_cmd_modifier} /bin/bash -c "{cmd}"'
        )
        result = os.system(docker_cmd)
        if result != 0:
            raise docker_run_error(f"nope, that didn't work {result}! - {docker_cmd}")

    def run(self, info: ExecutorInfo, files: List[Path]):
        "Run the docker command"

        # Unravel the file path. How we do this depends on how we are doing this work.
        filename = files[0].name

        # Write the file list into a filelist in the scripts directory. If that isn't going to be what we do, then
        # create it as a cmd line option.
        cmd_options = ""
        cmd_options += f"-d /data/{filename} "

        # We are just going to run
        cmd_options += "-r "

        # Docker command
        results_dir = tempfile.TemporaryDirectory()
        self.exec(f"cd /home/atlas; /scripts/{info.main_script} {cmd_options}")
        return results_dir


class docker_running_container:
    """
    This will start up a docker container running our analysis base.
    """

    def __init__(self, info, code_dir: str, files: List[Path]):
        "Init with directories for mapping, etc"

        self._code_dir = code_dir
        self._files = files

    def __enter__(self):
        "Get the docker command up and running"
        self._results_dir = tempfile.TemporaryDirectory()
        results_dir = Path(self._results_dir.name)
        results_dir.chmod(results_dir.stat().st_mode | 0o777)
        code_dir = Path(self._code_dir)
        code_dir.chmod(code_dir.stat().st_mode | 0o555)
        data_dir = self._files[0].parent
        data_dir.chmod(data_dir.stat().st_mode | 0o555)
        docker_cmd = f'docker run --name test_func_xAOD --rm -d -v {code_dir.absolute()}:/scripts -v {results_dir.absolute()}:/results -v {data_dir.absolute()}:/data:ro gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.42 /bin/bash -c "while [ 1 ] ; do sleep 1; echo hi ; done"'
        r = os.system(docker_cmd)
        if r != 0:
            raise RuntimeError(f"Unable to start docker deamon: {r} - {docker_cmd}")
        return docker_runner("test_func_xAOD", self._results_dir.name)

    def __exit__(self, type, value, traceback):
        with self._results_dir:
            r = os.system("docker rm -f test_func_xAOD")
            if r != 0:
                raise RuntimeError(f"Unable to stop docker container: {r}")


def run_docker(
    info: ExecutorInfo,
    code_dir: Path,
    files: List[str],
    data_file_on_cmd_line: bool = False,
    compile_only: bool = False,
    run_only: bool = False,
    add_position_argument_at_start: Optional[str] = None,
    extra_flag: Optional[str] = None,
    output_dir: Optional[str] = None,
    mount_output: bool = True,
) -> TemporaryDirectory:
    "Run the docker command"

    # Unravel the file path. How we do this depends on how we are doing this work.
    assert len(files) == 1
    filepath = Path(files[0])
    base_dir = filepath.parent
    filename = filepath.name

    # Write the file list into a filelist in the scripts directory. If that isn't going to be what we do, then
    # create it as a cmd line option.
    cmd_options = ""
    if data_file_on_cmd_line:
        cmd_options += f"-d /data/{filename} "
    else:
        with (code_dir / "filelist.txt").open("w") as f_out:
            f_out.writelines([f"/data/{filename}"])

    # Compile or run only?
    if compile_only:
        cmd_options += "-c "
    if run_only:
        cmd_options += "-r "

    # Extra random flag
    if extra_flag is not None:
        cmd_options += f"{extra_flag} "

    if output_dir is not None:
        cmd_options += f"-o {output_dir} "
    else:
        output_dir = "/results"

    results_dir = tempfile.TemporaryDirectory()
    mount_output_options = ""
    if mount_output:
        results_path = Path(results_dir.name)
        mount_output_options = (
            f"-v {str(results_path)}:{output_dir}" if mount_output else ""
        )
        # Make sure we can write to this directory!
        results_path.chmod(Path(results_path).stat().st_mode | 0o777)

    # Add an argument at the start?
    initial_args = ""
    if add_position_argument_at_start is not None:
        initial_args = f"{add_position_argument_at_start} "

    # Docker command
    code_dir.chmod(code_dir.stat().st_mode | 0o555)
    docker_cmd = f"docker run --rm {mount_output_options} -v {base_dir.absolute()}:/data:ro -v {code_dir.absolute()}:/scripts:ro gitlab-registry.cern.ch/atlas/athena/analysisbase:25.2.42 /scripts/{info.main_script} {initial_args} {cmd_options}"
    result = os.system(docker_cmd)
    if result != 0:
        raise docker_run_error(f"nope, that didn't work {result} - {docker_cmd}!")
    return results_dir


def test_good_cpp_total_run(cache_directory):
    "Good C++, and no arguments that does full run"

    info = generate_test_jet_fetch(cache_directory)
    with run_docker(info, cache_directory, [local_path]) as result_dir:
        assert os.path.exists(os.path.join(result_dir, info.output_filename))


def test_good_cpp_total_run_output_dir(cache_directory):
    "Good C++, and no arguments that does full run"

    info = generate_test_jet_fetch(cache_directory)
    with run_docker(
        info, cache_directory, [local_path], output_dir="/home/atlas/results"
    ) as result_dir:
        assert os.path.exists(os.path.join(result_dir, info.output_filename))


def test_good_cpp_total_run_output_dir_no_mount(cache_directory):
    "Good C++, and no arguments that does full run"

    info = generate_test_jet_fetch(cache_directory)
    with run_docker(
        info,
        cache_directory,
        [local_path],
        output_dir="/home/atlas/results",
        mount_output=False,
    ):
        # We aren't mounting so we can't look. So we just want to make sure no errors occur.
        pass


def test_good_cpp_total_run_file_as_arg(cache_directory):
    "Bad C++ generated, should throw an exception"

    info = generate_test_jet_fetch(cache_directory)
    with run_docker(
        info, cache_directory, [local_path], data_file_on_cmd_line=True
    ) as result_dir:
        assert os.path.exists(os.path.join(result_dir, info.output_filename))


def test_bad_cpp_total_run(cache_directory):
    "Bad C++, and no arguments that does full run"

    try:
        info = generate_test_jet_fetch_bad(cache_directory)
        with run_docker(
            info, cache_directory, [local_path], data_file_on_cmd_line=True
        ):
            assert False
    except docker_run_error:
        pass


def test_good_cpp_just_compile(cache_directory):
    "Good C++, only do the compile"

    info = generate_test_jet_fetch(cache_directory)
    with run_docker(
        info, cache_directory, [local_path], compile_only=True
    ) as result_dir:
        assert not os.path.exists(os.path.join(result_dir, info.output_filename))


def test_bad_cpp_just_compile(cache_directory):
    "Bad C++, only do the compile"

    try:
        info = generate_test_jet_fetch_bad(cache_directory)
        with run_docker(info, cache_directory, [local_path], compile_only=True):
            assert False
    except docker_run_error:
        pass


def test_good_cpp_compile_and_run(cache_directory):
    "Good C++, first do the compile, and then do the run"

    info = generate_test_jet_fetch(cache_directory)
    with docker_running_container(info, cache_directory, [Path(local_path)]) as runner:
        runner.compile(info)
        runner.run(info, [Path(local_path)])
        assert os.path.exists(os.path.join(runner.results_dir, info.output_filename))


def test_good_cpp_compile_and_run_2_files(cache_directory):
    "Make sure we can run a second file w/out seeing errors"
    info = generate_test_jet_fetch(cache_directory)
    with docker_running_container(info, cache_directory, [Path(local_path)]) as runner:
        runner.compile(info)
        runner.run(info, [Path(local_path)])
        runner.exec("chmod a+rw /results/ANALYSIS.root")
        out_file = Path(runner.results_dir) / info.output_filename
        assert out_file.exists()
        out_file.unlink()
        runner.run(info, [Path(local_path)])
        assert out_file.exists()


def test_run_with_bad_position_arg(cache_directory):
    "Pass in a bogus argument at the end with no flag"
    try:
        info = generate_test_jet_fetch(cache_directory)
        with run_docker(
            info,
            cache_directory,
            [local_path],
            add_position_argument_at_start="/results",
        ):
            assert False
    except docker_run_error:
        pass


def test_run_with_bad_flag(cache_directory):
    "Pass in a bogus flag"
    try:
        info = generate_test_jet_fetch(cache_directory)
        with run_docker(info, cache_directory, [local_path], extra_flag="-k"):
            assert False
    except docker_run_error:
        pass
