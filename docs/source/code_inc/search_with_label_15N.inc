.. code-block:: python

	#!/usr/bin/env python3.4
	# encoding: utf-8
	
	import ursgal
	import os
	
	
	def main():
	    '''
	    Executes a search with 3 different search engines on an example file from
	    the data from Barth et al. Two searches are performed pe engine for each
	    14N (unlabeled) and 15N labeling.
	
	    usage:
	        ./search_with_label_15N.py
	
	
	
	    '''
	
	    engine_list = [
	        'omssa_2_1_9',
	        'xtandem_piledriver',
	        'msgfplus_v9979',
	    ]
	
	    params = {
	        'database' : os.path.join(
	            os.pardir,
	            'example_data',
	            'Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta'
	        ),
	        'modifications' : [ ],
	        'csv_filter_rules' : [
	            ['PEP'      , 'lte'    , 0.01],
	            ['Is decoy' , 'equals' , 'false']
	        ],
	        'ftp_url'       : 'ftp.peptideatlas.org',
	        'ftp_login'         : 'PASS00269',
	        'ftp_password'      : 'FI4645a',
	        'ftp_include_ext'   : [
	            'JB_FASP_pH8_2-3_28122012.mzML',
	        ],
	        'ftp_output_folder' : os.path.join(
	            os.pardir,
	            'example_data',
	            'search_with_label_15N'
	        ),
	        'http_url': 'http://www.uni-muenster.de/Biologie.IBBP.AGFufezan/misc/Creinhardtii_281_v5_5_CP_MT_with_contaminants_target_decoy.fasta' ,
	        'http_output_folder' : os.path.join(
	            os.pardir,
	            'example_data'
	        )
	    }
	
	    if os.path.exists(params['ftp_output_folder']) is False:
	        os.mkdir(params['ftp_output_folder'])
	
	    uc = ursgal.UController(
	        profile = 'LTQ XL low res' ,
	        params = params
	    )
	    mzML_file = os.path.join(
	        params['ftp_output_folder'],
	        params['ftp_include_ext'][0]
	    )
	    if os.path.exists(mzML_file) is False:
	        uc.fetch_file(
	            engine     = 'get_ftp_files_1_0_0'
	        )
	    if os.path.exists(params['database']) is False:
	        uc.fetch_file(
	            engine     = 'get_http_files_1_0_0'
	        )
	
	    mgf_file = uc.convert_to_mgf_and_update_rt_lookup(
	        input_file       = mzML_file,
	    )
	
	    for label in [ '14N', '15N' ]:
	        validated_files_list = []
	        uc.params['label'] = label
	        uc.params['prefix'] = label
	        for engine in engine_list:
	            unified_result_file = uc.search(
	                input_file = mgf_file,
	                engine     = engine,
	            )
	
	            validated_file = uc.validate(
	                input_file = unified_result_file,
	                engine     = 'percolator_2_08',
	            )
	
	            filtered_file = uc.filter_csv(
	                input_file = validated_file,
	            )
	
	            validated_files_list.append( filtered_file )
	        uc.visualize(
	            input_files     = validated_files_list,
	            engine          = 'venndiagram',
	        )
	
	    return
	
	if __name__ == '__main__':
	    main()
