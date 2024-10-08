#!/bin/bash

# This script downloads the fMRI data used in some analyses.
# Data was collected by Chen et al. (2017) and is available on the Princeton
# Neuroscience Institute's website, here:
# http://arks.princeton.edu/ark:/88435/dsp01nz8062179
# The link used below is the direct download link, though you can verify this
# yourself by copying the download link next to "SherlockMovies_published.tgz"
# on the page linked above.

# NOTE: this takes quite a while to complete (~1 hour)
# ALSO NOTE: the scan data will take up ~11.44 GB of space on your computer

# the file to download and decompress
SRC=https://dataspace.princeton.edu/jspui/bitstream/88435/dsp01nz8062179/7/SherlockMovies_published.tgz

# the destination for the files
DEST=/mnt/data/processed/fMRI

# create the new directory
mkdir -p $DEST

# download compressed file, extract contents to fMRI directory
wget -c $SRC -O - | tar -xz -C $DEST --strip-components=1

# gzip each .nii file to save some space
gzip $DEST/*
