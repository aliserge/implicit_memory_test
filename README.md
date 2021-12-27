
# Implicit memory test

The application 


## Licence
This program is licensed under GNU GPLv3 licence: https://www.gnu.org/licenses/gpl.html

# Installation 
The software is written using Python language version 3.
In addition to main Python package, it uses the following Python modules:

* PyQt5 for UI.
* pandas for data analysis.

Both for Windows and Linux users I recommend using precompiled bundles available at: https://drive.google.com/drive/folders/1T7a5yPCZ_EtZPkDqLkil7dvPMXQ7TyHp?usp=sharing

## Manual installation

Alternatively one can install python and all required packages manually. 
The same way should work for Mac also. 
However, the application was not tested on Mac.

### Installing python packages 
Execute the following commands from your Conda shell

    pip install pyqt5 
    pip install pandas


## The main program installation
Just checkout from master branch.

`git clone https://github.com/aliserge/implicit_memory_test.git`

Then navigate to program base folder and start.

# Usage

Unzip the archive "dist.zip". Then you have the folder "dist" that contents "SRT_visual" and "SRT_audial". They are to programs: test (visual) and re-test (audial). Go to the "SRT_visual". You will see a lot of folders, archives and files. Please ensure that the folder "sounds" and the file "config.ini" are presented there. If not, please download them from Google Drive and put into the "SRT_visual" folder. 

After that please find the file "SRT_visual" and run it (with double click). The OS will ask you what should it do with this file - so choose the option "Run". If everything is OK, you will see the fullscreen program window with two text lines: "Name" and "Date of birth". After filling this information, click on the button "Start". You will see the warning window with message which describes the test rules. Click "Ok" to start testing. 

Since the testing is over, you will see the window with message again. Now it says: "The testing is ended. Thank you!" Click "Ok" to continue.

When you click "Ok", the program closes. Now you can find the result files in the folder "SRT_visual": "Users_to hash", "res_unreadable_sequence.tsv", "res_the_same_unreadable_sequence.tsv.proc.tsv". Users_to_hash file has a list of one-to-one matches between input user data (name and date of birth) and hash sequence. So here you can find which _unreadable_sequence_ you should find in files which start with "res_". After you found it, you can roll the folder and find your raw results (res_hash_sequence.tsv) and proceeded results (res_hash_sequence.tsv.proc.tsv). Both files can be opened with Microsoft Excel (or LibreOffice Calc). Also you can open them with any text notebook. 

You can also try to run the "SRT_audial" in the equal way. Just read the "Usage" from the very beginning and replace "SRT_visual" to "SRT_audial".

### Output data

Inside the raw results file you can see a table with columns "Sequence", "Position", "Right_answer", "User_answer", "Correctness", "Start_time", "Stop_time", "RT". 

In the column "Sequence" you can see "A" or "B", where A means experimental (learning) sequence with large probability and B means control (unknown) sequence with small probability. 

In the column "Position" you can see numbers from 0 to 11. Each number means the position (counted from zero) in the sequence. 

In the column "Right_answer" you can see the key which was excpected to be tipped.

In the column "User_answer" you can see the key which was pressed by participant.

In the column "Correctness" you can see if "Right_answer" and "User_answer" are equal (True) or not (False).

In the column "Start_time" you can see the time when the red square was shown.

In the column "Stop_time" you can see the time when the button was pressed.

In the column "RT" you can see the "Start_time" - "Stop_time" delta.


Inside the proceeded results file you can see a table with columns "Sequence", "Position", "Right_answer", "User_answer", "Correctness", "Start_time", "Stop_time", "RT", "Normilized_RT" and "ReactionRatio_to_latest_control".

The columns "Sequence", "Position", "Right_answer", "User_answer", "Correctness", "Start_time", "Stop_time", "RT" are equal to the raw results file' ones.

You can pay your attention to the fact of that only True in the column "Correctness" are presented. For now we calculate statistics only for correct answers. But of course, we always have all the mistakes in the raw results file.

In the column "Normilized_RT" you can see RT that was normilized by average RT for both (experimental and control) sequences throug the whole experiment.

In the column "ReactionRatio_to_latest_control" you can see this ratio: (RT from sequence A)/(RT of the latest equal button from sequence B). It is equal to -1 when there is no previous equal button from sequence B (i.e. in first rows 
where we show only sequence A to the participant in order to let him remember it).

### Config settings

You can also change experimental settings using the file "Config.ini". It is presented in the folders "SRT_audial" and "SRT_visual" and these files are separated, so if you want to change settings in both experiments you have to transfer new settings to the both config files. 

In the config file you can see variables: repeats, change_seq_chance, numbers_to_learn, max_stay_in_control, answer_delay, seq_a and seq_b. 

_repeats_ means how many elements from the both sequences will be shown during the experiment. It includes the "training part" and the "testing part"

_change_seq_chance_ means the probability of second-order transitions (from A to B) in percents. If it is 0, you always are in the experimental sequence.

_numbers_to_learn_ means how many elements from the sequence A will be shown to the participant before it will become possible to make any second-order transitions.

_max_stay_in_control_ means how many elements from the sequence B can be shown in a row before the program makes the forced second-order transition from B to A.

_answer_delay_ means how much time would pass after the button was pressed before the next element was shown (in ms; this customisation are not available now, I will implement it later; if you need it now, write me, I will help).

_seq_a_ is the sequence with high probability. (ALWAYS 12 ELEMENTS)

_seq_b_ is the sequence with low probability. (ALWAYS 12 ELEMENTS)

In case you want to customise the config settings you should change the variables you need and than save the config file. After that you can run the program in a usual way.
