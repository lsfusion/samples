function featuresStoreCards() {
    return {
        render: function (element, controller) {
            let cards = document.createElement("div");
            cards.classList.add("features-store-cards");

            element.cards = cards;
            element.appendChild(cards);
        },
        update: function (element, controller, list) {
            while (element.cards.lastElementChild) {
                element.cards.removeChild(element.cards.lastElementChild);
            }

            for (let item of list) {
                let card = document.createElement("div");
                card.classList.add("features-store-card");
                if (controller.isCurrent(item))
                    card.classList.add("features-store-card-current");

                card.textContent = (item.name || '') + (item.sinteger != null ? ': ' + item.sinteger : '');

                card.onclick = function (event) {
                    if (!controller.isCurrent(item))
                        controller.changeObject(item);
                }

                element.cards.appendChild(card);
            }
        }
    }
}

function featuresCounter() {
    return {
        render: function (element, controller) {
            let button = document.createElement("button");
            button.classList.add("features-counter");

            element.button = button;
            element.appendChild(button);
        },
        update: function (element, controller, value) {
            element.button.textContent = value != null ? value : 0;
            element.button.onclick = function (event) {
                controller.change((value || 0) + 1);
            }
        }
    }
}
