# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import numpy as np # Numpy for general purpose processing
import SimpleITK as sitk # SimpleITK to load images
import sys
import subprocess
import os
sys.path.append('../')
from core.ialm import recover # Candes et al.’s RPCA approach

# <codecell>

# load first image
data_folder = '/home/xiaoxiao/work/data/BRATS/Challenge'
affine_registered_folder = data_folder +'/aligned_to_atlas_T1'
result_folder = '/home/xiaoxiao/work/data/BRATS/Challenge/RPCAResults_T1'
im_names = [ \
 data_folder+'/HG/0301/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17569.mha',
 data_folder+'/HG/0302/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17573.mha',
 data_folder+'/HG/0303/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17577.mha',
 data_folder+'/HG/0304/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17581.mha',
 data_folder+'/HG/0305/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17585.mha',
 data_folder+'/HG/0306/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17589.mha',
 data_folder+'/HG/0307/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17593.mha',
 data_folder+'/HG/0308/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17597.mha',
 data_folder+'/HG/0309/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17601.mha',
 data_folder+'/HG/0310/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17605.mha']
reference_im_name = data_folder +'/'+'SRI24_T1_Atlas_Affine_AlignedTo301.mha'

#affine register all the images to 301
def AffineReg(fixedIm,movingIm,outputIm):
    executable = '/home/xiaoxiao/work/bin/BRAINSTolls/bin/BRAINSFit'
    arguments = ' --fixedVolume  ' + fixedIm \
               +' --movingVolume ' + movingIm \
               +' --outputVolume ' + outputIm \
               +' --initializeTransformMode Off --useAffine --numberOfSamples 100000 --splineGridSize 14,10,12  \
                  --numberOfIterations 1500 --maskProcessingMode NOMASK --outputVolumePixelType float \
                  --backgroundFillValue 0 --maskInferiorCutOffFromCenter 1000 --interpolationMode Linear \
                  --minimumStepLength 0.005 --translationScale 1000 --reproportionScale 1 --skewScale 1 \
                  --maxBSplineDisplacement 0 --numberOfHistogramBins 50 --numberOfMatchPoints 10 --fixedVolumeTimeIndex 0 --movingVolumeTimeIndex 0 --medianFilterSize 0,0,0 --removeIntensityOutliers 0 --useCachingOfBSplineWeightsMode ON --useExplicitPDFDerivativesMode AUTO --ROIAutoDilateSize 0 --ROIAutoClosingSize 9 --relaxationFactor 0.5 --maximumStepLength 0.2 --failureExitCode -1 --numberOfThreads -1 --forceMINumberOfThreads -1 --debugLevel 0 --costFunctionConvergenceFactor 1e+09 --projectedGradientTolerance 1e-05 --costMetric MMI'
    cmd = executable + ' ' + arguments
    os.system(cmd)
    # subprocess.call([executable,arguments])
    return 
    
  
num_of_data = len(im_names)     
for i in range(num_of_data):
    outputIm =  affine_registered_folder+'/'+ 'T1_' + str(i)  + '.mha'
    AffineReg(reference_im_name,im_names[i],outputIm)

# <codecell>

im_ref = sitk.ReadImage(reference_im_name) # image in SITK format
im_ref_array = sitk.GetArrayFromImage(im_ref) # get numpy array
z_dim, x_dim, y_dim = im_ref_array.shape # get 3D volume shape
tmp = im_ref_array.reshape(-1) # vectorize

# <codecell>

selection = [0,1,2,4]
Y = np.zeros((len(tmp),len(selection)))
for i in range(len(selection)) :
    im_file =  affine_registered_folder+'/'+ 'T1_' + str(selection[i])  + '.mha'
    tmp = sitk.ReadImage(im_file)
    tmp = sitk.GetArrayFromImage(tmp)
    Y[:,i] = tmp.reshape(-1)

# <codecell>


# <codecell>

from datetime import datetime

lamda = 1.1
def rpca(Y,lamda):
    print  str(datetime.now())
    Y = Y.astype(np.float32, copy=False)
    gamma = lamda* sqrt(float(Y.shape[1])/Y.shape[0])
    low_rank, sparse, n_iter,rank, sparsity = recover(Y,gamma)
    low_rank = low_rank.astype(np.float32, copy=False)
    sparse = sparse.astype(np.float32, copy=False)
    print  str(datetime.now())
    return (low_rank, sparse, n_iter,rank, sparsity)

low_rank, sparse, n_iter,rank, sparsity = rpca(Y,lamda)

# <codecell>

slice_nr = 80
def showSlice(dataMatrix,title):
    fig = plt.figure(figsize=(15,5))
    for i  in range(len(selection)): 
        fig.add_subplot(1,len(selection),i)
        im = np.array(dataMatrix[:,i]).reshape(z_dim,x_dim,y_dim)
        implot = imshow(im[slice_nr,:,:],cm.gray)
        plt.title(title)
        # plt.colorbar()
        implot.set_clim(0,560)
    return

def saveImagesFromDM(dataMatrix,outputPrefix): 
    for i in range(len(selection)):
        im = np.array(dataMatrix[:,i]).reshape(z_dim,x_dim,y_dim)
        img = sitk.GetImageFromArray(im)
        img.SetOrigin(im_ref.GetOrigin())
        img.SetSpacing(im_ref.GetSpacing())
        fn = outputPrefix+str(i)+'.mha'       
        sitk.WriteImage(img,fn)   
    return
it =1
saveImagesFromDM(low_rank,result_folder+'/'+ 'Iter'+str(it) +'_LowRank')
showSlice(Y,'Input')    
showSlice(np.abs(low_rank),'low rank')
showSlice(np.abs(sparse),'sparse')

# <codecell>

#image registration
#register to the reference image (normal control)

# call BrainsFit
import sys

def BSplineReg(fixedIm,movingIm,outputIm, outputTransform):
    executable = '/home/xiaoxiao/work/bin/BRAINSTolls/bin/BRAINSFit'
    arguments = ' --fixedVolume  ' + fixedIm \
               +' --movingVolume ' + movingIm \
               +' --outputVolume ' + outputIm \
               +' --outputTransform ' + outputTransform \
               +' --initializeTransformMode Off --useBSpline --numberOfSamples 100000 --splineGridSize 14,10,12 --numberOfIterations 1500 --maskProcessingMode NOMASK --outputVolumePixelType float --backgroundFillValue 0 --maskInferiorCutOffFromCenter 1000 --interpolationMode Linear --minimumStepLength 0.005 --translationScale 1000 --reproportionScale 1 --skewScale 1 --maxBSplineDisplacement 0 --numberOfHistogramBins 50 --numberOfMatchPoints 10 --fixedVolumeTimeIndex 0 --movingVolumeTimeIndex 0 --medianFilterSize 0,0,0 --removeIntensityOutliers 0 --useCachingOfBSplineWeightsMode ON --useExplicitPDFDerivativesMode AUTO --ROIAutoDilateSize 0 --ROIAutoClosingSize 9 --relaxationFactor 0.5 --maximumStepLength 0.2 --failureExitCode -1 --numberOfThreads -1 --forceMINumberOfThreads -1 --debugLevel 0 --costFunctionConvergenceFactor 1e+09 --projectedGradientTolerance 1e-05 --costMetric MMI'
    cmd = executable + ' ' + arguments
    tempFile = open('./tempExports.txt', 'w')
    process = subprocess.Popen(cmd, stdout=tempFile, shell=True)
    process.wait()
    tempFile.close()
    return
    
def ConvertTransform(fixedIm, outputTransform,outputDVF):    
    cmd ='/home/xiaoxiao/work/bin/Slicer/Slicer-build/lib/Slicer-4.3/cli-modules/BSplineToDeformationField' \
       + ' --tfm '      + outputTransform \
       + ' --refImage ' + fixedIm \
       + ' --defImage ' + outputDVF
   
    tempFile = open('./tempExports2.txt', 'w')
    process = subprocess.Popen(cmd, stdout=tempFile, shell=True)
    process.wait()
    tempFile.close()
    return 
    
    
def updateInputImage(inputImage,refImage, transform, newInputImage):
    cmd='/home/xiaoxiao/work/bin/BRAINSTolls/bin/BRAINSResample' \
      +' --inputVolume '    +  inputImage \
      +' --referenceVolume '+  refImage   \
      +' --outputVolume '   +  newInputImage\
      +' --pixelType float ' \
      +' --warpTransform '  + transform \
      +' --defaultValue 0 --numberOfThreads -1 '     
    tempFile = open('./tempExports3.txt', 'w')
    process = subprocess.Popen(cmd, stdout=tempFile, shell=True)
    process.wait()
    tempFile.close()
    return 
       
for i in range(len(selection)):
    movingIm = result_folder+'/'+ 'Iter'+ str(it)+'_LowRank' + str(i)  +'.mha'
    outputIm =  result_folder+'/'+ 'Iter'+ str(it)+'_Deformed' + str(i)  + '.mha'
    outputTransform = result_folder+'/'+ 'Iter'+ str(it)+'_Transform' + str(i) +  '.tfm'
    outputDVF = result_folder+'/'+ 'Iter'+ str(it)+'_DVF' + str(i) +  '.mha'
    #BSplineReg(reference_im_name,movingIm,outputIm, outputTransform)
    #ConvertTransform(reference_im_name,outputTransform,outputDVF)
    
    previousInputImage = affine_registered_folder+'/'+ 'T1_' + str(selection[i])  + '.mha'
    newInputImage = result_folder+'/'+ 'Iter'+ str(it+1)+'_T1_' +str(i) +  '.mha'
    updateInputImage(previousInputImage,reference_im_name, outputTransform,newInputImage)
    

# <codecell>

it = it+1
for i in range(len(selection)) :
    im_file =  result_folder +'/'+ 'Iter'+ str(it)+'_T1_' +str(i) +  '.mha'
    tmp = sitk.ReadImage(im_file)
    tmp = sitk.GetArrayFromImage(tmp)
    Y[:,i] = tmp.reshape(-1)
    
low_rank, sparse, n_iter,rank, sparsity = rpca(Y,lamda)

saveImagesFromDM(low_rank,result_folder+'/'+ 'Iter'+str(it) +'_LowRank')
showSlice(Y,'Input')    
showSlice(np.abs(low_rank),'low rank')
showSlice(np.abs(sparse),'sparse')

