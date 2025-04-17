import bdsf 


def basic_processing(filepath):
    img = bdsf.process_image(filepath)

    img.write_catalog(clobber = True)

    return 0


def adaptive_rms(filepath):
    img = bdsf.process_image(filepath, adaptive_rms_box = True)

    img.write_catalog(clobber = True)

    return 0