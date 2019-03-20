###
### Submodule power
###

print('windpype submodule "power" imported')

import windpype.aux as aux
import numpy as np
import pandas as pd
import dateutil.parser
import xml.etree.ElementTree as ET 
from scipy import signal
import scipy.integrate as integrate
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.transforms as mtransforms
from matplotlib.ticker import MaxNLocator
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.axes_grid1.colorbar import colorbar
from matplotlib import colors
import seaborn as sns
import datetime as dt
from iteration_utilities import duplicates
import sys as sys


d_plot = '../../plots/'

class PowerData():
    ''' This class defines an object that contains the time series of power produced and consumed from a specific dataset (e.g. DK1 or Bornholm). 
    '''

    def __init__(self,**kwargs):

        # handle default values and kwargs
        args                =   dict(file_path='',file_name='',ext='')
        args                =   aux.update_dictionary(args,kwargs)

        self.file_path      =   args['file_path']
        self.file_name      =   args['file_name']
        self.ext            =   args['ext']

    def info(self,verbose=True):
        ''' Prints basic info about this dataset.
        '''

        data_df = self.data_df
        if verbose:
            print('\n--------')
            print('Data object contains:')
            print('%s data points' % len(data_df))
            print('from %s to %s' % (np.min(data_df.datetime),np.max(data_df.datetime)))
            print('Minimum time step: %s sec' % (np.min(data_df.time_steps.values)))
            print('Maximum time step: %s sec' % (np.max(data_df.time_steps.values)))
            print('Most common time step: %s sec' % (np.median(data_df.time_steps.values)))
            print('--------')

        return(np.min(data_df.datetime),np.max(data_df.datetime))

    ### Data analysis

    def AddExceptionTest(self,**kwargs):

        # create a custom namespace for this method
        argkeys_needed      =   ['power_name','exc_dev','test_plot','time_cut']
        a                   =   aux.handle_args(kwargs,argkeys_needed,verbose=False)

        data_df             =   self.data_df.copy()

        if a.test_plot:
            # TEST, cutting out part of data
            data_df = data_df[np.array([(data_df['datetime'].values > a.time_cut[0]) & (data_df['datetime'].values < a.time_cut[1])])[0]]

        datetime            =   data_df['datetime'].values
        power               =   data_df[a.power_name].values

        # Calculate deviations from previous data point:
        new_segment         =   True
        index               =   0
        exc_keep            =   np.array(len(data_df)*[False])
        for _ in range(2*len(data_df)):
            # print(index)
            if new_segment:
                # print('new segment!!')
                # Just calculate min and max values
                min_val,max_val =   power[index]-a.exc_dev,power[index]+a.exc_dev
                new_segment     =   False
            else:
                # Calculate if point is outside valid range:
                inside          =   (min_val < power[index] < max_val)
                # print(min_val,power[index],max_val)
                if not inside:
                    # print('not inside')
                    exc_keep[index] = True
                    exc_keep[index-1] = True
                    new_segment = True
                    index -= 1
                if inside:
                    pass
                    # print('inside')

            index += 1
            if index > len(data_df)-1: break

        exc_keep[0] = True
        exc_drop = [exc_keep == False]

        self.exc_keep       =   exc_keep
        self.exc_drop       =   exc_drop

        if a.test_plot:
            fig = plt.figure(figsize=(15,8))
            ax1 = fig.add_subplot(2,1,1)
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Power [MW]')
            self.PlotTimeSeries(col_names=[a.power_name],colors=['k'],labels=[a.power_name],\
                legend=False,ylab='Power [MW]',add=True,time_cut=a.time_cut)
            ax1 = plt.gca()
            ax1.plot(datetime[self.exc_drop],power[self.exc_drop],'ro',label='dropped after exception test')
            ax1.plot(datetime[self.exc_keep],power[self.exc_keep],'bo',label='kept after exception test')
            plt.legend()

    def AddSDA(self,**kwargs):
        ''' Runs a Swinging Door Algorithm on the power data to look for ramps up and down.
        '''

        # create a custom namespace for this method
        argkeys_needed      =   ['power_name','comp_dev','test_plot','time_cut','fig_name']
        a                   =   aux.handle_args(kwargs,argkeys_needed,verbose=False)

        print('\nNow applying Swinging Door Algorithm to %s data' % a.power_name)
        
        data_df = self.data_df.copy()

        if a.test_plot:
            # TEST, cutting out part of data
            data_df = data_df[np.array([(data_df['datetime'].values > a.time_cut[0]) & (data_df['datetime'].values < a.time_cut[1])])[0]]

        datetime = data_df['datetime'].values
        delta_time = data_df['delta_time'].values
        power = data_df[a.power_name].values

        # Remove unnecessary data
        self.AddExceptionTest(**kwargs)

        print('original dataframe of %s rows' % len(data_df))
        red_data_df         =     data_df[self.exc_keep]
        print('reduced to %s rows after exception test' % len(red_data_df))
        delta_time = red_data_df['delta_time'].values
        power = red_data_df[a.power_name].values
        datetime = red_data_df['datetime'].values

        indices             =   []
        index               =   0
        recent_archive_time =   delta_time[0]
        for _ in range(2*len(red_data_df)):
            # print('\n',index)
            incoming_value      =   power[index]
            time                =   delta_time[index]
            time_step           =   time - recent_archive_time

            if index == 0:
                recent_archive_value = incoming_value
                recent_archive_time = time
                indices.append(index)
                # print('Very first point, keeping this index %s' % index)
                new_segment         =   True
            else:
                if new_segment:
                    if time_step == 0:
                        # print('Very first point in this new segment, only storing value')
                        recent_archive_value = incoming_value
                        recent_archive_time = time
                    else:
                        # print('First time step in new segment! Not sure yet, if keeping this index (%s)' % index)
                        current_snapshot_value = incoming_value #snapshot for next time...
                        max_slope       =   (incoming_value+a.comp_dev - recent_archive_value)/time_step
                        min_slope       =   (incoming_value-a.comp_dev - recent_archive_value)/time_step
                        # print('Slopes:')
                        # print(min_slope,max_slope)
                        new_segment = False
                else:
                    # Calculate ref slope
                    ref_slope       =   (incoming_value - recent_archive_value)/time_step
                    # print('ref slope after %s sec: %s' % (time_step,ref_slope))
                    # print(min_slope,max_slope,ref_slope)
                    if not (min_slope < ref_slope < max_slope):
                        # print('point at index %s outside swinging door, go back one to start a new segment' % index)
                        # Start new segment with this incoming value as new archive value
                        recent_archive_value = power[index-1]
                        recent_archive_time = delta_time[index-1]
                        # time_step           =   time - recent_archive_time
                        new_segment         =   True
                        indices.append(index-1)
                        index               -=  2
                    else:
                        # print('point at index %s within swinging door, set as new snapshot value')
                        # print('Previous index %s NOT kept' % (index-1))
                        current_snapshot_value = incoming_value #snapshot for next time...
                        # Do not store this index, but update max and min slopes
                        new_max_slope       =   (incoming_value+a.comp_dev - recent_archive_value)/time_step
                        new_min_slope       =   (incoming_value-a.comp_dev - recent_archive_value)/time_step
                        # Making sure that the opening narrows
                        max_slope           =   min(max_slope,new_max_slope)
                        min_slope           =   max(min_slope,new_min_slope)
                        # print('new slopes:')
                        # print(min_slope,max_slope)


                    # a = asf 
            index           +=  1
            if index > len(red_data_df)-1: break

        print('Identified about %s ramps ' % (len(indices)))

        times_ADS       =   datetime[indices]
        power_ADS       =   power[indices]

        ramps           =   np.array([power[indices[_+1]] - power[indices[_]] for _ in range(len(indices)-1)])
        ramp_index      =   np.arange(len(times_ADS)-1)
        ramp_up_index   =   ramp_index[ramps > 0]
        ramp_do_index   =   ramp_index[ramps < 0]

        times_up_ramps  =   [[times_ADS[_],times_ADS[_+1]] for _ in ramp_up_index]
        power_up_ramps  =   [[power_ADS[_],power_ADS[_+1]] for _ in ramp_up_index]
        times_do_ramps  =   [[times_ADS[_],times_ADS[_+1]] for _ in ramp_do_index]
        power_do_ramps  =   [[power_ADS[_],power_ADS[_+1]] for _ in ramp_do_index]

        if a.test_plot:
            fig = plt.gcf()
            ax1 = fig.add_subplot(2,1,2)
            ax1.plot(times_ADS,power_ADS,'x',ms=15,mew=2,color='purple',label='SDA selected')
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Power [MW]')
            for _ in range(len(times_up_ramps)):
                ax1.plot(times_up_ramps[_],power_up_ramps[_],'--',color='g')
            for _ in range(len(times_do_ramps)):
                ax1.plot(times_do_ramps[_],power_do_ramps[_],'--',color='r')
            plt.legend()
            if a.fig_name: plt.savefig(d_plot+a.fig_name+'.pdf', format='pdf', dpi=500)

        durations_min = np.array([[times_ADS[_+1]-times_ADS[_]] for _ in ramp_index])/np.timedelta64(1, 'm')
        setattr(self,a.power_name+'_SDA_ramp_durations_min',durations_min.flatten())
        setattr(self,a.power_name+'_SDA_ramp_magnitudes',ramps)
        setattr(self,a.power_name+'_SDA_times_up_ramps',times_up_ramps)
        setattr(self,a.power_name+'_SDA_power_up_ramps',power_up_ramps)
        setattr(self,a.power_name+'_SDA_times_ramps',times_ADS[0:-1])

    ### Visualization

    def PlotHisto(self,**kwargs):
        ''' Plot histogram of an attribute, a column in the dataframe or a supplied data array.
        '''

        # create a custom namespace for this method
        argkeys_needed      =   ['histogram_values','epoch','fig_name','bins','max_val','log','ylog','power_name',\
            'xlog','labels','colors','ls','alpha','xlim','xlab','ylab','add','data','remove_zeros','legend']
        a                   =   aux.handle_args(kwargs,argkeys_needed)

        data_df = self.data_df.copy()

        if a.add:
            fig = plt.gcf()
            ax1 = plt.gca()
        else:
            fig = plt.figure(figsize=(10,6))
            ax1 = fig.add_subplot(1,1,1)
            if a.xlab:
                ax1.set_xlabel(a.xlab)
            else:
                ax1.set_xlabel('Values')
            if a.ylab:
                ax1.set_ylabel(a.ylab)
            else:
                ax1.set_ylabel('Histogram [%]')

        for _,histogram_value in enumerate(a.histogram_values):
            try:
                array = getattr(self,histogram_value)
            except:
                try:
                    array = data_df[histogram_value].values
                except:
                    print('Could not find values for %s, will look for supplied data' % histogram_value)
                    try:
                        array = a.data
                    except ValueError:
                        print('No data supplied')

            # if a.epoch != 2:
            #     array = array[data_df['low_penetration_index_'+ a.power_name] == a.epoch]

            if a.max_val:
                array = array[array <= a.max_val]

            if a.log:
                array = np.log10(abs(array[abs(array) > 0]))

            if a.xlim:
                array = array[(array >= a.xlim[0]) & (array <= a.xlim[1])]


            hist, bins = np.histogram(array, bins=a.bins)
            delta_bin = bins[1]-bins[0]
            hist = np.append(0,hist)
            hist = hist*100/np.sum(hist)
            bins_center = np.append(bins[0]-delta_bin,bins[0:-1])+delta_bin/2.
            if a.remove_zeros:
                bins_center = bins_center[hist != 0]
                hist = hist[hist != 0]
            # Add zeros:
            hist = np.append(0,hist)
            hist = np.append(hist,0)
            bins_center = np.append(bins_center[0]-delta_bin,bins_center)
            bins_center = np.append(bins_center,bins_center[-1]+delta_bin)
            hist = hist*100/np.trapz(hist,x=bins_center)
            # hist = hist*100/np.sum(hist)

            if a.labels:
                label = a.labels[_]
            else:
                try:
                    label = aux.pretty_label(histogram_value)
                except:
                    label = histogram_value
            ax1.plot(bins_center,hist,color=a.colors[_],ls=a.ls[_],drawstyle='steps',alpha=a.alpha,label=label)
        if a.legend: plt.legend(fontsize=13)
        if a.ylog:
            ax1.set_yscale('log')
        if a.xlog:
            ax1.set_xscale('log')
        if a.xlim: ax1.set_xlim(a.xlim)

    ### Data handling

    def RestoreData(self):
        ''' Restores data dataframe from a saved pandas file.
        '''
        self.data_df = pd.read_pickle(self.file_path + self.file_name + self.ext)

class CombPowerData(PowerData):
    ''' This class defines an object that contains *combined* power info from the time series of several datasets. 
    '''

    def __init__(self,**kwargs):

        # handle default values and kwargs
        args                =   dict(ob_1=False,ob_2=False,file_path='',file_name='',ext='',dataframe=False,method=False)
        args                =   aux.update_dictionary(args,kwargs)

        if type(args['dataframe']) != bool:
            self.data_df = args['dataframe']
        else:
            self.file_path      =   args['file_path']
            self.file_name      =   args['file_name']
            self.ext            =   args['ext']

        if args['method']:
            self.data_df = aux.CombineDataFrames(args['ob_1'].data_df,args['ob_2'].data_df,**args)
        else:
            print('No method set for combining, will look for passed dataframe')
            if type(args['dataframe']) != bool:
                self.data_df = args['dataframe']
                print('Dataframe stored as attribute')
            else:
                print('No dataframe given, will look for saved file')
                try:
                    self.RestoreData()
                    print('Restored dataframe')
                except:
                    print('No stored dataframe found, could not initialize combined object')

        self.N_datapoints = len(self.data_df)



