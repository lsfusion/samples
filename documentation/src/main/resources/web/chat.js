function chatMessageRender() {
    return {
        render: function (element) {
            element.style.removeProperty("max-height");
            element.parentElement.style.removeProperty("height");

            var message = document.createElement("div")
            message.classList.add("chat-message");

            var header = document.createElement("div");
            header.classList.add("chat-header");

            var author = document.createElement("div");
            author.classList.add("chat-author");

            element.author = author;
            header.appendChild(author);

            var replyAction = document.createElement("a");
            replyAction.classList.add("chat-reply-action");

            var replyCaption = document.createTextNode("Reply");
            replyAction.appendChild(replyCaption);

            element.replyAction = replyAction;
            header.appendChild(replyAction);

            message.appendChild(header);

            var replyContent = document.createElement("div");
            replyContent.classList.add("chat-reply-content");

            var replyAuthor = document.createElement("div");
            replyAuthor.classList.add("chat-reply-author");

            element.replyAuthor = replyAuthor;
            replyContent.appendChild(replyAuthor);

            var replyText = document.createElement("div");
            replyText.classList.add("chat-reply-text");

            element.replyText = replyText;
            replyContent.appendChild(replyText);

            element.replyContent = replyContent;
            message.appendChild(replyContent);

            var text = document.createElement("div");
            text.classList.add("chat-text");

            element.text = text;
            message.appendChild(text);

            var time = document.createElement("div");
            time.classList.add("chat-time");

            element.time = time;
            message.appendChild(time);

            element.message = message;
            element.appendChild(message);
        },

        update: function (element, controller, value) {
            var obj = JSON.parse(value);
            element.author.innerHTML = obj.author;

            element.replyAuthor.innerHTML = obj.replyAuthor;
            element.replyText.innerHTML = obj.replyText;

            element.time.innerHTML = obj.time;
            element.text.innerHTML = obj.text;

            if (obj.own) {
                element.message.classList.add('chat-message-own');
            } else
                element.message.classList.remove('chat-message-own');

            element.replyAction.onclick = function(event) {
                controller.changeValue(JSON.stringify({ action : 'reply' }));
                $(this).closest("div[lsfusion-container='chat']").find(".chat-message-input-area").focus();
            }

            element.replyContent.onmousedown = function(event) {
                controller.changeValue(JSON.stringify({ action : 'goToReply' }));
            }
        }
    }
}

function chatMessageInputRender() {
    return {
        render: function (element) {
            var input = document.createElement("div");
            input.classList.add("chat-message-input");

            var reply = document.createElement("div");
            reply.classList.add("chat-reply");

            var replyContent = document.createElement("div");
            replyContent.classList.add("chat-reply-content");

            var replyAuthor = document.createElement("div");
            replyAuthor.classList.add("chat-reply-author");

            element.replyAuthor = replyAuthor;
            replyContent.appendChild(replyAuthor);

            var replyText = document.createElement("div");
            replyText.classList.add("chat-reply-text");

            element.replyText = replyText;
            replyContent.appendChild(replyText);

            element.replyContent = replyContent;
            reply.appendChild(replyContent);

            var replyRemove = document.createElement("div");
            replyRemove.classList.add("chat-reply-remove");

            element.replyRemove = replyRemove;
            reply.appendChild(replyRemove);

            input.appendChild(reply);

            var text = document.createElement("div");
            text.classList.add("chat-message-input-area");
            text.contentEditable = "true";

            element.text = text;
            input.appendChild(text);

            element.appendChild(input);
        },
        update: function (element, controller, value) {
            if (value !== null) {
                var obj = JSON.parse(value);

                element.replyAuthor.innerHTML = obj.replyAuthor;
                element.replyText.innerHTML = obj.replyText;

                element.replyRemove.innerHTML = (obj.replyAuthor === '') ? '' : '❌';

                element.text.innerHTML = obj.text;

                element.replyRemove.onclick = function(event) {
                    controller.changeValue(JSON.stringify({ action : 'replyRemove' }));
                }

                element.text.onkeydown = function(event) {
                    if (event.keyCode == 10 || event.keyCode == 13)
                        if (event.ctrlKey)
                            controller.changeValue(JSON.stringify({ action : 'send', value : element.text.innerHTML }))
                        else
                            event.stopPropagation();
                }

                element.text.onblur = function (event) {
                    controller.changeValue(JSON.stringify({ action : 'change', value : element.text.innerHTML }));
                }
            }
        }
    }
}