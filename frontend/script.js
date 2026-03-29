const input = document.getElementById("add-task-input")
const addTaskButton = document.getElementById("add-task-button")
const taskListContainer = document.getElementById("task-list-container")
const message = document.getElementById("message")
const description = document.getElementById("add-description")
const completedTaskContainer = document.getElementById("task-completed-container")
const taskSection = document.getElementById("task-section")
const showButton = document.getElementById("show-button")
const showIcon = document.getElementById("show-icon")
const authInput = document.getElementById("add-auth-input")
const loadTaskButton = document.getElementById("load-task-button")


function authError(response){
    if(response.status===401){
        message.textContent = "Unauthorized"
        taskSection.style.display = "none"
        return true
    }
    return false
}

addTaskButton.addEventListener("click" , function(){
    const token = authInput.value?.trim()
    if(!token){
      
        return
    }
    
    const taskTitle = input.value.trim()
    const taskData = { title : taskTitle}
    const taskDescription = description.value.trim()
    if(taskDescription!==""){
        taskData.description = taskDescription
    }
    if(taskTitle === "") return 

    fetch("https://taskmanagerbackend-13uo.onrender.com/tasks" , {
        method : "POST", 
        headers : {
            "Authorization" : `Bearer ${token}`,
            "Content-Type" : "application/json"
        },
        body: JSON.stringify(taskData)
        
    })
    .then(response=>{
        if(authError(response)){
            throw new Error("Failed to add task.")
        }
        return response.json()
    })
    .then(data=> {
        console.log(data)
        input.value = ""
        description.value = ""
        message.textContent = ""
        viewTasks()
    })
   
    .catch(error => console.error("Error:" , error))
})


taskSection.addEventListener("click" , function(e){
    const token = authInput.value?.trim()
    if(!token){
        
        return
    }
    message.textContent = ""
    if(e.target.classList.contains("delete-button")){
        const taskId= e.target.parentElement.dataset.id
        fetch(`https://taskmanagerbackend-13uo.onrender.com/tasks/${taskId}` , {
            method : "DELETE" ,
            headers : {
            "Authorization" : `Bearer ${token}`
            }
        })
        .then(response=>{
            if(authError(response)){
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
        const token = authInput.value?.trim()
        if(!token){
          
            return
        }
        message.textContent = ""
        if(e.target.classList.contains("check-box") ){
            const taskId = e.target.parentElement.dataset.id
            const checkBoolean = e.target.checked
            fetch(`https://taskmanagerbackend-13uo.onrender.com/tasks/${taskId}` , {
                method : "PATCH" , 
                headers : {"Authorization" : `Bearer ${token}` , 
                            "Content-Type" : "application/json"
                } ,
                body : JSON.stringify({completed:checkBoolean})
            })
            .then(response=>{
                if(authError(response)){
                    throw new Error("Failed to update the task")
                }
               
                return response.json()
            })
            .then(data=>{
                const container = e.target.checked ? completedTaskContainer : taskListContainer
                container.appendChild(e.target.parentElement)
                e.target.parentElement.classList.toggle("completed", e.target.checked)
                console.log(data)
               
            })
            .catch (error=> console.log("Error : " , error))
        
    }
})



function viewTasks(){
    const token = authInput.value?.trim()


    fetch("https://taskmanagerbackend-13uo.onrender.com/tasks" , {
        method : "GET" ,
        headers : {
            "Authorization" : `Bearer ${token}`
        }
    })
    .then(response=>{
        if(authError(response)){
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

showButton.addEventListener("click" , ()=>{
    const isPassword = authInput.type === "password"
    authInput.type = isPassword ? "text" : "password"
    showIcon.className = isPassword ? "fa-regular fa-eye-slash" : "fa-regular fa-eye"
})
authInput.addEventListener("input"  , ()=>{
    const token = authInput.value?.trim() 
    if(!token){
      
        taskSection.style.display = "none" ;
        return
    } 
    message.textContent="";
})

loadTaskButton.addEventListener("click" , ()=>{
    const token = authInput.value?.trim()
    if(!token){
        message.textContent = "Token Required"
        taskSection.style.display="none"
        return
    }
    taskSection.style.display="block"
    message.textContent = ""
    viewTasks()
})