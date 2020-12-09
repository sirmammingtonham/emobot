const typingAnim = `<p class="botTyping"><span class="jumping-dots">
<span class="dot-1">.</span>
<span class="dot-2">.</span>
<span class="dot-3">.</span>
</span></p>`;


function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
  var current_emotion = (document.cookie.match(
    /^(?:.*;)?\s*current_emotion\s*=\s*([^;]+)(?:.*)?$/
  ) || [, null])[1];
  if (current_emotion === null) {
    document.cookie = `current_emotion=Neutral;`;
  }

  $("#textInput").val("");
  $("#chatbox").append(userHtml);

  // setting timeout so it feels more natural when bot responds (not instant)
  setTimeout(() => {
    $("#chatbox").append(typingAnim);
    document
      .getElementById("userInput")
      .scrollIntoView({ block: "end", behavior: "smooth" });
    $.get("/parse_text", {
      msg: rawText,
      current_emotion: current_emotion,
    }).done(function (data) {
      console.log(`tone: ${data.tone}`)
      console.log(`emotion: ${data.emotion}`)

      var botHtml = '<p class="botText"><span>' + data.response + "</span></p>";

      $("#chatbox").children().last().html(botHtml); // change typing animation to response
      document
        .getElementById("userInput")
        .scrollIntoView({ block: "end", behavior: "smooth" });
    });
  }, 400);
}

function stop_webcam(_) {
  var stream = video.srcObject;
  var tracks = stream.getTracks();

  for (var i = 0; i < tracks.length; i++) {
    var track = tracks[i];
    track.stop();
  }
  video.srcObject = null;
}

function take_snapshot() {
  var canvas = document.createElement("canvas");
  var context = canvas.getContext("2d");

  canvas.width = 720;
  canvas.height = 480;
  context.drawImage(video, 0, 0);

  // Get base64 data to send to server for upload
  var imagebase64data = canvas.toDataURL("image/jpeg", 1.0);

  $.ajax({
    type: "POST",
    data: imagebase64data,
    url: "/parse_image",
    contentType: false,
    processData: false,
    success: function (emotion) {
      document.cookie = `current_emotion=${emotion};`;
    },
  });
}
