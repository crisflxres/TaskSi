const URL = "http://127.0.0.1:5000/tareas"; //Ruta de la API Flask

async function cargarTareas() {
    const respuesta = await fetch(URL);
    const datos = await respuesta.json();
    const lista = document.getElementById("taskList");
    lista.innerHTML = "";  //limpia la lista antes de recargar

    datos.tareas.forEach(tarea => {
        const li = document.createElement('li');

        if(tarea.completada) li.className = 'completer'; //si la tarea esta marcada como 1 en BD, le asignamos la clase CSS para tacharla
        li.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px; flex-grow: 1;">
                <input type="checkbox" 
                    ${tarea.completada ? 'checked' : ''} 
                    onclick="completarTarea(${tarea.id}, ${tarea.completada}, '${tarea.titulo}', '${tarea.descripcion}')"
                    style="cursor: pointer; width: 18px; height: 18px;">
        
                <div class="task-info" style="flex-grow: 1;">
                    <b>${tarea.titulo}</b>
                    <p style="margin: 0; color: #666; font-size: 0.9em;">${tarea.descripcion || ''}</p>
                </div>
            </div>
            <div class="actions">
                <button onclick="editarTarea(${tarea.id}, '${tarea.titulo}', '${tarea.descripcion}')">✏️</button>
                <button onclick="borrarTarea(${tarea.id})">🗑️</button>
            </div>`;
        lista.appendChild(li);
    });
}
//Envia una nueva tarea
async function addTask() {
    const titulo = document.getElementById("taskTitle").value;
    const desc = document.getElementById("taskDescription").value;

    if(!titulo) return alert("El título es obligatorio");

    await fetch(URL, {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({titulo: titulo, descripcion: desc})
    });
    //Limmpia los inputs y refresca la lista
    document.getElementById("taskTitle").value = "";
    document.getElementById("taskDescription").value = "";
    cargarTareas();
}
//Elimina un registro de la BD usuando ID
async function borrarTarea(id) {
    if(confirm("Borrar tarea?")) {
        await fetch(`${URL}/${id}`, {method: "DELETE"});
        cargarTareas();
    }
}
//Filtra visualmente las tareas q coincidan con el texto
function filterTasks() {
        const query = document.getElementById("searchBar").value.toLowerCase();
        const items = document.querySelectorAll("#taskList li");
        items.forEach(item => {
            const text = item.innerText.toLowerCase();
            item.style.display = text.includes(query) ? "flex" : "none";
     });
}
    //Modifica los datos de una tarea
async function editarTarea(id, tituloActual, descActual) {
    const nuevoTitulo = prompt("Editar título:", tituloActual);
    const nuevaDesc = prompt("Editar descripción:", descActual);

    if (nuevoTitulo !== null) {
        await fetch(`${URL}/${id}`, {
            method: "PUT",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                titulo: nuevoTitulo, 
                descripcion: nuevaDesc
            })
        });
        cargarTareas();
    }
}
//Cambia el estado (0/1) el presionar
async function completarTarea(id, estadoActual, titulo, descripcion) {
    const nuevoEstado = estadoActual ? 0 : 1;

    await fetch(`${URL}/${id}`, {
        method: "PUT",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            titulo: titulo,
            descripcion: descripcion,
            completada: nuevoEstado
        })
    });
    cargarTareas();
}
cargarTareas();//Carga las tareas al abrir la página