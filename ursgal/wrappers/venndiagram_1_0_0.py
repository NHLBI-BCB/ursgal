#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import csv
import os.path

# csv.field_size_limit(sys.maxsize)

class venndiagram_1_0_0( ursgal.UNode ):
    """Venn Diagram uNode"""
    META_INFO = {
        'engine_type'           : {
            'converter'         : False,
            'validation_engine' : False,
            'search_engine'     : False,
            'meta_engine'       : False,
            'visualizer'        : True,
        },
        'output_extension'    : '.svg',
        'output_suffix'       : 'venndiagram',
        'input_types'         : ['.csv',],
        'include_in_git'            : True,
        'in_development'            : False,
        'utranslation_style'    : 'venndiagram_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'            : 'venndiagram_1_0_0.py',
                },
            },
        },

    }
    def __init__(self, *args, **kwargs):
        super(venndiagram_1_0_0, self).__init__(*args, **kwargs)


    def _execute( self ):
        '''
        Plot Venn Diagramm for a list of .csv result files (2-5)

        Arguments are set in uparams.py but passed to the engine by self.params attribute

        Returns:
            dict: results for the different areas e.g. dict['C-(A|B|D)']['results']

            Output file is written to the common_top_level_dir
        '''
        # Keyword Arguments:
        #     Input files (self.params['_input_file_dicts']): list of dictionaries created by multi_run
        #     column_names (list)     : list of column names (str) used for the comparison
        #                               columns are merged if more than one column name given
        #     header (str)            : header of the produced Venn diagram
        #     label_list (list)       : list of labels in the same order as the input files list
        #                               names of last_search_engine are used if no label_list given
        #     output_file_name (str)  : created by self.magic_name_generator if None
        #     opacity (float)

        print('[ -ENGINE- ] Plotting Venn diagram ..')
        self.time_point(tag = 'execution')
        venndiagram_main = self.import_engine_as_python_function()

        venn_params = {}
            # 'opacity' : self.params['opacity']
            # }

        translations = self.params['_TRANSLATIONS_GROUPED_BY_TRANSLATED_KEY']
        import pprint
        pprint.pprint(translations)
        exit(1)

        column_sets = {}

        default_label = ['label_A','label_B','label_C','label_D','label_E','label_F']

        input_file_dicts = self.params['input_file_dicts']

        data = []

        for result_file in input_file_dicts:
            data_field = (
                result_file['last_engine'],
                os.path.join(
                    result_file['dir'],
                    result_file['file']
                )
            )
            data.append( data_field )

        all_are_csv = all( [f[1].upper().endswith('.CSV') for f in data] )
        assert all_are_csv == True, "VennDiagram input files all have to be .csv"

        # output_file_name = os.path.join(
        #     self.params['output_dir_path'],
        #     self.params['output_file']
        # )
        # self.params['output_file_incl_path'] = output_file_name

        # if output_file_name == None:
        #     head, tail = self.determine_common_common_head_tail_part_of_names( input_file_dicts=input_file_dicts)
        #     output_file_name = head + tail

        # output_file_dir = self.params['output_dir_path']

        # output_incl_path = os.path.join(
        #     output_file_dir,
        #     output_file_name
        # )

        assert len(data) <= 5, '''
            ERROR: input_file_list can only contain two to five result files,
            you can merge files before, if you need. 
            Current number of files: {0}'''.format(len(data))

        used_labels = []

        for n, (engine, file_path) in enumerate(data):
            if self.params['label_list'] == None:
                label = engine
            else:
                label = self.params['label_list'][n]
            venn_params[default_label[n]] = label
            column_sets[ label ]     = set()
            used_labels.append(label)
            print('[ Reading  ] Venn set {0} / file #{1} : {0}'.format(
                n,
                file_path)
            )
            file_object = open(file_path, 'r')
            csv_input = csv.DictReader(
                filter(
                    lambda row: row[0] != '#', file_object
                )
            )
            for line_dict in csv_input:
                value = ''
                for column_name in self.params['column_names']:
                    value += '||{0}'.format( line_dict[column_name] )
                column_sets[ label ].add( value )

        in_sets = []
        for label in used_labels:
            in_sets.append( column_sets[label] )

        return_dict = venndiagram_main(
            *in_sets,
            output_file = output_incl_path,
            **venn_params
            )

        return return_dict
