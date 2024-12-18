# for a given file with csv data of the airfoil at a certain Reynolds number
# the code below will load the data and find the closest CL and CD values for a given alpha value
# this is used in calculating power_hover in PERFORMANCE/powers.py

class AirfoilData:
    def __init__(self):
        # Define the filename
        self.filename = r'C:\\Users\\Jan\\Documents\\GitHub\\DSE24_eVTOL_Final\\Aero\\xf-n0012-il-500000.csv'
        
        # Initialize lists to store the data
        self.alpha = []
        self.CL = []
        self.CD = []
        self.CDp = []
        self.CM = []
        self.top_xtr = []
        self.bot_xtr = []
        
        # Load the airfoil data upon initialization
        self.load_airfoil_data()

    def load_airfoil_data(self):
        """Loads airfoil data from the provided CSV file."""
        try:
            with open(self.filename, 'r') as file:
                # Skip the first few lines if necessary (e.g., skip headers and any non-data lines)
                for _ in range(9):  # Skip the first nine lines (adjust if needed)
                    next(file)
                
                for line in file:
                    # Split the line into parts and make sure it's valid for conversion to float
                    parts = line.split(',')
                    if len(parts) == 7:  # Check if the line contains the expected number of columns
                        try:
                            self.alpha.append(float(parts[0]))
                            self.CL.append(float(parts[1]))
                            self.CD.append(float(parts[2]))
                            self.CDp.append(float(parts[3]))
                            self.CM.append(float(parts[4]))
                            self.top_xtr.append(float(parts[5]))
                            self.bot_xtr.append(float(parts[6]))
                        except ValueError:
                            # If there's a non-numeric value, handle it (e.g., skip that line)
                            print(f"Skipping invalid line: {line}")
        except FileNotFoundError:
            print(f"Error: The file {self.filename} was not found.")

    def find_cl_cd_for_alpha(self, alpha_input):
        """Finds the closest CL and CD values for the given alpha_input."""
        # Find the index of the closest alpha value to the input
        closest_index = min(range(len(self.alpha)), key=lambda i: abs(self.alpha[i] - alpha_input))
        
        # Return the corresponding CL and CD for the closest alpha
        closest_CL = self.CL[closest_index]
        closest_CD = self.CD[closest_index]
        
        return closest_CL, closest_CD

# Example usage to find CL and CD for a given alpha value
if __name__ == "__main__":
    # Initialize the AirfoilData object
    airfoil_data = AirfoilData()
    
    # Input alpha value for which we want to find the corresponding CL and CD
    alpha_input = 5.0  # Example: replace with your desired alpha value
    
    # Find the closest CL and CD for the given alpha input
    closest_CL, closest_CD = airfoil_data.find_cl_cd_for_alpha(alpha_input)
    
    # Print the results
    print(airfoil_data.find_cl_cd_for_alpha(alpha_input)[0])
