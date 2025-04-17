#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms  # type: ignore
import os

process = cms.Process("Demo")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

filelistPath = "filelist.txt"
fileNames = tuple([f"file:{line}" for line in open(filelistPath, "r").readlines()])

process.source = cms.Source(
    "PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames=cms.untracked.vstring(*fileNames),
)

process.demo = cms.EDAnalyzer("Analyzer")

output_file = os.environ["CMS_OUTPUT_FILE"]

process.TFileService = cms.Service("TFileService", fileName=cms.string(output_file))

process.p = cms.Path(process.demo)
