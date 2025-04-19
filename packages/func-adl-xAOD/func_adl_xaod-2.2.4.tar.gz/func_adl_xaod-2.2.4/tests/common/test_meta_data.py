import ast
from dataclasses import dataclass
from typing import Callable, List

import pytest

from func_adl_xAOD.common import cpp_types
import func_adl_xAOD.common.statement as statement
from func_adl_xAOD.atlas.xaod.event_collections import (
    atlas_xaod_event_collection_collection,
    atlas_xaod_event_collection_container,
)
from func_adl_xAOD.cms.aod.event_collections import cms_aod_event_collection_collection
from func_adl_xAOD.cms.miniaod.event_collections import (
    cms_miniaod_event_collection_collection,
)
from func_adl_xAOD.common.ast_to_cpp_translator import query_ast_visitor
from func_adl_xAOD.common.cpp_ast import CPPCodeSpecification
from func_adl_xAOD.common.cpp_types import collection, method_type_info, terminal
from func_adl_xAOD.common.event_collections import (
    EventCollectionSpecification,
    event_collection_coder,
    event_collection_container,
)
from func_adl_xAOD.common.executor import executor
from func_adl_xAOD.common.meta_data import (
    InjectCodeBlock,
    JobScriptSpecification,
    generate_script_block,
    process_metadata,
)
from tests.utils.base import dataset, dummy_executor  # type: ignore


def test_malformed_meta_data():
    "Pass a bogus metadata and watch it burn"
    metadata = [
        {
            "one": "two",
        }
    ]
    with pytest.raises(ValueError) as e:
        process_metadata(metadata)

    assert "one" in str(e)


def test_bad_meta_data():
    "Pass a bogus metadata and watch it burn"
    metadata = [
        {
            "metadata_type": "add_method_type_info_iiii",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type": "int",
        }
    ]

    with pytest.raises(ValueError) as e:
        process_metadata(metadata)

    assert "add_method_type_info_iiii" in str(e)


def test_md_method_type_double():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type": "double",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert t.r_type.type == "double"
    assert not t.r_type.is_a_pointer
    assert t.deref_depth == 0


def test_md_method_type_double_tree_type():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type": "double",
            "tree_type": "int",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert t.r_type.tree_type.type == "int"


def test_md_method_type_double_deref():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type": "double",
            "deref_count": 2,
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert t.r_type.type == "double"
    assert not t.r_type.is_a_pointer
    assert t.deref_depth == 2


def test_md_method_type_collection():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type_element": "double",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert isinstance(t.r_type, collection)
    assert t.r_type.type == "std::vector<double>"
    assert isinstance(t.r_type.element_type, terminal)
    assert str(t.r_type.element_type) == "double"
    assert not t.r_type.is_a_pointer


def test_md_method_type_collection_item_ptr():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type_element": "double*",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert isinstance(t.r_type, collection)
    assert t.r_type.type == "std::vector<double*>"
    assert isinstance(t.r_type.element_type, terminal)
    assert str(t.r_type.element_type) == "double*"
    assert t.r_type.element_type.p_depth == 1
    assert not t.r_type.is_a_pointer


def test_md_method_type_custom_collection():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type_element": "double",
            "return_type_collection": "MyCustomCollection",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert isinstance(t.r_type, collection)
    assert t.r_type.type == "MyCustomCollection"
    assert str(t.r_type.element_type) == "double"
    assert not t.r_type.is_a_pointer


def test_md_method_type_collection_ptr():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "pT",
            "return_type_element": "double",
            "return_type_collection": "vector<double>*",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "pT")
    assert t is not None
    assert isinstance(t.r_type, collection)
    assert t.r_type.is_a_pointer


def test_md_method_type_object_pointer():
    "Make sure a double can be set"
    metadata = [
        {
            "metadata_type": "add_method_type_info",
            "type_string": "my_namespace::obj",
            "method_name": "vertex",
            "return_type": "my_namespace::vertex*",
        }
    ]

    process_metadata(metadata)

    t = method_type_info("my_namespace::obj", "vertex")
    assert t is not None
    assert t.r_type.type == "my_namespace::vertex"
    assert t.r_type.is_a_pointer


def test_with_method_call_with_type(caplog):
    'Call a function that is "ok" and has type info declared in metadata'

    (
        my_dataset()
        .MetaData(
            {
                "metadata_type": "add_method_type_info",
                "type_string": "my_namespace::obj",
                "method_name": "pT",
                "return_type": "int",
            }
        )
        .Select(lambda e: e.info("fork").pT())
        .value()
    )

    assert "pT" not in caplog.text


def test_md_code_block():
    "make sure all options of a code block work"
    metadata = [
        {
            "metadata_type": "inject_code",
            "name": "my_code_block",
            "body_includes": ["file1.h", "file2.h"],
            "header_includes": ["file3.h", "file4.h"],
            "private_members": ["int first;"],
            "instance_initialization": ["first(10)"],
            "ctor_lines": ["first = first * 10;"],
            "initialize_lines": ["line1", "line2"],
            "link_libraries": ["lib1", "lib2"],
        }
    ]

    result = process_metadata(metadata)

    assert len(result) == 1
    s = result[0]
    assert isinstance(s, InjectCodeBlock)
    assert s.body_includes == ["file1.h", "file2.h"]
    assert s.header_includes == ["file3.h", "file4.h"]
    assert s.private_members == ["int first;"]
    assert s.instance_initialization == ["first(10)"]
    assert s.ctor_lines == ["first = first * 10;"]
    assert s.link_libraries == ["lib1", "lib2"]
    assert s.initialize_lines == ["line1", "line2"]


def test_md_code_block_one_at_a_time():
    md = {
        "body_includes": ["file1.h", "file2.h"],
        "header_includes": ["file3.h", "file4.h"],
        "private_members": ["int first;"],
        "instance_initialization": ["first(10)"],
        "ctor_lines": ["first = first * 10;"],
        "link_libraries": ["lib1", "lib2"],
    }
    for k in md.keys():
        metadata = [
            {
                "metadata_type": "inject_code",
                "name": "my_code_block",
                k: md[k],
            }
        ]

        process_metadata(metadata)


def test_md_code_block_bad_item():
    metadata = [
        {
            "metadata_type": "inject_code",
            "body_includes": ["file1.h", "file2.h"],
            "header_includes": ["file3.h", "file4.h"],
            "private_members": ["int first;"],
            "instance_initialization": ["first(10)"],
            "ctor_lines": ["first = first * 10;"],
            "link_libraries_f": ["lib1", "lib2"],
        }
    ]

    with pytest.raises(ValueError) as e:
        process_metadata(metadata)

    assert "link_libraries_f" in str(e)


def test_md_code_block_empty():
    metadata = [
        {
            "metadata_type": "inject_code",
        }
    ]
    r = process_metadata(metadata)
    assert len(r) == 0


def test_md_code_block_duplicate():
    "make sure all options of a code block work"
    block1 = {
        "metadata_type": "inject_code",
        "name": "my_code_block",
        "body_includes": ["file1.h", "file2.h"],
        "header_includes": ["file3.h", "file4.h"],
        "private_members": ["int first;"],
        "instance_initialization": ["first(10)"],
        "ctor_lines": ["first = first * 10;"],
        "initialize_lines": ["line1", "line2"],
        "link_libraries": ["lib1", "lib2"],
    }
    metadata = [block1, dict(block1)]
    r = process_metadata(metadata)
    assert len(r) == 1


def test_md_code_block_duplicate_bad():
    "make sure all options of a code block work"
    block1 = {
        "metadata_type": "inject_code",
        "name": "my_code_block",
        "body_includes": ["file1.h", "file2.h"],
        "header_includes": ["file3.h", "file4.h"],
        "private_members": ["int first;"],
        "instance_initialization": ["first(10)"],
        "ctor_lines": ["first = first * 10;"],
        "initialize_lines": ["line1", "line2"],
        "link_libraries": ["lib1", "lib2"],
    }
    block2 = dict(block1)
    block2["body_includes"] = ["file5.h"]
    metadata = [block1, block2]

    with pytest.raises(ValueError) as e:
        process_metadata(metadata)

    assert "my_code_block" in str(e)


def test_md_atlas_collection():
    "Make a collection container md"
    metadata = [
        {
            "metadata_type": "add_atlas_event_collection_info",
            "name": "TruthParticles",
            "include_files": ["file1.h", "file2.h"],
            "container_type": "xAOD::ElectronContainer",
            "element_type": "xAOD::Electron",
            "contains_collection": True,
        }
    ]
    result = process_metadata(metadata)
    assert len(result) == 1
    s = result[0]
    assert isinstance(s, EventCollectionSpecification)
    assert s.backend_name == "atlas"
    assert s.name == "TruthParticles"
    assert s.include_files == ["file1.h", "file2.h"]
    assert isinstance(s.container_type, atlas_xaod_event_collection_collection)
    assert s.container_type.element_type.type == "xAOD::Electron"
    assert s.container_type.type == "xAOD::ElectronContainer"
    assert s.libraries == []


def test_md_atlas_collection_single_obj():
    "A collection container that does not have other things"
    metadata = [
        {
            "metadata_type": "add_atlas_event_collection_info",
            "name": "EventInfo",
            "include_files": ["xAODEventInfo/EventInfo.h"],
            "container_type": "xAOD::EventInfo",
            "link_libraries": ["xAODEventInfo"],
            "contains_collection": False,
        }
    ]
    result = process_metadata(metadata)
    assert len(result) == 1
    s = result[0]
    assert isinstance(s, EventCollectionSpecification)
    assert s.backend_name == "atlas"
    assert s.name == "EventInfo"
    assert s.include_files == ["xAODEventInfo/EventInfo.h"]
    assert isinstance(s.container_type, atlas_xaod_event_collection_container)
    assert s.container_type.type == "xAOD::EventInfo"
    assert s.libraries == ["xAODEventInfo"]


def test_md_atlas_collection_no_element():
    "A collection container that needs an element type"
    metadata = [
        {
            "metadata_type": "add_atlas_event_collection_info",
            "name": "EventInfo",
            "include_files": ["xAODEventInfo/EventInfo.h"],
            "container_type": "xAOD::EventInfo",
            "contains_collection": True,
        }
    ]
    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_atlas_collection_no_collection_and_element():
    "A collection container that needs an element type"
    metadata = [
        {
            "metadata_type": "add_atlas_event_collection_info",
            "name": "EventInfo",
            "include_files": ["xAODEventInfo/EventInfo.h"],
            "container_type": "xAOD::EventInfo",
            "contains_collection": False,
            "element_type": "Fork",
        }
    ]

    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_atlas_collection_bogus_extra():
    "A collection container that needs an element type"
    metadata = [
        {
            "metadata_type": "add_atlas_event_collection_info",
            "name": "EventInfo",
            "include_files": ["xAODEventInfo/EventInfo.h"],
            "container_type": "xAOD::EventInfo",
            "contains_collection": True,
            "element_type": "Fork",
            "what_the_heck": 23,
        }
    ]

    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_aod_collection():
    "Make a CMS AOD collection container"
    metadata = [
        {
            "metadata_type": "add_cms_aod_event_collection_info",
            "name": "Vertex",
            "include_files": ["DataFormats/VertexReco/interface/Vertex.h"],
            "container_type": "reco::VertexCollection",
            "contains_collection": True,
            "element_type": "reco::Vertex",
            "element_pointer": False,
        }
    ]
    result = process_metadata(metadata)
    assert len(result) == 1
    s = result[0]
    assert isinstance(s, EventCollectionSpecification)
    assert s.backend_name == "cms_aod"
    assert s.name == "Vertex"
    assert s.include_files == ["DataFormats/VertexReco/interface/Vertex.h"]
    assert isinstance(s.container_type, cms_aod_event_collection_collection)
    assert s.container_type.element_type.type == "reco::Vertex"
    assert s.container_type.type == "reco::VertexCollection"


def test_md_cms_miniaod_collection():
    "Make a CMS miniAOD collection container"
    metadata = [
        {
            "metadata_type": "add_cms_miniaod_event_collection_info",
            "name": "Muon",
            "include_files": ["DataFormats/PatCandidates/interface/Muon.h"],
            "container_type": "pat::MuonCollection",
            "contains_collection": True,
            "element_type": "pat::Muon",
            "element_pointer": False,
        }
    ]
    result = process_metadata(metadata)
    assert len(result) == 1
    s = result[0]
    assert isinstance(s, EventCollectionSpecification)
    assert s.backend_name == "cms_miniaod"
    assert s.name == "Muon"
    assert s.include_files == ["DataFormats/PatCandidates/interface/Muon.h"]
    assert isinstance(s.container_type, cms_miniaod_event_collection_collection)
    assert s.container_type.element_type.type == "pat::Muon"
    assert s.container_type.type == "pat::MuonCollection"


def test_md_cms_aod_collection_extra():
    "Make a CMS AOD collection container"
    metadata = [
        {
            "metadata_type": "add_cms_aod_event_collection_info",
            "name": "Vertex",
            "include_files": ["DataFormats/VertexReco/interface/Vertex.h"],
            "container_type": "reco::VertexCollection",
            "contains_collection": True,
            "element_type": "reco::Vertex",
            "element_pointer": False,
            "fork_it_over": True,
        }
    ]

    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_miniaod_collection_extra():
    "Make a CMS miniAOD collection container"
    metadata = [
        {
            "metadata_type": "add_cms_miniaod_event_collection_info",
            "name": "Muon",
            "include_files": ["DataFormats/PatCandidates/interface/Muon.h"],
            "container_type": "pat::MuonCollection",
            "contains_collection": True,
            "element_type": "pat::Muon",
            "element_pointer": False,
            "fork_it_over": True,
        }
    ]

    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_aod_collection_no_element_type():
    "Make a CMS aod collection container badly"
    metadata = [
        {
            "metadata_type": "add_cms_aod_event_collection_info",
            "name": "Vertex",
            "include_files": ["DataFormats/VertexReco/interface/Vertex.h"],
            "container_type": "reco::VertexCollection",
            "contains_collection": False,
            "element_type": "reco::Vertex",
            "element_pointer": False,
        }
    ]
    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_miniaod_collection_no_element_type():
    "Make a CMS miniAOD collection container badly"
    metadata = [
        {
            "metadata_type": "add_cms_miniaod_event_collection_info",
            "name": "Muon",
            "include_files": ["DataFormats/PatCandidates/interface/Muon.h"],
            "container_type": "pat::MuonCollection",
            "contains_collection": False,
            "element_type": "pat::Muon",
            "element_pointer": False,
        }
    ]
    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_aod_collection_element_type_needed():
    "Make a CMS aod collection container badly"
    metadata = [
        {
            "metadata_type": "add_cms_aod_event_collection_info",
            "name": "Vertex",
            "include_files": ["DataFormats/VertexReco/interface/Vertex.h"],
            "container_type": "reco::VertexCollection",
            "contains_collection": True,
            "element_pointer": False,
        }
    ]
    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_cms_miniaod_collection_element_type_needed():
    "Make a CMS miniaod collection container badly"
    metadata = [
        {
            "metadata_type": "add_cms_miniaod_event_collection_info",
            "name": "Muon",
            "include_files": ["DataFormats/PatCandidates/interface/Muon.h"],
            "container_type": "pat::MuonCollection",
            "contains_collection": True,
            "element_pointer": False,
        }
    ]
    with pytest.raises(ValueError):
        process_metadata(metadata)


def test_md_function_call():
    "Inject code to run some C++"
    metadata = [
        {
            "metadata_type": "add_cpp_function",
            "name": "MyDeltaR",
            "include_files": ["TVector2.h", "math.h"],
            "arguments": ["eta1", "phi1", "eta2", "phi2"],
            "code": [
                "auto d_eta = eta1 - eta2;",
                "auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);",
                "auto result = sqrt(d_eta*d_eta + d_phi*d_phi);",
            ],
            "return_type": "double",
        }
    ]

    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, CPPCodeSpecification)
    assert spec.name == "MyDeltaR"
    assert spec.include_files == ["TVector2.h", "math.h"]
    assert spec.arguments == ["eta1", "phi1", "eta2", "phi2"]
    assert len(spec.code) == 3
    assert spec.result == "result"
    assert spec.cpp_return_type.name == "double"


def test_md_function_call_pointer():
    "Inject code to run some C++"
    metadata = [
        {
            "metadata_type": "add_cpp_function",
            "name": "MyDeltaR",
            "include_files": ["TVector2.h", "math.h"],
            "arguments": ["eta1", "phi1", "eta2", "phi2"],
            "code": [
                "auto d_eta = eta1 - eta2;",
                "auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);",
                "auto result = sqrt(d_eta*d_eta + d_phi*d_phi);",
            ],
            "return_type": "double*",
            "return_pointer_depth": 1,
        }
    ]

    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, CPPCodeSpecification)
    assert spec.cpp_return_type.pointer_depth == 1
    assert spec.cpp_return_type.name == "double"


def test_md_method_call():
    "Inject code to run some C++ as a method"
    metadata = [
        {
            "metadata_type": "add_cpp_function",
            "name": "getAttributeFloat",
            "include_files": [],
            "arguments": ["name"],
            "instance_object": "obj_j",
            "method_object": "xAOD::Jet_v1",
            "code": ["auto result = obj_j->getAttribute<float>(name);"],
            "return_type": "double",
        }
    ]

    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, CPPCodeSpecification)

    assert spec.method_object == "xAOD::Jet_v1"
    assert spec.instance_object == "obj_j"


def test_md_function_call_renamed_result():
    "Check result name is properly set"
    metadata = [
        {
            "metadata_type": "add_cpp_function",
            "name": "MyDeltaR",
            "include_files": ["TVector2.h", "math.h"],
            "arguments": ["eta1", "phi1", "eta2", "phi2"],
            "code": [
                "auto d_eta = eta1 - eta2;",
                "auto d_phi = TVector2::Phi_mpi_pi(phi1-phi2);",
                "auto result_fork = sqrt(d_eta*d_eta + d_phi*d_phi);",
            ],
            "return_type": "double",
            "result_name": "result_fork",
        }
    ]

    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, CPPCodeSpecification)
    assert spec.result == "result_fork"


def test_md_add_config_script():
    "Check we can properly add some md script"
    metadata = [
        {
            "metadata_type": "add_job_script",
            "name": "script1",
            "script": [
                "from AnaAlgorithm.AnaAlgorithmConfig import AnaAlgorithmConfig",
                "config = AnaAlgorithmConfig( 'CP::SysListLoaderAlg/SysLoaderAlg' )",
                "config.sigmaRecommended = 1",
                "job.algsAdd( config )",
            ],
        }
    ]
    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, JobScriptSpecification)
    assert spec.name == "script1"
    assert spec.depends_on == []
    assert len(spec.script) == 4
    assert spec.script[2] == "config.sigmaRecommended = 1"


def test_md_add_config_script_dependencies():
    "Check we can properly add some md script"
    metadata = [
        {
            "metadata_type": "add_job_script",
            "name": "script1",
            "script": [
                "from AnaAlgorithm.AnaAlgorithmConfig import AnaAlgorithmConfig",
                "config = AnaAlgorithmConfig( 'CP::SysListLoaderAlg/SysLoaderAlg' )",
                "config.sigmaRecommended = 1",
                "job.algsAdd( config )",
            ],
            "depends_on": ["name1", "name2"],
        }
    ]
    specs = process_metadata(metadata)
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, JobScriptSpecification)
    assert spec.depends_on == ["name1", "name2"]


def test_md_jb_single():
    "Check we correctly put a single script block into script"
    blocks = [JobScriptSpecification("block1", ["line1", "line2"], [])]
    script = generate_script_block(blocks)

    assert script == ["line1", "line2"]


def test_md_jb_no_dep():
    "Check that a missing dependency causes an error"
    blocks = [JobScriptSpecification("block1", ["line1", "line2"], ["block2"])]

    with pytest.raises(ValueError) as e:
        generate_script_block(blocks)

    assert "block2" in str(e)


def test_md_jb_dep():
    blocks = [
        JobScriptSpecification("block1", ["line1", "line2"], ["block2"]),
        JobScriptSpecification("block2", ["line3", "line4"], []),
    ]

    script = generate_script_block(blocks)

    assert script == ["line3", "line4", "line1", "line2"]


def test_md_jb_duplicate():
    blocks = [
        JobScriptSpecification("block2", ["line3", "line4"], []),
        JobScriptSpecification("block2", ["line3", "line4"], []),
    ]

    script = generate_script_block(blocks)

    assert script == ["line3", "line4"]


def test_md_jb_duplicate_different_depends():
    blocks = [
        JobScriptSpecification("block1", ["line1"], []),
        JobScriptSpecification("block2", ["line2"], []),
        JobScriptSpecification("block3", ["line3", "line4"], ["block1"]),
        JobScriptSpecification("block3", ["line3", "line4"], ["block2"]),
    ]

    script = generate_script_block(blocks)

    assert script == ["line1", "line2", "line3", "line4"]


def test_md_jb_dup_script_dif():
    blocks = [
        JobScriptSpecification("block2", ["line3", "line5"], []),
        JobScriptSpecification("block2", ["line3", "line4"], []),
    ]

    with pytest.raises(ValueError) as e:
        generate_script_block(blocks)

    assert "block2" in str(e)


def test_md_jb_dup_dep_dif():
    blocks = [
        JobScriptSpecification("block2", ["line3", "line4"], ["block1"]),
        JobScriptSpecification("block2", ["line3", "line4"], ["block0"]),
        JobScriptSpecification("block2", ["line3", "line4"], []),
    ]

    with pytest.raises(ValueError) as e:
        generate_script_block(blocks)

    assert "block2" in str(e)


def test_md_jb_dep_rev():
    blocks = [
        JobScriptSpecification("block2", ["line3", "line4"], []),
        JobScriptSpecification("block1", ["line1", "line2"], ["block2"]),
    ]

    script = generate_script_block(blocks)

    assert script == ["line3", "line4", "line1", "line2"]


def test_md_jb_double():
    blocks = [
        JobScriptSpecification("block2", ["line3", "line4"], []),
        JobScriptSpecification("block1", ["line1", "line2"], ["block2"]),
        JobScriptSpecification("block3", ["line5", "line6"], ["block2", "block1"]),
    ]

    script = generate_script_block(blocks)

    assert script == ["line3", "line4", "line1", "line2", "line5", "line6"]


def test_md_jb_dep_circle():
    blocks = [
        JobScriptSpecification("block0", ["line-1", "line0"], []),
        JobScriptSpecification("block1", ["line1", "line2"], ["block2"]),
        JobScriptSpecification("block2", ["line3", "line4"], ["block1"]),
    ]

    with pytest.raises(ValueError) as e:
        generate_script_block(blocks)

    assert "circular" in str(e)


def test_md_extended_present():
    "Check we can properly add some docker metadata using the extensible interface"

    @dataclass
    class TestMetadata:
        name: str
        value: str

    metadata = [
        {
            "metadata_type": "docker",
            "name": "fork",
            "value": "test",
        }
    ]

    specs = process_metadata(metadata, {"docker": TestMetadata("t1", "t2")})
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, TestMetadata)
    assert spec.name == "fork"
    assert spec.value == "test"


def test_md_extended_partial_update():
    "Check we can properly add some docker metadata using the extensible interface"

    @dataclass
    class TestMetadata:
        name: str
        value: str

    metadata = [
        {
            "metadata_type": "docker",
            "name": "fork",
        }
    ]

    specs = process_metadata(metadata, {"docker": TestMetadata("t1", "t2")})
    assert len(specs) == 1
    spec = specs[0]
    assert isinstance(spec, TestMetadata)
    assert spec.name == "fork"
    assert spec.value == "t2"


def test_md_extended_not_present():
    "Make sure that no metadata is returned if the md isn't present"

    @dataclass
    class TestMetadata:
        name: str
        value: str

    metadata = []

    specs = process_metadata(metadata, {"docker": TestMetadata("t1", "t2")})
    assert len(specs) == 0


def test_md_define_enum():
    "Add an enum"
    metadata = [
        {
            "metadata_type": "define_enum",
            "namespace": "xAOD.Jet",
            "name": "Color",
            "values": ["one", "two", "three"],
        }
    ]

    process_metadata(metadata)

    ns = cpp_types.get_toplevel_ns("xAOD")
    assert ns is not None
    ns_jet = ns.get_ns("Jet")
    assert ns_jet is not None

    e_info = ns_jet.get_enum("Color")
    assert e_info is not None
    assert len(e_info.values) == 3


def test_md_define_enum_twice():
    "Add an enum"
    metadata = [
        {
            "metadata_type": "define_enum",
            "namespace": "xAOD.Jet",
            "name": "Color",
            "values": ["one", "two", "three"],
        }
    ]

    process_metadata(metadata)
    process_metadata(metadata)


# Some integration tests!
# We need to setup a whole dummy dataset so we can test this in isolation of CMS and ATLAS
# code.
class my_event_collection_container(event_collection_container):
    def __init__(self, obj_name: str):
        super().__init__(obj_name, True)

    def __str__(self):
        return "my_namespace::obj"


class dummy_collection_container(event_collection_container):
    def __init__(self):
        super().__init__("my_namespace::obj", True)

    def __str__(self):
        return "my_namespace::obj"


dummy_collections = [
    EventCollectionSpecification(
        "dummy", "info", ["xAODEventInfo/EventInfo.h"], dummy_collection_container(), []
    ),
]


class dummy_event_collection_coder(event_collection_coder):
    def get_running_code(self, container_type: event_collection_container) -> List[str]:
        return [f"{container_type} result;"]


class dummy_book_ttree(statement.book_ttree):
    def __init__(self):
        super().__init__("hi", ["one", "two"])

    def emit(self, e):
        pass


class dummy_ttree_fill(statement.ttree_fill):
    def __init__(self):
        super().__init__("hi")

    def emit(self, e):
        pass


class dummy_query_ast_visitor(query_ast_visitor):
    def __init__(self):
        super().__init__("dummy")

    def create_book_ttree_obj(
        self, tree_name: str, leaves: list
    ) -> statement.book_ttree:
        return dummy_book_ttree()

    def create_ttree_fill_obj(self, tree_name: str) -> statement.ttree_fill:
        return dummy_ttree_fill()


class my_executor(executor):
    def __init__(self):
        ecc = dummy_event_collection_coder()
        functions = {
            md.name: lambda cn: ecc.get_collection(md, cn) for md in dummy_collections
        }
        super().__init__([], "dummy.sh", "dude/shark", functions)

    def get_visitor_obj(self) -> query_ast_visitor:
        return dummy_query_ast_visitor()

    def build_collection_callback(
        self, metadata: EventCollectionSpecification
    ) -> Callable[[ast.Call], ast.Call]:
        raise NotImplementedError()


class my_dummy_executor(dummy_executor):
    "A dummy executor that will return basic ast visiting"

    def __init__(self):
        super().__init__()

    def get_executor_obj(self):
        return my_executor()

    def get_visitor_obj(self):
        return dummy_query_ast_visitor()


class my_dataset(dataset):
    "A dummy dataset to base func_adl queries on"

    def __init__(self):
        super().__init__()

    def get_dummy_executor_obj(self) -> dummy_executor:
        return my_dummy_executor()


def test_no_type_info_warning(caplog):
    'Call a function that is "ok" but has no type info'
    (my_dataset().Select(lambda e: e.info("fork").pT()).value())

    assert "pT" in caplog.text
