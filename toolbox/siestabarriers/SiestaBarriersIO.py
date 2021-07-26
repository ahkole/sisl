# -*- coding: utf-8 -*-
########################################################################################
# Copyright (c), The SiestaBarriers authors. All rights reserved.                       #
#                                                                                      #
# SiestaBarriers is hosted on GitHub at https://github.com/.................. #
# For further information on the license, see the LICENSE.txt file                     #
########################################################################################
from __future__ import absolute_import

#from SiestaBarriers import SiestaBarriersBase
#from neb_siesta import NEBBase
#from SiestaBarriers.Utils.utils_siesta import read_siesta_fdf,read_siesta_XV
#from SiestaBarriers.Utils.utils_vacancy_exchange import pre_prepare_sisl,is_frac_or_cart_or_index,pre_prepare_ase_after_relax
from .Utils.utils_siesta import read_siesta_fdf,read_siesta_XV
from .Utils.utils_vacancy_exchange import pre_prepare_sisl,is_frac_or_cart_or_index,pre_prepare_ase_after_relax

import os
import glob,shutil
#from SiestaBarriers.Utils.utils_io import Ghost_block , file_cat,string_cat
#from SiestaBarriers.Utils.utils_analysis import NEB_Barrier
#from SiestaBarriers.Utils.utils_io import replace
#from SiestaBarriers.Utils.utils_analysis import NEB_Fix

from .Utils.utils_io import Ghost_block , file_cat,string_cat
from .Utils.utils_analysis import NEB_Barrier
from .Utils.utils_io import replace
from .Utils.utils_analysis import NEB_Fix


__author__ = "Arsalan Akhatar"
__copyright__ = "Copyright 2021, SIESTA Group"
__version__ = "0.1"
__maintainer__ = "Arsalan Akhtar"
__email__ = "arsalan_akhtar@outlook.com," + \
        " miguel.pruneda@icn2.cat "
__status__ = "Development"
__date__ = "Janurary 30, 2021"


class SiestaBarriersIO():
    """
    """
    def __init__(self,
                 sisl_images,
                 flos_path ,
                 flos_file_name_relax,
                 flos_file_name_neb,
                 number_of_images,
                 initial_relaxed_path,
                 final_relaxed_path,
                 relax_engine,
                 relaxed,
                 ghost,
                 initial_relaxed_fdf_name,
                 final_relaxed_fdf_name,
                 neb_results_path = None,
                 ):
        
        self.sisl_images = sisl_images
        self.flos_path = flos_path
        self.flos_file_name_relax = flos_file_name_relax
        self.flos_file_name_neb = flos_file_name_neb
        self.number_of_images = number_of_images
        self.initial_relaxed_path = initial_relaxed_path 
        self.final_relaxed_path = final_relaxed_path
        self.relax_engine = relax_engine
        self.relaxed = relaxed 
        self.ghost = ghost
        self.initial_relaxed_fdf_name = initial_relaxed_fdf_name
        self.final_relaxed_fdf_name = final_relaxed_fdf_name
        self.neb_results_path = neb_results_path

    def write_all_images_sisl(self, fname = 'images',folder_name = 'all' , out_format = 'xyz'):
        """
        """
        if self.relaxed == True:
            print ("Generating All Images After Relaxation")
            folder_name = folder_name + '_relaxed'
            if os.path.isdir(folder_name):
                print (" The All Image Folder Relaxed is there Already PASS")
                print (" Check The Folder: '{}' ".format(folder_name))
                pass
            else:
                os.mkdir(folder_name)
                os.chdir(folder_name)
                for i in range(self.number_of_images+2):
                    self.sisl_images[i].write(fname +'-'+str(i)+"."+out_format)
                    print (" All images generated in The Folder: '{}' ".format(folder_name))
                os.chdir('../')
        else:
            print ("Generating All Images Before Relaxation")
            folder_name = folder_name + '_initial'            
            if os.path.isdir(folder_name):
                print (" The All Image Folder Initial is there Already PASS")
                print (" Check The Folder: '{}' ".format(folder_name))
                pass
            else:
                os.mkdir(folder_name)
                os.chdir(folder_name)
                for i in range(self.number_of_images+2):
                    self.sisl_images[i].write(fname +'-'+str(i)+"."+out_format)
                os.chdir('../')

    def write_image_n_sisl(self,n,fname = 'images' , out_format = 'xyz' ):
        """

        """
        self.sisl_images[n].write(fname +'-'+str(n)+"."+out_format)

    def prepare_endpoint_relax(self, folder_name="image", fname = 'input' , out_format = 'fdf'):

        """
        """
        if self.relaxed == True :
            print (" The Relaxed Flag is True endpoint relaxation PASS...!")
            pass
        else:
            final_image_n = self.number_of_images +  1
            if os.path.isdir(folder_name+"-0"):
                print (" The Image 0  Folder is there Already PASS")
                print (" Check The Folder: '{}' ".format(folder_name+"-0"))
                pass
            else:
                os.mkdir(folder_name+"-0")
                os.chdir(folder_name+"-0")
                self.sisl_images[0].write(fname+'.fdf')
                if self.relax_engine == 'lua':
                    shutil.copy(self.flos_path + self.flos_file_name_relax,'./')
                if self.ghost == True:
                    #-----------------------
                    # Adding Constrant
                    #------------------------
                    print ("Adding Ghost Constaint Block")
                    Ghost_block(self.sisl_images)
                    file_cat('input.fdf','ghost_block_temp','input.fdf')
                    os.remove("ghost_block_temp")
                os.chdir('../')
            if os.path.isdir(folder_name+"-"+str(final_image_n)):
                print (" The Image {}  Folder is there".format(final_image_n))
                print (" Check The Folder: '{}' ".format(folder_name+"-"+str(final_image_n)))
                pass
            else:
                os.mkdir(folder_name+"-"+str(final_image_n))
                os.chdir(folder_name+"-"+str(final_image_n))
                self.sisl_images[final_image_n].write(fname+'.fdf')
                if self.relax_engine == 'lua':
                    shutil.copy(self.flos_path + self.flos_file_name_relax,'./')
                if self.ghost == True:
                    #-----------------------
                    # Adding Constrant
                    #------------------------
                    print ("Adding Ghost Constaint Block")
                    Ghost_block(self.sisl_images)
                    file_cat('input.fdf','ghost_block_temp','input.fdf')
                    os.remove("ghost_block_temp")

                os.chdir('../')
            print ("Endpoint Relaxation Images Folder Created!")

    def prepare_neb(self,neb_folder_name='neb'):
        """
        """
        if self.relaxed == True:
            if self.initial_relaxed_path == None or self.final_relaxed_path == None :
                sys.exit("intial/final relaxed path not provided")
            if self.initial_relaxed_fdf_name == None or self.final_relaxed_fdf_name == None :
                sys.exit("intial/final relaxed fdf not provided")

            if os.path.isdir(neb_folder_name):
                print (" The NEB Folder is there Already PASS")
                print (" Check The Folder: '{}' ".format(neb_folder_name))
                pass
            else:
                os.mkdir(neb_folder_name)
                os.chdir(neb_folder_name)
                self.sisl_images[0].write('input.fdf')
                #self.write_all_images_sisl()
                for i in range(self.number_of_images+2):
                    self.write_image_n_sisl(i)
                if self.ghost == True:
                    #-----------------------
                    # Adding Constrant
                    #------------------------
                    print ("Adding Ghost Constaint Block")
                    Ghost_block(self.sisl_images)
                    file_cat('input.fdf','ghost_block_temp','input.fdf')
                    os.remove("ghost_block_temp")
                else:
                    string_cat("input.fdf","%include parameters.fdf","input.fdf")
                for file in glob.glob(self.initial_relaxed_path+"/*.DM"):
                    print("Copying DM 0  ...")
                    print(file)
                    shutil.copy(file,'./NEB.DM.0')
                for file in glob.glob(self.final_relaxed_path+"/*.DM"):
                    print("Copying DM {} ... ".format(self.number_of_images+1))
                    print(file)
                    shutil.copy(file,'./NEB.DM.{}'.format(self.number_of_images+1))

                shutil.copy(self.flos_path + self.flos_file_name_neb,'./')
                replace("local n_images = 7" , "local n_images = " + str(self.number_of_images) , "neb.lua")
                os.chdir('../')
                print("NEB Folder Ready to Run!")
        else:
            print("RELAX Your Endpoint Images First!")

    def prepare_neb_ring(self,neb_folder_name='neb'):
        """
        """
        if os.path.isdir(neb_folder_name):
            print (" The NEB Folder is there Already PASS")
            print (" Check The Folder: '{}' ".format(neb_folder_name))
        else:
            os.mkdir(neb_folder_name)
            os.chdir(neb_folder_name)
            self.sisl_images[0].write('input.fdf')
            #self.write_all_images_sisl()
            for i in range(self.number_of_images+2):
                self.write_image_n_sisl(i)
            shutil.copy(self.flos_path + self.flos_file_name_neb,'./')
            os.chdir('../')
            print("NEB Folder Ready to Run!")




    def Plot_NEB(self,figname = "NEB" , dpi_in = 800):
        """
        """
        print (self.neb_results_path) 
        NEB_Barrier(self.neb_results_path,self.number_of_images,figname , dpi_in)

    def prepare_neb_analysis(self,image_n,folder_name ="neb-analysis-image",flos_name="neb_analysis.lua"):
        """
        """
        self.flos_file_name_neb = flos_name 
        folder_name = folder_name +"-"+str(image_n)
        if os.path.isdir(folder_name):
            print (" The NEB Folder is there Already PASS")
            print (" Check The Folder: '{}' ".format(folder_name))
            pass
        else:
            os.mkdir(folder_name)
            os.chdir(folder_name)
            shutil.copy(self.neb_results_path+"/NEB.DM.{}".format(image_n),'./')
            print("Copying image {} ... ".format(image_n))
            shutil.copy(self.neb_results_path+"/images-{}.xyz".format(image_n),'./')
            print("Copying image {} ... ".format(image_n))
            for file in glob.glob(self.neb_results_path+"/*.psf"):
                print("Copying psf {} ... ") 
                print(file)
                shutil.copy(file,'./')
            for file in glob.glob(self.neb_results_path+"/*.psml"):
                print("Copying psml {} ... ") 
                print(file)
                shutil.copy(file,'./')
            for file in glob.glob(self.neb_results_path+"/*.fdf"):
                print("Copying psml {} ... ")
                print(file)
                shutil.copy(file,'./')
            shutil.copy(self.flos_path + self.flos_file_name_neb,'./')

            replace('neb.lua','neb_analysis.lua',"parameters.fdf")
            replace("local image_number = 3" , "local image_number = " + str(image_n) , "neb_analysis.lua")
            os.chdir('../')

    def write_n_NEB_image(self,image_n,fdf_name = "input.fdf",image_in="images",image_out="neb_images"):
        """
        """

        NEB_Fix(self.neb_results_path, 
                fdf_name,
                image_in+"-{}.xyz".format(image_n),
                image_out+"-{}".format(image_n))

