//const test = document.getElementById('upload');

//test.addEventListener('click', () => {
//   fetch('http://localhost:8765/')
//        .then(response => response.json())
//        .then(data => {
//            document.getElementById('responseData').innerText = JSON.stringify(data);
//        })
//        .catch(error => {
//            console.error('Error:', error);
//        });
//});


const upload = document.getElementById('upload');

upload.addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        fetch('http://localhost:8765/upload/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Aquí puedes manejar la respuesta del servidor
            console.log('Respuesta del servidor:', data);
        })
        .catch(error => {
            console.error('Error al subir archivo:', error);
        });
    } else {
        alert('Por favor, seleccione una foto.');
    }
});