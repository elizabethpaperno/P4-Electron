function addRestaurantText(restuarant) {
    //create new list element
    newRestaurant = document.createElement("li")
    //set innerHTML of new list element to the restaurant being asked
    newRestaurant.innerHTML = restaurant
    //append this new list element to the list of restaurants
    rlist.appendChild(newRestaurant)

    console.log("added text for the restaurant:", restaurant)
    return rlist.lastElementChild
}

function addRestaurant(restuarant, dict) {
    //get the restaurant
    restuarant = addRestaurantText(restuarant)
    //create and append a line break
    br = document.createElement("br")
    restuarant.appendChild(br)
    //get a list of keys (option text) in the dictionary
    keys = Object.keys(dict)
    
    for(i = 0; i < keys.length; i++) {
        //create and append a radio button for each MCQ option
        id = restuarant.childElementCount + "-" + i
        radioButton = document.createElement("input")
        radioButton.setAttribute("type", "radio")
        radioButton.setAttribute("id", id)
        radioButton.setAttribute("name", "q" + quiz.childElementCount)
        //set the value of the radio button
        radioButton.setAttribute("value", dict[keys[i]])
        restuarant.appendChild(radioButton)

        //create and append a label for the radio button
        label = document.createElement("label")
        label.setAttribute("for", id)
        label.innerHTML = keys[i]
        restuarant.appendChild(label)
        
        //create and append a line break
        br = document.createElement("br")
        restuarant.appendChild(br)
    }

    //create and append a line break
    br = document.createElement("br")
    restuarant.appendChild(br)
}