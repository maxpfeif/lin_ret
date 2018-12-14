# Reverse Engineering Tools for LIN Logs 

lin_ret contains reverse engineering tools for filtering and plotting LIN data by PID and Byte. 

The plotting and filtration tools require a .csv file with the format "TIME, PID, DATA" as the first 
input argument, with additional aruments to specify filter and plot parameters. 

lin_ret was designed around analyzing Saleae Logic output files, and contains a .csv conversion script, 
logic_lin, which conerts the rather unweildy .csv output from Logic to the "TIME, PID, DATA" format. 

To process Saleae Logic logs, simply setup the LIN analyzer to decode your bus, making sure that the Display Radix setting is set to Hex in Analyzer Settings, take a log and save the output using the 'export search results' command on the Decoded Protocols menu. 

The resulting .csv file can be converted by calling ```python logic_lin.py example_lin_log.csv ```

Which will produce an output.csv file with "lin_" appended to the front of the input file argument, in our case example_lin_log.csv

From here, the rest of the tools in this repository can be used, in addition to [Colorflog](https://github.com/maxpfeif/colorflog), a simple tool for adding color to logs, enabling visual pattern recognition by ID. 

## Using lin_ret tools 

filtlin can be executed by calling ```python filtlin.py example_lin_log.csv 12``` where 12 is the id we want to filter. 

This simply prints the resulting filtered log information to the console. 

plotlin required matplotlib and can be executed by calling ```python plotlin.py example_lin_log.csv 12``` to print the cumulative 
byte data for PID 12, or can be execuded as ```python plotlin.py example_lin_log.csv 12 1``` to only plot byte 1. Extending the arguments 
to multiple bytes will produce multiple plots, one for each byte passed in the argument. For example; ```python plotlin.py example_lin_log.csv 12 0 1 2``` will produce 3 plots, saved as .png files to the working directory, and also shown in the a Python window.

