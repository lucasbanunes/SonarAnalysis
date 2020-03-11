# Projeto Marinha do Brasil

# Autor: Natanael Junior (natmourajr@gmail.com)
# Laboratorio de Processamento de Sinais - UFRJ
# Laboratorio de Tecnologia Sonar - UFRJ/Marinha do Brasil


import sys
import os
import os.path

import wave
import pickle

from sklearn.externals import joblib

import numpy as np

from scipy.io import loadmat
from sklearn.externals import joblib

print('Starting '+os.path.basename(__file__))

# System var. point to external folders
datapath = os.getenv('/home/lucas/SonarAnalysis/Lofar')
datapath = os.environ.get('/home/lucas/SonarAnalysis/Lofar')

# Variable to chance Database
database = "4classes"

# lofar analysis params
# n_pts_fft = 1024;
# decimation_rate = 3;
# spectrum_bins_left = 400;

n_pts_fft = int(sys.argv[1])  #used 1024
num_overlap = int(sys.argv[2])  #used 0
decimation_rate = int(sys.argv[3])  #used  3
spectrum_bins_left = int(sys.argv[4])  #used 400


if not os.path.exists("%s/%s/data_info_file.mat"%(datapath,database)):
    print('No file: %s'%("%s/%s/data_info_file.mat"%(datapath,database)))
    exit()
else:
    data_info = loadmat("%s/%s/data_info_file.mat"%(datapath,database))
    class_labels = {}
    data = None
    trgt = None
    for iclass in range(data_info['data_info']['class_labels'][0][0][0].shape[0]):
        class_labels[iclass] = str(data_info['data_info']['class_labels'][0][0][0][iclass][0])
        class_filename = ('lofar_data_file_fft_%i_overlap_%i_decimation_%i_spectrum_left_%i'%
                          (n_pts_fft,num_overlap, decimation_rate,spectrum_bins_left))
        print("Reading class: %s"%(class_labels[iclass]))
        if not os.path.exists("%s/%s/%s/%s.mat"%(datapath,database,class_labels[iclass],class_filename)):
            #print "%s/%s/%s/%s.mat"%(datapath,database,class_labels[iclass],class_filename)
            exit()
        else:
            aux_data = []
            aux_trgt = []
            lofar_data = loadmat("%s/%s/%s/%s.mat"%(datapath,database,class_labels[iclass],class_filename))
            for irun in range(lofar_data['lofar_data'][0].shape[0]):
                aux_data = lofar_data['lofar_data'][0][irun]
                if data is None:
                    data = aux_data
                else:
                    data= np.append(data,aux_data,axis=1)
                if trgt is None:
                    trgt = iclass*np.ones([aux_data.shape[1]])
                else:
                    trgt = np.append(trgt,iclass*np.ones([aux_data.shape[1]]))
    if not data is None:
        data = data.T
    joblib.dump([data,trgt,class_labels],'%s/%s/lofar_data_file_fft_overlap_%i_%i_decimation_%i_spectrum_left_%i.jbl'%(datapath,database,n_pts_fft, num_overlap, decimation_rate,spectrum_bins_left),compress=9)



