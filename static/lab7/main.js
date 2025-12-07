function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            films.forEach(film => {
                const tr = document.createElement('tr');

                const tdTitle = document.createElement('td');
                tdTitle.textContent = film.title;

                const tdTitleRus = document.createElement('td');
                if (film.title_ru && film.title_ru !== film.title) {
                    const span = document.createElement('span');
                    span.className = 'original-name';
                    span.textContent = `(${film.title_ru})`;
                    tdTitleRus.appendChild(span);
                } else if (film.title_ru) {
                    tdTitleRus.textContent = film.title_ru;
                }

                const tdYear = document.createElement('td');
                tdYear.textContent = film.year;

                const tdActions = document.createElement('td');

                const editButton = document.createElement('button');
                editButton.textContent = 'редактировать';
                editButton.onclick = () => editFilm(film.id);

                const delButton = document.createElement('button');
                delButton.textContent = 'удалить';
                delButton.onclick = () => deleteFilm(film.id, film.title);

                tdActions.append(editButton, delButton);
                tr.append(tdTitle, tdTitleRus, tdYear, tdActions);
                tbody.append(tr);
            });
        })
        .catch(err => console.error('Ошибка:', err));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) {
        return;
    }

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList());
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('id').value = film.id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;
            showModal();
        });
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: document.getElementById('year').value,
        description: document.getElementById('description').value
    };
    
    let url, method;
    
    if (!id) {
        url = '/lab7/rest-api/films/';
        method = 'POST';
    } else {
        url = `/lab7/rest-api/films/${id}`;
        method = 'PUT';
    }
    
    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (response.status === 400) {
            return response.json();
        }
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        throw new Error('Ошибка сети');
    })
    .then(errors => {
        if (errors && errors.description) {
            document.getElementById('description-error').innerText = errors.description;
        }
        if (errors && errors.title_ru) {
            alert(errors.title_ru);
        }
        if (errors && errors.year) {
            alert(errors.year);
        }
        if (errors && errors.title) {
            alert(errors.title);
        }
    })
    .catch(error => console.error('Ошибка:', error));
}

function showModal() {
    document.getElementById('description-error').innerText = '';
    document.querySelector('div.modal').style.display = 'block';
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

window.addEventListener('load', fillFilmList);

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';
    showModal();
}