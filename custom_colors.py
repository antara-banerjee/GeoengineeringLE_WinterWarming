"""make up some colormaps for your custom"""
import matplotlib.colors as colors
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

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
   elif word == 'matlab':
       #var = colors.LinearSegmentedColormap.from_list('matlab',[( 25, 25, 112),( 10, 50, 120),(15, 75, 165),(60, 160, 240),(80, 180, 250),(130, 210, 255), (160, 240, 255),(200, 250, 255),(255, 255, 255),(255, 255, 255),(255, 232, 120),(255, 192, 60),(255, 160, 0), (255, 96, 0),(255, 50, 0),(192, 0, 0),(165, 0, 0),(128, 0, 0)])
       var = colors.LinearSegmentedColormap.from_list('matlab',[\
rgb_to_hex(( 25, 25, 112)),\
rgb_to_hex(( 10, 50, 120)),\
rgb_to_hex((15, 75, 165)),\
rgb_to_hex((60, 160, 240)),\
rgb_to_hex((80, 180, 250)),\
rgb_to_hex((130, 210, 255)),\
#rgb_to_hex((160, 240, 255)),\ # was 240; below is the new
rgb_to_hex((160, 225, 255)),\
#rgb_to_hex((200, 250, 255)),\
rgb_to_hex((255, 255, 255)),\
rgb_to_hex((255, 255, 255)),\
#rgb_to_hex((255, 232, 120)),\ # original yellow
rgb_to_hex((255, 232, 90)),\
#rgb_to_hex((255, 192, 60)),\
rgb_to_hex((255, 160, 0)),\
rgb_to_hex((255, 96, 0)),\
rgb_to_hex((255, 50, 0)),\
rgb_to_hex((192, 0, 0)),\
rgb_to_hex((165, 0, 0)),\
rgb_to_hex((128, 0, 0))])
       return var
   elif word == 'precip':
       #var = colors.LinearSegmentedColormap.from_list('matlab',[( 25, 25, 112),( 10, 50, 120),(15, 75, 165),(60, 160, 240),(80, 180, 250),(130, 210, 255), (160, 240, 255),(200, 250, 255),(255, 255, 255),(255, 255, 255),(255, 232, 120),(255, 192, 60),(255, 160, 0), (255, 96, 0),(255, 50, 0),(192, 0, 0),(165, 0, 0),(128, 0, 0)])
       var = colors.LinearSegmentedColormap.from_list('precip',[\
rgb_to_hex((127, 39, 4)),\
rgb_to_hex((166, 54, 3)),\
rgb_to_hex((217, 72, 1)),\
rgb_to_hex((241, 105, 19)),\
rgb_to_hex((253, 141, 60)),\
rgb_to_hex((253, 174, 107)),\
rgb_to_hex((253, 208, 162)),\
rgb_to_hex((254, 230, 206)),\
rgb_to_hex((255, 255, 255)),\
rgb_to_hex((255, 255, 255)),\
rgb_to_hex((229, 245, 224)),\
rgb_to_hex((199, 233, 192)),\
rgb_to_hex((161, 217, 155)),\
rgb_to_hex((116, 196, 118)),\
rgb_to_hex((65, 171, 93)),\
rgb_to_hex((35, 139, 69)),\
rgb_to_hex((0, 109, 44)),\
rgb_to_hex((0, 68, 27))])
       return var
   #else:
   #   raise Exception, "Your choice is not yet specified - if you have an idea: add it to the code in colors_peer.py!"
   del var,darkblue,midnightblue,blue1,blue2,turquoise,lightblue,oceanblue,mustard,saffron,cantaloupe,redwine,burgundy

#,1,2,3,4,5,6,7,8,9,10,11,12],[
#,bla,blb,\blc,bld,ble,'white',gold,'orange',darkorange,orangered,'red',darkred]]


# original temp/psl colorbar from Amy:
#rgb_to_hex(( 25, 25, 112)),\
#rgb_to_hex(( 10, 50, 120)),\
#rgb_to_hex((15, 75, 165)),\
#rgb_to_hex((60, 160, 240)),\
#rgb_to_hex((80, 180, 250)),\
#rgb_to_hex((130, 210, 255)),\
#rgb_to_hex((160, 240, 255)),\ 
#rgb_to_hex((200, 250, 255)),\
#rgb_to_hex((255, 255, 255)),\
#rgb_to_hex((255, 255, 255)),\
#rgb_to_hex((255, 232, 120)),\
#rgb_to_hex((255, 192, 60)),\
#rgb_to_hex((255, 160, 0)),\
#rgb_to_hex((255, 96, 0)),\
#rgb_to_hex((255, 50, 0)),\
#rgb_to_hex((192, 0, 0)),\
#rgb_to_hex((165, 0, 0)),\
#rgb_to_hex((128, 0, 0))])
