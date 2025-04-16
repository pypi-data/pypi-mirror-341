"""Utilities to handle CWL."""

from pathlib import Path
from typing import Any

from cwl_utils.parser import load_document_by_uri
from cwl_utils.parser.cwl_v1_2 import CommandOutputArraySchema, File
from cwl_utils.parser.cwl_v1_2_utils import load_inputfile

LFN_PREFIX = "lfn://"
LFN_DIRAC_PREFIX = "LFN:"
LOCAL_PREFIX = "file://"


def translate_cwl_workflow(
    cwl_workflow: Path, cvmfs_base_path: Path, apptainer_options: list[Any]
) -> dict[str, Any]:
    """Translate the CWL workflow description into Dirac compliant execution."""
    cwl_obj = load_document_by_uri(cwl_workflow)
    output_dict = {"CWLDesc": cwl_obj, "OutputSandbox": [], "OutputData": []}
    if cwl_obj.class_ != "CommandLineTool":
        return output_dict
    if cwl_obj.hints:
        cwl_obj = translate_docker_hints(cwl_obj, cvmfs_base_path, apptainer_options)

    return extract_and_translate_output_files(cwl_obj)


def translate_docker_hints(
    cwl_obj, cvmfs_base_path: Path, apptainer_options: list[Any]
):
    """Translate CWL DockerRequirement into Dirac compliant execution."""
    for index, hints in enumerate(cwl_obj.hints):
        if hints.class_ == "DockerRequirement":
            image = hints.dockerPull
            cmd = [
                "apptainer",
                "run",
                *apptainer_options,
                str(cvmfs_base_path / f"{image}"),
            ]
            if isinstance(cwl_obj.baseCommand, str):
                cmd += [cwl_obj.baseCommand]
            else:
                cmd += cwl_obj.baseCommand
            cwl_obj.baseCommand = cmd
            del cwl_obj.hints[index]
    return cwl_obj


def extract_and_translate_output_files(cwl_obj) -> dict[str, Any]:
    """Translate output files into a DIRAC compliant usage.

    Extract local outputs and lfns.
    Remove outputs path prefix.
    """
    output_lfns = []
    output_sandboxes = []
    for index, outputs in enumerate(cwl_obj.outputs):
        if not verify_cwl_output_type(outputs.type_):
            continue
        glob = outputs.outputBinding.glob
        if isinstance(glob, str):
            cwl_obj.outputs[index].outputBinding.glob = translate_sandboxes_and_lfns(
                glob, output_sandboxes, output_lfns
            )
        if isinstance(glob, list):
            for sub_index, glob_item in enumerate(glob):
                cwl_obj.outputs[index].outputBinding.glob[
                    sub_index
                ] = translate_sandboxes_and_lfns(
                    glob_item, output_sandboxes, output_lfns
                )
    return {
        "CWLDesc": cwl_obj,
        "OutputSandbox": output_sandboxes,
        "OutputData": output_lfns,
    }


def verify_cwl_output_type(output_type) -> bool:
    """Verify the cwl output type.

    True if the type is File or CommandOutputArraySchema
    or a list of 'null' and File/CommandOutputArraySchema
    else False.
    """
    if isinstance(output_type, list):
        for type in output_type:
            if type == "File" or isinstance(type, CommandOutputArraySchema):
                return True
    if output_type == "File" or isinstance(output_type, CommandOutputArraySchema):
        return True
    return False


# TODO: how to deal with default values not present in the input file but in the cwl?
def extract_and_translate_input_files(cwl_inputs: Path) -> dict[str, Any]:
    """Extract input files from CWL inputs, rewrite file prefix.

    If the file is a Sandbox, ensure there is no absolute path,
    and store it in the input sandbox list.
    If the file is a LFN, remove the lfn prefix and store it in the lfns list.
    """
    input_sandboxes = []
    input_lfns = []
    input_obj = load_inputfile(str(cwl_inputs))
    for _, input_value in input_obj.items():
        if isinstance(input_value, list):
            for file in input_value:
                if isinstance(file, File):
                    file.path = translate_sandboxes_and_lfns(
                        file, input_sandboxes, input_lfns
                    )
        elif isinstance(input_value, File):
            input_value.path = translate_sandboxes_and_lfns(
                input_value, input_sandboxes, input_lfns
            )
    return {
        "InputDesc": input_obj,
        "InputSandbox": input_sandboxes,
        "InputData": input_lfns,
    }


def translate_sandboxes_and_lfns(file: File | str, sandboxes: list, lfns: list) -> str:
    """Extract local files as sandboxes and lfns as input data."""
    if isinstance(file, File):
        if not file.path:
            raise NotImplementedError("File path is not defined.")
        path = file.path
    elif isinstance(file, str):
        path = file
    if LFN_PREFIX in path:
        path = path.replace(LFN_PREFIX, "")
        lfns.append(LFN_DIRAC_PREFIX + path)
        return Path(path).name
    path = path.replace(LOCAL_PREFIX, "")
    sandboxes.append(path)
    return Path(path).name
