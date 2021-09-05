![](https://github.com/PanduKonala/PanduKonala/blob/main/header_.png)
<br>
# Batfish-Network-Visulizer
## Overview
> An Open Source python tool which helps the user / learners to understand the configurations provided to Batfish by generating a network diagram. This tool uses [Pybatfish](https://github.com/batfish/pybatfish) and [N2G](https://pypi.org/project/N2G/) modules for visualization of the network from configuration files.
## Prerequisites
1.[Install Python3](https://www.python.org/downloads/)
<br/>
2.[Install Batfish](https://github.com/batfish/batfish/blob/master/README.md)

Ignore if you have already installed.

## Tool Execution
<br/>
Step1: Make sure the Batfish docker is up and running.
<br/>
Step2: Intall the requirments.txt file using pip i.e. pip install -r requirements.txt
<br/>
Step3: Prepare a directory structure as shown in the image located at Images --> directory_structure.jpg and make sure the configuration files end with "cfg" as an extension.
<br/>
Step4: Run the tool --> python3 batfish_network_visualizer_v1.py
<br/>
# Caution if theres an errors such as module missing while execution then please install that module using pip --> pip install {module_name}
<br/>
Step5: After few seconds the tool will generate the output in the "results" directory which is present along with snapshot directory.
<br/>
Step6: Import the file "network_map.drawio" to https://app.diagrams.net for visualization.

## Conclusion
> I hope this tool helps many people to understand more about Batfish. Visualization always helps to learn faster and effectively.
> Special Thanks to [Anton Karneliuk](https://karneliuk.com/2021/06/network-analysis-1-setting-up-and-getting-started-with-batfish-in-multivendor-network-with-cisco-arista-and-cumulus/) for an awesome tutorial on Batfish which helped to get me started.
