from CdBURY.classes import CadmiumMassIsotope

def calculate(input_flux: CadmiumMassIsotope,
              oxyhydroxide_flux: CadmiumMassIsotope,
              carbonate_flux: CadmiumMassIsotope,
              clay_flux: CadmiumMassIsotope,
              organic_flux: CadmiumMassIsotope,
              sulphide_flux: CadmiumMassIsotope) -> tuple[float,tuple[float,float]]:
    """Take the fluxes and calculate gradients in the mass and isotopic composition
    
    :param input_flux: Input mass and isotopic composition
    :type input_flux: CadmiumMassIsotope 
    :param oxyhydroxide_flux: Oxyhydroxide mass and isotopic composition
    :type oxyhydroxide_flux: CadmiumMassIsotope 
    :param carbonate_flux: Carbonate mass and isotopic composition
    :type carbonate_flux: CadmiumMassIsotope 
    :param clay_flux: Clay mass and isotopic composition
    :type clay_flux: CadmiumMassIsotope 
    :param organic_flux: Organic mass and isotopic composition
    :type organic_flux: CadmiumMassIsotope 
    :param sulphide_flux: Sulphide mass and isotopic composition
    :type sulphide_flux: CadmiumMassIsotope """
    cadmium_mass_gradient: float = input_flux.mass - oxyhydroxide_flux.mass - carbonate_flux.mass - clay_flux.mass - organic_flux.mass - sulphide_flux.mass
    cadmium_114_gradient: float = input_flux.mass_114 - (oxyhydroxide_flux.mass_114 + carbonate_flux.mass_114 + clay_flux.mass_114 + organic_flux.mass_114 + sulphide_flux.mass_114)
    cadmium_110_gradient: float = input_flux.mass_110 - (oxyhydroxide_flux.mass_110 + carbonate_flux.mass_110 + clay_flux.mass_110 + organic_flux.mass_110 + sulphide_flux.mass_110)
                                
    return (cadmium_mass_gradient,(cadmium_114_gradient,cadmium_110_gradient))