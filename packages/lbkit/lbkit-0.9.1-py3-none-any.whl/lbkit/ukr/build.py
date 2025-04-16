"""组件构建"""
import os
import yaml
import shutil
import re
import json
import tempfile
from string import Template
from multiprocessing import Pool
import traceback
from argparse import ArgumentParser
from jsonschema import validate, ValidationError
from git import Repo
from git.exc import InvalidGitRepositoryError
from mako.lookup import TemplateLookup
from lbkit.misc import Color, load_yml_with_json_schema_validate, get_json_schema_file, load_json_schema
from lbkit import errors
from lbkit.codegen.codegen import CodeGen, history_versions
from lbkit.tools import Tools
from lbkit.build_conan_parallel import BuildConanParallel
from lbkit.codegen.codegen import Version
from lbkit.tasks.task_download import DownloadTask
from lbkit.misc import DownloadFlag
from lbkit.tools import Tools
from lbkit.utils.env_detector import EnvDetector


tools = Tools("comp_build")
log = tools.log
lb_cwd = os.path.split(os.path.realpath(__file__))[0]

class SourceDest():
    def __init__(self, cfg):
        self.source = cfg.get("source")
        self.dest = cfg.get("dest")

    def copy(self, source_dir, dest_dir, with_template, **kwargs):
        source = os.path.join(source_dir, self.source)
        dest = os.path.join(dest_dir, self.dest)
        if os.path.isfile(dest):
            os.unlink(dest)
        dest_dir = os.path.dirname(dest)
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)
        log.info(f"cp {source} to  {dest}")
        if with_template:
            with open(source, "r") as fp:
                template = Template(fp.read())
            content = template.safe_substitute(kwargs)
            with open(dest, "w+") as fp:
                fp.write(content)
        else:
            shutil.copyfile(source, dest)


class BuildGeneral():
    def __init__(self, config, cwd, cfg_key, dir_name):
        self.cwd = cwd
        self.name = cfg_key
        self.work_dir = os.path.join(cwd, ".temp")
        self.output = os.path.join(self.work_dir, "output")
        if not os.path.isdir(self.output):
            os.makedirs(self.output)
        os.chdir(self.work_dir)
        self.arch = config.get("base").get("arch")
        self.cross_compile = config.get("base").get("cross_compile")
        self.cfg = config.get(cfg_key)
        self.dir_name = os.path.realpath(dir_name)
        self.tools = Tools(self.dir_name + ".log")

    def download(self):
        tmp_file = self.dir_name + ".tar.gz"
        url = self.cfg.get("url")
        sha256 = self.cfg.get("sha256")
        verify = self.cfg.get("verify", True)
        strip_components = self.cfg.get("strip_components")
        cfg = {
            "url": url,
            "file": tmp_file,
            "decompress": {
                "dirname": os.getcwd(),
                "strip_components": strip_components
            },
            "sha256": sha256,
            "verify": verify
        }
        task = DownloadTask(cfg, os.getcwd())
        task.start()
        _, sha = DownloadFlag.read(self.dir_name)
        if sha == sha256:
            return
        cmd = f"tar -xf {task.dst} -C {self.dir_name}"
        if task.strip_components:
            cmd += f" --strip-components={task.strip_components}"
        if os.path.isdir(self.dir_name):
            shutil.rmtree(self.dir_name)
        os.makedirs(self.dir_name)
        self.tools.exec(cmd)
        DownloadFlag.create(self.dir_name, url, sha256)

    def prepare_defconfig(self):
        defconf = self.cfg.get("defconfig")
        compiler_path=os.path.join(self.work_dir, "toolchain")
        sd = SourceDest(defconf)
        sd.copy(self.cwd, os.path.join(self.work_dir, self.dir_name), True, compiler_path=compiler_path)
        os.environ["ARCH"] = self.arch
        os.environ["CROSS_COMPILE"] = self.cross_compile + "-"
        path = os.environ.get("PATH", "")
        if compiler_path not in path:
            path += ":" + compiler_path + "/bin"
            os.environ["PATH"] = path
        self.defconfig = os.path.basename(sd.dest)

    def build(self):
        os.chdir(self.dir_name)
        cmd = f"make {self.defconfig}"
        self.tools.exec(cmd, verbose=True)
        if self.name == "compiler":
            cmd = f"make sdk -j" + str(os.cpu_count())
        else:
            cmd = f"make -j" + str(os.cpu_count())
        self.tools.exec(cmd, verbose=True)

    def tar_files(self):
        os.chdir(self.dir_name)
        cfgs = self.cfg.get("tar", [])
        for cfg in cfgs:
            sd = SourceDest(cfg)
            src = os.path.join(self.dir_name, sd.source)
            dst = os.path.join(self.dir_name, sd.dest)
            cmd = f"tar -czf {dst} -C {src} ."
            self.tools.exec(cmd)

    def package(self):
        os.chdir(self.dir_name)
        cfgs = self.cfg.get("output", [])
        for cfg in cfgs:
            sd = SourceDest(cfg)
            sd.copy(self.dir_name, self.output, False)

    def run(self):
        self.download()
        self.prepare_defconfig()
        self.build()
        self.tar_files()
        self.package()
        os.chdir(self.cwd)

class BuildCompiler(BuildGeneral):
    def __init__(self, config, cwd):
        super().__init__(config, cwd, "compiler", "buildroot")

    def package(self):
        super().package()
        cfgs = self.cfg.get("output", [])
        for cfg in cfgs:
            sd = SourceDest(cfg)
            dest = os.path.join(self.output, sd.dest)
            install_path = os.path.join(self.work_dir, "toolchain")
            if os.path.isdir(install_path):
                shutil.rmtree(install_path)
            os.makedirs(install_path)
            cmd = f"tar -xzf {dest} -C {install_path} --strip-components=1"
            self.tools.exec(cmd)

class BuildRootfs(BuildGeneral):
    def __init__(self, config, cwd):
        super().__init__(config, cwd, "buildroot", "buildroot")

    def build(self):
        os.chdir(self.dir_name)
        shutil.rmtree("output", ignore_errors=True)
        return super().build()

class BuildLinux(BuildGeneral):
    def __init__(self, config, cwd):
        super().__init__(config, cwd, "linux", "linux")

class BuildUBoot(BuildGeneral):
    def __init__(self, config, cwd):
        super().__init__(config, cwd, "uboot", "uboot")


class UKRBuild():
    def __init__(self, env_detector: EnvDetector):
        os.chdir(env_detector.ukr.folder)
        self.env_detector = env_detector

    def run(self):
        cwd = os.getcwd()
        with open("config.yml") as fp:
            cfg = yaml.full_load(fp)
        build = BuildCompiler(cfg, cwd)
        build.run()
        build = BuildRootfs(cfg, cwd)
        build.run()
        build = BuildLinux(cfg, cwd)
        build.run()
        build = BuildUBoot(cfg, cwd)
        build.run()
        cmd = f"tar -czf {cwd}/.temp/output/firmware.tar.gz -C {cwd}/.temp/output/images ."
        tools.exec(cmd)