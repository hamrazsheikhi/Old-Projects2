$(function() {
  // Define variables and constants for various elements
  const chatInput = $("#chat-input");
  const sendButton = $("#send-btn");
  const chatContainer = $(".chat-container");
  const themeButton = $("#theme-btn");
  const deleteButton = $("#delete-btn");

  // Initialize userText variable
  let userText = null;

  // Load data from local storage
  const loadDataFromLocalstorage = () => {
    // Get theme color from local storage and toggle body class
    const themeColor = localStorage.getItem("themeColor");
    $("body").toggleClass("light-mode", themeColor === "light_mode");

    // Set theme button text based on body class
    themeButton.text(
      $("body").hasClass("light-mode") ? "dark_mode" : "light_mode"
    );

    // Set default text if no chats are stored in local storage
    const defaultText = `<button class="openbtn" onclick="openNav()">☰</button>
  
                                <div class="default-text">
                                <h1>خوش آمدید</h1>
                                <br>
                                <p>یک گفت‌وگو را آغاز کنید و به دنیای خلاقیت پی ببرید.
                                <br> تاریخچه گفت‌وگوی شما در اینجا نمایش داده خواهد شد.
                                <br> لطفاً یک عدد وارد کنید تا API را بررسی کنید.</p>
                            </div>`;

    // Set chat container HTML to stored chats or default text
    chatContainer.html(localStorage.getItem("all-chats") || defaultText);

    // Scroll to bottom of chat container
    // chatContainer.scrollTop(chatContainer[0].scrollHeight)
    chatContainer.scrollTop(chatContainer[0].scrollHeight);

    // $(".chat-container").scrollTop($(".chat-container")[0].scrollHeight);


    // Add click/tap event listener to sidebar button
    $(".btn-nav").on("click tap", function () {
      $(this).toggleClass("animated");
    });
  };

  // Create a chat element with the given content and class name
  const createChatElement = (content, className) => {
    const chatDiv = $("<div>")
      .addClass("chat")
      .addClass(className)
      .html(content);
    return chatDiv;
  };

  // Retrieve a chat response from an external API and add it to the chat container
  const getChatResponse = (incomingChatDiv) => {
    const API_URL = "https://jsonplaceholder.typicode.com/todos/";
    const pElement = $("<p>");
    const copyBtn = $("<span>").addClass("material-symbols-rounded copy-response").text("content_copy");

    // Make AJAX request to API and handle response
    $.ajax({
      url: API_URL + userText,
      success: function (response) {
        pElement.text(response.title);
      },
      error: function () {
        pElement
          .addClass("error")
          .text(
            "Oops! Something went wrong while retrieving the response. Please try again."
          );
      },
      complete: function () {
        // Remove typing animation and add chat details and copy button
        incomingChatDiv.find(".typing-animation").remove();
        incomingChatDiv.find(".chat-details").append(pElement);
        incomingChatDiv.find(".chat-details").append(copyBtn);
        incomingChatDiv.find(".chat-details").append("<span class='time-text'>" + new persianDate().format("h:mm a") + "</span>");

        // Store all chats in local storage and scroll to bottom of chat container
        localStorage.setItem("all-chats", chatContainer.html());
        chatContainer.scrollTop(chatContainer[0].scrollHeight);
      },
    });
  };

  // Copy chat response to clipboard
  const copyResponse = (copyBtn) => {
    const reponseTextElement = $(copyBtn).parent().find("p");
    navigator.clipboard.writeText(reponseTextElement.text());
    $(copyBtn).text("done");
    setTimeout(() => $(copyBtn).text("content_copy"), 1000);
  };

  // Show typing animation and retrieve chat response
  const showTypingAnimation = () => {
    const html = `<div class="chat-content">
                        <div class="chat-details">
                            <img src="images/GPTicon.jpg" alt="chatbot-img">
                            <div class="typing-animation">
                                <div class="typing-dot" style="--delay: 0.2s"></div>
                                <div class="typing-dot" style="--delay: 0.3s"></div>
                                <div class="typing-dot" style="--delay: 0.4s"></div>
                            </div>
                            
                          </div>
                      </div>`;
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.append(incomingChatDiv);
    chatContainer.scrollTop(chatContainer[0].scrollHeight);
    getChatResponse(incomingChatDiv);
  };

  // Handle outgoing chat messages
  const handleOutgoingChat = () => {
    userText = chatInput.val().trim();
    if (!userText) return;

    // Clear chat input and set its height to initial value
    chatInput.val("");
    chatInput.css("height", `${initialInputHeight}px`);

    // Create outgoing chat element and add it to chat container
    const html = `<div class="chat-content">
                        <div class="chat-details">
                            <img src="images/user.jpg" alt="user-img">
                            <p>${userText}</p>
                            <span class="time-text">${new persianDate().format("h:mm a")}</span>
                            </div>
                    </div>`;
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.find(".default-text")?.remove();
    chatContainer.append(outgoingChatDiv);
    chatContainer.scrollTop(chatContainer[0].scrollHeight);

    // Hide send button and show typing animation after a delay
    $('#send-btn').css('visibility', 'hidden');
    setTimeout(showTypingAnimation, 500);
  };

  // Add click event listener to delete button
  deleteButton.click(function () {
    if (confirm("Are you sure you want to delete all the chats?")) {
      localStorage.removeItem("all-chats");
      loadDataFromLocalstorage();
    }
  });

  // Add click event listener to theme button
  themeButton.click(function () {
    // Toggle body class and store theme color in local storage
    $("body").toggleClass("light-mode");
    localStorage.setItem("themeColor", themeButton.text());
    themeButton.text(
      $("body").hasClass("light-mode") ? "dark_mode" : "light_mode"
    );
  });

  // Set initial input height and add input event listener to adjust height
  const initialInputHeight = chatInput[0].scrollHeight;
  chatInput.on("input", function () {
    chatInput.css("height", `${initialInputHeight}px`);
    chatInput.css("height", `${chatInput[0].scrollHeight}px`);
  });

  // Add keydown event listener to chat input for sending messages
  chatInput.keydown(function (e) {
    let oneAtTimeRequestCond = chatContainer[0].children[chatContainer[0].children.length-1].classList.contains('incoming'); 
    let firstMessage =  chatContainer[0].children.length==2;
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800 && (oneAtTimeRequestCond || firstMessage)) {
      e.preventDefault();
      handleOutgoingChat();
    }
  });

  // Load data from local storage and add click event listener to send button
  loadDataFromLocalstorage();
  sendButton.click(handleOutgoingChat);

  // Add click event listener to copy button
  $(document).on("click", ".copy-response", function () {
    copyResponse(this);
  });

  // Show or hide send button based on input validity
  $('#chat-input').on('input', function() {
    if (this.validity.valid) {
      $('#send-btn').css('visibility', 'visible');
    } else {
      $('#send-btn').css('visibility', 'hidden');
    }
  });
});

// Open and close sidebar functions
const openNav = () => {
  document.getElementById("mySidebar").style.width = "200px";
};
const closeNav = () => {
  document.getElementById("mySidebar").style.width = "0";
};

// Add click/tap event listener to sidebar button for animation
$(".btn-nav").on("click tap", function () {
  $(this).toggleClass("animated");
});