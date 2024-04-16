function processCode(){

    var generalizeFunctions = document.getElementById('generalizeFunctions').checked;
    var generalizeVariables = document.getElementById('generalizeVariables').checked;
    var generalizeString = document.getElementById('generalizeStrings').checked;
    var language = document.getElementById('languageSelection').value;
    var errorRecovery = document.getElementById('errorRecovery').checked;
    var replacementSelection = + !document.getElementById('replacementSelection').value.includes("Simple");
    var returnTypeSelection = + !document.getElementById('returnTypeSelection').value.includes("tokens");
    console.log(returnTypeSelection)
    console.log(generalizeVariables)
    console.log(generalizeString)
    console.log(language)
    
    var content = document.getElementById("code").value
    //fetch("https://vsgate-http.dei.isep.ipp.pt:11085/process", {
    fetch("http://192.168.57.10:8080/process", {

    method: "POST",
    body: JSON.stringify({
        code: content,
        generalizeFunctionNames:generalizeFunctions,
        generalizeVariableNames:generalizeVariables,
        generalizeStrings:generalizeString,
        replacementStrategy:replacementSelection,
        tryRecoverFromErrors:errorRecovery,
        returnType:returnTypeSelection,
        language: language
    }),
    headers: {
        "Content-type": "application/json; charset=UTF-8"
    }
    }).then(
        (response) => {
            console.log(response.body)
            return response.json()
        }
    ).then((data) => {
        const modals = document.getElementById("resultado");
            const result_container = document.getElementById("api-result");
            let textString = JSON.parse(data)['result'];
            if(returnTypeSelection == 0){
                textString = textString.map(String).join(' | ');
            }
            result_container.innerText = textString
            modals.style.display = "flex";
    });
}


// Seleciona o botÃ£o que abre o modal
const openModalButton = document.getElementById("openModalButton");

// Seleciona o modal

// Seleciona o botÃ£o para fechar o modal
const closeModalButton = document.getElementById("closePlaceholder");


function closeModal(){
    const modal = document.getElementById("resultado");
    modal.style.display = "none"
}


