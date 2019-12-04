rm -rf ru
mkdir ru 
cd ru
mkdir samples
mkdir logdir
cd logdir
wget https://github.com/sokolegg/speechsyn/releases/download/0.0.1/checkpoint
wget https://github.com/sokolegg/speechsyn/releases/download/0.0.1/graph.pbtxt
wget https://github.com/sokolegg/speechsyn/releases/download/0.0.1/model_gs_400k.data-00000-of-00001
wget https://github.com/sokolegg/speechsyn/releases/download/0.0.1/model_gs_400k.index
wget https://github.com/sokolegg/speechsyn/releases/download/0.0.1/model_gs_400k.meta