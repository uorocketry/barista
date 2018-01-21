import altimeter

alt = altimeter.Altimeter()

input = raw_input("Enter barometric setting: \n")
alt.write_bar_setting(input)
for x in range(10):
	print("Temp:\t" + str(alt.temp()))
	print("Altitude:\t" +str(alt.altitude()))
