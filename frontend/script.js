const input = document.getElementById("add-task-input")
const addTaskButton = document.getElementById("add-task-button")
const taskListContainer = document.getElementById("task-list-container")
const message = document.getElementById("message")
const description = document.getElementById("add-description")
const completedTaskContainer = document.getElementById("task-completed-container")
const taskSection = document.getElementById("task-section")
const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3NDcxMzI3NiwianRpIjoiN2M2NDA1ZTgtMTZmOS00MDZhLWJkMTYtYTczNTgyOTA1ZThkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjQiLCJuYmYiOjE3NzQ3MTMyNzYsImV4cCI6MTc3NDcxNDE3Nn0.126yMkpgM7rT-jkEdGE3YiSp-QoN1s425hvDj3cmndc"

window.onload = function(){
    viewTasks()
}

addTaskButton.addEventListener("click" , function(){
    const taskTitle = input.value.trim()
    const taskData = { title : taskTitle}
    const taskDescription = description.value.trim()
    if(taskDescription!==""){
        taskData.description = taskDescription
    }
    if(taskTitle === "") return 

    fetch("http://127.0.0.1:5000/tasks" , {
        method : "POST", 
        "headers" : {
            "Authorization" : `Bearer ${token}`,
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(taskData)
        
    })
    .then(response=>{
        if(!response.ok){
            throw new Error("Failed to add task.")
        }
        return response.json()
    })
    .then(data=> {
        console.log(data)
        input.value = ""
        description.value = ""
        viewTasks()
    })
   
    .catch(error => console.error("Error:" , error))
})


taskSection.addEventListener("click" , function(e){
    
    if(e.target.classList.contains("delete-button")){
        const taskId= e.target.parentElement.dataset.id
        fetch(`http://127.0.0.1:5000/tasks/${taskId}` , {
            method : "DELETE" ,
            "headers" : {
            "Authorization" : `Bearer ${token}`
            }
        })
        .then(response=>{
            if(!response.ok){
                throw new Error("Failed to delete task.")
            }
            viewTasks()

        })
        
        .catch(error=>{
            console.log("Error : " , error)
        })
    }
  
})

taskSection.addEventListener("change" , function(e){

        if(e.target.classList.contains("check-box") ){
            const taskId = e.target.parentElement.dataset.id
            const checkBoolean = e.target.checked
            fetch(`http://127.0.0.1:5000/tasks/${taskId}` , {
                method : "PATCH" , 
                "headers" : {"Authorization" : `Bearer ${token}` , 
                            "Content-Type" : "application/json"
                } ,
                body : JSON.stringify({completed:checkBoolean})
            })
            .then(response=>{
                if(!response.ok){
                    throw new Error("Failed to update the task")
                }
                const container = e.target.checked ? completedTaskContainer : taskListContainer
                container.appendChild(e.target.parentElement)
                e.target.parentElement.classList.toggle("completed", e.target.checked)
                return response.json()
            })
            .then(data=>{
                console.log(data)
               
            })
            .catch (error=> console.log("Error : " , error))
        
    }
})



function viewTasks(){
    fetch("http://127.0.0.1:5000/tasks" , {
        method : "GET" ,
        "headers" : {
            "Authorization" : `Bearer ${token}`
        }
    })
    .then(response=>{
        if(!response.ok){
            throw new Error("Failed to view task.")
        }
        return response.json()
    })
    .then(data=>{
        taskListContainer.innerHTML = ""
        completedTaskContainer.innerHTML =""
        data.tasks.forEach(task=>{
              
            const li = document.createElement("li")
            const titleDescContainer =document.createElement("div")
            titleDescContainer.classList.add("titleDescContainer")
            li.classList.add("task")
            li.dataset.id = task.id

            const checkBox =  document.createElement("input")
            checkBox.type = "checkbox"
            checkBox.classList.add("check-box")
            checkBox.checked = task.completed
            li.appendChild(checkBox)
            li.classList.toggle("completed" , checkBox.checked)
             
            const titleContent = document.createElement("p")
            titleContent.classList.add("task-title")
           
            titleContent.textContent = task.title
            titleDescContainer.appendChild(titleContent)
           

            if(task.description&&task.description.trim()!==""){
                const descriptionContent = document.createElement("p")
                descriptionContent.textContent = task.description
                descriptionContent.classList.add("task-description")
                titleDescContainer.appendChild(descriptionContent)
            }
            li.appendChild(titleDescContainer)

            const deleteBtn = document.createElement("button")
            deleteBtn.textContent = "X"
            deleteBtn.classList.add("delete-button")
            li.appendChild(deleteBtn)
         
          
            task.completed ? completedTaskContainer.appendChild(li) : taskListContainer.appendChild(li)
          
        })
    })
    .catch(error => console.log("Error : " , error))
}

