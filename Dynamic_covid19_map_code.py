import pandas as pd
import geopandas as gpd
import PIL
import io

# Reading in the csv data
data = pd.read_csv('Dynamic_map_data.csv')

# Group the data by the states
data = data.groupby('States').sum()

#Create a transpose of the dataframe
data_transposed = data.T
data_transposed.plot(y = ['Lagos', 'FCT', 'Kano', 'Osun', 'Oyo'], use_index = True, figsize = (8, 8), marker = '.')



# Read in Nigeria Map shapefile
Nigeria = gpd.read_file(r'C:\Users\luqman\Desktop\GIS Projects\Corona virus project\NIR-level_1_SHP\NIR-level_1.shp')
Nigeria = Nigeria.drop(columns = ['AREA', 'PERIMETER', 'CAPTION'])

Nigeria.replace('Ogun', 'OGUN', inplace = True) 

#checking the name of the states for any discrepancies
for index, row in data.iterrows():
      
      if index not in Nigeria['ID'].to_list():    
         print(index +  'is not in the list')
      else:
          pass


merge = Nigeria.join(data, on = 'ID', how = 'right')

image_frames =[]
for dates in merge.columns.to_list()[2:74]:
    
     #plot
     ax = merge.plot(column = dates,
                cmap = 'OrRd',
                figsize = (10,10),
                legend = True,
               
                scheme = 'user_defined',
                classification_kwds = {'bins':[0,5,10,50,100,500,1000,2000,5000]},
                edgecolor = 'black',
                linewidth = 0.4)
    #Add a title to the map
     ax.set_title('Total Confirmed Coronavirus Cases:' +  dates, fontdict = 
             {'fontsize':20}, pad = 12.5)
     

     

     #Remove the axes
     ax.set_axis_off()

     #Move the legend
     ax.get_legend().set_bbox_to_anchor((1.1, 0.5))
    
     
     img = ax.get_figure()
     
     f =io.BytesIO()
     img.savefig(f, format = 'png', bbox_inches = 'tight')
     f.seek(0)
     image_frames.append(PIL.Image.open(f))
     

#Create a GIF animation
image_frames[0].save('Dynamic COVID-19 Map2.gif', format = 'GIF',
            append_images = image_frames[1:],
            save_all = True, duration = 300,
            loop = 3)

f.close()
