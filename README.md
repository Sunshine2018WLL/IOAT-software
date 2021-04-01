# IOAT-software
An interactive tool for statistical analysis and visualization of omics data and clinical data



                                                                                 USER MANUAL FOR IOAT 
Chapter 1. Software Overview
This system is a data analysis tool based on machine learning. In multi-omics data using bioinformatics, the clinical data survival time and survival status of multi-omics data can be combined with multiple omics data such as gene expression data , Methylated data, copy number combination, pre-processing data through relevant machine learning methods, feature screening, clustering the filtered features to use the clustered results as the true labels of data for survival analysis. 
 
Chapter 2. Installation
The chapter explains how to download and install IOAT on the user’s computer.
2.1 Requirement
1)	Hardware requirements
a)	Intel Pentium III/800 MHz or higher (or compatible) although one should probably not go below a dual core processor.
b)	2 GB RAM minimum.
2)	Software requirements
a)	Supported operating system (OS) versions (32-bit or 64-bit)
Windows 7 SP1
Windows Server 2008 R2 SP1
Windows Server 2008 SP2
Windows Server 2012 R2
Windows 8
Windows 10
b)	Python v3.5.6 (for Windows) .
c)	R v3.5.1 (for Windows) .

2.2 Configuration of R Environment

2.2.1 Setting system environment variable
After installing R v3.5.1, users should add the path of RScript.exe into the system environment variable before using IOAT. Because IOAT implements some R-based methods by calling Rscript.exe to execute the R codes. When there are several versions of R installed in a user’s computer, IOAT will call the Rscript.exe whose path is added into the system environment variable. 
By default, RScript.exe is in the path such as “c:\Program Files\R\R-3.3.3\bin\”. Then, this path should be added into the system environment variable. In addition, the path “c:\Program Files\R\R-3.5.1\bin\x64\” should also be added for the 64-bit OS.

2.2.2 Installing R packages
The required R packages and their installation commands are listed below:
install.packages("rgl")
install.packages("survival")
install.packages("stringr")
install.packages("rms")
install.packages("caret")
install.packages("scatterplot3d")
install.packages("riskRegression")
install.packages("RColorBrewer")
install.packages("gplots")
install.packages("survival")
install.packages("coin")
install.packages("Rcpp")
install.packages("lattice") 
install.packages("mice")
source("http://bioconductor.org/biocLite.R")
biocLite("Biobase") 
biocLite("limma")
biocLite("impute")
biocLite("R.methodsS3")
biocLite("matrixStats")
biocLite("samr")
Users should install these R packages before starting IOAT. Users are recommended to install these packages one by one in case there are dependent packages required to install and click the “R requirement” button in the Help menu to check if the R environment and required R packages are correctly configured and installed. 

2.2.3 Installing python packages
absl-py==0.10.0
astunparse==1.6.3
attrs==19.3.0
autograd==1.3
autograd-gamma==0.4.1
backcall==0.1.0
bleach==1.5.0
cachetools==4.1.1
certifi==2018.8.24
chardet==3.0.4
colorama==0.4.3
comtypes==1.1.7
cycler==0.10.0
decorator==4.4.1
defusedxml==0.6.0
docx==0.2.4
entrypoints==0.3
enum34==1.1.10
future==0.18.2
gast==0.3.3
google-auth==1.21.2
google-auth-oauthlib==0.4.1
google-pasta==0.2.0
grpcio==1.32.0
h5py==2.10.0
html5lib==0.9999999
hyperopt==0.1.2
idna==2.10
imbalanced-learn==0.6.1
imblearn==0.0
importlib-metadata==1.3.0
ipykernel==5.1.3
ipython==7.9.0
ipython-genutils==0.2.0
jedi==0.15.2
Jinja2==2.10.3
joblib==0.14.1
jsonschema==3.2.0
jupyter-client==5.3.4
jupyter-core==4.6.1
Keras-Preprocessing==1.1.2
kiwisolver==1.1.0
lifelines==0.22.8
lxml==4.4.2
Markdown==3.2.2
MarkupSafe==1.1.1
matplotlib==3.0.3
mistune==0.8.4
more-itertools==8.0.2
nbconvert==5.6.1
nbformat==4.4.0
networkx==2.4
notebook==6.0.2
numpy==1.17.2
oauthlib==3.1.0
opt-einsum==3.3.0
pandas==0.25.3
pandocfilters==1.4.2
parso==0.5.2
patsy==0.5.1
pickleshare==0.7.5
Pillow==5.2.0
pip==19.3.1
prettytable==0.7.2
prometheus-client==0.7.1
prompt-toolkit==2.0.10
protobuf==3.13.0
pyasn1==0.4.8
pyasn1-modules==0.2.8
Pygments==2.5.2
pymongo==3.10.0
pyparsing==2.4.5
PyQt5==5.13.2
PyQt5-sip==12.7.0
pyrsistent==0.15.6
python-dateutil==2.8.1
python-docx==0.8.7
pytz==2019.3
pywin32==227
pywinpty==0.5.7
pyzmq==18.1.1
requests==2.24.0
requests-oauthlib==1.3.0
rpy2==2.9.5
rsa==4.6
scikit-learn==0.22.2.post1
scipy==1.4.1
seaborn==0.9.0
Send2Trash==1.5.0
setuptools==50.3.0
six==1.13.0
sklearn==0.0
statsmodels==0.10.2
tensorboard==2.3.0
tensorboard-plugin-wit==1.7.0
tensorflow==1.4.0
tensorflow-estimator==2.3.0
tensorflow-tensorboard==0.4.0
termcolor==1.1.0
terminado==0.8.1
testpath==0.4.4
toolz==0.8.0
tornado==4.4.1
tqdm==4.35.0
traitlets==4.3.0
unicodecsv==0.14.1
urllib3==1.25.10
Wand==0.5.7
wcwidth==0.1.7
webencodings==0.5.1
Werkzeug==1.0.1
wheel==0.31.1
widgetsnbextension==1.2.6
win-unicode-console==0.5
wincertstore==0.2
wrapt==1.12.1
xgboost==0.90
xlrd==1.0.0
XlsxWriter==0.9.3
xlwings==0.10.0
xlwt==1.1.2
zipp==0.6.0
zope.exceptions==4.3
zope.interface==4.6.0

2.3 Download
IOAT can be freely downloaded from https://github.com/WlSunshine/IOAT-software. Compress the zip package (or 7z) into a specified file folder.Click the "Windows" button and "R" button, enter "cmd" into the background, enter "pyhton file location /mainUI.py" to run IOAT and the graphical user interface (GUI) of IOAT will be shown.
 





