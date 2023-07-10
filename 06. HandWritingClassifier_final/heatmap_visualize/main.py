import HeatmapMaker as hm

fname_loc = {'improved' : 'improved_custom_data.txt',
              'unimproved' : 'unimproved_custom_data.txt'}

fname = fname_loc['improved']

floc = '/Users/ijimin/Desktop/Python Code/MNISTCUSTOM_CNN_Classifier/06. HandWritingClassifier_final/datafile/' + fname

heatmap = hm.HeatmapMaker(floc=floc, softmax=True)
heatmap.printing()

