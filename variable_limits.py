""" These limits define acceptable values for the variables """

low_limit = {"temp_inside": -200,
             "temp_outside": -200,
             "humidity_inside": 0,
             "humidity_outside": 0,
             "barometer": 700,
             "wind_dir": 0,
             "wind_speed": 0,
             "solar_rad": 0,
             "uv": 0,
             "evapotranspiration": 0,
             "rain_rate": 0,
             "heat_index": -200,
             "dew_point": -200,
             "wind_chill": -200,
             "pulseheights": 0,
             "integrals": 0,
             "event_rate": 0}


high_limit = {"temp_inside": 200,
              "temp_outside": 200,
              "humidity_inside": 100,
              "humidity_outside": 100,
              "barometer": 1200,
              "wind_dir": 360,
              "wind_speed": 500,
              "solar_rad": 1500,
              "uv": 50,
              "evapotranspiration": 1000,
              "rain_rate": 1000,
              "heat_index": 200,
              "dew_point": 200,
              "wind_chill": 200,
              "pulseheights": 25000,
              "integrals": 1000000000,
              "event_rate": 3.5}