from bzip2_encode import *
files = ['sample_text_short.txt','sample_text.txt','monte_cristo.txt','sample_tiff_img.tiff','sample_cat.jpg']
multiple = input("Specify a file here. If none specified, it will remove all files (except the originals) related to 'sample_text_short.txt','sample_text.txt','monte_cristo.txt','sample_tiff_img.tiff','sample_cat.jpg' ")
if multiple == '':
    print('Deleting all related files.')
    for file in files:
        run_clean_up(file)
else:
    print('Deleting files related to ', multiple)
    run_clean_up(multiple)
