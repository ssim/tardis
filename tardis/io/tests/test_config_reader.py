# tests for the config reader module

from tardis.io import config_reader
from astropy import units as u
import os
import pytest
import yaml

from numpy.testing import assert_almost_equal, assert_array_almost_equal
from tardis.util import parse_quantity

def data_path(filename):
    data_dir = os.path.dirname(__file__)
    return os.path.join(data_dir, 'data', filename)

def test_config_namespace_attribute_test():
    namespace = config_reader.TARDISConfigurationNameSpace({'param1':1})
    assert namespace.param1 == 1

def test_config_namespace_attribute_test():
    namespace = config_reader.TARDISConfigurationNameSpace({'param1':1})
    with pytest.raises(AttributeError):
        assert namespace.param2 == 1

def test_quantity_linspace():
    quantity_linspace_dict = dict(start='1.1e4 km/s', stop='2e4 cm/h', num=1000)
    quantity_linspace = config_reader.parse_quantity_linspace(quantity_linspace_dict)
    assert_almost_equal(quantity_linspace[0].value, 1.1e4)
    assert_almost_equal(quantity_linspace[-1].to('cm/h').value, 2e4)
    assert len(quantity_linspace) == 1001

class TestParsePaper1Config:

    def setup(self):
        #general parsing of the paper config
        self.config = config_reader.TARDISConfiguration.from_yaml(data_path('paper1_tardis_configv1.yml'),
                                                                  test_parser=True)
        self.yaml_data = yaml.load(open(data_path('paper1_tardis_configv1.yml')))



    def test_abundances(self):
        oxygen_abundance = self.yaml_data['model']['abundances']['O']
        assert_array_almost_equal(oxygen_abundance, self.config.abundances.ix[8].values)

        assert True

    def test_velocities(self):
        assert_almost_equal(parse_quantity(self.yaml_data['model']['structure']['velocity']['start']),
                            self.config.structure.v_inner[0])
        assert_almost_equal(parse_quantity(self.yaml_data['model']['structure']['velocity']['stop']),
                    self.config.structure.v_outer[-1])
        assert len(self.config.structure.v_outer) == self.yaml_data['model']['structure']['velocity']['num']

    def test_densities(self):
        pass

class TestParseConfigV1ASCIIDensity:

    def setup(self):
        #general parsing of the paper config
        filename = 'tardis_configv1_ascii_density.yml'
        self.config = config_reader.TARDISConfiguration.from_yaml(data_path(filename),
                                                                  test_parser=True)
        self.yaml_data = yaml.load(open(data_path(filename)))


    def test_velocities(self):
        assert self.config.structure.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.config.structure.v_inner[0].value, 1e4 * 1e5)

    def test_abundances(self):
        oxygen_abundance = self.yaml_data['model']['abundances']['O']
        assert_array_almost_equal(oxygen_abundance, self.config.abundances.ix[8].values)


class TestParseConfigV1ArtisDensity:

    def setup(self):
        #general parsing of the paper config
        filename = 'tardis_configv1_artis_density.yml'
        self.config = config_reader.TARDISConfiguration.from_yaml(data_path(filename),
                                                                  test_parser=True)
        self.yaml_data = yaml.load(open(data_path(filename)))


    def test_velocities(self):
        assert self.config.structure.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.config.structure.v_inner[0].value, 1.259375e+03 * 1e5)

    def test_abundances(self):
        oxygen_abundance = self.yaml_data['model']['abundances']['O']
        assert_array_almost_equal(oxygen_abundance, self.config.abundances.ix[8].values)




class TestParseConfigV1ArtisDensityAbundances:

    def setup(self):
        #general parsing of the paper config
        filename = 'tardis_configv1_artis_density.yml'

        self.yaml_data = yaml.load(open(data_path(filename)))
        self.yaml_data['model']['abundances'] = {'type': 'file',
                                                 'filename': 'tardis/io/tests/data/artis_abundances.dat',
                                                 'filetype': 'artis'}

        self.config = config_reader.TARDISConfiguration.from_config_dict(self.yaml_data,
                                                                  test_parser=True)


    def test_velocities(self):
        assert self.config.structure.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.config.structure.v_inner[0].value, 1.259375e+03 * 1e5)

    def test_abundances(self):
        assert_almost_equal(self.config.abundances.ix[14, 54], 0.21864420000000001)


class TestParseConfigV1ArtisDensityAbundancesVSlice:

    def setup(self):
        #general parsing of the paper config
        filename = 'tardis_configv1_artis_density_v_slice.yml'

        self.yaml_data = yaml.load(open(data_path(filename)))
        self.yaml_data['model']['abundances'] = {'type': 'file',
                                                 'filename': 'tardis/io/tests/data/artis_abundances.dat',
                                                 'filetype': 'artis'}

        self.config = config_reader.TARDISConfiguration.from_config_dict(self.yaml_data,
                                                                  test_parser=True)


    def test_velocities(self):
        assert self.config.structure.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.config.structure.v_inner[0], 9000 * u.km/u.s)

    def test_abundances(self):
        assert_almost_equal(self.config.abundances.ix[14, 31], 2.156751e-01)

        
class TestParseConfigV1ArtisDensityAbundancesAllAscii:

    def setup(self):
        #general parsing of the paper config
        filename = 'tardis_configv1_ascii_density_abund.yml'

        self.yaml_data = yaml.load(open(data_path(filename)))
        self.yaml_data['model']['structure']['filename'] = 'tardis/io/tests/data/density.dat'
        self.yaml_data['model']['abundances']['filename'] = 'tardis/io/tests/data/abund.dat'
    
        self.config = config_reader.TARDISConfiguration.from_config_dict(self.yaml_data,
                                                                  test_parser=True)


    def test_velocities(self):
        assert self.config.structure.v_inner.unit == u.Unit('cm/s')
        assert_almost_equal(self.config.structure.v_inner[0], 11000 * u.km/u.s)

    def test_abundances(self):
        assert_almost_equal(self.config.abundances.ix[14, 0], 0.1)
        assert_almost_equal(self.config.abundances.ix[14, 1], 0.2)
        assert_almost_equal(self.config.abundances.ix[14, 2], 0.2)
        assert_almost_equal(self.config.abundances.ix[14, 3], 0.2)
        assert_almost_equal(self.config.abundances.ix[14, 4], 0.2)
        assert_almost_equal(self.config.abundances.ix[14, 5], 0.2)
        assert_almost_equal(self.config.abundances.ix[14, 6], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 0], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 1], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 2], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 3], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 4], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 5], 0.0)
        assert_almost_equal(self.config.abundances.ix[6, 6], 0.5)

    def test_densities(self):
        assert_almost_equal(self.config.structure.mean_densities[0], 9.7656229e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[1], 4.8170911e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[2], 2.5600000e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[3], 1.4450533e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[4], 8.5733893e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[5], 5.3037103e-11 * u.Unit('g/cm3') / 13.0**3 )
        assert_almost_equal(self.config.structure.mean_densities[6], 3.3999447e-11 * u.Unit('g/cm3') / 13.0**3 )
        
        
def test_ascii_reader_power_law():
    with open(data_path('tardis_configv1_density_power_law_test.yml')) as f:
        yaml_data = yaml.load(f)
    #for later use
    density_data = yaml_data['model']['structure']['density']
    t_explosion = density_data['time_0']
    rho_0 = density_data['rho_0']
    exponent = density_data['exponent']
    
    v_inner =  yaml_data['model']['structure']['velocity']['start']
    v_outer =  yaml_data['model']['structure']['velocity']['stop']
    my_conf = config_reader.TARDISConfiguration.from_yaml(data_path('tardis_configv1_density_power_law_test.yml'),test_parser=True)
    structure = my_conf.config_dict['structure']
    
    expected_densites = [3.29072513e-14,  2.70357804e-14,  2.23776573e-14,  1.86501954e-14,  1.56435277e-14,  1.32001689e-14, 1.12007560e-14,  9.55397475e-15,  8.18935779e-15, 7.05208050e-15,  6.09916083e-15,  5.29665772e-15, 4.61758699e-15,  4.04035750e-15,  3.54758837e-15, 3.12520752e-15,  2.76175961e-15,  2.44787115e-15, 2.17583442e-15,  1.93928168e-15]
    expected_unit = 'g / (cm3)'
    
    assert structure['no_of_shells'] == 20
    for i, mdens in enumerate(expected_densites):
        assert_almost_equal(structure['mean_densities'][i].value,mdens)
        assert structure['mean_densities'][i].unit ==  u.Unit(expected_unit)
        
       
    
def test_ascii_reader_exponential_law():
    with open(data_path('tardis_configv1_density_exponential_test.yml')) as f:
        yaml_data = yaml.load(f)
    #for later use
    density_data = yaml_data['model']['structure']['density']
    t_explosion = density_data['time_0']
    rho_0 = density_data['rho_0']
    v0 = density_data['v_0']
    
    v_inner =  yaml_data['model']['structure']['velocity']['start']
    v_outer =  yaml_data['model']['structure']['velocity']['stop']
    my_conf = config_reader.TARDISConfiguration.from_yaml(data_path('tardis_configv1_density_exponential_test.yml'),test_parser=True)
    structure = my_conf.config_dict['structure']
    
    expected_densites = [5.18114795e-14,  4.45945537e-14,  3.83828881e-14, 3.30364579e-14,  2.84347428e-14,  2.44740100e-14, 2.10649756e-14,  1.81307925e-14,  1.56053177e-14, 1.34316215e-14,  1.15607037e-14,  9.95038990e-15, 8.56437996e-15,  7.37143014e-15,  6.34464872e-15, 5.46088976e-15,  4.70023138e-15,  4.04552664e-15, 3.48201705e-15,  2.99699985e-15]
    expected_unit = 'g / (cm3)'
    
    assert structure['no_of_shells'] == 20
    for i, mdens in enumerate(expected_densites):
        assert_almost_equal(structure['mean_densities'][i].value,mdens)
        assert structure['mean_densities'][i].unit ==  u.Unit(expected_unit)
    
    
    
#write tests for inner and outer boundary indices
