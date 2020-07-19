# thread-data-mapping
This repository embrace the scripts (Python) used to perform experiments on thread and data mapping as well the resulting data and scripts (R) used to analyze it.
Thread and data mapping policies are used to optimize Machine Learning applications with Tensorflow. To pursue this goal, the benchmark ai-benchmark is used. The Py package of the benchmark can be acessed in [AI-Benchmark](https://pypi.org/project/ai-benchmark/) and more details in [AI-Benchmark Site](http://ai-benchmark.com/).

## Repository Structure
* Charts: Self explanatory, the charts summarazing the experiments results.
* Data: Contains a csv file with the raw experiment results.
* R-scripts: Scripts used to analyze the raw data mentioned above.
* Src: Python Scripts used to produce DOE settings and run the experiments.
* ai-benchmark: The benchmark src with wrapper scripts, to be able to select more precisely which applications were executed, and which modes.

## Dependencies
To run the benchmark, the source was downloaded from  [AI-Benchmark src](https://files.pythonhosted.org/packages/99/9e/6685285db14f407d5061e6022f96400f6fe958a70ba320472178151ded4b/ai-benchmark-0.1.2.tar.gz), so we can select more precisely which application were executed and with custom configurations. The source archive used is present in ai-benchmark folder.
Running the benchmark using the direct source has some drawbacks, as the dependencies aren't resolved automatically by pip. To circunvent this, the following dependencies need to be installed:
```` 
pip install psutil 
pip install numpy
pip install py-cpuinfo
pip install Pillow
pip install setuptools
pip install requests
````

