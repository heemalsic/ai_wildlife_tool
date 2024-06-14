# AI Tool for Wildlife Images Segregation  
  
A windows-based command line tool which can segregate wildlife images. It is trained on the wildlife images dataset provided by the Wildlife Institute of India and fine tuned over Leopard National Park, Russia's dataset.  
  
# Installation and Use  
  
# Installation  

The tool is compatible with the windows platorm and can be installed by following these steps:  

1. Download [inf_11.zip](https://drive.google.com/uc?export=download&id=1T7sI3z7YvgeSqhwR4jJrf5qMyLsdDl3L).
2. Unzip the compressed file.
3. Download the checkpoint from [here](https://drive.google.com/file/d/1aMDwvLvWZBjnwKKK5fu9Z0iG2cAl9v4B/view?usp=sharing)
  
The application is now ready to be used.  
  
# Use  
  
How to use:  
  
1. Upon unzipping, edit the "paths.txt" file with the respective file paths in your system.  
2. In the model_path, overwrite the absolute path of the checkpoint you have saved in your system.  
3. In input_dir, add the location of the images you want to inference and segregate (use jpg formats).  
4. In output_dir, add the location where you want the images to be segregated.  
5. Now, run the oai_shift.exe file.  
6. You will be asked to confirm whether the file paths are correct (y/n).  
7. You will be asked if you want bounding boxes over the images (y/n).  
8. The application will now create folders according to the class the model has given output labels.  
9. In case of multiple detections, the image will be stored in the class folder having higher confidence, and a shortcut will be created in the class folder with lower confidence.  
