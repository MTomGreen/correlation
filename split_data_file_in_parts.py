import tables
from scipy import array
from datetime import date, datetime

from get_number_of_variable_values import get_number_of_variable_values


def split_data_file_in_parts(variable, seconds):

    dat_sorted = []

    for i in range(len(variable)):

        station_ID = variable[i][2]
        with tables.openFile(variable[i][1], 'r') as data:
            tree = "data.root.s%s.%s.col('timestamp')" % (station_ID, variable[i][3])
            timestamps = eval(tree)

            tree = "data.root.s%s.%s.col('%s')" % (station_ID, variable[i][3], variable[i][0])
            var_data = eval(tree)

        list = []
        number_of_plates = get_number_of_variable_values(var_data)

        if number_of_plates == 4:
            list = zip(var_data[:, 0].tolist(), var_data[:, 1].tolist(), var_data[:, 2].tolist(), var_data[:, 3].tolist())
        elif number_of_plates == 2:
            list = zip(var_data[:, 0].tolist(), var_data[:, 2].tolist())
        elif number_of_plates == 1:
            list = var_data.tolist()
        else:
            print 'weird!'
        del var_data

        dat_sorted_part = sorted(zip(timestamps, list))
        dat_sorted.extend(dat_sorted_part)

    begin = dat_sorted[0][0] # set begin equal to first timestamp e.g. 1323302400

    # make list with the index of every first of every time interval of seconds (e.g. every hour if 'seconds' = 86400)

    time_interval_list = []

    for i in range(len(dat_sorted)):
        if dat_sorted[i][0] >= begin:
            time_interval_list.append(i)

            begin = dat_sorted[i][0] - (dat_sorted[i][0] - begin) + seconds # kijk hier nog even naar
    # e.g. begin = 1323302400 - (1323302400  - 1323302400) + 86400 = 1323302400 - 0 + 86400 = 1323388800
    # e.g. begin = 1323388804 - (1323388804  - 1323388800) + 86400 = 1323388804 - 4 + 86400 = 1323475200
    # e.g. begin = 1323475200 - (1323475200  - 1323475200) + 86400 = 1323475200 - 0 + 86400 = 1323561600
    # e.g. begin = 1323561601 - (1323561601  - 1323561600) + 86400 = 1323561601 - 1 + 86400 = 1323648000 etc.

    # make list with the timestamps in the middle of every time interval (for later use in plot)
    times_timestamp = [dat_sorted[0][0] + (seconds / 2) + i * seconds
                       for i in range(len(time_interval_list))]

    # e.g. time_interval_list = [1000000000, 1000001000, 100002000, 1000003000, 1000004000]
    # e.g seconds = 1000

    # e.g. times_timestamp = 1000000000 + 1000/2 + 0*1000 = 1000000000 + 500 + 0    = 1000000500
    # e.g. times_timestamp = 1000000000 + 500    + 1*1000 = 1000000000 + 500 + 1000 = 1000001500
    # e.g. times_timestamp = 1000000000 + 500    + 2*1000 = 1000000000 + 500 + 2000 = 1000002500 etc.

    # split data list (timestamp, variable) into n chunks each containing around n seconds of data
    time_chunks = []

    for j in range(len(time_interval_list)):
        if j != range(len(time_interval_list))[-1]:
            time_chunks.append(dat_sorted[time_interval_list[j]:time_interval_list[j + 1]])
        else:
            time_chunks.append(dat_sorted[time_interval_list[j]:len(dat_sorted)])

    del time_interval_list

    variable_list_in_n_parts = [] # e.g. list containing n days of part_plist

    for day in time_chunks:
        # e,g, list with pulseheights of n plates (timestamps removed)
        list_with_pulseheights = [i[1] for i in day]
        variable_list_in_n_parts.append(array(list_with_pulseheights))

    return variable_list_in_n_parts, times_timestamp, number_of_plates


if __name__=="__main__":
    variable = [('pulseheights', 'data_s501_2011,12,8_2011,12,12.h5', '501', 'events')]
    #variable = [('integrals','data_s501_2011,12,7_2011,12,8.h5','501','events','')]
    #variable = [('pulseheights','data_s501_2011,12,7_2011,12,8.h5','501','events'),('pulseheights','data_s501_2011,12,8_2011,12,9.h5','501','events')]

    #variable = [('barometer','data_s501_2011,12,7_2011,12,8.h5','501','weather','')]
    seconds = 86400

    list, times = split_data_file_in_parts(variable, seconds)
