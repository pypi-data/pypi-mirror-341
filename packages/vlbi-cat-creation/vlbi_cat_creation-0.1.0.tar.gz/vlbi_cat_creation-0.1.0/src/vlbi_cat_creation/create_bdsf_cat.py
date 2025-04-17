import bdsf 


def basic_processing(filepath):
    img = bdsf.process_image(filepath)

    img.write_catalog(clobber = True)

    return 0