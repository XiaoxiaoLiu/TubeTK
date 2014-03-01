import sys
sys.path.append('/home/xiaoxiao/work/src/TubeTK/Base/Python/pyrpca/examples')

from low_rank_atlas_iter import *


tumor_im_names =[\
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0001/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6560.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0002/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6562.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0003/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6564.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0004/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6566.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0005/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6568.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0006/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6570.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0007/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6572.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0008/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6574.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0009/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6576.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0010/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6578.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0011/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6580.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0012/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6582.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0013/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6584.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0014/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6586.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0015/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6588.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0022/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6590.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0024/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6592.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0025/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6594.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0026/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6596.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0027/VSD.Brain_3more.XX.XX.OT/VSD.Brain_3more.XX.XX.OT.6598.mha'
]


flair_im_names = [ \
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0001/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.684.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0002/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.691.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0003/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.697.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0004/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.703.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0005/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.709.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0006/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.715.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0007/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.721.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0008/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.727.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0009/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.733.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0010/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.739.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0011/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.745.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0012/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.751.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0013/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.757.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0014/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.763.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0015/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.769.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0022/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.775.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0024/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.781.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0025/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.787.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0026/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.793.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/HG/0027/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.799.mha'
    ]

selection = [0,1,3,4,6,7,9,10]

result_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/TumorMask'
reference_im_name = '/home/xiaoxiao/work/data/SRI24/T1_Crop.nii.gz'
os.system('mkdir '+result_folder)
num_of_data = len(selection)

for i in range(num_of_data):
        flairIm = flair_im_names[selection[i]] 
        outputIm1 = result_folder+'/affineflair_'+str(i)+'.nrrd'
        outputTransform = result_folder +'affine'+str(i)+'.tfm'
        AffineReg(reference_im_name,flairIm,outputIm1, outputTransform)
        outputIm2 =  result_folder+'/affine3more_' + str(i)  + '.nrrd'
        tumorIm = tumor_im_names[selection[i]] 
        applyLinearTransform(tumorIm, reference_im_name, outputTransform,outputIm2, True)
