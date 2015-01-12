

#   ____________________________________________
#   |                                          |
#   |  Technik Autonomer Systeme -TUM          |
#   |  Gruppe 09                               |
#   |                                          |
#   |  erstellt: WS 2014/2015 - (c) Tim Stahl  |
#   |__________________________________________|

import math
import numpy
import matplotlib.pyplot as plt

if __name__ == '__main__':

	# Parameters (insert scandata or manual scanpattern)
	increment = 0.004363
	angle_min = -1.570796
	ranges =(0.558000,0.557000,0.557000,0.556000,0.556000,0.554000,0.556000,0.554000,0.554000,0.548000,0.548000,0.548000,0.555000,0.555000,0.555000,0.556000,0.556000,0.553000,0.553000,0.553000,0.552000,0.552000,0.550000,0.550000,0.550000,0.551000,0.552000,0.552000,0.552000,0.552000,0.551000,0.547000,0.546000,0.546000,0.543000,0.546000,0.546000,0.547000,0.550000,0.554000,0.550000,0.550000,0.546000,0.546000,0.546000,0.546000,0.546000,0.553000,0.553000,0.547000,0.545000,0.547000,0.545000,0.547000,0.547000,0.547000,0.547000,0.547000,0.547000,0.555000,0.555000,0.555000,0.553000,0.553000,0.553000,0.559000,0.562000,0.562000,0.559000,0.559000,0.555000,0.555000,0.559000,0.566000,0.566000,0.566000,0.559000,0.558000,0.558000,0.559000,0.563000,0.563000,0.563000,0.563000,0.560000,0.560000,0.560000,0.572000,0.572000,0.572000,0.570000,0.570000,0.559000,0.568000,0.568000,0.568000,0.562000,0.568000,0.568000,0.568000,0.565000,0.565000,0.563000,0.563000,0.563000,0.569000,0.573000,0.573000,0.573000,0.574000,0.577000,0.581000,0.581000,0.580000,0.577000,0.580000,0.580000,0.577000,0.582000,0.582000,0.579000,0.579000,0.584000,0.584000,0.584000,0.586000,0.588000,0.588000,0.589000,0.590000,0.596000,0.596000,0.596000,0.596000,0.598000,0.592000,0.600000,0.600000,0.592000,0.592000,0.603000,0.605000,0.606000,0.610000,0.610000,0.610000,0.612000,0.612000,0.615000,0.615000,0.612000,0.610000,0.610000,0.610000,0.619000,0.619000,0.619000,0.620000,0.619000,0.620000,0.620000,0.632000,0.633000,0.634000,0.633000,0.632000,0.634000,0.634000,0.646000,0.651000,0.653000,0.653000,0.653000,0.654000,0.654000,0.654000,0.661000,0.662000,0.664000,0.665000,0.666000,0.666000,0.666000,0.666000,0.667000,0.674000,0.676000,0.684000,0.684000,0.685000,0.685000,0.685000,0.685000,0.686000,0.690000,0.697000,0.697000,0.704000,0.707000,0.707000,0.707000,0.707000,0.704000,0.704000,0.704000,0.712000,0.718000,0.730000,0.730000,0.730000,0.731000,0.733000,0.733000,0.745000,0.745000,0.746000,0.746000,0.741000,0.735000,0.732000,0.732000,0.728000,0.728000,0.728000,0.729000,0.727000,0.729000,0.727000,0.730000,0.726000,0.723000,0.723000,0.723000,0.723000,0.723000,0.730000,0.801000,2.513000,2.513000,2.513000,2.502000,2.486000,2.474000,2.465000,2.458000,2.437000,2.430000,2.429000,2.427000,2.424000,2.413000,2.395000,2.395000,2.392000,2.390000,2.387000,2.387000,2.373000,2.370000,2.370000,2.369000,2.363000,2.361000,2.361000,2.361000,2.360000,2.360000,2.361000,2.364000,2.365000,2.366000,2.366000,2.366000,2.366000,2.366000,2.301000,2.181000,2.161000,2.152000,2.148000,2.136000,2.132000,2.126000,2.126000,2.118000,2.118000,2.105000,2.105000,2.104000,2.102000,2.101000,2.085000,2.078000,2.075000,2.072000,2.066000,2.063000,2.054000,2.053000,2.050000,2.045000,2.030000,2.024000,1.869000,1.752000,1.714000,1.690000,1.683000,1.660000,1.657000,1.657000,1.656000,1.651000,1.648000,1.637000,1.635000,1.634000,1.634000,1.633000,1.633000,1.623000,1.621000,1.618000,1.618000,1.615000,1.615000,1.610000,1.609000,1.609000,1.610000,1.630000,1.712000,1.791000,1.811000,1.827000,1.861000,1.897000,1.926000,1.967000,1.984000,2.010000,2.049000,2.076000,2.118000,2.150000,2.192000,2.223000,2.275000,2.310000,2.348000,2.392000,2.441000,2.486000,2.537000,2.589000,2.643000,2.705000,2.754000,2.808000,2.881000,2.938000,3.016000,3.090000,3.181000,3.278000,3.355000,3.420000,3.527000,3.638000,3.767000,3.879000,3.899000,3.902000,3.904000,3.904000,3.904000,3.905000,3.906000,3.905000,3.906000,3.906000,3.919000,3.948000,4.038000,4.175000,4.265000,7.652000,7.828000,8.833000,8.833000,8.845000,11.366000,11.408000,11.427000,11.438000,11.444000,11.504000,14.151000,14.151000,float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),float("inf"),17.959000,17.981001,17.981001,17.9336000,17.9336000,17.9336000,14.170000,14.170000,14.170000,14.053000,13.392000,13.372000,13.372000,13.393000,13.393000,13.406000,13.406000,13.406000,13.406000,12.028000,12.010000,12.010000,12.014000,12.019000,12.036000,12.036000,float("inf"),float("inf"),float("inf"),float("inf"),8.046000,8.046000,7.849000,7.617000,7.465000,7.217000,7.003000,6.892000,6.781000,6.636000,6.495000,6.353000,6.282000,4.496000,4.496000,4.496000,5.673000,5.673000,5.570000,5.464000,5.357000,5.262000,5.183000,5.121000,5.018000,4.933000,4.862000,4.776000,4.704000,4.633000,4.600000,4.599000,4.599000,4.599000,4.614000,4.626000,4.632000,4.632000,4.632000,2.932000,2.924000,2.924000,2.924000,2.952000,4.688000,4.690000,4.698000,4.698000,4.698000,4.698000,4.696000,4.687000,4.672000,4.632000,4.577000,4.533000,4.472000,4.437000,4.407000,4.347000,4.305000,4.265000,4.218000,4.193000,4.148000,4.097000,4.072000,4.017000,3.990000,3.959000,3.931000,3.898000,3.861000,3.829000,3.795000,3.762000,3.745000,3.721000,3.688000,3.640000,3.621000,3.581000,3.561000,3.529000,3.511000,3.476000,3.450000,3.437000,3.410000,3.379000,3.370000,3.261000,3.260000,3.248000,3.248000,3.242000,3.231000,3.202000,3.181000,3.144000,3.134000,3.117000,3.093000,3.084000,3.062000,3.047000,3.028000,2.992000,2.988000,2.965000,2.946000,2.935000,2.930000,2.906000,2.884000,2.873000,1.547000,1.517000,1.516000,1.516000,1.526000,1.516000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.614000,2.620000,2.620000,2.614000,2.606000,2.594000,2.582000,2.556000,2.546000,2.536000,2.528000,2.523000,2.522000,2.506000,2.492000,2.472000,2.456000,2.451000,2.447000,2.435000,2.422000,2.422000,2.419000,2.405000,2.391000,2.382000,2.367000,2.366000,2.349000,2.341000,2.334000,2.318000,2.315000,2.307000,2.301000,2.292000,2.282000,2.276000,2.274000,2.260000,2.254000,2.237000,2.232000,2.224000,2.218000,2.204000,2.202000,2.185000,2.185000,2.183000,2.182000,2.178000,2.172000,2.162000,2.138000,2.106000,2.106000,2.106000,2.106000,2.088000,2.091000,2.091000,2.091000,2.091000,2.091000,2.088000,2.081000,2.079000,2.076000,2.070000,2.066000,2.043000,2.043000,2.043000,2.042000,2.042000,2.026000,2.022000,2.022000,2.020000,2.016000,2.011000,2.007000,1.990000,1.990000,1.988000,1.985000,1.985000,1.980000,1.972000,1.966000,1.962000,1.962000,1.954000,1.952000,1.950000,1.944000,1.939000,1.939000,1.935000,1.935000,1.924000,1.920000,1.920000,1.919000,1.919000,1.914000,1.914000,1.906000,1.895000,1.895000,1.894000,1.893000,1.891000,1.883000,1.875000,1.874000,1.872000,1.871000,1.866000,1.865000,1.859000,1.856000,1.853000,1.852000,1.850000,1.845000,1.842000,1.837000,1.842000,1.836000,1.830000,1.833000,1.833000,1.830000,1.828000,1.820000,1.819000,1.819000,1.819000,1.819000,1.819000,1.819000,1.818000,1.812000,1.806000,1.803000,1.800000,1.795000,1.793000,1.793000)
	
	# Waypoints (insert generated or manual waypoints)
	waypoints_x = (1.772260697508826, 2.6211725477347123,3.317584687671193,4.0139968276076736,4.86290867783356,5.7118205280594472, 6.408232667995928)
	waypoints_y = (1.2898021370145685, 1.0471766273000218,1.5898815183478852, 2.1325864093957483,1.8899608996812014,1.6473353899666545,2.190040281014518)
	
	# Variables
	datapoints_x = []
	datapoints_y = []
	
	# Calculate Plot Datapoints
	i = 0
	while i<len(ranges):
		
		# Skip inf values
		if ranges[i] < 99:		
			datapoints_x.append(math.cos(angle_min + increment * i) * ranges[i])
			datapoints_y.append(math.sin(angle_min + increment * i) * ranges[i])
			
		i += 1
		
	plt.plot(datapoints_x, datapoints_y, 'ro')
	plt.plot(waypoints_x, waypoints_y, 'g^')
	
	plt.show()
