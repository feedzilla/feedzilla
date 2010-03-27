COMPRESS_CSS = {
    'common_styles': {
        'source_filenames': ('feedzilla/css/reset.css', 'feedzilla/css/style.css'),
        'output_filename': 'css/common_styles.r?.css',
    }
}

COMPRESS_JS = {
    'common_scripts': {
        'source_filenames': ('feedzilla/js/jquery.js', 'feedzilla/js/fix_tags.js',
                             'feedzilla/js/jquery.highlight-2.js'),
        'output_filename': 'js/common_scripts.r?.js',
    }
}
COMPRESS_VERSION = True
