// scripts.js

/**
 * Function to toggle the visibility of different feature forms based on user selection.
 */
function toggleFeatures() {
    console.log("toggleFeatures() called"); // Log function call for debugging
    var feature = document.getElementById("feature").value; // Get the selected feature value
    console.log("Selected feature value:", feature); // Log the selected feature

    // Array of form IDs corresponding to each feature
    var forms = ["crop_efficiency_form", "water_management_form", "localized_water_data_form", "eco_tips_form"];
    
    // Iterate over each form ID to hide them initially
    forms.forEach(function(form) {
        var element = document.getElementById(form); // Get the form element by ID
        if (element) {
            element.style.display = "none"; // Hide the form
            element.setAttribute('aria-hidden', 'true'); // Update ARIA attribute for accessibility
            console.log("Hiding form:", form); // Log which form is being hidden
        } else {
            console.log("Form not found:", form); // Log if the form element is not found
        }
    });

    // Determine which form to display based on the selected feature
    if (feature === "1") {
        var selectedForm = document.getElementById("crop_efficiency_form"); // Get Crop Efficiency Planner form
        if (selectedForm) {
            selectedForm.style.display = "block"; // Show the form
            selectedForm.setAttribute('aria-hidden', 'false'); // Update ARIA attribute
            console.log("Showing form:", "crop_efficiency_form"); // Log which form is being shown
        } else {
            console.log("Form not found:", "crop_efficiency_form"); // Log if form is not found
        }
    } else if (feature === "2") {
        var selectedForm = document.getElementById("water_management_form"); // Get Water Management Tool form
        if (selectedForm) {
            selectedForm.style.display = "block"; // Show the form
            selectedForm.setAttribute('aria-hidden', 'false'); // Update ARIA attribute
            console.log("Showing form:", "water_management_form"); // Log which form is being shown
        } else {
            console.log("Form not found:", "water_management_form"); // Log if form is not found
        }
    } else if (feature === "3") {
        var selectedForm = document.getElementById("localized_water_data_form"); // Get Localized Water Data form
        if (selectedForm) {
            selectedForm.style.display = "block"; // Show the form
            selectedForm.setAttribute('aria-hidden', 'false'); // Update ARIA attribute
            console.log("Showing form:", "localized_water_data_form"); // Log which form is being shown
        } else {
            console.log("Form not found:", "localized_water_data_form"); // Log if form is not found
        }
    } else if (feature === "4") {
        var selectedForm = document.getElementById("eco_tips_form"); // Get Eco-Tips Section form
        if (selectedForm) {
            selectedForm.style.display = "block"; // Show the form
            selectedForm.setAttribute('aria-hidden', 'false'); // Update ARIA attribute
            console.log("Showing form:", "eco_tips_form"); // Log which form is being shown
        } else {
            console.log("Form not found:", "eco_tips_form"); // Log if form is not found
        }
    }
}

/**
 * Event listener for DOMContentLoaded to ensure the script runs after the DOM is fully loaded.
 */
document.addEventListener("DOMContentLoaded", function() {
    var form = document.querySelector("form"); // Select the first form element on the page

    /**
     * Event listener for form submission to handle client-side validation and display loading indicators.
     */
    form.addEventListener("submit", function(e) {
        var executeButton = document.getElementById("execute-button"); // Get the Execute button
        var loadingSpinner = document.getElementById("loading-spinner"); // Get the Loading Spinner element
        
        // Perform Client-Side Validation
        // Example: Ensure all required inputs are filled
        var selectedFeature = document.getElementById("feature").value; // Get the selected feature value
        var valid = true; // Flag to track validation status
        var errorMessage = ""; // Initialize error message string

        if (!selectedFeature) { // Check if no feature is selected
            valid = false; // Set validation flag to false
            errorMessage += "Please select a feature.\n"; // Append error message
        } else {
            if (selectedFeature === "1") { // If Advanced Crop Efficiency Planner is selected
                // Retrieve input values for Crop Efficiency Planner
                var cropType = document.getElementById("crop_type").value.trim();
                var soilQuality = document.getElementById("soil_quality").value;
                var farmSize = document.getElementById("farm_size").value;
                var fertilizerLevel = document.getElementById("fertilizer_level").value;
                var irrigationEff = document.getElementById("irrigation_eff").value;

                // Validate Crop Type
                if (!cropType) {
                    valid = false;
                    errorMessage += "Crop type is required.\n";
                }
                // Validate Soil Quality within range
                if (!soilQuality || soilQuality < 1 || soilQuality > 100) {
                    valid = false;
                    errorMessage += "Soil quality must be between 1 and 100.\n";
                }
                // Validate Farm Size as positive number
                if (!farmSize || farmSize <= 0) {
                    valid = false;
                    errorMessage += "Farm size must be a positive number.\n";
                }
                // Validate Fertilizer Level as non-negative number
                if (!fertilizerLevel || fertilizerLevel < 0) {
                    valid = false;
                    errorMessage += "Fertilizer level must be a non-negative number.\n";
                }
                // Validate Irrigation Efficiency within range
                if (!irrigationEff || irrigationEff < 0.5 || irrigationEff > 1.0) {
                    valid = false;
                    errorMessage += "Irrigation efficiency must be between 0.5 and 1.0.\n";
                }
            } else if (selectedFeature === "2") { // If Enhanced Water Management Tool is selected
                // Retrieve input values for Water Management Tool
                var irrigationMethod = document.getElementById("irrigation_method").value.trim();
                var soilType = document.getElementById("soil_type").value.trim();
                var region = document.getElementById("region").value.trim();

                // Validate Irrigation Method
                if (!irrigationMethod) {
                    valid = false;
                    errorMessage += "Irrigation method is required.\n";
                }
                // Validate Soil Type
                if (!soilType) {
                    valid = false;
                    errorMessage += "Soil type is required.\n";
                }
                // Validate Region
                if (!region) {
                    valid = false;
                    errorMessage += "Region is required.\n";
                }
            } else if (selectedFeature === "3") { // If Enhanced Localized Water Data is selected
                // Retrieve input value for Localized Water Data
                var localizedRegion = document.getElementById("localized_region").value;

                // Validate Localized Region selection
                if (!localizedRegion) {
                    valid = false;
                    errorMessage += "Please select a region.\n";
                }
            }
            // Feature 4 (Eco-Tips) requires no additional inputs
        }

        if (!valid) { // If validation fails
            e.preventDefault(); // Prevent form submission
            alert(errorMessage); // Display alert with error messages
            executeButton.disabled = false; // Re-enable the Execute button
            executeButton.innerText = "Execute"; // Reset button text
            if (loadingSpinner) {
                loadingSpinner.style.display = "none"; // Hide the loading spinner
            }
            return; // Exit the function
        }

        // If validation passes, disable the Execute button and show the loading spinner
        executeButton.disabled = true; // Disable the button to prevent multiple submissions
        executeButton.innerText = "Executing..."; // Change button text to indicate processing
        if (loadingSpinner) {
            loadingSpinner.style.display = "block"; // Show the loading spinner
        }
    });
});
