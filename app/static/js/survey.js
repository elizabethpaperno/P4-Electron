console.log("this page is connected to survey.js")
var quiz = document.getElementById("questions")

function addQuestionText(question) {
    //create new list element
    newQuestion = document.createElement("li")
    //set innerHTML of new list element to the question being asked
    newQuestion.innerHTML = question
    //append this new list element to the list of questions
    quiz.appendChild(newQuestion)

    console.log("added text for the question:", question)
    return quiz.lastElementChild
}

function addMCQ(question, dict) {
    //get the question
    question = addQuestionText(question)
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
        radioButton.setAttribute("name", "q" + quiz.childElementCount)
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

function addRanking(question, dict) {
    //get the question
    question = addQuestionText(question)
    //create and append a line break
    br = document.createElement("br")
    question.appendChild(br)
    //get a list of keys in the dictionary
    keys = Object.keys(dict)
}



addMCQ("Who are you?", {
    "To be or not to be?" : "That is the question",
    "Whether tis nobler in the mind" : "To suffer the slings and arrows of outrageous fortune"
})

addMCQ("What's your favorite fruit?", {
    "I like apples" : "apples",
    "Blueberries are cool" : "Blueberries",
    "Dragonfruits look awesome" : "Dragonfruit"
})
