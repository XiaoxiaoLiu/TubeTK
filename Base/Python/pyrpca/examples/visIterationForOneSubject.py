import sys
sys.path.append('/home/xiaoxiao/work/src/TubeTK/Base/Python/pyrpca/examples')
from low_rank_atlas_iter import *


result_folder ='/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/LRA_Results_T1_20inputs_w0.5' 
outputPNGFolder = '/mnt/nas2/Projects/LowRankAtlas/results/BRATS2-syn-20inputs_w0.5'
os.system('mkdir '+outputPNGFolder)
inputNumber = 5
madality = 'T1'
NUM_OF_ITERATIONS = 10


def showIteraionSlices(typename, row, numList):
     ii = 0
     for i in numList:
          inputIm = result_folder+'/'+ 'Iter'+ str(i)+'_'+typename+'_' + str(inputNumber) +  '.nrrd'
          im= sitk.ReadImage(inputIm) # image in SITK format
	  im_array = sitk.GetArrayFromImage(im) # get numpy array
	  z_dim, x_dim, y_dim = im_array.shape # get 3D volume shape

          plt.subplot2grid((3,NUM_OF_ITERATIONS),(row,ii))
          ii = ii + 1
	  implot = plt.imshow(np.flipud(im_array[z_dim/2,:,:]),plt.cm.gray)
          plt.axis('off')
          plt.title('Iter'+str(ii) +' '+typename)



#for inputNumber in [5,18]:
for inputNumber in range(20):
     fig = plt.figure(figsize=(15,5))
     showIteraionSlices('T1',0, range(0,NUM_OF_ITERATIONS)) #iteraion i's input image is output of iter(i-!)
     showIteraionSlices('LowRank',1, range(1,NUM_OF_ITERATIONS+1))
     showIteraionSlices('Sparse',2,range(1,NUM_OF_ITERATIONS+1))
 
     plt.savefig(outputPNGFolder+'/'+'Input'+str(inputNumber) +'All'+str(NUM_OF_ITERATIONS)+'Iterations.png')
     fig.clf()
     plt.close(fig)

