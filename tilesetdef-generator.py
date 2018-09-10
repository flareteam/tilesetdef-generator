#!/usr/bin/python2
import os, sys
import xml.etree.ElementTree as ET

def main():
	tileset_w = 0
	tileset_h = 0
	start_index = 0
	end_index = 1
	image_path_prefix = "images/tilesets/"

	# returns a formated line defining a tile
	def getTile(index, w, h, off_x, off_y):
		tiles_per_row = tileset_w / w
		true_index = index - start_index
		left_x = (true_index % tiles_per_row) * w
		top_y = (true_index / tiles_per_row) * h
		offset_x = (map_w / 2) - off_x
		offset_y = h - (map_h /2) - off_y
		return "tile=%d,%d,%d,%d,%d,%d,%d\n" % (index,left_x,top_y,w,h,offset_x,offset_y)

	# load the TMX file
	tiled_file = ""
	for opt in sys.argv:
		if (opt ==  sys.argv[0]):
			continue
		if (os.path.isfile(opt)):
			tiled_file = opt
			break

	if (tiled_file == ""):
		print "No Tiled TMX file specified"
		return

	parser = ET.parse(tiled_file)
	root = parser.getroot()

	# get the overall tilesize
	map_w = int(root.get('tilewidth'))
	map_h = int(root.get('tileheight'))

	# get the tileset filename
	map_name = "output"
	for prop in root.find('properties').findall('property'):
		if (prop.get('name') == "tileset"):
			map_name = os.path.basename(os.path.splitext(prop.get('value'))[0])
	map_name += ".txt"

	# create the tilesetdef file
	map_file = open(map_name,'w')

	# add the tileset filename
	map_file.write("# %s\n\n" % (map_name))

	# add each tile
	for tileset in root.findall('tileset'):
		tile_w = int(tileset.get('tilewidth'))
		tile_h = int(tileset.get('tileheight'))
		tileset_name = tileset.get('name')

		tileset_w = 0
		tileset_h = 0
		image = tileset.find('image')
		tileset_image = image_path_prefix + os.path.split(image.get('source'))[1]
		tileset_w = int(image.get('width'))
		tileset_h = int(image.get('height'))

		tileoffset_x = 0
		tileoffset_y = 0
		tileoffset = tileset.find('tileoffset')
		if (tileoffset != None):
			tileoffset_x = int(tileoffset.get('x'))
			tileoffset_y = int(tileoffset.get('y'))

		start_index = end_index

		# TODO use tilecount?
		end_index += (tileset_w/tile_w) * (tileset_h/tile_h)

		if (tileset_name != "collision" and tileset_name != "set_rules"):
			map_file.write("# " + tileset_name + "\n")
			map_file.write("[tileset]\n")
			map_file.write("img=%s\n\n" % (tileset_image))

			for i in range(start_index,end_index):
				map_file.write(getTile(i, tile_w, tile_h, tileoffset_x, tileoffset_y))

			map_file.write("\n\n")

	map_file.close()

if __name__ == "__main__":
	main()
