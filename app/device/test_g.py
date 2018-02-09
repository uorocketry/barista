import gyro

g = gyro.Gyro()
g.read()
g.display_data(g.readable())
