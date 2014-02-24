# -*- coding: utf-8 -*-
import sys
sys.path.append('./')
from low_rank_atlas_iter import *
import pickle


# global variables
data_folder = ''
reference_im_name = ''
result_folder = ''
selection = []
im_names =[]
tissues_Image =  '/home/xiaoxiao/work/data/SRI24/tissues_crop_direct.nrrd'

#CropImage('/home/xiaoxiao/work/data/SRI24/tissues.nrrd',tissues_Image,[50,20,0],[50,30,0])
# also need to reset origina and direction

###############################  the main pipeline #############################
def collectStatstics(InputNum, NUM_OF_ITERATIONS):
    allStats = [ ]
    for currentIter in range(1,NUM_OF_ITERATIONS+1):
        outputComposedDVFIm = result_folder+'/'+ 'Iter'+ str(currentIter)+'_Composed_DVF_' + str(InputNum) +  '.nrrd'
        newInputImage = result_folder+'/Iter'+ str(currentIter)+'_T1_' +str(InputNum) +  '.nrrd'

        outputTissueImage = result_folder+'/tissues_'+str(InputNum) + '_Iter'+ str(currentIter) +  '.nrrd'
        logFile = open(result_folder+'/Iter'+str(currentIter)+'_TissueStats_'+ str(InputNum)+'.log', 'w')


        applyInverseDVFToTissue(outputComposedDVFIm, tissues_Image, reference_im_name, outputTissueImage, True)

        # stats is a matrix of the statistics, including four metrics: mean, std, var,min, max
        stats = computeLabelStatistics(newInputImage,outputTissueImage)

        allStats.append(stats)

    return allStats


# Data info
def useData_BRATS_Challenge():
    global data_folder,result_folder,im_names,selection,reference_im_name
    data_folder = '/home/xiaoxiao/work/data/BRATS/Challenge'

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

    result_folder = '/home/xiaoxiao/work/data/BRATS/Challenge/LRA_Results_T1'

    # data selection
    selection = [0,1,2,3,4,5,6,7]
    reference_im_name = '/home/xiaoxiao/work/data/SRI24/T1_Crop.nii.gz'
    return (data_folder,result_folder,im_names,selection,reference_im_name)

def useData_BRATS2_Synthetic():
    global data_folder,result_folder,im_names,selection,reference_im_name
    data_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/HG'

    im_names = [ \
    data_folder +'/0001/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.866.mha',
    data_folder +'/0002/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.872.mha',
    data_folder +'/0003/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.878.mha',
    data_folder +'/0004/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.884.mha',
    data_folder +'/0005/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.890.mha',
    data_folder +'/0006/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.896.mha',
    data_folder +'/0007/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.902.mha',
    data_folder +'/0008/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.908.mha',
    data_folder +'/0009/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.914.mha',
    data_folder +'/0010/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.920.mha',
    data_folder +'/0011/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.926.mha',
    data_folder +'/0012/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.932.mha',
    data_folder +'/0013/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.938.mha',
    data_folder +'/0014/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.944.mha',
    data_folder +'/0015/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.950.mha',
    data_folder +'/0016/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.956.mha',
    data_folder +'/0017/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.962.mha',
    data_folder +'/0018/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.968.mha',
    data_folder +'/0019/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.974.mha',
    data_folder +'/0020/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.980.mha',
    data_folder +'/0021/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.986.mha',
    data_folder +'/0022/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.992.mha',
    data_folder +'/0023/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.998.mha',
    data_folder +'/0024/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.1004.mha',
    data_folder +'/0025/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.1010.mha'
    ]

    result_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Synthetic_Data/LRA_Results_T1_20inputs'

    # data selection
    selection = [0,1,2,3,4,5,6,7]
    reference_im_name = '/home/xiaoxiao/work/data/SRI24/T1_Crop.nii.gz'
    return (data_folder,result_folder,im_names,selection,reference_im_name)


def useData_BRATS2():
    global data_folder,result_folder,im_names,selection,reference_im_name
    data_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data'

    im_names = [ \
    data_folder+'/HG/0001/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.685.mha',
    data_folder+'/HG/0002/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.692.mha',
    data_folder+'/HG/0003/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.698.mha',
    data_folder+'/HG/0004/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.704.mha',
    data_folder+'/HG/0005/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.710.mha',
    data_folder+'/HG/0006/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.716.mha',
    data_folder+'/HG/0007/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.722.mha',
    data_folder+'/HG/0008/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.728.mha',
    data_folder+'/HG/0009/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.734.mha',
    data_folder+'/HG/0010/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.740.mha',
    data_folder+'/HG/0011/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.746.mha',
    data_folder+'/HG/0012/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.752.mha',
    data_folder+'/HG/0013/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.758.mha',
    data_folder+'/HG/0014/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.764.mha',
    data_folder+'/HG/0015/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.770.mha',
    data_folder+'/HG/0022/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.776.mha',
    data_folder+'/HG/0024/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.782.mha',
    data_folder+'/HG/0025/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.788.mha',
    data_folder+'/HG/0026/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.794.mha',
    data_folder+'/HG/0027/VSD.Brain.XX.O.MR_T1/VSD.Brain.XX.O.MR_T1.800.mha'
    ]
    result_folder = '/home/xiaoxiao/work/data/BRATS/BRATS-2/Image_Data/LRA_Results_T1'
    # data selection
    selection = [0,1,2,3,4,5,6,7]
    reference_im_name = '/home/xiaoxiao/work/data/SRI24/T1_Crop.nii.gz'
    return


#######################################  main ##################################
def main():

    #useData_BRATS_Challenge()
    #useData_BRATS2()
    useData_BRATS2_Synthetic()

    # save script to the result folder for paramter checkups
    os.system('cp /home/xiaoxiao/work/src/TubeTK/Base/Python/pyrpca/examples/TissueStatisticsValidation.py   ' +result_folder)
    sys.stdout = open(result_folder+'/RUN_tissue_stats.log', "w")

    num_of_data = len(selection)
    NUM_OF_ITERATIONS = 15

    # collect label statistics and save into txt files
    for inputNum in range(num_of_data):
        # a list of stats matrix ( numOfLables  *  5)
        allStats = collectStatstics(inputNum, NUM_OF_ITERATIONS)
        with open(result_folder+ '/input'+str(inputNum)+'_label_stats.txt', 'wb') as f:
           pickle.dump(allStats,f)
           f.close()

    # plot label statistics for each input over the iterations
    for inputNum in range(num_of_data):
        # visualize std
        with open(result_folder+ '/input'+str(inputNum)+'_label_stats.txt', 'r') as f:
            allstats =  pickle.load(f)
            plotIterStats(inputNum,allstats,1,'STD',NUM_OF_ITERATIONS)
            plotIterStats(inputNum,allstats,2,'VAR',NUM_OF_ITERATIONS)
            plotIterStats(inputNum,allstats,0,'MEAN',NUM_OF_ITERATIONS)
            plotIterStats(inputNum,allstats,3,'MIN',NUM_OF_ITERATIONS)
            plotIterStats(inputNum,allstats,4,'MAX',NUM_OF_ITERATIONS)
            f.close()

    # plot population label statistics 
    plotAllStats(num_of_data,NUM_OF_ITERATIONS,1,'STD')
    plotAllStats(num_of_data,NUM_OF_ITERATIONS,2,'VAR')
    plotAllStats(num_of_data,NUM_OF_ITERATIONS,0,'MEAN')
    plotAllStats(num_of_data,NUM_OF_ITERATIONS,3,'MIN')
    plotAllStats(num_of_data,NUM_OF_ITERATIONS,4,'MAX')

    return

def plotAllStats(num_of_data,NUM_OF_ITERATIONS,metricInx,metricType):
    CSF = np.zeros((num_of_data,NUM_OF_ITERATIONS))
    WM = np.zeros((num_of_data,NUM_OF_ITERATIONS))
    GM = np.zeros((num_of_data,NUM_OF_ITERATIONS))
    for inputNum in range(num_of_data):
        with open(result_folder+ '/input'+str(inputNum)+'_label_stats.txt', 'r') as f:
          allstats =  pickle.load(f)
          for j in range(NUM_OF_ITERATIONS):
             iterStats = allstats[j]
             CSF[inputNum,j] = iterStats[1, metricInx]
             WM[inputNum,j]  = iterStats[2, metricInx]
             GM[inputNum,j]  = iterStats[3, metricInx]
          f.close()
    plt.figure()
    plt.boxplot(CSF)
    plt.title('CSF label '+ metricType)
    plt.xlabel('Iteration')
    plt.savefig(result_folder +'/CSF_label_'+metricType+'.png')
    plt.close()

    plt.figure()
    plt.boxplot(GM)
    plt.title('GM label '+ metricType)
    plt.xlabel('Iteration')
    plt.savefig(result_folder +'/GM_label_'+metricType+'.png')
    plt.close()

    plt.figure()
    plt.boxplot(WM)
    plt.title('WM label '+ metricType)
    plt.xlabel('Iteration')
    plt.savefig(result_folder +'/WM_label_'+metricType+'.png')
    plt.close()
    return

def plotIterStats(inputNum, allStats,metricInx,metricType,NUM_OF_ITERATIONS):
    fig = plt.figure()
    CSF = np.zeros(NUM_OF_ITERATIONS)
    GM = np.zeros(NUM_OF_ITERATIONS)
    WM = np.zeros(NUM_OF_ITERATIONS)
    for j in range(NUM_OF_ITERATIONS):
         iterStats = allStats[j]
         CSF[j] = iterStats[1,metricInx]
         WM[j] = iterStats[2,metricInx]
         GM[j] = iterStats[3,metricInx]
    plt.plot(CSF)
    plt.plot(WM)
    plt.plot(GM)
    plt.legend(['CSF','WM','GM'])
    plt.title('input'+str(inputNum)+' tissue label stats:' + metricType)
    plt.xlabel('iteration')
    plt.savefig(result_folder+ '/input'+str(inputNum)+'_label_'+metricType+'.png')
    plt.close(fig)

if __name__ == "__main__":
    main()
