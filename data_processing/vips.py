import pyvips


image_left = pyvips.Image.new_from_file('images/100001747275.jpg')
image_center = pyvips.Image.new_from_file('images/100001747271.jpg')
image_right = pyvips.Image.new_from_file('images/100001747272.jpg')

concat_image = image_left.mosaic(image_center, "horizontal", image_left.width, 0, 50, 0)
concat_image = image_left.merge(image_center, 'horizontal', -image_left.width, 0, mblend=-1)
concat_image = concat_image.globalbalance()
concat_image.write_to_file('images/output.tif')


images = [image_left, image_center]
concat_image = pyvips.Image.arrayjoin(images, across=100)
concat_image.write_to_file('images/join_image.tif')

