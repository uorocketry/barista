# Sandbox Simulation Manual

## Overview
The  Sandbox simulation environment simulates the rocket going through a flight
 by playing back recorded sensor values in real time with noise and logging the
  response of the rocket.

## Simulation Data Input
Simulation data is provided to the Sandbox through a csv. It should be named
 `'simulation.csv'` and it should be placed in the sandbox directory.
  The sandbox uses `pandas.read_csv()` to parse the csv into a Pandas
   `DataFrame` object. The DataFrame is further parsed into sensor-specific
    DataFrames containing a column for time in seconds and additional columns
     for relevant sensor data like acceleration or altitude.

## Sensor Modelling
The sandbox models sensors in two ways: Sandbox Sensors and Dummy sensors.


Dummy sensors return random sane sensor values when read.

Sandbox sensors return noised values from a `DataFrame` object. The `DataFrame`
 is generated using a csv from an OpenRocket simulation. It contains sensor
  values as if they had been processed by the `parse_raw_data()` function of a
   real sensor throughout a real flight, as well as timestamps associated with
    the values.

## Time
The simulation sandbox keeps track of time using the system clock and
 OpenRocket simulation data. While the simulated rocket has not taken off,
  time is only based of system time.

When the `launch` command is given, the instance of `Sandbox` saves the time as
 given by `time()` to the `launch_time` variable. The saved value will serve as
  a reference point for the values read from the OpenRocket `DataFrame`.

When the `read()` function of a sandbox sensor is called, it saves the system
 time `time()` to the variable `sample_time`. This is will be the time logged
  as the time the sensor was read. `sample_time-launch_time` gives the number
   of seconds that have passed since launch, and is the time value to be read
    from the simulation `DataFrame`. If no exact time match exists in the
     `DataFrame` the next greatest one is chosen.
