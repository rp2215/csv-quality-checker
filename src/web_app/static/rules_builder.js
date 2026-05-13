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
            step="0.01" <!-- smallest alllowed increment value --!>
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