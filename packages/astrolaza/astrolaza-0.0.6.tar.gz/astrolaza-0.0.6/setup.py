import setuptools
from setuptools import setup,find_packages

setup(
	name='astrolaza',
	version='0.0.6',
	author='A. Laza-Ramos',
	author_email='andres.laza@uv.es',
	packages=setuptools.find_packages(),
	install_requires=["numpy>=2.1.0","matplotlib>=3.8.0","bagpipes>=1.1.0","scipy>=1.15.0","astropy>=7.0.1","natsort>=8.4","moviepy>=2.0.0"],
	include_package_data = True,
    	classifiers=(
        	"Programming Language :: Python :: 3",
        	"License :: OSI Approved :: MIT License",
        	"Operating System :: OS Independent",
        	),
        )
        	
		
#[testpypi]
#  username = __token__
#  password = pypi-AgENdGVzdC5weXBpLm9yZwIkYjdiYTc5MWYtMjkyMi00M2NiLThmYzUtOWZmN2VmMWVjYTEyAAIqWzMsIjYxNDU0ZTc2LWU5ZTItNDJkMy04OWVmLTljNWY4ZjQ0YWFiNyJdAAAGIIUJLhIVHhAxzDoMFDNMeQmNobTuY0zlhRXRxz22s_f_	
#[pypi]
#password = pypi-AgEIcHlwaS5vcmcCJDFkYjQ4NTI3LWZhNjItNDJjMy04OTQ5LWQyNTNmYTI1NmQ1YgACKlszLCIxZDg1YmEzNi1kZGE0LTQzOGItOWU3NS1lOWUyYmExMDgyZmUiXQAABiDtGFA0EnZYadw2I81mYTAC0epyPX3z4nQAeaVlJi9MMA

