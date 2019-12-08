import sys
import numpy as np
from os.path import join as opj
from brainiak.searchlight.searchlight import Searchlight
from nilearn.image import load_img
from scipy.stats import pearsonr
from searchlight_config import config


# voxel function for searchlight
def sfn(l, msk, sl_rad, bcast_var):
    b = l[0][msk, :].T
    c = np.corrcoef(b).ravel()
    return pearsonr(c, bcast_var.ravel())[0]


subid, perm = int(sys.argv[1]), int(sys.argv[2])

input_dir = opj(config['datadir'], 'inputs')
traj_path = opj(input_dir, 'warped', f'sub{subid}_dtw.npy')
scan_path = opj(input_dir, 'fMRI', f'sherlock_movie_s{subid}_10000.nii.gz')
results_dir = opj(config['datadir'], 'outputs', 'searchlight_recall')

# load time-warped recall model
recall_model = np.load(traj_path)

# load fMRI data, create mask
scan_data = load_img(scan_path).get_data()
mask = scan_data[:, :, :, 0] != 10000

try:
    # ensure random shift is consistent across participants
    np.random.seed(perm)
    shift = np.random.randint(1, recall_model.shape[0] - 1)
    result_path = opj(results_dir, 'perms', f'sub{subid}_perm{perm}_shift{shift}.npy')
except ValueError:
    # run searchlight on unaltered data (perm == -1)
    shift = 0
    result_path = opj(results_dir, f'sub{subid}.npy')

# shift recall model timeseries, compute shifted correlation matrix
shifted = np.roll(recall_model, shift=shift, axis=0)
shifted_corrmat = np.corrcoef(shifted)

# create Searchlight object
sl = Searchlight(sl_rad=5)

# distribute data to processes
sl.distribute([scan_data], mask)
sl.broadcast(shifted_corrmat)

# run searchlight, save data
result = sl.run_searchlight(sfn)
np.save(result_path, result)
