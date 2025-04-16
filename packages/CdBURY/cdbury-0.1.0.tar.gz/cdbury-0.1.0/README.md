# CdBURY

## Introduction

Cadmium is a trace nutrient in seawater. Of particular interest are its two stable isotopes, <sup>114</sup>Cd and <sup>110</sup>Cd. Cadmium enters the ocean primarily through riverine input and is removed via burial in association with five key compounds:
- organic carbon
- sulphide
- oxyhydroxide
- clay
- carbonate

Some of these fluxes remove cadmium without bias toward either isotope, while others exhibit a preference. For instance, organic carbon burial preferentially remove <sup>114</sup>Cd over <sup>110</sup>Cd (leaving the ocean with a greater fraction of <sup>110</sup>Cd).
The ratio of the two isotopes of cadmium in seawater can be changed if either the input flux or output fluxes are: large and isotopically distinct from seawater. 

Of the burial fluxes, carbonate, oxyhydroxide, and clay are relatively minor, collectively accounting for less than 5% of total cadmium burial. The flux of cadmium associated with sulphide is the dominant output, comprising approximately 80% of cadmium burial. Whether one isotope is favoured during sulphide burial depends on the burial environment: in euxinic conditions (oxygen depleted but sulphide rich), there is no isotopic bias, whereas in other environments, a preference may exist. The flux of cadmium associated with organic carbon accounts for about 20% of cadmium burial, and  preferentially removes 114Cd with an isotopic offset from seawater of up to -0.8‰.

## About CdBURY

CdBURY is a single-box model designed to simulate the fluxes of cadmium in the ocean as described above. It supports forward simulations, allowing users to perturb parameters at specific times, as well as inverse simulations. In the inverse mode, the model is provided with a record of δ<sup>114</sup>Cd changes in seawater over time and adjusts the prescribed fluxes to match the observed data. Currently, the model supports inversion for organic carbon burial fluxes.

## Example Usage
Here is an example which starts with a steady state system for seawater cadmium, estimates how this changes over one million years, with a perturbation which turns cadmium burial in organic carbon off 500,000 years into the run.

```python
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


time_configuration = Time(1.0,0.001,0.0,units="Myr")
model = CdBURY.Model(time_configuration,
                    initial_seawater,
                    initial_fluxes,
                    adjusted_isotope_offsets,
                    dynamic_mass=True)


model.change_flux(Perturbation(0.50,
                               FluxType.organic,
                               CadmiumMassIsotope(0.0,-0.8)))

model.solve()
```