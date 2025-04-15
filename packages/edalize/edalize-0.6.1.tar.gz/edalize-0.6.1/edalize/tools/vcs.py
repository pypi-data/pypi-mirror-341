# Copyright edalize contributors
# Licensed under the 2-Clause BSD License, see LICENSE for details.
# SPDX-License-Identifier: BSD-2-Clause

import logging
from pathlib import Path

from edalize.tools.edatool import Edatool
from edalize.utils import EdaCommands

logger = logging.getLogger(__name__)


class Vcs(Edatool):

    description = "VCS simulator from Synopsys"

    TOOL_OPTIONS = {
        "32bit": {
            "type": "bool",
            "desc": "Disable 64-bit mode",
        },
        "2_stage_flow": {
            "type": "bool",
            "desc": "Run VCS in 2-stage (elaborate+compile => simulate) instead of 3-stage mode (elaborate => compile => simulate)",
        },
        "vlogan_options": {
            "type": "str",
            "desc": "Additional options for analysis with vlogan",
            "list": True,
        },
        "vhdlan_options": {
            "type": "str",
            "desc": "Additional options for analysis with vhdlan",
            "list": True,
        },
        "vcs_options": {
            "type": "str",
            "desc": "Additional options for elaboration with vcs",
            "list": True,
        },
        "run_options": {
            "type": "str",
            "desc": "Additional run-time options for the simulation",
            "list": True,
        },
    }

    def setup(self, edam):
        super().setup(edam)

        self.commands = EdaCommands()
        self.f_files = {}
        self.workdirs = []
        self.target_files = []
        self.user_files = []

        incdirs = []
        include_files = []
        unused_files = self.files.copy()
        # Get all include dirs. Move include files to a separate list
        for f in self.files:
            if not "simulation" in f.get("tags", ["simulation"]):
                continue
            file_type = f.get("file_type", "")
            if file_type.startswith("verilogSource") or file_type.startswith(
                "systemVerilogSource"
            ):
                if self._add_include_dir(f, incdirs, force_slash=True):
                    include_files.append(f["name"])
                    unused_files.remove(f)

        full64 = [] if self.tool_options.get("32bit") else ["-full64"]
        if self.tool_options.get("2_stage_flow"):
            self._twostage_setup(edam, incdirs, include_files, unused_files, full64)
        else:
            self._threestage_setup(edam, incdirs, include_files, unused_files, full64)

        self.edam = edam.copy()
        self.edam["files"] = unused_files

        binary_name = self.name + ".simv"
        self.commands.add(
            ["vcs"]
            + full64
            + ["-o", binary_name, "-file", "vcs.f", "-parameters", "parameters.txt"]
            + self.vcs_files,
            [binary_name],
            self.target_files + self.user_files + ["vcs.f", "parameters.txt"],
        )

        self.commands.add(
            ["./" + binary_name, "$(EXTRA_OPTIONS)"]
            + self.tool_options.get("run_options", []),
            ["run"],
            [],
        )
        self.commands.set_default_target(binary_name)

    def _twostage_setup(self, edam, incdirs, include_files, unused_files, full64):

        user_files = []

        vlog_files = []
        has_sv = False
        for f in unused_files.copy():
            if not "simulation" in f.get("tags", ["simulation"]):
                continue

            fname = f.get("name")

            file_type = f.get("file_type", "")
            if file_type.startswith("verilogSource") or file_type.startswith(
                "systemVerilogSource"
            ):

                if file_type.startswith("systemVerilogSource"):
                    has_sv = True

                vlog_files.append(fname)
                unused_files.remove(f)
            elif file_type.startswith("vhdlSource"):
                logger.warning(
                    f"Only (system)Verilog supported in two-stage mode. Ignoring VHDL file {fname}"
                )
            elif file_type == "user":
                user_files.append(f["name"])

            if f.get("define"):
                logger.warning(
                    f"File-specific defines not supported in two-stage mode. Ignoring {fname}"
                )

        _args = []
        for k, v in self.vlogdefine.items():
            _args.append(
                "+define+{}={}".format(
                    k, self._param_value_str(v, str_quote_style='""')
                )
            )
        defines = " ".join(_args)

        options = ["-top", self.toplevel]
        if has_sv:
            options.append("-sverilog")
        options += self.tool_options.get("vcs_options", [])
        options += [defines]
        options += ["+incdir+" + d for d in incdirs]

        self.f_files["vcs.f"] = options

        self.target_files = include_files + vlog_files
        self.vcs_files = vlog_files

    def _threestage_setup(self, edam, incdirs, include_files, unused_files, full64):
        def absorb_node(nodes, node_to_absorb):
            for node, deps in nodes.items():
                if node_to_absorb in deps:
                    deps.remove(node_to_absorb)
                    deps += nodes[node_to_absorb]
            del nodes[node_to_absorb]

        libs = {}
        has_sv = False
        for f in unused_files.copy():
            lib = f.get("logical_name", "work")

            file_type = f.get("file_type", "")
            if file_type.startswith("verilogSource") or file_type.startswith(
                "systemVerilogSource"
            ):

                if file_type.startswith("systemVerilogSource"):
                    has_sv = True

                vlog_defines = self.vlogdefine.copy()
                vlog_defines.update(f.get("define", {}))

                _args = []
                for k, v in vlog_defines.items():
                    _args.append(
                        "+define+{}={}".format(
                            k, self._param_value_str(v, str_quote_style='""')
                        )
                    )
                defines = " ".join(_args)
                cmd = "vlogan"
            elif file_type.startswith("vhdlSource"):
                cmd = "vhdlan"
            elif file_type == "user":
                self.user_files.append(f["name"])
                cmd = None
            else:
                cmd = None

            if not "simulation" in f.get("tags", ["simulation"]):
                cmd = None

            if cmd:
                if not lib in libs:
                    libs[lib] = []
                libs[lib].append((cmd, f["name"], defines))
                unused_files.remove(f)

        libdeps = self.edam.get("library_dependencies", {})
        for lib in libdeps.copy():
            if not lib in libs:
                absorb_node(libdeps, lib)

        for lib, files in libs.items():
            cmds = {}
            has_vlog = False
            # Group into individual commands
            for cmd, fname, defines in files:
                if not (cmd, defines) in cmds:
                    cmds[(cmd, defines)] = []
                cmds[(cmd, defines)].append(fname)
                if cmd == "vlogan":
                    has_vlog = True
            i = 0
            f_files = {}
            for (cmd, defines), fnames in cmds.items():
                depfiles = fnames.copy()
                options = []
                if cmd == "vlogan":
                    if has_sv:
                        options.append("-sverilog")
                    options += self.tool_options.get("vlogan_options", [])
                    options += [defines]
                    options += ["+incdir+" + d for d in incdirs]
                    target_file = "AN.DB/make.vlogan"
                elif cmd == "vhdlan":
                    options += self.tool_options.get("vhdlan_options", [])
                    target_file = "64/vhmra.sdb"
                suffix = f"_{i}" if i else ""
                f_file = f"{lib}{suffix}.f"
                f_files[f_file] = options
                workdir = lib + suffix
                self.workdirs.append(workdir)
                i += 1
                if has_vlog:
                    depfiles += include_files
                libdepfiles = []
                for l in libdeps.get(lib, []):
                    if l in libs:
                        libdepfiles.append(l + "/AN.DB/make.vlogan")
                self.commands.add(
                    [cmd]
                    + full64
                    + ["-file", f_file, "-work", workdir, "-l", workdir + ".log"]
                    + fnames,
                    [workdir + "/" + target_file],
                    depfiles + [f_file] + libdepfiles,
                )
                self.target_files.append(workdir + "/" + target_file)
            self.f_files.update(f_files)

        self.f_files["vcs.f"] = ["-top", self.toplevel] + self.tool_options.get(
            "vcs_options", []
        )
        self.vcs_files = []

    def write_config_files(self):
        s = "WORK > DEFAULT\nDEFAULT : ./work\n"
        for lib in self.workdirs:
            if lib != "work":
                s += f"{lib} : ./{lib}\n"
        self.update_config_file("synopsys_sim.setup", s)
        for k, v in self.f_files.items():
            self.update_config_file(k, " ".join(v) + "\n")

        _parameters = {**self.vlogparam, **self.generic}
        s = ""
        for key, value in _parameters.items():
            _value = self._param_value_str(value, '"')
            s += f"assign {_value} {key}\n"
        self.update_config_file("parameters.txt", s)

    def run(self):
        args = ["run"]

        # Set plusargs
        if self.plusarg:
            plusargs = []
            for key, value in self.plusarg.items():
                plusargs += ["+{}={}".format(key, self._param_value_str(value))]
            args.append("EXTRA_OPTIONS=" + " ".join(plusargs))

        return ("make", args, self.work_root)
