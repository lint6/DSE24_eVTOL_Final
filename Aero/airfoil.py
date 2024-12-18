import numpy as np

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

    def interpolate_cl_cd(self, alpha_input):
        """Interpolates CL and CD values for a given alpha_input using linear interpolation."""
        # Convert alpha, CL, and CD to numpy arrays for easier interpolation
        alpha_array = np.array(self.alpha)
        CL_array = np.array(self.CL)
        CD_array = np.array(self.CD)
        
        # Check if alpha_input is within the range of available alpha values
        if alpha_input < alpha_array[0] or alpha_input > alpha_array[-1]:
            print("Warning: alpha_input is out of the range of available alpha values.")
            return None, None  # Return None if out of range
        
        # Perform linear interpolation to find CL and CD for the exact alpha_input
        CL_interp = np.interp(alpha_input, alpha_array, CL_array)
        CD_interp = np.interp(alpha_input, alpha_array, CD_array)
        
        return CL_interp, CD_interp

# Example usage to find interpolated CL and CD for a given alpha value
if __name__ == "__main__":
    # Initialize the AirfoilData object
    airfoil_data = AirfoilData()
    
    # Input alpha value for which we want to find the corresponding CL and CD
    alpha_input = 5.2  # Example: replace with your desired alpha value
    
    # Interpolate CL and CD for the given alpha input
    interpolated_CL, interpolated_CD = airfoil_data.interpolate_cl_cd(alpha_input)
    
    # Print the results
    if interpolated_CL is not None and interpolated_CD is not None:
        print(f"Interpolated CL: {interpolated_CL}, Interpolated CD: {interpolated_CD}")
