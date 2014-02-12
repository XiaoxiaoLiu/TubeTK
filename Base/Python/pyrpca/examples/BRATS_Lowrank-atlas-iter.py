
# In[ ]:

import sys
sys.path.append('./')
from low_rank_atlas_iter import *


# In[ ]:

# global settings
data_folder = '/home/xiaoxiao/work/data/BRATS/Challenge'
result_folder = '/home/xiaoxiao/work/data/BRATS/Challenge/Study1_T1_10inputs'
os.system('mkdir '+ result_folder)
im_names = [  data_folder+'/HG/0301/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17569.mha',
 data_folder+'/HG/0302/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17573.mha',
 data_folder+'/HG/0303/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17577.mha',
 data_folder+'/HG/0304/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17581.mha',
 data_folder+'/HG/0305/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17585.mha',
 data_folder+'/HG/0306/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17589.mha',
 data_folder+'/HG/0307/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17593.mha',
 data_folder+'/HG/0308/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17597.mha',
 data_folder+'/HG/0309/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17601.mha',
 data_folder+'/HG/0310/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.17605.mha']
reference_im_name = data_folder +'/'+'SRI24/T1.nii.gz'


# In[ ]:

# data selection and global parameters
selection = [0,1,2,3,4,5,6,7,8,9]    

num_of_data = len(selection)     
for i in range(num_of_data):
    outputIm =  result_folder+'/Iter0_T1_' + str(i)  + '.nrrd'
    #AffineReg(reference_im_name,im_names[selection[i]],outputIm)


# In[ ]:

# profile data size, save into global variables
im_ref = sitk.ReadImage(reference_im_name) # image in SITK format
im_ref_array = sitk.GetArrayFromImage(im_ref) # get numpy array
z_dim, x_dim, y_dim = im_ref_array.shape # get 3D volume shape
vector_length = z_dim* x_dim*y_dim

slice_nr = 75  # just for vis purpose

# display reference image
implot = plt.imshow(im_ref_array[slice_nr,:,:],plt.cm.gray)
plt.title('healthy atlas')

del im_ref_array


# In[ ]:

###############################  the main pipeline #############################
def runIteration(currentIter):
    # run RPCA
    Y = np.zeros((vector_length,num_of_data))
    for i in range(num_of_data) :
        im_file =  result_folder+'/'+ 'Iter'+str(currentIter - 1)+'_T1_' + str(i)  + '.nrrd'
        tmp = sitk.ReadImage(im_file)
        tmp = sitk.GetArrayFromImage(tmp)
        Y[:,i] = tmp.reshape(-1)
    
    low_rank, sparse, n_iter,rank, sparsity = rpca(Y,lamda)
    saveImagesFromDM(low_rank,result_folder+'/'+ 'Iter'+str(currentIter) +'_LowRank_', im_ref)
    saveImagesFromDM(sparse,result_folder+'/'+ 'Iter'+str(currentIter) +'_Sparse_', im_ref)
    # Visualize and inspect
    plt.figure(figsize=(15,15))
    showSlice(Y, 'Iter'+str(currentIter) +' Input',plt.cm.gray,0,im_ref)    
    showSlice(np.abs(low_rank),'Iter'+str(currentIter) +' low rank',plt.cm.gray,1, im_ref)
    showSlice(np.abs(sparse),'Iter'+str(currentIter) +' sparse',plt.cm.gray,2, im_ref)
    plt.savefig(result_folder+'/'+'Iter'+ str(currentIter)+'.png')
    
    # Register low-rank images to the reference (healthy) image, and update the input images to the next iteration
    for i in range(num_of_data):
        movingIm = result_folder+'/'+ 'Iter'+ str(currentIter)+'_LowRank_' + str(i)  +'.nrrd'
        outputIm = result_folder+'/'+ 'Iter'+ str(currentIter)+'_Deformed_LowRank' + str(i)  + '.nrrd'
        outputTransform = result_folder+'/'+ 'Iter'+ str(currentIter)+'_Transform_' + str(i) +  '.tfm'
        outputDVF = result_folder+'/'+ 'Iter'+ str(currentIter)+'_DVF_' + str(i) +  '.nrrd'
        
        # previousInputImage = result_folder+'/Iter'+str(currentIter-1)+ '_T1_' + str(i)  + '.nrrd'
        
        outputComposedDVFIm = result_folder+'/'+ 'Iter'+ str(currentIter)+'_Composed_DVF_' + str(i) +  '.nrrd'
       
        initialInputImage= result_folder+'/Iter0_T1_' +str(i) +  '.nrrd'

        newInputImage = result_folder+'/Iter'+ str(currentIter)+'_T1_' +str(i) +  '.nrrd'
        
        logFile = open(result_folder+'/Iter'+str(currentIter)+'_RUN_'+ str(i)+'.log', 'w')
        
        # pipe steps sequencially
        cmd1 = BSplineReg(reference_im_name,movingIm,outputIm, outputTransform)
        #print cmd1
        cmd2 = ConvertTransform(reference_im_name,outputTransform,outputDVF)
       
        # compose deformations
        DVFImageList=[]
        for k in range(currentIter):
            DVFImageList.append(result_folder+'/'+ 'Iter'+ str(k+1)+'_DVF_' + str(i) +  '.nrrd')
        cmd3 = composeMultipleDVFs(reference_im_name,DVFImageList,outputComposedDVFIm)
        
        cmd4 = updateInputImageWithDVF(initialInputImage,reference_im_name, outputComposedDVFIm,newInputImage)
        
         
        cmd = cmd1 + ";" + cmd2 + ";" +  cmd3 + ";" + cmd4
        
        process = subprocess.Popen(cmd, stdout = logFile, shell = True)
        process.wait()
        logFile.close()
        
    return sparsity
    


# In[ ]:

# main
import time

NUM_OF_ITERATIONS = 3
lamda = 1.5
sparsity = np.zeros(NUM_OF_ITERATIONS)
s = time.clock() 
  
for j in range(NUM_OF_ITERATIONS):
    jj = j+1
    print 'iteration ' +  str(jj)
    sparsity[j]= runIteration(jj)
    
e = time.clock()
l = e - s
print 'Time spent is:  %f'%l


# In[ ]:

plt.figure()
plt.plot(range(NUM_OF_ITERATIONS), sparsity)
plt.savefig(result_folder+'/sparsity.png')

