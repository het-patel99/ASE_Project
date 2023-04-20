import os
import subprocess

# Create out directory if it does not exist
if not os.path.exists("../out"):
    os.makedirs("../out")

current_dir = os.getcwd() 
print(current_dir)
# Change to src directory
os.chdir("src")

# Loop through all files in the data directory
for file in os.listdir("etc/data"):
    if file.endswith(".csv"):
        print("Processing", file)
        # Run main.py with the csv name, and save output to out/csv_name.out
        data_file = os.path.join("..", "data", file)
        print("here")
        print(current_dir)
        output_file = os.path.join("..", "out", os.path.splitext(file)[0] + ".out")
        command = "time python3 main.py -f {} --color false > {} 2>&1".format(
            data_file, output_file
        )
        subprocess.run(command, shell=True)

# Change back to the previous directory
os.chdir("..")