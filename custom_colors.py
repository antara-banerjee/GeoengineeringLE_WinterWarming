'''
Define own colormaps.
'''

import matplotlib.colors as colors

#*********************************************************************************
def rgb_to_hex(rgb):

    return '#%02x%02x%02x' % rgb

#*********************************************************************************
def custom_colors(word):	 

   if word == 'BlueRed':
      var = colors.LinearSegmentedColormap.from_list(word,[\
      rgb_to_hex(( 25, 25, 112)),\
      rgb_to_hex(( 10, 50, 120)),\
      rgb_to_hex((15, 75, 165)),\
      rgb_to_hex((60, 160, 240)),\
      rgb_to_hex((80, 180, 250)),\
      rgb_to_hex((130, 210, 255)),\
      rgb_to_hex((160, 225, 255)),\
      rgb_to_hex((255, 255, 255)),\
      rgb_to_hex((255, 255, 255)),\
      rgb_to_hex((255, 232, 90)),\
      rgb_to_hex((255, 160, 0)),\
      rgb_to_hex((255, 96, 0)),\
      rgb_to_hex((255, 50, 0)),\
      rgb_to_hex((192, 0, 0)),\
      rgb_to_hex((165, 0, 0)),\
      rgb_to_hex((128, 0, 0))])
      return var
   elif word == 'BrownGreen':
      var = colors.LinearSegmentedColormap.from_list(word,[\
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

#********************************************************************************************************
# END
#********************************************************************************************************
