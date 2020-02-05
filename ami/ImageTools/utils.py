import gdal, rasterio
import subprocess
import numpy as np

def convert(input_filename, output_filename, verbose=False, **kwargs):
    """
    convert: converts input filename to output filename. the formats are inferred from filenames.
    If the output file type is not .tif, an output file containing the metadata will be generated with the filepath:
    output_filename +'.aux.xml'
    Params:
    :param input_filename: file to convert to output format
    :param output_filename: destination for converted file
    :param *args: optional arguments for gdal_translate.exe. 
    More info at https://gdal.org/programs/gdal_translate.html
    Input them as strings (ex. to add '-r nearest', do r='nearest'). If argument has no value (ex. add '-q') do q=''
    returns:
    :return: output_filename
    """
    
    if 'colorinterp' not in kwargs.keys():  # if no specified colorinterp arg
        kwargs['colorinterp'] = 'red,green,blue,alpha'
    if not verbose:
        kwargs['q'] = ''
    kwargs_list = [item for key, value in kwargs.items() for item in ['-{}'.format(key), value] if value != '']
    answer = subprocess.check_output(['gdal_translate', *kwargs_list, input_filename, output_filename], shell=verbose)
    if verbose: 
        print(answer.decode('ANSI'))
    return output_filename


def stack_tifs(filenames, output_filename):
    textfile=output_filename.replace('.tif','.txt')
    with open(textfile, 'w+') as f:
        files = ['"{}"'.format(fname) for fname in f]
        files='\n'.join(filenames)
        f.write(files)

    subprocess.check_output(['gdalbuildvrt','-separate','-resolution','average','-input_file_list',textfile,output_filename,'-srcnodata','"-10000"'])
    combined=gdal.Open(output_filename)
    array=combined.ReadAsArray()
    array = np.ma.masked_equal(array, -10000)
    #print(array)
    return array
