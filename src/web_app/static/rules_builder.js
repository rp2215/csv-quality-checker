const rulesContainer = document.getElementById("rules-container");
const rulesPreview = document.getElementById("rules-preview");

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

        const columnRules = {}; // rules for one column

        columnRules.required = requiredValue === "true";

        // only add type and missing percent when user selected one
        if (typeValue !== ""){
            columnRules.type = typeValue;
        }
        if (missingPercentValue !== ""){
            columnRules.max_missing_percent = Number (missingPercentValue);
        }

        rules.columns[columnName] = columnRules // add column to rules object

    });

    return rules;
}

// update live preview of added rules
function updatePreview() {

    const rules = buildRulesObject();

    rulesPreview.textContent = JSON.stringify(rules,null,4);
}

// download as JSON file
function downloadRulesFile(){

    const rules = buildRulesObject();

    // check at least one column rule exists
    if (Object.keys(rules.columns).length === 0){
        alert("Add at least one column rule before downloading.")
        return;
    }

    const rulesJson = JSON.stringify(rules, null, 4)

    const jsonFileBlob = new Blob([rulesJson], {type: "application/json",}); // create the downloadable JSON file

    const downloadLink = document.createElement("a") // temp link

    // attach file to link and set name
    downloadLink.href = URL.createObjectURL(jsonFileBlob)
    downloadLink.download = "custom_rules.json";

    downloadLink.click(); // trigger donwload

    URL.revokeObjectURL(downloadLink.href); // releases the temp object URL

}
// update preview whenver user input changes
document.addEventListener("input", updatePreview) 
addRuleBlock(); // on first load add blank