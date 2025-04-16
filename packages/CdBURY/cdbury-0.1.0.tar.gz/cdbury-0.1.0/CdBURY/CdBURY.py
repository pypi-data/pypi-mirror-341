import numpy,pandas
import CdBURY.core as core
from CdBURY.classes import CadmiumMassIsotope, FluxType, CadmiumFluxes, Time, Perturbation

from typing import Self

class Model:
    def __init__(self:Self,
                 time:Time,
                 initial_seawater:CadmiumMassIsotope,
                 initial_fluxes:CadmiumFluxes,
                 isotope_offsets:CadmiumFluxes,
                 dynamic_mass:bool =True) -> None:
        """Creates a new Model object with everything needed to initialise the model
        
        :param time: A Time object that describes the time steps that the model will take
        :type time: Time 
        :param initial_seawater: The mass and isotope ratio of the initial seawater
        :type initial_seawater: CadmiumMassIsotope 
        :param initial_fluxes: The masses and isotope ratios of the initial fluxes
        :type initial_fluxes: CadmiumFluxes 
        :param isotope_offsets: The offsets of the isotope ratios from 0‰
        :type isotope_offsets: CadmiumFluxes 
        :param dynamic_mass: Flag which determines if the fluxes should be responsive to the mass of cadmium in the seawater
        :type dynamic_mass: bool
        
        :return: Model
        :rtype: Model"""
        self.time = time
        self.perturbations = []
        self.isotope_offsets = isotope_offsets
        self.dynamic_mass = dynamic_mass

        self.seawater = numpy.empty(time.length+2,dtype="object")
        self.seawater[0] = initial_seawater

        self.flux_multiplier = numpy.empty(time.length+2)
        self.flux_multiplier[0] = 0.0

        self.input_flux = numpy.empty(time.length+2,dtype="object")
        self.input_flux[0] = CadmiumMassIsotope(initial_fluxes.input,isotope_offsets.input)

        self.oxyhydroxide_flux = numpy.empty(time.length+2,dtype="object")
        self.oxyhydroxide_flux[0] = CadmiumMassIsotope(initial_fluxes.oxyhydroxide,initial_seawater.isotope_delta+isotope_offsets.oxyhydroxide)

        self.carbonate_flux = numpy.empty(time.length+2,dtype="object")
        self.carbonate_flux[0] = CadmiumMassIsotope(initial_fluxes.carbonate,isotope_offsets.carbonate+initial_seawater.isotope_delta)

        self.clay_flux = numpy.empty(time.length+2,dtype="object")
        self.clay_flux[0] = CadmiumMassIsotope(initial_fluxes.clay,isotope_offsets.clay+initial_seawater.isotope_delta)

        self.organic_flux = numpy.empty(time.length+2,dtype="object")
        self.organic_flux[0] = CadmiumMassIsotope(initial_fluxes.organic,isotope_offsets.organic+initial_seawater.isotope_delta)

        self.sulphide_flux = numpy.empty(time.length+2,dtype="object")
        self.sulphide_flux[0] = CadmiumMassIsotope(initial_fluxes.sulphide,isotope_offsets.sulphide+initial_seawater.isotope_delta)

    @staticmethod
    def adjust_fluxes(seawater: CadmiumMassIsotope, 
                  cadmium_fluxes: CadmiumFluxes, 
                  isotope_offsets: CadmiumFluxes, 
                  flux_multiplier: float = 0.0) -> CadmiumFluxes:
        """adjust_fluxes changes the fluxes to maintain a constant isotopic offset from seawater, and to account for the mass of cadmium in the seawater if needed
        
        :param seawater: Current seawater mass and isotope ratio
        :type seawater: CadmiumMassIsotope 
        :param cadmium_fluxes: Mass and isotope ratio of input and output fluxes
        :type cadmium_fluxes: CadmiumFluxes 
        :param isotope_offsets: Isoptope offsets from 0‰
        :type isotope_offsets: CadmiumFluxes 
        :param flux_multiplier: Multiplicative value to adjust flux magnitude as a function of seawater cadmium mass
        :type flux_multiplier: float
        
        :return: Adjusted fluxes
        :rtype: CadmiumFluxes
        """
        next_input_flux = cadmium_fluxes.input

        total_flux_multiplier = 1.0+flux_multiplier

        next_oxyhydroxide_flux = CadmiumMassIsotope(cadmium_fluxes.oxyhydroxide.mass*total_flux_multiplier,
                                            seawater.isotope_delta+isotope_offsets.oxyhydroxide)
        next_carbonate_flux = CadmiumMassIsotope(cadmium_fluxes.carbonate.mass*total_flux_multiplier,
                                    seawater.isotope_delta+isotope_offsets.carbonate)
        next_clay_flux = CadmiumMassIsotope(cadmium_fluxes.clay.mass*total_flux_multiplier,
                                            isotope_delta=seawater.isotope_delta+isotope_offsets.clay)
        next_organic_flux = CadmiumMassIsotope(cadmium_fluxes.organic.mass*total_flux_multiplier,
                                    seawater.isotope_delta+isotope_offsets.organic)
        next_sulphide_flux = CadmiumMassIsotope(cadmium_fluxes.sulphide.mass*total_flux_multiplier,
                                seawater.isotope_delta+isotope_offsets.sulphide)
        
        output_cadmium_fluxes = CadmiumFluxes(next_input_flux,
                                              next_oxyhydroxide_flux,
                                              next_carbonate_flux,
                                              next_clay_flux,
                                              next_organic_flux,
                                              next_sulphide_flux)
        return output_cadmium_fluxes

    def get_fluxes(self:Self,
                   timestep:int) -> CadmiumFluxes:
        """get_fluxes returns the fluxes at a given timestep
        
        :param timestep: Timestep number
        :type timestep: int
        
        :return: Fluxes at the given timestep
        :rtype: CadmiumFluxes"""
        return CadmiumFluxes(self.input_flux[timestep],
                             self.oxyhydroxide_flux[timestep],
                             self.carbonate_flux[timestep],
                             self.clay_flux[timestep],
                             self.organic_flux[timestep],
                             self.sulphide_flux[timestep])

    def change_flux(self:Self,
                    perturbation:Perturbation) -> None:
        """change_flux adds a perturbation to the model
        
        :param perturbation: Perturbation object which describes the timing, type, and magnitude of the perturbation
        :type perturbation: Perturbation 
        
        :return: None
        :rtype: None"""
        self.perturbations.append(perturbation)

    @staticmethod
    def step_forward(timestep:int,
                     seawater:CadmiumMassIsotope,
                     fluxes:CadmiumFluxes,
                     isotope_offsets:CadmiumFluxes,
                     flux_multiplier:float,
                     dynamic_mass:bool = True) -> tuple[CadmiumMassIsotope, CadmiumFluxes, float, tuple[float, tuple[float, float]]]:
        """step_forward calculates the next timestep of the model
        
        :param timestep: Timestep number
        :type timestep: int 
        :param seawater: Current seawater mass and isotope ratio
        :type seawater: CadmiumMassIsotope 
        :param fluxes: Mass and isotope ratio of input and output fluxes
        :type fluxes: CadmiumFluxes 
        :param isotope_offsets: Isoptope offsets from 0‰
        :type isotope_offsets: CadmiumFluxes 
        :param flux_multiplier: Multiplicative value to adjust flux magnitude as a function of seawater cadmium mass
        :type flux_multiplier: float 
        :param dynamic_mass: Flag which determines if the fluxes should be responsive to the mass of cadmium in the seawater
        :type dynamic_mass: bool 
        
        :return: Next seawater mass and isotope ratio, adjusted fluxes, next flux multiplier, and gradients
        :rtype: tuple[CadmiumMassIsotope, CadmiumFluxes, float, tuple[float, tuple[float, float]]]"""
        adjusted_fluxes = Model.adjust_fluxes(seawater,fluxes,isotope_offsets,flux_multiplier)
        mass_gradient,(gradient_114,gradient_110) = core.calculate(adjusted_fluxes.input,
                                                                    adjusted_fluxes.oxyhydroxide,
                                                                    adjusted_fluxes.carbonate,
                                                                    adjusted_fluxes.clay,
                                                                    adjusted_fluxes.organic,
                                                                    adjusted_fluxes.sulphide)
        next_seawater = seawater.mass + (mass_gradient*timestep)
        next_cadmium_114_mass = seawater.mass_114 + (gradient_114*timestep)
        next_cadmium_110_mass = seawater.mass_110 + (gradient_110*timestep)

        next_seawater_isotopes = CadmiumMassIsotope.from_masses(next_cadmium_114_mass,next_cadmium_110_mass)
        next_flux_multiplier = (mass_gradient*timestep)/seawater.mass if dynamic_mass else 0.0

        return (next_seawater_isotopes,adjusted_fluxes,next_flux_multiplier,(mass_gradient,(gradient_114,gradient_110)))

    def record(self:Self,
               seawater_isotopes:CadmiumMassIsotope,
               fluxes:CadmiumFluxes,
               flux_multiplier:float,
               timestep:int) -> None:
        """record results to file
        
        :param seawater_isotopes: Current seawater mass and isotope ratio
        :type seawater_isotopes: CadmiumMassIsotope 
        :param fluxes: Mass and isotope ratio of input and output fluxes
        :type fluxes: CadmiumFluxes 
        :param flux_multiplier: Multiplicative value to adjust flux magnitude as a function of seawater cadmium mass
        :type flux_multiplier: float 
        :param timestep: Timestep number
        :type timestep: int 
        
        :return: None
        :rtype: None"""
        match self.time:
            case Time():
                self.seawater[timestep+1] = seawater_isotopes
                self.input_flux[timestep+1] = fluxes.input
                self.oxyhydroxide_flux[timestep+1] = fluxes.oxyhydroxide
                self.carbonate_flux[timestep+1] = fluxes.carbonate
                self.clay_flux[timestep+1] = fluxes.clay
                self.organic_flux[timestep+1] = fluxes.organic
                self.sulphide_flux[timestep+1] = fluxes.sulphide
                self.flux_multiplier[timestep+1] = flux_multiplier


    def solve(self:Self) -> None:
        """solve runs the model through all timesteps
        
        :param self: Description
        :type self: Self 
        
        :return: None
        :rtype: None"""
        time_array = self.time.as_array()
        if time_array is None:
            raise ValueError("time.as_array() returned None")
        for timestep, time in enumerate(time_array):
            current_fluxes = self.get_fluxes(timestep)
            current_seawater = self.seawater[timestep]
            current_flux_multiplier = self.flux_multiplier[timestep]

            (seawater_isotopes_0,
             adjusted_fluxes_0,
             flux_multiplier_0,
             gradients_0) = Model.step_forward(self.time.step_in_yr,
                                                                        current_seawater,
                                                                        current_fluxes,
                                                                        self.isotope_offsets,
                                                                        current_flux_multiplier,
                                                                        self.dynamic_mass)

            (seawater_isotopes_1,
             adjusted_fluxes_1,
             flux_multiplier_1,
             gradients_1) = Model.step_forward(self.time.step_in_yr,
                                                                        seawater_isotopes_0,
                                                                        adjusted_fluxes_0,
                                                                        self.isotope_offsets,
                                                                        flux_multiplier_0,
                                                                        self.dynamic_mass)
            

            average_seawater_isotopes = (seawater_isotopes_0+seawater_isotopes_1)*0.5
            average_isotope_fluxes = (adjusted_fluxes_0+adjusted_fluxes_1)*0.5
            average_flux_multiplier = (flux_multiplier_0+flux_multiplier_1)*0.5
            
            self.record(average_seawater_isotopes,average_isotope_fluxes,average_flux_multiplier,timestep)

            for perturbation in self.perturbations:
                if time>perturbation.time and time<=perturbation.time+self.time.step:
                    if perturbation.type == FluxType.input:
                        self.input_flux[timestep+1] = perturbation.isotope_flux
                    elif perturbation.type == FluxType.oxyhydroxide:
                        self.oxyhydroxide_flux[timestep+1] = perturbation.isotope_flux
                    elif perturbation.type == FluxType.carbonate:
                        self.carbonate_flux[timestep+1] = perturbation.isotope_flux
                    elif perturbation.type == FluxType.clay:
                        self.clay_flux[timestep+1] = perturbation.isotope_flux
                    elif perturbation.type == FluxType.organic:
                        self.organic_flux[timestep+1] = perturbation.isotope_flux
                    elif perturbation.type == FluxType.sulphide:
                        self.sulphide_flux[timestep+1] = perturbation.isotope_flux
                    else:
                        raise ValueError("Unknown perturbation type")
        if self.input_flux[-1] is None:
            self.seawater = self.seawater[:-1]
            self.input_flux = self.input_flux[:-1]
            self.oxyhydroxide_flux = self.oxyhydroxide_flux[:-1]
            self.carbonate_flux = self.carbonate_flux[:-1]
            self.clay_flux = self.clay_flux[:-1]
            self.organic_flux = self.organic_flux[:-1]
            self.sulphide_flux = self.sulphide_flux[:-1]

    def invert(self:Self,
               dataset_values: numpy.ndarray,
               parameter: FluxType) -> None:
        """invert changes the specified parameter to try and match a dataset
        
        :param dataset_ages: Ages of the dataset you want the model to try and match
        :type dataset_ages:  
        :param dataset_values: δ114Cd dataset you want the model to try and match
        :type dataset_values:  
        :param parameter: Specifies the type of flux you want to change
        :type parameter: FluxType 
        
        :return: None
        :rtype: None"""        
        # Calculate the required change in the chosen parameter
        match parameter:
            case FluxType.organic:
                for timestep,time in enumerate(self.time.as_array()[:-2]):
                    # Calculate the target isotope ratio
                    target_cadmium_isotope_delta = dataset_values[timestep+1]
                    # target_cadmium_isotope_ratio = self.delta_to_ratio(target_cadmium_isotope_delta)

                    current_fluxes = self.get_fluxes(timestep)
                    current_seawater = self.seawater[timestep]
                    current_flux_multiplier = self.flux_multiplier[timestep]

                    # Calculate the organic ratio required to reach the target
                    extra_organic_flux_0 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                                    current_seawater,
                                                                    current_fluxes,
                                                                    self.time.step_in_yr)
                    organic_flux_per_year_0 = current_fluxes.organic.mass+extra_organic_flux_0/self.time.step_in_yr
                    if organic_flux_per_year_0<0.0:
                        organic_flux_per_year_0 = 0.0
                    estimated_organic_flux_0 = CadmiumMassIsotope(organic_flux_per_year_0,current_fluxes.organic.isotope_delta)

                    # Group the fluxes with the new estimated organic flux
                    current_fluxes_with_organic = CadmiumFluxes(current_fluxes.input,
                                                                current_fluxes.oxyhydroxide,
                                                                current_fluxes.carbonate,
                                                                current_fluxes.clay,
                                                                estimated_organic_flux_0,
                                                                current_fluxes.sulphide)

                    # Perform the first timestep with the estimated organic flux
                    (seawater_isotopes_0,
                    adjusted_fluxes_0,
                    flux_multiplier_0,
                    gradients_0) = Model.step_forward(self.time.step_in_yr,
                                                                current_seawater,
                                                                current_fluxes_with_organic,
                                                                self.isotope_offsets,
                                                                current_flux_multiplier,
                                                                self.dynamic_mass)

                    # Perform another timestep
                    target_cadmium_isotope_delta = dataset_values[timestep+2]
                    # target_cadmium_isotope_ratio = self.delta_to_ratio(target_cadmium_isotope_delta)

                    extra_organic_flux_1 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                                    seawater_isotopes_0,
                                                                    adjusted_fluxes_0,
                                                                    self.time.step_in_yr)
                    organic_flux_per_year_1 = adjusted_fluxes_0.organic.mass + extra_organic_flux_1/self.time.step_in_yr
                    if organic_flux_per_year_1<0.0:
                        organic_flux_per_year_1 = 0.0
                    estimated_organic_flux_1 = CadmiumMassIsotope(organic_flux_per_year_1,adjusted_fluxes_0.organic.isotope_delta)

                    # Group the fluxes with the new estimated organic flux
                    next_fluxes = CadmiumFluxes(adjusted_fluxes_0.input,
                                                adjusted_fluxes_0.oxyhydroxide,
                                                adjusted_fluxes_0.carbonate,
                                                adjusted_fluxes_0.clay,
                                                estimated_organic_flux_1,
                                                adjusted_fluxes_0.sulphide)
                
                    (seawater_isotopes_1,
                    adjusted_fluxes_1,
                    flux_multiplier_1,
                    gradients_1) = Model.step_forward(self.time.step_in_yr,
                                                                seawater_isotopes_0,
                                                                next_fluxes,
                                                                self.isotope_offsets,
                                                                flux_multiplier_0,
                                                                self.dynamic_mass)
                    
                    # Average the two estimated organic fluxes
                    average_seawater_isotopes = (seawater_isotopes_0+seawater_isotopes_1)*0.5
                    average_isotope_fluxes = (adjusted_fluxes_0+adjusted_fluxes_1)*0.5
                    average_flux_multiplier = (flux_multiplier_0+flux_multiplier_1)*0.5

                    # if average_organic_flux.mass<0:
                    #     average_organic_flux.mass = CadmiumMassIsotope(0.0,self.seawater[timestep].isotope_delta+self.isotope_offsets.organic).mass

                    # Record the new fluxes
                    self.record(average_seawater_isotopes,average_isotope_fluxes,average_flux_multiplier,timestep)
                    
                    a = 5
            case _:
                raise(ValueError("I don't know how to do this yet"))

    def invert_rk4(self,
                   dataset_values: numpy.ndarray,
                   parameter: FluxType) -> None:
        match parameter:
            case FluxType.organic:
                for timestep,time in enumerate(self.time.as_array()[:-2]):
                    current_fluxes = self.get_fluxes(timestep)
                    current_seawater = self.seawater[timestep]
                    current_flux_multiplier = self.flux_multiplier[timestep]

                    initial_seawater = current_seawater
                    initial_flux_multiplier = current_flux_multiplier

                    average_fluxes = self.invert_rk4_step_organic(current_fluxes,
                                                            current_seawater,
                                                            current_flux_multiplier,
                                                            timestep,
                                                            dataset_values)
                    # Apply the averaged fluxes
                    step_length = numpy.abs(self.time.steps[timestep+1]-self.time.steps[timestep])
                    
                    (seawater_isotopes_final,
                    adjusted_fluxes_final,
                    flux_multiplier_final,
                    gradients_final) = Model.step_forward(step_length*self.time.units,
                                                                initial_seawater,
                                                                average_fluxes,
                                                                self.isotope_offsets,
                                                                initial_flux_multiplier,
                                                                self.dynamic_mass)
                    
                    # Record
                    self.record(seawater_isotopes_final,adjusted_fluxes_final,flux_multiplier_final,timestep)
            case _:
                raise(ValueError("I don't know how to do this yet"))
                        
    def invert_rk4_step_organic(self,
                         current_fluxes: CadmiumFluxes,
                         current_seawater: CadmiumMassIsotope,
                         current_flux_multiplier: float,
                         timestep: int,
                         dataset_1_values: numpy.ndarray) -> CadmiumFluxes:
        """invert changes the specified parameter to try and match a dataset

        :param dataset_ages: Ages of the dataset you want the model to try and match
        :type dataset_ages: numpy.ndarray
        :param dataset_values: δ114Cd dataset you want the model to try and match
        :type dataset_values: numpy.ndarray
        :param parameter: Specifies the type of flux you want to change
        :type parameter: FluxType
        """
        initial_fluxes = current_fluxes
        initial_seawater = current_seawater
        initial_flux_multiplier = current_flux_multiplier
        
        half_step_length = numpy.abs(self.time.steps[timestep+1]-self.time.steps[timestep])/2
        half_step_length_in_yr = half_step_length*self.time.units

        # Calculate the target isotope ratio
        target_cadmium_isotope_delta = current_seawater.isotope_delta + (dataset_1_values[timestep+1]-current_seawater.isotope_delta)*0.5

        # Calculate the organic ratio required to reach the target
        extra_organic_flux_0 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)
        organic_flux_per_year_0 = current_fluxes.organic.mass+extra_organic_flux_0/half_step_length_in_yr
        estimated_organic_flux_0 = CadmiumMassIsotope(organic_flux_per_year_0,current_fluxes.organic.isotope_delta)

        if organic_flux_per_year_0<0.0:
            organic_flux_per_year_0 = 0.0


        # Group the fluxes with the new estimated organic flux
        fluxes_0 = CadmiumFluxes(current_fluxes.input,
                            current_fluxes.oxyhydroxide,
                            current_fluxes.carbonate,
                            current_fluxes.clay,
                            estimated_organic_flux_0,
                            current_fluxes.sulphide)
        
        # Perform another timestep
        # Perform the first timestep with the estimated organic flux
        (seawater_isotopes_0,
        adjusted_fluxes_0,
        flux_multiplier_0,
        gradients_0) = Model.step_forward(half_step_length*self.time.units,
                                                    initial_seawater,
                                                    fluxes_0,
                                                    self.isotope_offsets,
                                                    initial_flux_multiplier,
                                                    self.dynamic_mass)
        
        current_seawater = seawater_isotopes_0
        current_fluxes = adjusted_fluxes_0
        current_flux_multiplier = flux_multiplier_0

        target_cadmium_isotope_delta = dataset_1_values[timestep+1]

        extra_organic_flux_1 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)
        

        organic_flux_per_year_1 = adjusted_fluxes_0.organic.mass + extra_organic_flux_1/(half_step_length*self.time.units)

        if organic_flux_per_year_1<0.0:
            organic_flux_per_year_1 = 0.0

        estimated_organic_flux_1 = CadmiumMassIsotope(organic_flux_per_year_1,adjusted_fluxes_0.organic.isotope_delta)

        # Group the fluxes with the new estimated organic flux
        fluxes_1 = CadmiumFluxes(adjusted_fluxes_0.input,
                                    adjusted_fluxes_0.oxyhydroxide,
                                    adjusted_fluxes_0.carbonate,
                                    adjusted_fluxes_0.clay,
                                    estimated_organic_flux_1,
                                    adjusted_fluxes_0.sulphide)
        
        # Do another step
        (seawater_isotopes_1,
        adjusted_fluxes_1,
        flux_multiplier_1,
        gradients_1) = Model.step_forward(half_step_length*self.time.units,
                                                    initial_seawater,
                                                    fluxes_1,
                                                    self.isotope_offsets,
                                                    initial_flux_multiplier,
                                                    self.dynamic_mass)
        
        current_seawater = seawater_isotopes_1
        current_fluxes = adjusted_fluxes_1
        current_flux_multiplier = flux_multiplier_1

        target_cadmium_isotope_delta = dataset_1_values[timestep+1]

        extra_organic_flux_2 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)
        
        organic_flux_per_year_2 = adjusted_fluxes_1.organic.mass + extra_organic_flux_2/(half_step_length*self.time.units)

        if organic_flux_per_year_2<0.0:
            organic_flux_per_year_2 = 0.0

        estimated_organic_flux_2 = CadmiumMassIsotope(organic_flux_per_year_2,adjusted_fluxes_1.organic.isotope_delta)

        # Group the fluxes with the new estimated organic flux
        fluxes_2 = CadmiumFluxes(adjusted_fluxes_1.input,
                                    adjusted_fluxes_1.oxyhydroxide,
                                    adjusted_fluxes_1.carbonate,
                                    adjusted_fluxes_1.clay,
                                    estimated_organic_flux_2,
                                    adjusted_fluxes_1.sulphide)
        
        # Do final step                        
        (seawater_isotopes_2,
        adjusted_fluxes_2,
        flux_multiplier_2,
        gradients_2) = Model.step_forward(half_step_length*self.time.units,
                                                    seawater_isotopes_1,
                                                    fluxes_2,
                                                    self.isotope_offsets,
                                                    flux_multiplier_1,
                                                    self.dynamic_mass)

        target_cadmium_isotope_delta = seawater_isotopes_2.isotope_delta + (dataset_1_values[timestep+2]-seawater_isotopes_2.isotope_delta)*0.5

        extra_organic_flux_3 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        seawater_isotopes_2,
                                                        adjusted_fluxes_2,
                                                        half_step_length_in_yr)
        
        half_step_length = numpy.abs(self.time.steps[timestep+2]-self.time.steps[timestep+1])/2
        half_step_length_in_yr = half_step_length*self.time.units

        organic_flux_per_year_3 = adjusted_fluxes_2.organic.mass + extra_organic_flux_3/half_step_length_in_yr

        if organic_flux_per_year_3<0.0:
            organic_flux_per_year_3 = 0.0

        estimated_organic_flux_3 = CadmiumMassIsotope(organic_flux_per_year_3,adjusted_fluxes_2.organic.isotope_delta)

        # Group the fluxes with the new estimated organic flux
        fluxes_3 = CadmiumFluxes(adjusted_fluxes_2.input,
                                    adjusted_fluxes_2.oxyhydroxide,
                                    adjusted_fluxes_2.carbonate,
                                    adjusted_fluxes_2.clay,
                                    estimated_organic_flux_3,
                                    adjusted_fluxes_2.sulphide)
        
        # Average the fluxes
        average_fluxes = (fluxes_0 + fluxes_1*2.0 + fluxes_2*2.0 + fluxes_3)*(1/6)
        return average_fluxes

    def invert2_rk4(self:Self,
                    dataset_1_values: numpy.ndarray,
                    parameter_1: FluxType,
                    dataset_2_values: numpy.ndarray,
                    parameter_2: FluxType) -> None:
        """invert2 changes the specified parameters to try and match two datasets using the Runge-Kutta 4th order method

        :param dataset_ages: Ages of the first dataset you want the model to try and match
        :type dataset_ages: numpy.ndarray
        :param dataset_1_values: δ114Cd dataset you want the model to try and match
        :type dataset_1_values: numpy.ndarray
        :param parameter_1: Specifies the type of flux you want to change
        :type parameter_1: FluxType
        :param dataset_2_values: [Cd]sw dataset you want the model to try and match
        :type dataset_2_values: numpy.ndarray
        :param parameter_2: Specifies the type of flux you want to change
        :type parameter_2: FluxType

        :return: None
        :rtype: None"""
        # Calculate the required change in the chosen parameter
        match parameter_1, parameter_2:
            case FluxType.organic, FluxType.sulphide:        
                for timestep,time in enumerate(self.time.as_array()[:-2]):
                    current_fluxes = self.get_fluxes(timestep)
                    current_seawater = self.seawater[timestep]
                    current_flux_multiplier = self.flux_multiplier[timestep]

                    initial_seawater = current_seawater
                    initial_flux_multiplier = current_flux_multiplier

                    average_fluxes = self.invert2_rk4_step_organicsulphide(current_fluxes,
                                                            current_seawater,
                                                            current_flux_multiplier,
                                                            timestep,
                                                            dataset_1_values,
                                                            dataset_2_values)


                    # Apply the averaged fluxes
                    step_length = numpy.abs(self.time.steps[timestep+1]-self.time.steps[timestep])
                    
                    (seawater_isotopes_final,
                    adjusted_fluxes_final,
                    flux_multiplier_final,
                    gradients_final) = Model.step_forward(step_length*self.time.units,
                                                                initial_seawater,
                                                                average_fluxes,
                                                                self.isotope_offsets,
                                                                initial_flux_multiplier,
                                                                self.dynamic_mass)
                    
                    # Record
                    self.record(seawater_isotopes_final,adjusted_fluxes_final,flux_multiplier_final,timestep)

    def invert2_rk4_step_organicsulphide(self,
                         current_fluxes: CadmiumFluxes,
                         current_seawater: CadmiumMassIsotope,
                         current_flux_multiplier: float,
                         timestep: int,
                         dataset_1_values: numpy.ndarray,
                         dataset_2_values: numpy.ndarray) -> CadmiumFluxes:
        initial_fluxes = current_fluxes
        initial_seawater = current_seawater
        initial_flux_multiplier = current_flux_multiplier
        
        half_step_length = numpy.abs(self.time.steps[timestep+1]-self.time.steps[timestep])/2
        half_step_length_in_yr = half_step_length*self.time.units

        # Calculate the target isotope ratio
        target_cadmium_isotope_delta = current_seawater.isotope_delta + (dataset_1_values[timestep+1]-current_seawater.isotope_delta)*0.5

        # Calculate the target seawater mass
        target_seawater_mass = current_seawater.mass + (dataset_2_values[timestep+1]-current_seawater.mass)*0.5

        # Calculate the organic ratio required to reach the target
        extra_organic_flux_0 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)
        extra_sulphide_flux_0 = self.calculate_sulphide_to_target(target_seawater_mass,
                                                        current_seawater,
                                                        current_fluxes,
                                                        extra_organic_flux_0)
        
        organic_flux_per_year_0 = current_fluxes.organic.mass+extra_organic_flux_0/half_step_length_in_yr
        sulphide_flux_per_year_0 = current_fluxes.sulphide.mass+extra_sulphide_flux_0/half_step_length_in_yr

        estimated_organic_flux_0 = CadmiumMassIsotope(organic_flux_per_year_0,current_fluxes.organic.isotope_delta)
        estimated_sulphide_flux_0 = CadmiumMassIsotope(sulphide_flux_per_year_0,current_fluxes.sulphide.isotope_delta)

        if organic_flux_per_year_0<0.0:
            organic_flux_per_year_0 = 0.0
        if sulphide_flux_per_year_0<0.0:
            sulphide_flux_per_year_0 = 0.0


        # Group the fluxes with the new estimated organic flux
        fluxes_0 = CadmiumFluxes(current_fluxes.input,
                            current_fluxes.oxyhydroxide,
                            current_fluxes.carbonate,
                            current_fluxes.clay,
                            estimated_organic_flux_0,
                            estimated_sulphide_flux_0)
        
        # Perform another timestep
        # Perform the first timestep with the estimated organic flux
        (seawater_isotopes_0,
        adjusted_fluxes_0,
        flux_multiplier_0,
        gradients_0) = Model.step_forward(half_step_length*self.time.units,
                                                    initial_seawater,
                                                    fluxes_0,
                                                    self.isotope_offsets,
                                                    initial_flux_multiplier,
                                                    self.dynamic_mass)
        
        current_seawater = seawater_isotopes_0
        current_fluxes = adjusted_fluxes_0
        current_flux_multiplier = flux_multiplier_0

        target_cadmium_isotope_delta = dataset_1_values[timestep+1]

        extra_organic_flux_1 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)
        
        extra_sulphide_flux_1 = self.calculate_sulphide_to_target(target_seawater_mass,
                                                        current_seawater,
                                                        current_fluxes,
                                                        extra_organic_flux_1)

        organic_flux_per_year_1 = adjusted_fluxes_0.organic.mass + extra_organic_flux_1/(half_step_length*self.time.units)
        sulphide_flux_per_year_1 = adjusted_fluxes_0.sulphide.mass + extra_sulphide_flux_1/(half_step_length*self.time.units)

        if organic_flux_per_year_1<0.0:
            organic_flux_per_year_1 = 0.0
        if sulphide_flux_per_year_1<0.0:
            sulphide_flux_per_year_1 = 0.0

        estimated_organic_flux_1 = CadmiumMassIsotope(organic_flux_per_year_1,adjusted_fluxes_0.organic.isotope_delta)
        estimated_sulphide_flux_1 = CadmiumMassIsotope(sulphide_flux_per_year_1,adjusted_fluxes_0.sulphide.isotope_delta)

        # Group the fluxes with the new estimated organic flux
        fluxes_1 = CadmiumFluxes(adjusted_fluxes_0.input,
                                    adjusted_fluxes_0.oxyhydroxide,
                                    adjusted_fluxes_0.carbonate,
                                    adjusted_fluxes_0.clay,
                                    estimated_organic_flux_1,
                                    estimated_sulphide_flux_1)
        
        # Do another step
        (seawater_isotopes_1,
        adjusted_fluxes_1,
        flux_multiplier_1,
        gradients_1) = Model.step_forward(half_step_length*self.time.units,
                                                    initial_seawater,
                                                    fluxes_1,
                                                    self.isotope_offsets,
                                                    initial_flux_multiplier,
                                                    self.dynamic_mass)
        
        current_seawater = seawater_isotopes_1
        current_fluxes = adjusted_fluxes_1
        current_flux_multiplier = flux_multiplier_1

        target_cadmium_isotope_delta = dataset_1_values[timestep+1]

        extra_organic_flux_2 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        current_seawater,
                                                        current_fluxes,
                                                        half_step_length_in_yr)

        extra_sulphide_flux_2 = self.calculate_sulphide_to_target(target_seawater_mass,
                                                        current_seawater,
                                                        current_fluxes,
                                                        extra_organic_flux_2)
        
        organic_flux_per_year_2 = adjusted_fluxes_1.organic.mass + extra_organic_flux_2/(half_step_length*self.time.units)
        sulphide_flux_per_year_2 = adjusted_fluxes_1.sulphide.mass + extra_sulphide_flux_2/(half_step_length*self.time.units)

        if organic_flux_per_year_2<0.0:
            organic_flux_per_year_2 = 0.0
        if sulphide_flux_per_year_2<0.0:
            sulphide_flux_per_year_2 = 0.0

        estimated_organic_flux_2 = CadmiumMassIsotope(organic_flux_per_year_2,adjusted_fluxes_1.organic.isotope_delta)
        estimated_sulphide_flux_2 = CadmiumMassIsotope(sulphide_flux_per_year_2,adjusted_fluxes_1.sulphide.isotope_delta)
        
        # Group the fluxes with the new estimated organic flux
        fluxes_2 = CadmiumFluxes(adjusted_fluxes_1.input,
                                    adjusted_fluxes_1.oxyhydroxide,
                                    adjusted_fluxes_1.carbonate,
                                    adjusted_fluxes_1.clay,
                                    estimated_organic_flux_2,
                                    estimated_sulphide_flux_2)
        
        # Do final step                        
        (seawater_isotopes_2,
        adjusted_fluxes_2,
        flux_multiplier_2,
        gradients_2) = Model.step_forward(half_step_length*self.time.units,
                                                    seawater_isotopes_1,
                                                    fluxes_2,
                                                    self.isotope_offsets,
                                                    flux_multiplier_1,
                                                    self.dynamic_mass)

        target_cadmium_isotope_delta = seawater_isotopes_2.isotope_delta + (dataset_1_values[timestep+2]-seawater_isotopes_2.isotope_delta)*0.5
        target_seawater_mass = seawater_isotopes_2.mass + (dataset_2_values[timestep+2]-seawater_isotopes_2.mass)*0.5
        
        extra_organic_flux_3 = self.calculate_organic_to_target(target_cadmium_isotope_delta,
                                                        seawater_isotopes_2,
                                                        adjusted_fluxes_2,
                                                        half_step_length_in_yr)
        extra_sulphide_flux_3 = self.calculate_sulphide_to_target(target_seawater_mass,
                                                        seawater_isotopes_2,
                                                        adjusted_fluxes_2,
                                                        extra_organic_flux_3)
        
        half_step_length = numpy.abs(self.time.steps[timestep+2]-self.time.steps[timestep+1])/2
        half_step_length_in_yr = half_step_length*self.time.units

        organic_flux_per_year_3 = adjusted_fluxes_2.organic.mass + extra_organic_flux_3/half_step_length_in_yr
        sulphide_flux_per_year_3 = adjusted_fluxes_2.sulphide.mass + extra_sulphide_flux_3/half_step_length_in_yr
        
        if organic_flux_per_year_3<0.0:
            organic_flux_per_year_3 = 0.0
        if sulphide_flux_per_year_3<0.0:
            sulphide_flux_per_year_3 = 0.0

        estimated_organic_flux_3 = CadmiumMassIsotope(organic_flux_per_year_3,adjusted_fluxes_2.organic.isotope_delta)
        estimated_sulphide_flux_3 = CadmiumMassIsotope(sulphide_flux_per_year_3,adjusted_fluxes_2.sulphide.isotope_delta)
        
        # Group the fluxes with the new estimated organic flux
        fluxes_3 = CadmiumFluxes(adjusted_fluxes_2.input,
                                    adjusted_fluxes_2.oxyhydroxide,
                                    adjusted_fluxes_2.carbonate,
                                    adjusted_fluxes_2.clay,
                                    estimated_organic_flux_3,
                                    estimated_sulphide_flux_3)
        
        # Average the fluxes
        average_fluxes = (fluxes_0 + fluxes_1*2.0 + fluxes_2*2.0 + fluxes_3)*(1/6)
        return average_fluxes


    @staticmethod
    def integrate_organic(organic_flux:list,
                          timestep_in_yr:float) -> float:
        """integrate_organic calculates the total mass of organic carbon buried during the model simulation
        
        :param organic_flux: List of organic carbon fluxes
        :type organic_flux: list 
        :param timestep_in_yr: Length of each timestep in years
        :type timestep_in_yr: float 
        
        :return: Total mass of organic carbon buried
        :rtype: float"""
        organic_masses = numpy.array(organic_flux)
        return numpy.sum(numpy.array([mass*timestep_in_yr for mass in organic_masses]))
    
    @staticmethod
    def integrate_excess_organic(organic_flux:list,
                                 timestep_in_yr:float) -> float:
        """integrate_excess_organic calculates the total mass of excess organic carbon buried during the model simulation
        
        :param organic_flux: List of organic carbon fluxes
        :type organic_flux: list 
        :param timestep_in_yr: Length of each timestep in years
        :type timestep_in_yr: float 
        
        :return: Total mass of excess organic carbon buried
        :rtype: float"""
        organic_flux_array = numpy.array(organic_flux)
        excess_organic_masses = organic_flux_array-organic_flux_array[0]
        return numpy.sum(numpy.array([mass*timestep_in_yr for mass in excess_organic_masses]))

    def to_json(self:Self) -> dict:
        """to_json converts the model to a JSON serializable dictionary
        
        :param self: Description
        :type self: Self 
        
        :return: JSON serializable dictionary
        :rtype: dict"""
        return {
            "time":list(self.time.as_array()),
            "time_multiplier":self.time.units,
            "seawater_mass":[flux.mass for flux in self.seawater[:-1] if flux is not None],
            "seawater_δ114Cd":[flux.isotope_delta for flux in self.seawater[:-1] if flux is not None],
            "input_mass":[flux.mass for flux in self.input_flux[:-1] if flux is not None],
            "input_δ114Cd":[flux.isotope_delta for flux in self.input_flux[:-1] if flux is not None],
            "oxyhydroxide_mass":[flux.mass for flux in self.oxyhydroxide_flux[:-1] if flux is not None],
            "oxyhydroxide_δ114Cd":[flux.isotope_delta for flux in self.oxyhydroxide_flux[:-1] if flux is not None],
            "carbonate_mass":[flux.mass for flux in self.carbonate_flux[:-1] if flux is not None],
            "carbonate_δ114Cd":[flux.isotope_delta for flux in self.carbonate_flux[:-1] if flux is not None],
            "clay_mass":[flux.mass for flux in self.clay_flux[:-1] if flux is not None],
            "clay_δ114Cd":[flux.isotope_delta for flux in self.clay_flux[:-1] if flux is not None],
            "organic_mass":[flux.mass for flux in self.organic_flux[:-1] if flux is not None],
            "organic_δ114Cd":[flux.isotope_delta for flux in self.organic_flux[:-1] if flux is not None],
            "sulphide_mass":[flux.mass for flux in self.sulphide_flux[:-1] if flux is not None],
            "sulphide_δ114Cd":[flux.isotope_delta for flux in self.sulphide_flux[:-1] if flux is not None],
            "flux_multiplier":list(self.flux_multiplier[:-1])
        }
    def to_excel(self:Self,
                 filename:str) -> None:
        """to excel writes the model to an excel file
        
        :param filename: Name of the file to write the model to
        :type filename: str 
        
        :return: None
        :rtype: None"""
        dataframe = pandas.DataFrame()
        dataframe["time"] = self.time.as_array()

        dataframe["seawater mass"] = [flux.mass for flux in self.seawater[:-1]]
        dataframe["seawater δ114Cd"] = [flux.isotope_delta for flux in self.seawater[:-1]]

        dataframe["input mass"] = [flux.mass for flux in self.input_flux[:-1]]
        dataframe["input δ114Cd"] = [flux.isotope_delta for flux in self.input_flux[:-1]]

        dataframe["oxyhydroxide mass"] = [flux.mass for flux in self.oxyhydroxide_flux[:-1]]
        dataframe["oxyhydroxide δ114Cd"] = [flux.isotope_delta for flux in self.oxyhydroxide_flux[:-1]]

        dataframe["carbonate mass"] = [flux.mass for flux in self.carbonate_flux[:-1]]
        dataframe["carbonate δ114Cd"] = [flux.isotope_delta for flux in self.carbonate_flux[:-1]]

        dataframe["clay mass"] = [flux.mass for flux in self.clay_flux[:-1]]
        dataframe["clay δ114Cd"] = [flux.isotope_delta for flux in self.clay_flux[:-1]]

        dataframe["organic mass"] = [flux.mass for flux in self.organic_flux[:-1]]
        dataframe["organic δ114Cd"] = [flux.isotope_delta for flux in self.organic_flux[:-1]]

        dataframe["sulphide mass"] = [flux.mass for flux in self.sulphide_flux[:-1]]
        dataframe["sulphide δ114Cd"] = [flux.isotope_delta for flux in self.sulphide_flux[:-1]]

        dataframe.to_excel(filename)

    @staticmethod
    def calculate_organic_to_target(target_delta,seawater,cadmium_fluxes,timestep):
        target_ratio = Model.delta_to_ratio(target_delta)
        
        total_114_input = cadmium_fluxes.input.mass_114*timestep
        total_110_input = cadmium_fluxes.input.mass_110*timestep

        total_114_oxyhydroxide = cadmium_fluxes.oxyhydroxide.mass_114*timestep
        total_110_oxyhydroxide = cadmium_fluxes.oxyhydroxide.mass_110*timestep

        total_114_carbonate = cadmium_fluxes.carbonate.mass_114*timestep
        total_110_carbonate = cadmium_fluxes.carbonate.mass_110*timestep

        total_114_clay = cadmium_fluxes.clay.mass_114*timestep
        total_110_clay = cadmium_fluxes.clay.mass_110*timestep

        total_114_organic = cadmium_fluxes.organic.mass_114*timestep
        total_110_organic = cadmium_fluxes.organic.mass_110*timestep

        total_114_sulphide = cadmium_fluxes.sulphide.mass_114*timestep
        total_110_sulphide = cadmium_fluxes.sulphide.mass_110*timestep

        a_114 = total_114_input - (total_114_oxyhydroxide + total_114_carbonate + total_114_clay + total_114_sulphide)
        a_110 = total_110_input - (total_110_oxyhydroxide + total_110_carbonate + total_110_clay + total_110_sulphide)

        # a_114 = cadmium_fluxes.input.mass_114 - (cadmium_fluxes.oxyhydroxide.mass_114 + cadmium_fluxes.carbonate.mass_114 + cadmium_fluxes.clay.mass_114 + cadmium_fluxes.sulphide.mass_114)
        # a_110 = cadmium_fluxes.input.mass_110 - (cadmium_fluxes.oxyhydroxide.mass_110 + cadmium_fluxes.carbonate.mass_110 + cadmium_fluxes.clay.mass_110 + cadmium_fluxes.sulphide.mass_110)

        organic_110 = ((seawater.mass_114 + seawater.mass_110 + a_114 + a_110) - ((a_110+seawater.mass_110)*(target_ratio + 1)))/(cadmium_fluxes.organic.isotope_ratio - target_ratio)
        organic_114 = organic_110*cadmium_fluxes.organic.isotope_ratio

        final_seawater_110 = seawater.mass_110 + total_110_input - (total_110_oxyhydroxide + total_110_carbonate + total_110_clay + total_110_sulphide + organic_110)
        final_seawater_114 = seawater.mass_114 + total_114_input - (total_114_oxyhydroxide + total_114_carbonate + total_114_clay + total_114_sulphide + organic_114)
        # final_seawater_110 = seawater.mass_110 + cadmium_fluxes.input.mass_110 - (cadmium_fluxes.carbonate.mass_110 + cadmium_fluxes.clay.mass_110 + cadmium_fluxes.oxyhydroxide.mass_110 + cadmium_fluxes.sulphide.mass_110 + organic_110)
        # final_seawater_114 = seawater.mass_114 + cadmium_fluxes.input.mass_114 - (cadmium_fluxes.carbonate.mass_114 + cadmium_fluxes.clay.mass_114 + cadmium_fluxes.oxyhydroxide.mass_114 + cadmium_fluxes.sulphide.mass_114 + organic_114)

        final_delta = Model.ratio_to_delta(final_seawater_114/final_seawater_110)

        test_organic = (organic_110+organic_114)/timestep

        extra_110 = organic_110 - total_110_organic
        extra_114 = organic_114 - total_114_organic

        return (extra_110+extra_114)
    @staticmethod
    def calculate_sulphide_to_target(target_mass,seawater,cadmium_fluxes,organic_flux):
        predicted_mass = seawater.mass + cadmium_fluxes.input.mass - cadmium_fluxes.oxyhydroxide.mass - cadmium_fluxes.carbonate.mass - cadmium_fluxes.clay.mass - organic_flux - cadmium_fluxes.sulphide.mass
        extra_sulphide = predicted_mass - target_mass
        return extra_sulphide
    @staticmethod
    def delta_to_ratio(delta,standard=2.30416):
        return ((delta/1000)+1)*standard
    @staticmethod
    def ratio_to_delta(ratio,standard=2.30416):
        return ((ratio/standard)-1)*1000
    @staticmethod
    def equilibrate_fluxes(initial_seawater,initial_fluxes,isotope_offsets):
        input_isotopes = CadmiumMassIsotope(initial_fluxes.input,isotope_offsets.input)
        carbonate_isotopes = CadmiumMassIsotope(initial_fluxes.carbonate,isotope_offsets.carbonate+initial_seawater.isotope_delta)
        organic_isotopes = CadmiumMassIsotope(initial_fluxes.organic,isotope_offsets.organic+initial_seawater.isotope_delta)

        difference = input_isotopes.isotope_mass - carbonate_isotopes.isotope_mass - organic_isotopes.isotope_mass

        mass_organic_needed = (difference-carbonate_isotopes.isotope_mass-(initial_fluxes.organic*carbonate_isotopes.isotope_delta))/(organic_isotopes.isotope_delta-carbonate_isotopes.isotope_delta)
        mass_carbonate_needed = carbonate_isotopes.mass-mass_organic_needed+initial_fluxes.organic

        if (mass_carbonate_needed<0) or (mass_organic_needed<0):
            raise ValueError("Masses are negative")
        return (mass_carbonate_needed,mass_organic_needed)
    @staticmethod
    def calculate_balanced_input(initial_seawater,initial_fluxes,isotope_offsets):
        input_isotopes = CadmiumMassIsotope(initial_fluxes.input,isotope_offsets.input)
        
        oxyhydroxide_isotopes = CadmiumMassIsotope(initial_fluxes.oxyhydroxide,isotope_offsets.oxyhydroxide+initial_seawater.isotope_delta)
        carbonate_isotopes = CadmiumMassIsotope(initial_fluxes.carbonate,isotope_offsets.carbonate+initial_seawater.isotope_delta)
        clay_isotopes = CadmiumMassIsotope(initial_fluxes.clay,isotope_offsets.clay+initial_seawater.isotope_delta)
        organic_isotopes = CadmiumMassIsotope(initial_fluxes.organic,isotope_offsets.organic+initial_seawater.isotope_delta)
        sulphide_isotopes = CadmiumMassIsotope(initial_fluxes.sulphide,isotope_offsets.sulphide+initial_seawater.isotope_delta)

        output_114 = oxyhydroxide_isotopes.mass_114 + carbonate_isotopes.mass_114 + clay_isotopes.mass_114 + organic_isotopes.mass_114 + sulphide_isotopes.mass_114
        output_110 = oxyhydroxide_isotopes.mass_110 + carbonate_isotopes.mass_110 + clay_isotopes.mass_110 + organic_isotopes.mass_110 + sulphide_isotopes.mass_110
        input_balanced = CadmiumMassIsotope.from_masses(output_114,output_110)

        return input_balanced
    @staticmethod
    def rebalance_with_organic(initial_seawater,initial_fluxes,isotope_offsets):
        input_isotopes = CadmiumMassIsotope(initial_fluxes.input,isotope_offsets.input)
        
        oxyhydroxide_isotopes = CadmiumMassIsotope(initial_fluxes.oxyhydroxide,isotope_offsets.oxyhydroxide+initial_seawater.isotope_delta)
        carbonate_isotopes = CadmiumMassIsotope(initial_fluxes.carbonate,isotope_offsets.carbonate+initial_seawater.isotope_delta)
        clay_isotopes = CadmiumMassIsotope(initial_fluxes.clay,isotope_offsets.clay+initial_seawater.isotope_delta)
        organic_isotopes = CadmiumMassIsotope(initial_fluxes.organic,isotope_offsets.organic+initial_seawater.isotope_delta)
        sulphide_isotopes = CadmiumMassIsotope(initial_fluxes.sulphide,isotope_offsets.sulphide+initial_seawater.isotope_delta)

        mass_110_needed = input_isotopes.mass_110 - (oxyhydroxide_isotopes.mass_110 + carbonate_isotopes.mass_110 + clay_isotopes.mass_110 + organic_isotopes.mass_110 + sulphide_isotopes.mass_110)
        mass_114_needed = input_isotopes.mass_114 - (oxyhydroxide_isotopes.mass_114 + carbonate_isotopes.mass_114 + clay_isotopes.mass_114 + organic_isotopes.mass_114 + sulphide_isotopes.mass_114)
        mass_needed = input_isotopes.mass - (oxyhydroxide_isotopes.mass + carbonate_isotopes.mass + clay_isotopes.mass + organic_isotopes.mass + sulphide_isotopes.mass)

        sulphide_ratio = sulphide_isotopes.mass_114/sulphide_isotopes.mass_110
        organic_ratio = organic_isotopes.mass_114/organic_isotopes.mass_110

        extra_110_organic = (mass_needed-(mass_110_needed*(1+sulphide_ratio)))/(organic_ratio-sulphide_ratio)
        extra_114_organic = extra_110_organic*organic_ratio

        extra_110_sulphide = mass_110_needed-extra_110_organic
        extra_114_sulphide = mass_114_needed-extra_114_organic

        extra_organic = extra_110_organic+extra_114_organic
        extra_sulphide = extra_110_sulphide+extra_114_sulphide

        # new_mass_balance = initial_fluxes.input - (oxyhydroxide_isotopes.mass + carbonate_isotopes.mass + clay_isotopes.mass + organic_isotopes.mass + sulphide_isotopes.mass + extra_sulphide + extra_organic)
        # new_114_mass_balance = input_isotopes.mass_114 - (oxyhydroxide_isotopes.mass_114 + carbonate_isotopes.mass_114 + clay_isotopes.mass_114 + organic_isotopes.mass_114 + sulphide_isotopes.mass_114 + extra_114_sulphide + extra_114_organic)
        # new_110_mass_balance = input_isotopes.mass_110 - (oxyhydroxide_isotopes.mass_110 + carbonate_isotopes.mass_110 + clay_isotopes.mass_110 + organic_isotopes.mass_110 + sulphide_isotopes.mass_110 + extra_110_sulphide + extra_110_organic)

        new_organic_flux = initial_fluxes.organic + extra_organic
        new_sulphide_flux = initial_fluxes.sulphide + extra_sulphide

        if new_organic_flux<0.0 or new_sulphide_flux<0.0:
            raise ValueError("Negative fluxes")

        return (new_organic_flux,new_sulphide_flux)


def linear_interpolate(x,y,x_new):
    return numpy.interp(x_new,x,y)
def sigmoid(a,b,x0,x):
    return a/(1+numpy.exp(-b*(x-x0)))