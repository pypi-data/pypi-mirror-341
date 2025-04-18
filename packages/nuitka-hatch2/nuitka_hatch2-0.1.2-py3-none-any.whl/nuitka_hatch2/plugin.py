from typing import Any
from hatchling.builders.hooks.plugin.interface import BuildHookInterface
import os
from loguru import logger
import subprocess


class NuitkaBuildHook(BuildHookInterface):
    PLUGIN_NAME = "nuitka2"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__output_dir = None

    @property
    def output_dir(self) -> str:
        if self.__output_dir is None:
            self.__output_dir = os.path.join(self.root, "nuitka_output")
        return self.__output_dir

    @property
    def artifact_patterns(self) -> str:
        return [os.path.join(self.output_dir, "*")]

    def get_inclusion_map(self) -> dict[str, str]:
        inclusion_map = {}
        from glob import glob

        for path in glob(os.path.join(self.output_dir, "*")):
            inclusion_map[path] = os.path.relpath(path, self.output_dir)
        return inclusion_map

    def initialize(self, version: str, build_data: dict[str, Any]) -> None:
        if self.target_name != "wheel":
            return

        package = self.build_config.packages[0]
        args = self.config.get("nuitka_args", [])
        default_args = [
            "--module",
            f"--include-package={package}",
            f"{package}",
            f"--output-dir={self.output_dir}",
            "--remove-output",
        ]
        args = args or default_args
        logger.info(f"Building wheel with Nuitka: {' '.join(args)}")
        process = subprocess.run(
            ["python", "-m", "nuitka", *args],
        )
        msg = process.stdout or process.stderr
        if process.returncode and not msg:
            raise Exception(f"Failed to build wheel: {process.returncode}/{msg}")

        build_data["infer_tag"] = True
        build_data["pure_python"] = False
        build_data["artifacts"].extend(self.artifact_patterns)
        build_data["force_include"] = self.get_inclusion_map()

    def finalize(self, version: str, build_data: dict[str, Any], artifact_path: str) -> None:
        files = [f.relative_path for f in self.build_config.builder.recurse_included_files()]
        print("Files included in the wheel:", files)
