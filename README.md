This is Anish Chhabra's attempt at the 2024 sw cardinal original fall challenge. 

Taking the tick files of all trades that happened for the fictional CTG stock on 9/16, reading and analyzing the data to create OHLCV files partitioned by the users own time input.

The python code is in the file Completed_swe_loader_challenge_Anish_C.py. And an example of it's output when given the command 20m which would be 20 minutes is in the example csv file OHLCV_output20m.csv
To run the data interface, run the python code, and input a time string(without spaces and using s for seconds , m for minutes, h for hours). You may have to change the directory path variable if running locally. The directory path variable was made based on my local repo.


Some of my struggles
Errors in the csv files: The errors I quickly noticed were empty inputs and negative (impossible) values for the price and size of the stock. These were obviously false so I took out all data that was found like this.
I also found duplicates within the data, any duplicates  were identified using a set and removed.
I also had an issue with malformed data, where it wouldn't parse into an int or a double sometimes, I am not too sure about the actual error this meant, however I simply just passed an exception to pass any rows like that. This may affect the accuracy of the data somewhat if there was some other reason for the data not converting.



I did not have much experience with the built in csv functions and csv files in general, I have used pandas before, however that is an external library. Almost all csv commands I had to search up and learn.
I also had to use a timedelta variable to take user input, as I found it easier to convert the times that the user inputed, especially when using multiple different units (ex: 2h30m).

What I could have done better:
Instead of taking out data such as duplicate values empty inputs I could assess the context within the duplicates and missing values to attempt to save some of these data, by either combining duplicates and taking the average price or using the tick that came first. 
