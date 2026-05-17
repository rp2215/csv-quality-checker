const rulesContainer = document.getElementById("rules-container");
const rulesPreview = document.getElementById("rules-preview");
const rulesFileNameInput = document.getElementById("rules-file-name")

// add one blank rule to page
function addRuleBlock() {

    const ruleBlock = document.createElement("div") // wrapper for one rule
    ruleBlock.className = "rule-builder-card"

    // add input fields
    ruleBlock.innerHTML = `

        <label> Column Name </label>
        
        <input 
            type="text"
            class="rule-column-name"
            placeholder="Example: age"
        >

        <label> Required Column </label>

        <select class = "rule-required">
            <option value="true">Yes</option>
            <option value="false">No</option>
        </select>

        <label> Type Check </label>

        <select class = "rule-type">
            <option value=""> No type check</option>
            <option value="integer">Integer</option>
            <option value="date">Date</option>
            <option value="boolean">Boolean</option>
        </select>

        <label> Max Missing Percentage </label>

        <input
            type="number"
            class="rule-missing-percent"
            min="0"
            max="100"
            step="0.01" 
            placeholder="Example: 0"
        >

        <label> Minimum Value </label>

        <input
            type="number"
            class="rule-min-value"
            placeholder="Example: 0"
        >

        <label> Maximum Value </label>

        <input
            type="number"
            class="rule-max-value"
            placeholder="Example: 120"
        >

        <label> Allowed Values </label>

        <input
            type="text"
            class="rule-allowed-values"
            placeholder="Example: Active, Inactive, Pending"
        >

        <label> Unique Values Only </label>

        <select class="rule-unique">
            <option value="">No unique check</option>
            <option value="true">Yes — no duplicates allowed</option>
        </select>

        <label> Date Min (earliest allowed date) </label>

        <input
            type="date"
            class="rule-date-min"
        >

        <label> Date Max (latest allowed date) </label>

        <input
            type="date"
            class="rule-date-max"
        >

        <button
            type="button"
            class="remove-button"
            onclick="removeRuleBlock(this)"
        >
            Remove Rule
        </button>
    `;

    // add rule block to page and update
    rulesContainer.appendChild(ruleBlock);
    updatePreview(); 
}

// removes one rule block from page
function removeRuleBlock(button){

    const ruleBlock = button.closest(".rule-builder-card") // block that contains clicked button
    ruleBlock.remove()
    updatePreview();
}

// read threshold inputs and return only the values the user has explicitly set
function buildThresholdsObject() {

    const thresholds = {};

    // map each input element ID to the JSON key the backend expects
    const thresholdFields = [
        { id: "threshold-missing-critical", key: "missing_critical" },
        { id: "threshold-missing-high",     key: "missing_high" },
        { id: "threshold-missing-medium",   key: "missing_medium" },
        { id: "threshold-missing-low",      key: "missing_low" },
        { id: "threshold-quality-critical", key: "quality_critical" },
        { id: "threshold-quality-high",     key: "quality_high" },
        { id: "threshold-quality-medium",   key: "quality_medium" },
        { id: "threshold-low-variation",    key: "low_variation_percent" },
    ];

    thresholdFields.forEach(({ id, key }) => {

        const value = document.getElementById(id).value;

        // blank use default
        if (value !== "") {
            thresholds[key] = Number(value);
        }
    });

    return thresholds;
}


// turn UI selections into valid json structure
function buildRulesObject() {

    const rules = {columns: {}, };

    const ruleBlocks = document.querySelectorAll(".rule-builder-card") // gets every block currently on page

    ruleBlocks.forEach((ruleBlock) => {

        const columnName = ruleBlock.querySelector(".rule-column-name").value.trim();

        if(columnName === ""){
            return;
        }

        // Get all user inputted values
        const requiredValue = ruleBlock.querySelector(".rule-required").value;
        const typeValue = ruleBlock.querySelector(".rule-type").value;
        const missingPercentValue = ruleBlock.querySelector(".rule-missing-percent").value;
        const minValue = ruleBlock.querySelector(".rule-min-value").value;
        const maxValue = ruleBlock.querySelector(".rule-max-value").value;
        const allowedValuesText = ruleBlock.querySelector(".rule-allowed-values").value;
        const uniqueValue = ruleBlock.querySelector(".rule-unique").value;
        const dateMinValue = ruleBlock.querySelector(".rule-date-min").value;
        const dateMaxValue = ruleBlock.querySelector(".rule-date-max").value;

        const columnRules = {}; // rules for one column

        columnRules.required = requiredValue === "true";

        // only add type and missing percent when user selected one
        if (typeValue !== ""){
            columnRules.type = typeValue;
        }
        if (missingPercentValue !== ""){
            columnRules.max_missing_percent = Number (missingPercentValue);
        }
        if (minValue !== "") {
            columnRules.min = Number(minValue);
        }
        if (maxValue !== "") {
            columnRules.max = Number(maxValue);
        }
        if (allowedValuesText !== ""){

            // split csv values into a list
            const allowedValues = allowedValuesText.split(",").map((value) => value.trim()).filter((value) => value !== "");

            if (allowedValues.length > 0){
                columnRules.allowed_values = allowedValues;
            }
        }

        if (uniqueValue === "true") {
            columnRules.unique = true;
        }

        if (dateMinValue !== "") {
            columnRules.date_min = dateMinValue; 
        }
        if (dateMaxValue !== "") {
            columnRules.date_max = dateMaxValue;
        }

        rules.columns[columnName] = columnRules // add column to rules object

        // add thresholds section only if the user set at least one value
        const thresholds = buildThresholdsObject();
        if (Object.keys(thresholds).length > 0) {
            rules.thresholds = thresholds;
    }


    });

    return rules;
}

// update live preview of added rules
function updatePreview() {

    const rules = buildRulesObject();

    rulesPreview.textContent = JSON.stringify(rules,null,4);
}

// create safe JSON filename from user input
function getRulesDownloadFileName(){

    let fileName = rulesFileNameInput.value.trim();

    // defualt if user input blank
    if (fileName === ""){
        fileName = "custom_rules";
    }

    // replace spaces with underscore and remove unsafe charcaters
    fileName = fileName.replaceAll(" ","_")
    fileName = fileName.replace(/[^a-zA-Z0-9_-]/g, "");

    // revert to default if empty after safe operations
    if (fileName === ""){
        fileName = "custom_rules"
    }

    // add extension if user forgot
    if (!fileName.endsWith(".json")){
        fileName = `${fileName}.json`;
    }

    return fileName
}

// download as JSON file
function downloadRulesFile(){

    const rules = buildRulesObject();

    // allow download if the user has set column rules, thresholds, or both
    const hasColumns = Object.keys(rules.columns).length > 0;
    const hasThresholds = rules.thresholds && Object.keys(rules.thresholds).length > 0;

    if (!hasColumns && !hasThresholds) {
        alert("Add at least one column rule or threshold value before downloading.")
        return;
    }

    const rulesJson = JSON.stringify(rules, null, 4)

    const jsonFileBlob = new Blob([rulesJson], {type: "application/json",}); // create the downloadable JSON file

    const downloadLink = document.createElement("a") // temp link

    // attach file to link and set name
    downloadLink.href = URL.createObjectURL(jsonFileBlob)
    downloadLink.download = getRulesDownloadFileName();

    downloadLink.click(); // trigger donwload

    URL.revokeObjectURL(downloadLink.href); // releases the temp object URL

}
// update preview whenver user input changes
document.addEventListener("input", updatePreview); 
document.addEventListener("change", updatePreview);

addRuleBlock(); // on first load add blank