function out() {
    let value = document.querySelector('.poll__input').value
    if (!value)
      return;
    let container=document.createElement('li');
    container.className = "poll__item";
    container.innerHTML = value;
    document.getElementById('poll__list').appendChild(container)
}