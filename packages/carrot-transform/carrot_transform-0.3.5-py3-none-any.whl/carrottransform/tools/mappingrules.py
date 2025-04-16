import os
import json
import carrottransform.tools as tools
from .omopcdm import OmopCDM

import logging
logger = logging.getLogger(__name__)

class MappingRules:
    """
    self.rules_data stores the mapping rules as untransformed json, as each input file is processed rules are reorganised 
    as a file-specific dictionary allowing rules to be "looked-up" depending on data content
    """

    def __init__(self, rulesfilepath: os.PathLike, omopcdm: OmopCDM):
        ## just loads the json directly
        self.rules_data = tools.load_json(rulesfilepath)
        self.omopcdm = omopcdm
        
        self.parsed_rules = {}
        self.outfile_names = {}

        self.dataset_name = self.get_dsname_from_rules()

    def dump_parsed_rules(self):
        return(json.dumps(self.parsed_rules, indent=2))

    def get_dsname_from_rules(self):
        dsname = "Unknown"

        if "metadata" in self.rules_data:
            if "dataset" in self.rules_data["metadata"]:
                dsname = self.rules_data["metadata"]["dataset"]

        return dsname

    def get_dataset_name(self):
        return self.dataset_name

    def get_all_outfile_names(self):
        return list(self.rules_data["cdm"])

    def get_all_infile_names(self):
        file_list = []

        for outfilename, conditions in self.rules_data["cdm"].items():
            for outfield, source_field in conditions.items():
                for source_field_name, source_data in source_field.items():
                    if "source_table" in source_data:
                        if source_data["source_table"] not in file_list:
                            file_list.append(source_data["source_table"])

        return file_list
        
    def get_infile_data_fields(self, infilename):
        data_fields_lists = {}

        outfilenames, outdata = self.parse_rules_src_to_tgt(infilename)

        for outfilename in outfilenames:
            data_fields_lists[outfilename] = []

        for key, outfield_data in outdata.items():
            keydata = key.split("~")
            outfile = keydata[-1]
            for outfield_elem in outfield_data:
                for infield, outfields in outfield_elem.items():
                    for outfield in outfields:
                        outfielddata = outfield.split("~")
                        if self.omopcdm.is_omop_data_field(outfile, outfielddata[0]):
                            if infield not in data_fields_lists[outfile]:
                                data_fields_lists[outfile].append(infield)

        return data_fields_lists

    def get_infile_date_person_id(self, infilename):
        outfilenames, outdata = self.parse_rules_src_to_tgt(infilename)
        datetime_source = ""
        person_id_source = ""

        for key, outfield_data in outdata.items():
            keydata = key.split("~")
            outfile = keydata[-1]
            for outfield_elem in outfield_data:
                for infield, outfield_list in outfield_elem.items():
                    logger.debug("{0}, {1}, {2}".format(outfile, infield, str(outfield_list)))
                    for outfield in outfield_list:
                        if outfield.split('~')[0] in self.omopcdm.get_omop_datetime_fields(outfile):
                            datetime_source = infield
                        if outfield.split('~')[0] == self.omopcdm.get_omop_person_id_field(outfile):
                            person_id_source = infield

        return datetime_source, person_id_source

    def get_person_source_field_info(self, tgtfilename):
        """
        Specific discovery of input data field names for 'person' in these rules
        """
        birth_datetime_source = None
        person_id_source = None
        if tgtfilename in self.rules_data["cdm"]:
            source_rules_data = self.rules_data["cdm"][tgtfilename]
            ## this loops over all the fields in the person part of the rules, which will lead to overwriting of the source variables and unneccesary looping
            for rule_name, rule_fields in source_rules_data.items():
                if "birth_datetime" in rule_fields:
                    birth_datetime_source = rule_fields["birth_datetime"]["source_field"]
                if "person_id" in rule_fields:
                    person_id_source = rule_fields["person_id"]["source_field"]

        return birth_datetime_source, person_id_source

    def parse_rules_src_to_tgt(self, infilename):
        """
        Parse rules to produce a map of source to target data for a given input file
        """
        ## creates a dict of dicts that has input files as keys, and infile~field~data~target as keys for the underlying keys, which contain a list of dicts of lists
        if infilename in self.outfile_names and infilename in self.parsed_rules:
            return self.outfile_names[infilename], self.parsed_rules[infilename]
        outfilenames = []
        outdata = {}

        for outfilename, rules_set in self.rules_data["cdm"].items():
            for datatype, rules in rules_set.items():
                key, data = self.process_rules(infilename, outfilename, rules)
                if key != "":
                    if key not in outdata:
                        outdata[key] = []
                    outdata[key].append(data)
                    if outfilename not in outfilenames:
                        outfilenames.append(outfilename)

        self.parsed_rules[infilename] = outdata
        self.outfile_names[infilename] = outfilenames
        return outfilenames, outdata

    def process_rules(self, infilename, outfilename, rules):
        """
        Process rules for an infile, outfile combination
        """
        outkey = ""
        data = {}
        plain_key = ""
        term_value_key = ""

        ## iterate through the rules, looking for rules that apply to the input file.
        for outfield, source_info in rules.items():
            if source_info["source_field"] not in data:
                data[source_info["source_field"]] = []
            if source_info["source_table"] == infilename:
                if "term_mapping" in source_info:
                    if type(source_info["term_mapping"]) is dict:
                        for inputvalue, term in source_info["term_mapping"].items():
                            ## add a key/add to the list of data in the dict for the given input file
                            term_value_key = infilename + "~" + source_info["source_field"] + "~" + str(inputvalue) + "~" + outfilename
                            data[source_info["source_field"]].append(outfield + "~" + str(source_info["term_mapping"][str(inputvalue)]))
                    else:
                        plain_key = infilename + "~" + source_info["source_field"] + "~" + outfilename
                        data[source_info["source_field"]].append(outfield + "~" + str(source_info["term_mapping"]))
                else:
                    data[source_info["source_field"]].append(outfield)
        if term_value_key != "":
            return term_value_key, data

        return plain_key, data
