import numpy
factor = 0.0563564211

beamline.append_beamline_element(beamline_element)


# test plot
if 0:
   from srxraylib.plot.gol import plot_scatter
   plot_scatter(beam.get_photon_energy_eV(nolost=1), beam.get_column(23, nolost=1), title='(Intensity,Photon Energy)', plot_histograms=0)
   plot_scatter(1e6 * beam.get_column(1, nolost=1), 1e6 * beam.get_column(3, nolost=1), title='(X,Z) in microns')

print(f'{beam.get_intensity(polarization=0):.6g} {beam.get_intensity(polarization=1):.6g} {beam.get_intensity(polarization=2):.6g}')
print(beam.get_column(23)[0:5], beam.get_column(24)[0:5], beam.get_column(25)[0:5])
