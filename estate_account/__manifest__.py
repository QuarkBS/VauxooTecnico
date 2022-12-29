{
    'name': 'Estate Account',
    'depends': ['estate', 'account'],
    'data' : [
        ],
    'assets': {
        'web.assets_backend': [
            'analytic/static/src/components/**/*',
        ],
        'web.qunit_suite_tests': [
            'analytic/static/tests/*.js',
        ],
    },   
    'license': 'LGPL-3',    
}
