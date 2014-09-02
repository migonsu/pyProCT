"""
Created on 1/9/2014

@author: victor
"""
from pyproct.data.matrix.protein.cases.dihedralCase import DihedralRMSDMatrixCalculator
from pyproct.data.matrix.protein.cases.autoChainMappingCase import ChainMappingRMSDMatrixCalculator
from pyproct.data.matrix.protein.cases.rmsdCase import RMSDMatrixBuilder

class matrixCalculator(object):
    """
    Handles the rmsd for trajectories cases 
    """
    
    CALCULATION_METHOD = "rmsd::ensemble"
    
    def __init__(self, params):
        pass

    def calculate(self, trajectory_handler, matrix_params):
        """
        :param parameters: One dictionary entry with at least the keys "method" and
        "parameters":
        
        {
            "method": STRING,
            "parameters":{
                ...
            }
        }
        
        "method": One of the available matrix generation types available. 
        
        For proteins:

        - "rmsd": Root Mean Square deviation of one body
    
                "parameters":{
                    "type": ENUM ["COORDINATES", "DIHEDRALS"]
                    "fit_selection": STRING,
                    "calc_selection": STRING,
                    "calculator_type": ENUM,
                    "chain_map": BOOL
                }
                
        "type": Type of coordinates used to get the rmsd. It is "COORDINATES" by default.
        "fit_selection": The Prody selection string used to describe the atoms to be superposed.
        "calc_selection": Another Prody selection string that describes the atoms used to calculate RMSD.
        "calculator_type": One of the calculators in pyRMSD.
        "chain_map": Calculates the RMSD of the best mapping of chains e.g. if one has the following 
        tetramer
        
                B
            A       C
                D
    
        and this "reordered" tetramer
    
                A
            B       D
                C
    
        given that all chains are equal, the 'normal' RMSD would be calculated (by default with the 
        chain ordering ABCD Vs ABCD, with a high RMSD value instead of 0, that would be the optimum 
        value for the ordering ABCD Vs BADC.
    
        @return: The created matrix.
        """
        
        coords_type = self.matrix_parameters.get_value("parameters.type", default_value="COORDINATES")

        if coords_type == "COORDINATES":
            mapping = self.matrix_parameters.get_value("parameters.chain_map", default_value=False)

            if not mapping:
                return  RMSDMatrixBuilder.build(trajectory_handler, self.matrix_parameters["parameters"])
            else:
                print "Performing Chain Mapping. This may take some time ..."
                return ChainMappingRMSDMatrixCalculator.calcRMSDMatrix(trajectory_handler.getMergedStructure(),
                                self.matrix_parameters.get_value("parameters.calculator_type", default_value="QCP_SERIAL_CALCULATOR"),
                                self.matrix_parameters.get_value("parameters.fit_selection", default_value="name CA"))

        elif coords_type == "DIHEDRALS":
            return DihedralRMSDMatrixCalculator.build(trajectory_handler.getMergedStructure())

        return self.distance_matrix