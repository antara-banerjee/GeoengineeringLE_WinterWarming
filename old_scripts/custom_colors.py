"""make up some colormaps for your custom"""
import matplotlib.colors as colors
def custom_colors(word):	 
   darkblue='#0000A0'
   midnightblue='#151B54'
   bla='#313695'
   blb='#4575B4'
   blc='#74ADD1'
   bld='#ABD9E9'
   ble='#E0F3F8'
   blue1 = '#0000CC'
   blue2 = '#000099'
   turquoise='#43C6DB'
   lightblue='#ADDFFF'
   oceanblue='#2B65EC'
   gold='#FFD700'
   darkorange='#FF8C00'
   mustard='#FFDB58'
   saffron='#FBB917'
   cantaloupe='#FFA62F'
   Scarlet='#FF2400'
   orangered='#FF4500'
   redwine='#990012'
   burgundy='#8C001A'
   firebrick='#800517'
   darkred='#8B0000'
   if word =='verycold_to_verywarm':
      var = colors.LinearSegmentedColormap.from_list('my_cmap',[midnightblue,darkblue,'blue','white','red',redwine,burgundy],256)
      return var
   elif word == 'cold_to_warm':
       var = colors.LinearSegmentedColormap.from_list('my_cmap',[midnightblue,darkblue,'blue',lightblue,\
       'white',Scarlet,'red',redwine,firebrick],256)
       return var
   elif word == 'avoid_green':
       var = colors.LinearSegmentedColormap.from_list('my_cmap',[midnightblue,darkblue,blue1,\
       'blue',oceanblue,lightblue,'white','yellow',saffron,'orange','red',redwine,burgundy],256)
       return var
   elif word == 'grads':
       #var = colors.LinearSegmentedColormap.from_list('my_cmap',[midnightblue,bla,blb,\
       #blc,bld,ble,'white',gold,'orange',darkorange,orangered,'red',darkred],256)
       var = colors.LinearSegmentedColormap.from_list('my_cmap',[midnightblue,bla,blb,blc,'white',gold,'orange','red',darkred],256)
       return var
   elif word == 'warm':
       var = colors.LinearSegmentedColormap.from_list('my_cmap',[ble,'white',gold,'orange',darkorange,orangered,'red',darkred],256)
       return var
   elif word == 'uneven':
       var = colors.LinearSegmentedColormap.from_list('my_cmap',[(0,midnightblue),(0.0000000001,'white'),(1,darkred)])
       return var
   #else:
   #   raise Exception, "Your choice is not yet specified - if you have an idea: add it to the code in colors_peer.py!"
   del var,darkblue,midnightblue,blue1,blue2,turquoise,lightblue,oceanblue,mustard,saffron,cantaloupe,redwine,burgundy

#,1,2,3,4,5,6,7,8,9,10,11,12],[
#,bla,blb,\blc,bld,ble,'white',gold,'orange',darkorange,orangered,'red',darkred]]
