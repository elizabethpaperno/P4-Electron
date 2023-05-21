console.log("this page is connected to survey.js")
var quiz = document.getElementById("questions")

function addQuestionText(question, name) {
    //create new list element
    newQuestion = document.createElement("li")
    //set innerHTML of new list element to the question being asked
    newQuestion.innerHTML = question
    //give the question and id
    newQuestion.setAttribute("id", name)
    //append the question
    quiz.appendChild(newQuestion)

    console.log("added text for the question:", question)
    return quiz.lastElementChild
}

function addRadioQuestion(question, name, dict) {
    //get the question
    question = addQuestionText(question, name)
    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
    //get a list of keys (option text) in the dictionary
    keys = Object.keys(dict)
    
    for(i = 0; i < keys.length; i++) {
        //create and append a radio button for each MCQ option
        id = quiz.childElementCount + "-" + i
        radioButton = document.createElement("input")
        radioButton.setAttribute("type", "radio")
        radioButton.setAttribute("id", id)
        radioButton.setAttribute("name", name)
        //set the value of the radio button
        radioButton.setAttribute("value", dict[keys[i]])
        question.appendChild(radioButton)

        //create and append a label for the radio button
        label = document.createElement("label")
        label.setAttribute("for", id)
        label.innerHTML = keys[i]
        question.appendChild(label)
        
        //create and append a line break
        br = document.createElement("br")
        question.appendChild(br)
    }

    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
}

function addTextQuestion(question, name) {
    //get the question
    question = addQuestionText(question, name)
    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)

    //create the text input
    id = quiz.childElementCount + "-0"
    textInput = document.createElement("input")
    textInput.setAttribute("type", "text")
    textInput.setAttribute("id", id)
    textInput.setAttribute("name", name)
    question.appendChild(textInput)

    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
}

function addCheckboxQuestion(question, name, dict) {
    //get the question
    question = addQuestionText(question, name)
    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
    //get a list of keys (option text) in the dictionary
    keys = Object.keys(dict)
    
    for(i = 0; i < keys.length; i++) {
        //create and append a checkbox for each option
        id = quiz.childElementCount + "-" + i
        checkbox = document.createElement("input")
        checkbox.setAttribute("type", "checkbox")
        checkbox.setAttribute("id", id)
        checkbox.setAttribute("name", name)
        //set the value of the radio button
        checkbox.setAttribute("value", dict[keys[i]])
        question.appendChild(checkbox)

        //create and append a label for the radio button
        label = document.createElement("label")
        label.setAttribute("for", id)
        label.innerHTML = keys[i]
        question.appendChild(label)
        
        //create and append a line break
        br = document.createElement("br")
        question.appendChild(br)
    }

    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
}

addCheckboxQuestion("What kinds of food do you like?", "food_category",{
    "Mexican" : "Mexican",
    "Chinese" : "Chinese",
    "English" : "English"
})

addTextQuestion("Where do you live? (please enter a valid address)", "location")
    
addRadioQuestion("Do you like alcohol?", "alcohol_preference", {
    "Yes" : true,
    "No" : false
})

addRadioQuestion("What's the minimum sanitation grade you want your restaurants to have?", "sanitation_preference", {
    "A" : 13,
    "B" : 27,
    "C" : 1000
})

addCheckboxQuestion("What dietary restrictions do you have?", "diet_restrictions", {
    "Kosher" : "Kosher",
    "Vegan" : "Vegan",
    "Vegetarian" : "Vegetarian",
    "Can't eat gluten" : "Gluten-Free",
    "Halal" : "Halal",
    "None" : "None"
})