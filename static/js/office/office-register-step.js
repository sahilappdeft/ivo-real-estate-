
$(document).ready(function () {
    console.log("aya yaa aya ya ")

    // call company role api 
    companyRole()
    var counter_email = 0
    // chips
    $('#chip-input').on('keypress', function (e) {
        if (e.which == 13) { // Enter key pressed
            e.preventDefault();
            var text = $(this).val().trim();
            if (text) {
                validEmail = formValidation('email', text, 'chip-container')
                if (validEmail){
                    var chip = $('<span class="chip"></span>').text(text);
                    var closeBtn = $(`<span class="close-btn" id="cancelInvite-${counter_email}">&times;</span>`);
                    chip.append(closeBtn);
                    $('#chip-show-box').append(chip);
                    $(this).val('');
                    
                    //add email to state
                    invite_employees[counter_email.toString()]=employee
                    emailValid = StateinviteEmployee(counter_email, "recipient_email", text)
                    counter_email += 1
                
                    // Trigger the select role modal here
                    $('#selectrolemodal').modal('show');
                    $('#selectrolemodal').on('show.bs.modal', function (e) {
                        // Remove active-role class from all profile-role divs
                        $('.profile-role').removeClass('active-role');
                        // Add active-role class to the admin profile-role
                        $('.profile-role[name="admin"]').addClass('active-role');
                    });
                
                }
            }
        }
    });

    $(document).on('click', '.chip .close-btn', function () {
        var id = $(this).attr('id');
        $(this).parent().remove();
        cancelInviteEmployee(id)
    });

    var counter = 0; // Initialize a counter for unique IDs

    $('#add-financial-fields').on('click', function () {
        var html = `<tr>
                        <td><input type="text" id="purpose-${counter}" class="form-control" name="purpose"
                         oninput="stateAccount(this.id, this.value, this.name)">
                         <span class='error-message text-danger'></span></td>
                        <td><input type="text" id="owner_name-${counter}" class="form-control" name="owner_name"
                        oninput="stateAccount(this.id, this.value, this.name)">
                        <span class='error-message text-danger'></span></td>
                        <td><input type="text" id="iban-${counter}" class="form-control" name="iban" 
                        oninput="stateAccount(this.id, this.value, this.name)">
                        <span class='error-message text-danger'></span></td>
                        <td><input type="text" id="bic-${counter}" class="form-control" name="bic" 
                        oninput="stateAccount(this.id, this.value, this.name)">
                        <span class='error-message text-danger'></span></td>
                        <td>
                            <div class="d-flex gap-3">
                                <i class='bx bxs-check-circle save-btn fs-4 text-gray-color' id='submitBank-${counter}'>
                                 </i><i class='bx bxs-plus-circle rotate-90 fs-4 text-gray-color' id='cancelBank-${counter}
                                 oncclick='removeBankAccount(this.id)' ></i>
                            </div>
                        </td>
                    </tr>`;

        $('#financial-table-form').append(html)

        // add tr to state
        addAccounts(counter)
        counter += 1
    });

    // Show the first step
    $('.form-step').first().addClass('active');

    var formStep = 1;
    // Handle the Next button click
    $('.next-btn').on('click', function () {

        // get all inouts fields under step1 of form
        var stepId = "step-" + formStep;
        var inputs = $("#" + stepId).find('.form-control'); 
        var isValid = true
        inputs.each(function() {
            var id = $(this).attr('id'); 
            var name =  $(this).attr('name'); 
            var value = $(this).val().trim(); 
            // check validation
            isValid = formValidation(name, value, id)
            console.log(isValid, "under iteration input")
    
        });
        console.log(isValid, "isValid isValid")
        if (isValid){
            var nextStep = $(this).data('next');
            var currentStep = $(this).closest('.form-step');
            var nextStepElement = $('#' + nextStep);

            currentStep.removeClass('active').hide();
            nextStepElement.addClass('active').show();

            $('.step-indicator').removeClass('active');
            $('#' + nextStep + '-indicator').addClass('active');
            // increase form step by 1
            formStep += 1;
        }
    });

    // Handle the Previous button click
    $('.prev-btn').on('click', function () {

        // subtract 1 step from the form step if its click back
        formStep -= 1;
        var prevStep = $(this).data('prev');
        var currentStep = $(this).closest('.form-step');
        var prevStepElement = $('#' + prevStep);

        currentStep.removeClass('active').hide();
        prevStepElement.addClass('active').show();

        $('.step-indicator').removeClass('active');
        $('#' + prevStep + '-indicator').addClass('active');
    });


    $(document).on('click', '.save-btn', function () {
        var row = $(this).closest('tr');
        var purpose = row.find('input[type="text"]').val();
        var ownername = row.find('input[type="text"]').val();
        var iban = row.find('input[type="text"]').val();
        var bic = row.find('input[type="text"]').val();


        var originalRow = '<tr>' +
            '<td>' + purpose + '</td>' +
            '<td>' + ownername + '</td>' +
            '<td>' + iban + '</td>' +
            '<td>' + bic + '</td>' +
            '<td><button class="btn btn-primary edit-btn">Edit</button> </td>' +
            '</tr>';

        row.replaceWith(originalRow);
    });

    // select role
    $(".profile-role").click(function () {
        // Remove active class from all roles
        $(".profile-role").removeClass("active-role");

        // Add active class to the clicked role
        $(this).addClass("active-role");
    });
});

