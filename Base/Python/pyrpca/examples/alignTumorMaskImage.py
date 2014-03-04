import sys
sys.path.append('/home/xiaoxiao/work/src/TubeTK/Base/Python/pyrpca/examples')

from low_rank_atlas_iter import *

tumor_im_names =[\
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0001/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1166.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0002/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1168.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0003/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1170.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0004/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1172.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0005/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1174.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0006/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1176.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0007/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1178.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0008/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1180.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0009/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1182.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0010/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1184.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0011/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1186.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0012/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1188.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0013/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1190.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0014/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1192.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0015/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1194.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0016/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1196.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0017/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1198.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0018/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1200.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0019/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1202.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0020/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1204.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0021/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1206.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0022/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1208.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0023/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1210.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0024/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1212.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0025/VSD.Brain_1more.XX.O.OT/VSD.Brain_1more.XX.O.OT.1214.mha'
]


flair_im_names = [ \
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0001/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.865.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0002/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.871.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0003/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.877.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0004/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.883.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0005/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.889.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0006/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.895.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0007/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.901.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0008/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.907.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0009/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.913.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0010/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.919.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0011/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.925.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0012/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.931.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0013/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.937.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0014/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.943.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0015/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.949.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0016/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.955.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0017/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.961.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0018/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.967.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0019/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.973.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0020/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.979.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0021/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.985.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0022/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.991.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0023/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.997.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0024/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.1003.mha',
'/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG/0025/VSD.Brain.XX.O.MR_Flair/VSD.Brain.XX.O.MR_Flair.1009.mha'
    ]


selection = [0,2,5,7,12,17,19,23]

result_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/TumorMask'
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
