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

addCheckboxQuestion("What kinds of restaurants do you like?", "food_category",{
    "Breakfast/Brunch": "breakfast_brunch",
    "Italian": "italian",
    "Cocktail Bars": "cocktailbars",
    "New American" : "newamerican",
    "Sandwiches": "sandwiches",
    "Pizza":'pizza',
    "Bars":'bars',
    "Coffee":'coffee',
    "Trade American":'tradamerican',
    "Seafood": 'seafood',
    "Mexican" : "mexican",
    "Chinese" : "chinese",
    "Japanese": "japanese",
    "Sushi": "sushi",
    "Cafes":'cafes',
    "Burgers":'burgers',
    "Wine Bars":'wine_bars',
    "Delis":'delis',
    "Salad":'salad',
    "Mediterranean":'mediterranean',
    "French":'french',
    "Noodles":'noodles',
    "Thai":'thai',
    "Korean":'korean',
    "Desserts":'desserts'
})

addCheckboxQuestion("What neighborhoods do you prefer to eat out in?", "location", {
  'Midtown West': 'Midtown West',
  'Greenwich Village': 'Greenwich Village',
  'East Harlem':'East Harlem',
  'Upper East Side': 'Upper East Side',
  'Midtown East': 'Midtown East',
  'Gramercy': 'Gramercy',
  'Little Italy': 'Little Italy',
  'Chinatown':'Chinatown',
  'SoHo': 'SoHo',
  'Harlem': 'Harlem',
  'Upper West Side': 'Upper West Side',
  'Tribeca': 'Tribeca',
  'Garment District': 'Garment District',
  'Stuyvesant Town': 'Stuyvesant Town',
  'Financial District': 'Financial District',
  'Chelsea': 'Chelsea',
  'Morningside Heights': 'Morningside Heights',
  'Times Square': 'Times Square',
  'Murray Hill': 'Murray Hill',
  'East Village': 'East Village',
  'Lower East Side': 'Lower East Side',
  "Hell's Kitchen": 'Hell\s Kitchen',
  'Central Park': 'Central Park'
})

addRadioQuestion("Do you regularly order (alcoholic) drinks at restaurants?", "alcohol_preference", {
    "Yes" : true,
    "No" : false
})

addRadioQuestion("What's the minimum sanitation grade you want your restaurants to have?", "sanitation_preference", {
    "A" : 13,
    "B" : 27,
    "C" : 1000
})

addCheckboxQuestion("What dietary restrictions do you have?", "diet_restrictions", {
    "Kosher" : "kosher",
    "Vegan" : "vegan",
    "Vegetarian" : "vegetarian",
    "Can't eat gluten" : "gluten_free",
    "Halal" : "halal",
    "None" : "None"
})
