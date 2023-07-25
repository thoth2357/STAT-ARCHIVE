$(document).ready(function () {
    // Retrieve the CSRF token
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    // Hide all upload forms initially except the active one
    $(".upload-form").not(".active").hide();

    // Handle click event on upload type buttons
    $(".upload-type-btn").click(function () {
        // Remove active class from all buttons
        $(".upload-type-btn").removeClass("active");
        // Add active class to the clicked button
        $(this).addClass("active");

        // Hide all upload forms
        $(".upload-form").hide();

        // Show the corresponding form based on data-target attribute
        var targetForm = $(this).attr("data-target");
        $("#" + targetForm).show();
    });

    // Handle click event on upload buttons
    $(".upload-btn").click(function () {
        // console.log("Upload button clicked!");
        // Get the form id of the active upload form
        var formId = $(".upload-type-btn.active").attr("data-target");
        // console.log(formId);
        var formData = new FormData();

        // Check if any required field is empty
        var isValid = validateFormFields(formId);
        if (!isValid) {
            //close modal
            var modal_close = document.getElementById("close-btn"); // Hide the upload modal
            modal_close.click();
            
            // Display an error message to the user
            Swal.fire({
                icon: "error",
                title: "Required Information",
                text: "Please fill in all the required fields.",
            });
            return; // Stop further execution
        }

        // Get the query parameter based on the form id
        var queryParam = "";
        if (formId === "pastQuestionsForm") {
            queryParam = "pq";
            formData = formPastQuestionsData();
        } else if (formId === "textbookForm") {
            queryParam = "txb";
            formData = formTextbookData();
        } else if (formId === "projectForm") {
            queryParam = "prj";
            formData = formProjectData();
        }

        // Display the progress bar
        var progressBar = $(".upload-progress .progress-bar");
        progressBar.css("width", "0%");
        progressBar.text("0%");
        progressBar.addClass("progress-bar-striped active");
        $(".upload-progress").show(); // Show the progress bar container

        // Send the form data to the server
        $.ajax({
            url: "/Stat-Archive/upload/?query=" + queryParam,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            beforeSend: function (xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function (event) {
                    if (event.lengthComputable) {
                        var progress = Math.round((event.loaded / event.total) * 100);
                        progressBar.css("width", progress + "%");
                        progressBar.text(progress + "%");
                        // console.log(progress + "in percent %");
                    }
                });
                return xhr;
            },
            success: function (response) {
                //close modal
                var modal_close = document.getElementById("close-btn"); // Hide the upload modal
                modal_close.click();

                // Display the success message
                Swal.fire({
                    icon: "success",
                    title: "Upload Successful!",
                    text: "Thanks Your file has been uploaded successfully!",
                });

                confetti({
                    particleCount: 500,
                    spread: 100,
                    origin: { y: 0.6 },
                });
            },
            error: function (xhr, status, error) {
                //close modal
                var modal_close = document.getElementById("close-btn"); // Hide the upload modal
                modal_close.click();
                // console.log(xhr.responseText, status, error);
                // Display the success message
                const errorMessage = `Your file hasnt been uploaded \n\n  ${xhr.responseText}, \n Try again!. If problem persist contact admin@sta-archive.com`;  
                Swal.fire({
                    icon: "error",
                    title: "Upload Not Successful!",
                    text: errorMessage,
                });
            },
        });
    });

    // Function to form the data for the past questions form
    function formPastQuestionsData() {
        var session = $("#sessionDropdown").val();
        var pastQuestionsType = $("#sessionDropdowntype").val();
        var pastQuestionsLecturerName = $("#pastQuestionsLecturerName").val();
        var pastQuestionsCourseName = $("#pastQuestionsCourseName").val();
        var pastQuestionsCourseCode = $("#pastQuestionsCourseCode").val();
        var pastQuestionFile = $("#pastQuestionsFileInput").prop("files")[0];

        var formData = new FormData();
        formData.append("session", session);
        formData.append("PastQuestionsType", pastQuestionsType);
        formData.append("LecturerName", pastQuestionsLecturerName);
        formData.append("CourseName", pastQuestionsCourseName);
        formData.append("CourseCode", pastQuestionsCourseCode);
        formData.append("QuestionFile", pastQuestionFile);
        return formData;
    }

    // Function to form the data for the textbook form
    function formTextbookData() {
        var textbookName = $("#textbookName").val();
        var textbookAuthor = $("#textbookAuthor").val();
        var textbookFile = $("#textbookFileInput").prop("files")[0];

        var formData = new FormData();
        formData.append("textbookName", textbookName);
        formData.append("textbookAuthor", textbookAuthor);
        formData.append("textbookFile", textbookFile);

        return formData;
    }

    // Function to form the data for the project form
    function formProjectData() {
        var session = $("#sessionDropdown2").val();
        var projectTopic = $("#projectTopic").val();
        var projectAuthor = $("#projectAuthor").val();
        var projectSupervisor = $("#projectSupervisor").val();
        var projectFile = $("#projectFileInput").prop("files")[0];

        var formData = new FormData();
        formData.append("session", session);
        formData.append("projectTopic", projectTopic);
        formData.append("projectAuthor", projectAuthor);
        formData.append("projectSupervisor", projectSupervisor);
        formData.append("projectFile", projectFile);
        return formData;
    }

    // Function to validate the form fields based on formId
    function validateFormFields(formId) {
        if (formId === "pastQuestionsForm") {
            var session = $("#sessionDropdown").val();
            var pastQuestionsType = $("#sessionDropdowntype").val();
            var pastQuestionsLecturerName = $("#pastQuestionsLecturerName").val();
            var pastQuestionsCourseName = $("#pastQuestionsCourseName").val();
            var pastQuestionsCourseCode = $("#pastQuestionsCourseCode").val();
            var pastQuestionFile = $("#pastQuestionsFileInput").prop("files")[0];

            // Check if any required field is empty
            if (!session || !pastQuestionsType || !pastQuestionsLecturerName || !pastQuestionsCourseName || !pastQuestionsCourseCode || !pastQuestionFile) {
                return false;
            }
        } else if (formId === "textbookForm") {
            var textbookName = $("#textbookName").val();
            var textbookAuthor = $("#textbookAuthor").val();
            var textbookFile = $("#textbookFileInput").prop("files")[0];

            // Check if any required field is empty
            if (!textbookName || !textbookAuthor || !textbookFile) {
                return false;
            }
        } else if (formId === "projectForm") {
            var session = $("#sessionDropdown2").val();
            var projectTopic = $("#projectTopic").val();
            var projectAuthor = $("#projectAuthor").val();
            var projectSupervisor = $("#projectSupervisor").val();
            var projectFile = $("#projectFileInput").prop("files")[0];
            // console.log(projectFile, projectSupervisor, projectAuthor, projectTopic, session, "prj");
            // Check if any required field is empty
            if (!session || !projectTopic || !projectAuthor || !projectSupervisor || !projectFile) {
                return false;
            }
        }

        return true; // All required fields are filled
    }
});
