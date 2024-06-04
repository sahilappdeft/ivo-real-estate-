
$(document).ready(function () {

    // chips
    $('#chip-input').on('keypress', function (e) {
        if (e.which == 13) { // Enter key pressed
            e.preventDefault();
            var text = $(this).val().trim();
            if (text) {
                var chip = $('<span class="chip"></span>').text(text);
                var closeBtn = $('<span class="close-btn">&times;</span>');
                chip.append(closeBtn);
                $('#chip-show-box').append(chip);
                $(this).val('');

                // Trigger the select role modal here
                $('#selectrolemodal').modal('show');
            }
        }
    });

    $(document).on('click', '.chip .close-btn', function () {
        $(this).parent().remove();
    });

    var counter = 0; // Initialize a counter for unique IDs

    $('#add-financial-fields').on('click', function () {
        var html = `<tr>
                        <td><input type="text" id="purpose-${counter}" class="form-control" name="purpose"
                         oninput="stateAccount(this.id, this.value, this.name)"></td>
                        <td><input type="text" id="owner_name-${counter}" class="form-control" name="owner_name"
                        oninput="stateAccount(this.id, this.value, this.name)"></td>
                        <td><input type="text" id="iban-${counter}" class="form-control" name="iban" 
                        oninput="stateAccount(this.id, this.value, this.name)"></td>
                        <td><input type="text" id="bic-${counter}" class="form-control" name="bic" 
                        oninput="stateAccount(this.id, this.value, this.name)"></td>
                        <td>
                            <div class="d-flex gap-3">
                                <i class='bx bxs-check-circle save-btn fs-4 text-gray-color'> </i><i class='bx bxs-plus-circle rotate-90 fs-4 text-gray-color' ></i>
                            </div>
                        </td>
                    </tr>`;

        $('#financial-table-form').append(html)
        counter += 1
    });

    // Show the first step
    $('.form-step').first().addClass('active');

    // Handle the Next button click
    $('.next-btn').on('click', function () {
        var nextStep = $(this).data('next');
        var currentStep = $(this).closest('.form-step');
        var nextStepElement = $('#' + nextStep);

        currentStep.removeClass('active').hide();
        nextStepElement.addClass('active').show();

        $('.step-indicator').removeClass('active');
        $('#' + nextStep + '-indicator').addClass('active');
    });

    // Handle the Previous button click
    $('.prev-btn').on('click', function () {
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

