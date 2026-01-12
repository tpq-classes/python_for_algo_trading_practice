#
# Using Plotly (Streaming in JupyterLab)
#
echo "*** INSTALLING ipympl ***"
conda install -y -c conda-forge ipympl
echo "*** INSTALLING widgetsnbextension ***"
conda install -y -c conda-forge widgetsnbextension
echo "*** INSTALLING nodejs ***"
conda install -y nodejs
echo "*** INSTALLING jupyterlab-manager ***"
jupyter labextension install @jupyter-widgets/jupyterlab-manager
echo "*** INSTALLING jupyter-matplotlib ***"
jupyter labextension install jupyter-matplotlib
echo "*** INSTALLING cufflinks ***"
pip install --upgrade cufflinks
echo "*** INSTALLING ipywidgets ***"
conda install -y ipywidgets
echo "*** INSTALLING jupyterlab-plotly ***"
jupyter labextension install jupyterlab-plotly
echo "*** INSTALLING plotly-widget ***"
jupyter labextension install plotlywidget
