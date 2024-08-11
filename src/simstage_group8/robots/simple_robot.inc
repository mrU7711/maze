define laser ranger(
	sensor(
		range [0.0 5.6]
		fov 120.0
		samples 240
	)

	color "blue"
	size [0.06 0.06 0.06]

	block(
		points 4
		point[0] [0 0]
		point[1] [0 1]
		point[2] [1 1]
		point[3] [1 0]
		z [0 1]
	)
)

define simple_robot position(
	odom_error [0.03 0.03 0.00 0.05]
	localization "odom"
	size [0.6 0.4 0.2]
	gui_nose 1
	drive "diff"
	color "orange"

	# Main Body - Central Octagon
	block(
		points 8
		point[0] [0.3 0.0]
		point[1] [0.5 0.0]
		point[2] [0.6 0.1]
		point[3] [0.6 0.3]
		point[4] [0.5 0.4]
		point[5] [0.3 0.4]
		point[6] [0.2 0.3]
		point[7] [0.2 0.1]
		z [0 0.2]
		color "orange"
	)


	# Arms - Wing-like side extensions
	block(
		points 4
		point[0] [0.6 0.1]
		point[1] [0.7 0.0]
		point[2] [0.8 0.1]
		point[3] [0.7 0.2]
		z [0 0.1]
		color "blue"
	)
	block(
		points 4
		point[0] [0.6 0.3]
		point[1] [0.7 0.2]
		point[2] [0.8 0.3]
		point[3] [0.7 0.4]
		z [0 0.1]
		color "blue"
	)

	# Tail - Long, sleek rear extension
	block(
		points 4
		point[0] [0.0 0.2]
		point[1] [0.2 0.3]
		point[2] [0.2 0.1]
		point[3] [0.0 0.2]
		z [0 0.1]
		color "red"
	)

	# Laser - Repositioned within the main body
	laser(pose [0.0 0.0 0.025 0.0])
)

