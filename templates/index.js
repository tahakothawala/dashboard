function index() {
    // barchart("Gender", "BP Meds");
    radarchart();
    pcp();
    piechart("Gender", "Current Smoker");
    heatmap("BMI", "Age", "CigsPerDay");
    scatterplot("Total Cholestrol", "BMI", "Heart Stroke");
}
