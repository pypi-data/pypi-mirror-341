# vlbi-cat-creation
Repository for developing tools for VLBI master catalogue creation


## Package Goals

This package aims to solve the following cataloguing problems in LOFAR-VLBI imaging:

- Producing and then combining catalogues at different resolutions and depth (eg. 0.3'', 0.6'', 1.2'' and 6'')
- Source deblending when multiple sources are detected at high-resolution
- Optical/IR identification if such a catalogue is provided
- Creating a master catalogue with relevant detection flags, component flags and fluxes given all information available for a source
- Minimising visual inspection
- Handling facet boundaries

## Running the Package

The package provides a cli interface which users can access after installation. The tool can also be run without a full download using a tool such as `uv`.

### Full Installation 

```bash
pip install vlbi-cat-creation
vlbi-cat-creation -h # To view command description and available options
vlbi-cat-creation --basic --images="['image1.fits', 'image2.fits']"
```


Or alternatively using uv:
```bash
uvx vlbi-cat-creation 
```

