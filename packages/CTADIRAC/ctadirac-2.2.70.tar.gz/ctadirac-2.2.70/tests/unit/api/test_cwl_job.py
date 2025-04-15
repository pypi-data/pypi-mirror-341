import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from CTADIRAC.Interfaces.API.CWLJob import CWLJob
from CTADIRAC.Interfaces.Utilities.CWL_utils import (
    LFN_DIRAC_PREFIX,
    LFN_PREFIX,
)

INPUT_DATA = ["/ctao/user/MC/prod.sim", "/ctao/user/MC/prod2.sim"]
INPUT_SANDBOX = ["/a/local/MC/simulation.py", "/path/to/MC.prod3.sim"]
CWL_INPUTS_EXAMPLE = f"""
local_script:
  - class: File
    path: {INPUT_SANDBOX[0]}
input_as_lfn:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[0]}
input_as_lfn_2:
  - class: File
    path: {LFN_PREFIX}{INPUT_DATA[1]}
  - class: File
    path: {INPUT_SANDBOX[1]}
dataset: "dataset://path/to/data"
input_param: "a random param"
"""
OUTPUT_DATA = ["/ctao/user/MC/fit*.out", "/ctao/usr/MC/data.sim"]
OUTPUT_SANDBOX = ["/path/to/test*.out", "/path/to/data_2.sim", "*.txt"]
BASE_COMMAND = "python"
IMAGE = "harbor.cta-observatory.org/proxy_cache/library/python:3.12-slim"
CWL_WORKFLOW_EXAMPLE = f"""
cwlVersion: v1.2
class: CommandLineTool
doc: |
      Test using local input/output data treated as Dirac
      input/output sandboxes.

inputs:
  local_script:
    type: File
    inputBinding:
      position: 1
  input_as_lfn:
    type: File?
    inputBinding:
      position: 2
  input_as_lfn_2:
    type: File[]
    inputBinding:
      position: 3
  dataset:
    type: [File, string]
    inputBinding:
      position: 4
  input_param:
    type: string
    inputBinding:
      position: 5

outputs:
  output_as_sb:
    type: File[]?
    outputBinding:
      glob: ["{OUTPUT_SANDBOX[0]}"]
  output_as_lfn:
    type: File?
    label: "LFN wildcards"
    outputBinding:
      glob: "{LFN_PREFIX}{OUTPUT_DATA[0]}"
  output_as_lfn_2:
    type: File[]
    label: "LFN files list"
    outputBinding:
      glob:
        - {LFN_PREFIX}{OUTPUT_DATA[1]}
        - {OUTPUT_SANDBOX[1]}
  output_as_array:
    type:
      type: array
      items: File
    outputBinding:
      glob: "{OUTPUT_SANDBOX[2]}"

baseCommand: ["{BASE_COMMAND}"]

hints:
  DockerRequirement:
    dockerPull: {IMAGE}
"""


@pytest.fixture
def mock_submit_job(mocker):
    return mocker.patch(
        "CTADIRAC.Interfaces.API.CWLJob.Dirac.submitJob",
        side_effect=lambda self: self._toXML(),
    )


@pytest.mark.parametrize(
    (
        "cwl_worflow",
        "cwl_inputs",
        "expected_input_data",
        "expected_input_sandbox",
        "expected_output_data",
        "expected_output_sandbox",
    ),
    [
        (
            CWL_WORKFLOW_EXAMPLE,
            CWL_INPUTS_EXAMPLE,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in INPUT_DATA],
            INPUT_SANDBOX,
            [f"{LFN_DIRAC_PREFIX}{data}" for data in OUTPUT_DATA],
            OUTPUT_SANDBOX,
        ),
    ],
)
def test_cwl_job_submit(
    mock_submit_job,
    tmp_path,
    cwl_worflow,
    cwl_inputs,
    expected_input_data,
    expected_input_sandbox,
    expected_output_data,
    expected_output_sandbox,
):
    cwl_workflow_example = tmp_path / "cwl_workflow_example.cwl"
    cwl_workflow_example.write_text(cwl_worflow)
    cwl_inputs_example = tmp_path / "cwl_inputs_example.cwl"
    cwl_inputs_example.write_text(cwl_inputs)

    job = CWLJob(
        cwl_workflow=cwl_workflow_example,
        cwl_inputs=cwl_inputs_example,
        cvmfs_base_path=Path("/cvmfs/ctao.dpps.test/"),
    )

    result = job.submit()
    mock_submit_job.assert_called_once_with(job)
    result_xml = ET.fromstring(result)
    input_data = result_xml.find(".//Parameter[@name='InputData']/value").text.split(
        ";"
    )
    assert input_data == expected_input_data
    output_sandbox = result_xml.find(
        ".//Parameter[@name='OutputSandbox']/value"
    ).text.split(";")
    assert set(expected_output_sandbox).issubset(output_sandbox)
    input_sandbox = result_xml.find(
        ".//Parameter[@name='InputSandbox']/value"
    ).text.split(";")
    assert set(expected_input_sandbox).issubset(input_sandbox)
    output_data = result_xml.find(".//Parameter[@name='OutputData']/value").text.split(
        ";"
    )
    assert output_data == expected_output_data
    executable = result_xml.find(
        ".//StepInstance/Parameter[@name='executable']/value"
    ).text
    assert executable == "cwltool"
