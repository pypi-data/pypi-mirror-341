from matplotlib import pyplot

from CdBURY.classes import Time,CadmiumMassIsotope,CadmiumFluxes,Perturbation,FluxType
from CdBURY import CdBURY

initial_seawater = CadmiumMassIsotope(1.0*8.36e11,-0.1)

isotope_offsets = CadmiumFluxes(-0.1,
                                0.0,
                                -0.55,
                                0.0,
                                -0.80,
                                0.0)

flux_proportions = CadmiumFluxes(1.0,
                            0.01,
                            0.03,
                            0.01,
                            0.11125,
                            0.84875)
flux_proportions.sulphide = flux_proportions.input-(flux_proportions.oxyhydroxide+flux_proportions.carbonate+flux_proportions.clay+flux_proportions.organic)
input_flux = 30000000.0
initial_fluxes = CadmiumFluxes(input_flux*flux_proportions.input,
                                input_flux*flux_proportions.oxyhydroxide,
                                input_flux*flux_proportions.carbonate,
                                input_flux*flux_proportions.clay,
                                input_flux*flux_proportions.organic,
                                input_flux*flux_proportions.sulphide)

input_balanced = CdBURY.Model.calculate_balanced_input(initial_seawater,
                                                                initial_fluxes,
                                                                isotope_offsets)

adjusted_isotope_offsets = CadmiumFluxes(input_balanced.isotope_delta,
                                            isotope_offsets.oxyhydroxide,
                                            isotope_offsets.carbonate,
                                            isotope_offsets.clay,
                                            isotope_offsets.organic,
                                            isotope_offsets.sulphide)


time_configuration = Time(1.0,0.001,0.0001,units="Myr")
model = CdBURY.Model(time_configuration,
                    initial_seawater,
                    initial_fluxes,
                    adjusted_isotope_offsets,
                    dynamic_mass=True)


model.change_flux(Perturbation(0.50,
                               FluxType.organic,
                               CadmiumMassIsotope(0.0,-0.8)))

model.solve()

figure,axes = pyplot.subplots(4,1,figsize=(5,5),sharex=True)
axes[0].plot(time_configuration.as_array(),[flux.isotope_delta for flux in model.seawater][0:-1],zorder=3)

axes[1].plot(time_configuration.as_array(),model.flux_multiplier[0:-1],zorder=3)

axes[2].plot(time_configuration.as_array(),[flux.mass for flux in model.sulphide_flux][0:-1],zorder=3)

axes[3].plot(time_configuration.as_array(),[flux.mass for flux in model.seawater][0:-1],zorder=3)
axes[3].scatter(time_configuration.as_array(),[flux.mass for flux in model.seawater][0:-1],zorder=5)


axes[0].invert_xaxis()

## Set y axis exponent to 0
axes[0].get_yaxis().get_major_formatter().set_useOffset(False)

axes[0].set_ylim((-0.5,0.5))

axes[-1].set_xlabel("Time (Myr)")
axes[0].set_ylabel("Seawater\n $\\delta^{114}$Cd")
axes[1].set_ylabel("Flux\n multiplier")
axes[2].set_ylabel("Sulphide\n flux")
axes[3].set_ylabel("Seawater\n flux")

pyplot.show()