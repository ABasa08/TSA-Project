# Import necessary libraries and modules
from flask import Flask, render_template, request, redirect, url_for  # Flask framework and utilities
import os  # Operating system interfaces
import random  # Generate random numbers
import numpy as np  # Numerical operations
import pandas as pd  # Data manipulation and analysis
from sklearn.linear_model import LinearRegression  # Linear regression model
from sklearn.metrics import mean_squared_error  # Evaluation metric
import matplotlib  # Plotting library
matplotlib.use('Agg')  # Use non-interactive backend for web compatibility
import matplotlib.pyplot as plt  # Plotting interface
import seaborn as sns  # Statistical data visualization
from rich.console import Console  # Rich library for enhanced console output
from rich.table import Table  # Rich library for table formatting
from rich.panel import Panel  # Rich library for panel formatting

# Initialize the Flask application
app = Flask(__name__)

# Historical Data Section
# This section contains environmental details for different crops
historical_data = {
    "wheat": {
        "yield": [300, 320, 290, 310, 315],  # Yield data over years
        "water_use": [400, 380, 410, 395, 405],  # Water usage data
        "fertilizer": [50, 55, 48, 53, 54],  # Fertilizer usage data
    },
    "corn": {
        "yield": [500, 520, 480, 510, 505],
        "water_use": [600, 590, 620, 605, 615],
        "fertilizer": [70, 75, 68, 72, 74],
    },
    "soy": {
        "yield": [250, 265, 240, 255, 260],
        "water_use": [350, 340, 360, 355, 345],
        "fertilizer": [40, 42, 38, 41, 39],
    },
    "rice": {
        "yield": [400, 420, 390, 410, 405],
        "water_use": [500, 490, 510, 505, 495],
        "fertilizer": [60, 65, 58, 62, 63],
    },
}

# Regional Data Section
# This section contains water-related data for different regions
regional_data = {
    "north": {
        "rainfall": 1000,  # Annual rainfall in mm
        "climate": "temperate",  # Climate type
        "avg_temp": 15,  # Average temperature in °C
        "seasonal_variation": [200, 300, 250, 250]  # Rainfall distribution across seasons
    },
    "south": {
        "rainfall": 500,
        "climate": "arid",
        "avg_temp": 28,
        "seasonal_variation": [100, 120, 130, 150]
    },
    "east": {
        "rainfall": 800,
        "climate": "humid",
        "avg_temp": 20,
        "seasonal_variation": [210, 220, 190, 180]
    },
    "west": {
        "rainfall": 600,
        "climate": "semi-arid",
        "avg_temp": 22,
        "seasonal_variation": [150, 160, 145, 145]
    },
}

# Directory for static visualizations (graphs will be saved here)
visuals_dir = os.path.join('static', 'visuals')  # Define the path for saving visualizations
if not os.path.exists(visuals_dir):  # Check if the directory exists
    os.makedirs(visuals_dir)  # Create the directory if it doesn't exist

# Feature 1: Crop Efficiency Planner
def crop_efficiency_web(crop_type, soil_quality, farm_size, fertilizer_level, irrigation_eff):
    # Create a new Console instance for this request
    console = Console(record=True)
    console.print(Panel("[bold blue]Advanced Crop Efficiency Planner[/bold blue]"))  # Display header panel
    try:
        # Check if the crop type exists in historical data
        if crop_type.lower() not in historical_data:
            available_crops = ', '.join(historical_data.keys())  # List available crops
            console.print(f"[red]Error: Crop type '{crop_type}' not found! Available: {available_crops}[/]")  # Display error
            return console.export_html()  # Return error message as HTML

        # Retrieve historical data for the selected crop
        crop_hist = historical_data[crop_type.lower()]
        df = pd.DataFrame({
            "yield": crop_hist["yield"],
            "water_use": crop_hist["water_use"],
            "fertilizer": crop_hist["fertilizer"],
        })  # Create DataFrame from historical data

        # Prepare data for linear regression
        X = df[["water_use", "fertilizer"]].values  # Features: water_use and fertilizer
        X = np.hstack([X, np.full((X.shape[0], 1), soil_quality * 0.1)])  # Add soil_quality as a feature
        y = np.array(df["yield"])  # Target variable: yield

        model = LinearRegression()  # Initialize linear regression model
        model.fit(X, y)  # Fit the model to the data

        # Calculate average water usage adjusted for irrigation efficiency
        avg_water = np.mean(crop_hist["water_use"]) * (1 - (1 - irrigation_eff) * 0.02)
        avg_fert = np.mean(crop_hist["fertilizer"]) + fertilizer_level  # Calculate adjusted fertilizer
        features = np.array([[avg_water, avg_fert, soil_quality * 0.1]])  # Prepare feature array

        predicted_yield = model.predict(features)[0]  # Predict yield
        rmse = np.sqrt(mean_squared_error(y, model.predict(X)))  # Calculate RMSE
        conf_interval = (predicted_yield - 1.96 * rmse, predicted_yield + 1.96 * rmse)  # 95% confidence interval

        # Display the results using Rich
        console.print(f"[bold cyan]Optimized Planting Layout:[/bold cyan] {farm_size:.2f} acres of {crop_type.capitalize()}")
        console.print(f"[bold cyan]Predicted Yield:[/bold cyan] {predicted_yield:.2f} units")
        console.print(f"[bold cyan]95% Confidence Interval:[/bold cyan] ({conf_interval[0]:.2f}, {conf_interval[1]:.2f})")
        console.print("[bold magenta]Recommendations:[/bold magenta]")
        console.print("- Adjust fertilizer input as per soil nutrient testing.")
        console.print("- Consider micro-irrigation to boost water efficiency.")
        console.print("- Regularly update historical data for better predictions.")
    except Exception as e:
        # Handle any exceptions that occur during processing
        console.print(f"[red]An error occurred: {str(e)}[/]")

    rich_output = console.export_html()  # Export the Rich output to HTML
    console.clear()  # Clear the console after exporting
    return rich_output  # Return the HTML output

# Feature 2: Water Management Tool
def water_management_web(irrigation_method, soil_type, region):
    # Create a new Console instance for this request
    console = Console(record=True)
    console.print(Panel("[bold blue]Enhanced Water Management Tool[/bold blue]"))  # Display header panel
    try:
        # Check if the region exists in regional data
        if region.lower() not in regional_data:
            console.print(f"[red]Error: Region '{region}' not found![/]")
            return console.export_html(), None  # Return error message and no visualization

        # Define efficiency mappings
        irrigation_efficiency_map = {"drip": 0.95, "sprinkler": 0.85}  # Irrigation method efficiencies
        soil_infiltration_map = {"clay": 0.7, "loam": 0.9, "sandy": 0.8}  # Soil type infiltration rates

        irrigation_efficiency = irrigation_efficiency_map.get(irrigation_method.lower(), 0.80)  # Get irrigation efficiency
        soil_infiltration = soil_infiltration_map.get(soil_type.lower(), 0.75)  # Get soil infiltration rate

        months = list(range(1, 13))  # List of months
        monthly_rainfall = np.array(regional_data[region.lower()]["seasonal_variation"])  # Seasonal rainfall data
        if monthly_rainfall.size < 12:  # Ensure 12 months of data
            monthly_rainfall = np.tile(monthly_rainfall, int(np.ceil(12 / monthly_rainfall.size)))[:12]  # Repeat data if necessary
            monthly_rainfall += np.random.randint(-10, 10, 12)  # Add randomness to rainfall data

        water_losses = []
        for m in months:
            base_loss = random.uniform(10, 30)  # Base water loss for the month
            adjusted_loss = base_loss * (1 - irrigation_efficiency) * (1 - soil_infiltration)  # Adjust loss based on efficiencies
            water_losses.append(adjusted_loss)  # Append adjusted loss to list

        # Set up the visualization using Seaborn and Matplotlib
        sns.set_theme(style="whitegrid")
        plt.figure(figsize=(10, 6))
        plt.plot(months, monthly_rainfall, marker='o', label='Monthly Rainfall (mm)', color="#3498db")  # Plot rainfall
        plt.plot(months, water_losses, marker='s', label='Simulated Water Loss (mm)', color="#e74c3c")  # Plot water loss
        plt.title(f"Seasonal Water Usage Simulation - {region.capitalize()} Region", fontsize=16)  # Set plot title
        plt.xlabel("Month", fontsize=14)  # X-axis label
        plt.ylabel("Water (mm)", fontsize=14)  # Y-axis label
        plt.legend()  # Show legend
        plt.xticks(months)  # Set x-ticks to months
        plt.tight_layout()  # Adjust layout

        visualization_filename = f"{region.lower()}_water_simulation_enhanced.png"  # Define filename for visualization
        visualization_path = os.path.join(visuals_dir, visualization_filename)  # Define full path
        plt.savefig(visualization_path, dpi=150)  # Save the plot as a PNG file
        plt.close()  # Close the plot to free memory

        # Display the results using Rich
        console.print(f"[bold cyan]Average Monthly Rainfall:[/bold cyan] {np.mean(monthly_rainfall):.2f} mm")
        console.print(f"[bold cyan]Average Simulated Water Loss:[/bold cyan] {np.mean(water_losses):.2f} mm")
        console.print(f"[bold cyan]Visualization saved to:[/bold cyan] {visualization_path}")  # Inform user about saved visualization
        console.print("[bold magenta]Advanced Suggestions:[/bold magenta]")
        console.print("- Consider scheduling irrigation during periods with low evaporation.")
        console.print("- Upgrade to smart irrigation systems for real-time adjustments.")
        console.print("- Use weather forecast data to further fine-tune irrigation schedules.")
    except Exception as e:
        # Handle any exceptions that occur during processing
        console.print(f"[red]An error occurred: {str(e)}[/]")

    rich_output = console.export_html()  # Export the Rich output to HTML
    console.clear()  # Clear the console after exporting

    visualization_url = None  # Initialize visualization URL
    if os.path.exists(visualization_path):  # Check if the visualization file exists
        visualization_url = url_for('static', filename=f'visuals/{visualization_filename}')  # Generate URL for visualization

    return rich_output, visualization_url  # Return the output and visualization URL

# Feature 3: Localized Water Data
def localized_water_data_web(region):
    # Create a new Console instance for this request
    console = Console(record=True)
    console.print(Panel("[bold blue]Enhanced Localized Water Data[/bold blue]"))  # Display header panel
    try:
        # Check if the region exists in regional data
        if region.lower() not in regional_data:
            console.print(f"[red]Error: Region '{region}' not found![/]")  # Display error message
            return console.export_html()  # Return error message as HTML

        region_info = regional_data[region.lower()]  # Retrieve data for the selected region
        console.print(f"[bold cyan]Region:[/bold cyan] {region.capitalize()}")  # Display region name
        console.print(f"[bold cyan]Annual Rainfall:[/bold cyan] {region_info['rainfall']} mm")  # Display annual rainfall
        console.print(f"[bold cyan]Climate:[/bold cyan] {region_info['climate'].capitalize()}")  # Display climate type
        console.print(f"[bold cyan]Average Temperature:[/bold cyan] {region_info['avg_temp']} °C")  # Display average temperature

        console.print("[bold cyan]Seasonal Rainfall Distribution (mm):[/bold cyan]")  # Display section header
        seasons = ["Spring", "Summer", "Autumn", "Winter"]  # Define seasons
        table = Table(show_header=True, header_style="bold magenta")  # Initialize Rich table
        table.add_column("Season")  # Add Season column
        table.add_column("Rainfall (mm)", justify="right")  # Add Rainfall column

        for season, rain in zip(seasons, region_info["seasonal_variation"]):  # Populate table with seasonal data
            table.add_row(season, str(rain))  # Add a row for each season

        console.print(table)  # Display the table

        console.print("[bold magenta]Region-Specific Recommendations:[/bold magenta]")  # Display recommendations header
        # Provide recommendations based on climate type
        if region_info['climate'] == "arid":
            console.print("- Implement rainwater harvesting techniques.")
            console.print("- Use drought-resistant crop varieties.")
        elif region_info['climate'] in ["temperate", "humid"]:
            console.print("- Optimize water distribution with smart sensors.")
            console.print("- Enhance soil moisture retention via organic mulches.")
        else:
            console.print("- Integrate seasonal forecasting into irrigation planning.")
            console.print("- Regularly assess and adjust soil moisture retention strategies.")
    except Exception as e:
        # Handle any exceptions that occur during processing
        console.print(f"[red]An error occurred: {str(e)}[/]")

    rich_output = console.export_html()  # Export the Rich output to HTML
    console.clear()  # Clear the console after exporting
    return rich_output  # Return the HTML output

# Feature 4: Eco-Tips Section
def eco_tips_web():
    # Create a new Console instance for this request
    console = Console(record=True)
    console.print(Panel("[bold blue]Eco-Tips Section[/bold blue]"))  # Display header panel

    try:
        # Define a list of eco-friendly tips categorized by their focus area
        tips = [
            {
                "category": "Soil Health",
                "tip": "Compost Organic Waste",
                "description": "Enhance soil organic matter by composting kitchen and garden waste."
            },
            {
                "category": "Soil Health",
                "tip": "Practice Crop Rotation",
                "description": "Naturally manage soil nutrients and reduce pest buildup by rotating crops each season."
            },
            {
                "category": "Water Conservation",
                "tip": "Adopt Drip Irrigation",
                "description": "Minimize water waste by delivering water directly to plant roots."
            },
            {
                "category": "Water Conservation",
                "tip": "Harvest Rainwater",
                "description": "Collect and store rainwater for irrigation to reduce dependence on external water sources."
            },
            {
                "category": "Energy Efficiency",
                "tip": "Use Solar-Powered Pumps",
                "description": "Reduce energy consumption by utilizing renewable solar energy for irrigation systems."
            },
            {
                "category": "Energy Efficiency",
                "tip": "Upgrade to LED Lighting",
                "description": "Lower energy usage and costs by switching to energy-efficient LED lighting in greenhouses."
            },
            {
                "category": "Soil Conservation",
                "tip": "Minimize Tillage",
                "description": "Maintain soil structure and reduce erosion by limiting the use of tillage equipment."
            },
            {
                "category": "Soil Conservation",
                "tip": "Utilize Cover Cropping",
                "description": "Protect the soil during off-seasons with cover crops that prevent erosion and improve soil health."
            },
            {
                "category": "Pest Management",
                "tip": "Introduce Beneficial Insects",
                "description": "Control pests naturally by attracting or introducing insects that prey on harmful pests."
            },
            {
                "category": "Pest Management",
                "tip": "Use Organic Pesticides",
                "description": "Reduce chemical usage by opting for environmentally friendly pesticide alternatives."
            },
        ]

        # Create a Rich table with categories, tips, and descriptions
        table = Table(title="Eco-Tips", show_header=True, header_style="bold magenta")
        table.add_column("Category", style="bold green")  # Category column
        table.add_column("Tip", style="bold")  # Tip column
        table.add_column("Description", style="italic")  # Description column

        for tip in tips:  # Populate the table with tips
            table.add_row(tip["category"], tip["tip"], tip["description"])  # Add a row for each tip

        console.print(table)  # Display the table
    except Exception as e:
        # Handle any exceptions that occur during processing
        console.print(f"[red]An error occurred: {str(e)}[/]")

    # Export the Rich output to HTML
    rich_output = console.export_html()
    console.clear()  # Clear the console after exporting
    return rich_output  # Return the HTML output

# Define the main route for the Flask application
@app.route('/', methods=['GET', 'POST'])
def index():
    output = None  # Initialize output variable
    visualization_url = None  # Initialize visualization URL variable
    error = None  # Initialize error message variable

    if request.method == 'POST':  # Check if the request is a POST
        feature = request.form.get('feature')  # Get the selected feature from the form

        if feature == '1':  # Advanced Crop Efficiency Planner
            # Retrieve form data
            crop_type = request.form.get('crop_type')
            soil_quality = request.form.get('soil_quality')
            farm_size = request.form.get('farm_size')
            fertilizer_level = request.form.get('fertilizer_level')
            irrigation_eff = request.form.get('irrigation_eff')

            # Validate that all required fields are filled
            if not all([crop_type, soil_quality, farm_size, fertilizer_level, irrigation_eff]):
                error = "All fields are required for Crop Efficiency Planner."  # Set error message
                return render_template('index.html', output=output, visualization_url=visualization_url, error=error)  # Render template with error

            try:
                # Convert input values to appropriate data types
                soil_quality = int(soil_quality)
                farm_size = float(farm_size)
                fertilizer_level = float(fertilizer_level)
                irrigation_eff = float(irrigation_eff)
            except ValueError:
                error = "Invalid input types. Please ensure numeric fields are correctly filled."  # Set error message
                return render_template('index.html', output=output, visualization_url=visualization_url, error=error)  # Render template with error

            # Call the Crop Efficiency Planner function and get the output
            output = crop_efficiency_web(crop_type, soil_quality, farm_size, fertilizer_level, irrigation_eff)

        elif feature == '2':  # Enhanced Water Management Tool
            # Retrieve form data
            irrigation_method = request.form.get('irrigation_method')
            soil_type = request.form.get('soil_type')
            region = request.form.get('region')

            # Validate that all required fields are filled
            if not all([irrigation_method, soil_type, region]):
                error = "All fields are required for Water Management Tool."  # Set error message
                return render_template('index.html', output=output, visualization_url=visualization_url, error=error)  # Render template with error

            # Call the Water Management Tool function and get the output and visualization URL
            output, visualization_url = water_management_web(irrigation_method, soil_type, region)

        elif feature == '3':  # Enhanced Localized Water Data
            # Retrieve form data
            region = request.form.get('localized_region')

            # Validate that the region is selected
            if not region:
                error = "Region selection is required for Localized Water Data."  # Set error message
                return render_template('index.html', output=output, visualization_url=visualization_url, error=error)  # Render template with error

            # Call the Localized Water Data function and get the output
            output = localized_water_data_web(region)

        elif feature == '4':  # Eco-Tips Section
            # Call the Eco-Tips function and get the output
            output = eco_tips_web()

        elif feature == '5':  # Exit
            # Redirect to the home page or display a goodbye message
            return redirect(url_for('index'))

    # Render the main template with the output, visualization URL, and any error messages
    return render_template('index.html', output=output, visualization_url=visualization_url, error=error)

# Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)  # Start the Flask development server with debug mode enabled
