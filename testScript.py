import os
import subprocess

# Create out directory if it does not exist
if not os.path.exists("../out"):
    os.makedirs("../out")

# Get the current directory
current_dir = os.getcwd()
current_dir = current_dir + "/etc/data"
# Change to src directory
os.chdir("src")

# Loop through all files in the data directory
for file in os.listdir(os.path.join(current_dir)):
    if file.endswith(".csv"):
        print("running... ", file)
        # Run main.py with the csv name, and save output to out/csv_name.out
        data_file = os.path.join(current_dir, "../data", file)
        output_file = os.path.join(current_dir, "../out", os.path.splitext(file)[0] + ".out")
        command = "time python3 main.py -f {} --color false > {} 2>&1".format(
            data_file, output_file
        )
        subprocess.run(command, shell=True)

# Change back to the previous directory
os.chdir(current_dir)
