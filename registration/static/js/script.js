$(document).ready(function () {
    // Sticky navbar on scroll
    $(window).scroll(function () {
        if (this.scrollY > 20) {
            $('.navbar').addClass("sticky");
        } else {
            $('.navbar').removeClass("sticky");
        }

        // Show/hide scroll-up button
        if (this.scrollY > 500) {
            $('.scroll-up-btn').addClass("show");
        } else {
            $('.scroll-up-btn').removeClass("show");
        }
    });

    // Slide-up script
    $('.scroll-up-btn').click(function () {
        $('html').animate({ scrollTop: 0 });
        $('html').css("scrollBehavior", "auto");
    });

    // Toggle menu/navbar script
    $('.menu-btn').click(function () {
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });

    // Smooth scroll on menu items click and close the menu
    $('.navbar .menu li a').click(function (e) {
        e.preventDefault(); // Prevent default link behavior

        // Smooth scroll to the section
        let targetSection = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(targetSection).offset().top
        }, 800); // Adjust 800 for scroll speed

        // Close the menu and deactivate the hamburger icon
        $('.navbar .menu').removeClass('active');
        $('.menu-btn i').removeClass('active');
    });

    // Modal functionality
    const modal = document.getElementById('registrationModal');
    const mosqueBtn = document.getElementById('mosqueBtn');
    const closeModal = document.getElementsByClassName('close')[0];

    mosqueBtn.onclick = function () {
        modal.style.display = 'block';
    }

    closeModal.onclick = function () {
        modal.style.display = 'none';
    }

    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }

    // Prevent form submission for demo purposes
    const form = document.getElementById('registrationForm');
    form.onsubmit = function (event) {
        event.preventDefault();
        alert('Mosque registered successfully!');
        modal.style.display = 'none';
    }

});
// Open the modal when the apply button is clicked
document.querySelectorAll('.apply-btn').forEach(button => {
    button.addEventListener('click', function () {
        const modalId = this.getAttribute('data-modal');
        document.getElementById(modalId).style.display = 'block';
    });
});

// Close the modal when the close button is clicked
document.querySelectorAll('.modal .close').forEach(closeBtn => {
    closeBtn.addEventListener('click', function () {
        this.closest('.modal').style.display = 'none';
    });
});

// Close the modal when clicking outside of the modal content
// window.addEventListener('click', function (event) {
//     if (event.target.classList.contains('modal')) {
//         event.target.style.display = 'none';
//     }
// });
// Show the registration form when 'Register here' is clicked
document.getElementById('showQarjRegister').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('qarjLoginForm').style.display = 'none';
    document.getElementById('qarj-registration-form').style.display = 'block';
});

// Handle registration form submission
document.getElementById('qarjRegisterForm').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Registered successfully! Redirecting to login...');
    // After registration, redirect to login form
    document.getElementById('qarj-registration-form').style.display = 'none';
    document.getElementById('qarjLoginForm').style.display = 'block';
});

// Handle login form submission
document.getElementById('qarjLoginForm').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Logged in successfully! Redirecting to apply form...');
    // After login, show the apply form
    document.getElementById('qarjLoginForm').style.display = 'none';
    document.getElementById('qarj-application-form').style.display = 'block';
});
// Show Forgot Password Form
document.getElementById('forgotPasswordLink').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('qarjLoginForm').style.display = 'none';
    document.getElementById('forgot-password-form').style.display = 'block';
});

// Handle Forgot Password Form Submission
document.getElementById('forgotPasswordForm').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Password reset instructions sent. Please check your email.');
    document.getElementById('forgot-password-form').style.display = 'none';
    document.getElementById('qarjLoginForm').style.display = 'block';
});

// Back to Login from Forgot Password Form
document.getElementById('backToLogin').addEventListener('click', function (e) {
    e.preventDefault();
    document.getElementById('forgot-password-form').style.display = 'none';
    document.getElementById('qarjLoginForm').style.display = 'block';
});

// Handle apply form submission
document.getElementById('qarjApplyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    alert('Application submitted successfully!');
    // You can add additional actions here after applying
});
$(document).ready(function(){
    function slideNotice() {
        $('.notice-slider ul').animate({left: '-100%'}, 10000, 'linear', function(){
            $(this).css('left', '100%');
        });
    }

    setInterval(slideNotice, 0); // Continue sliding infinitely
    
    // Pause on hover
    $('.notice-slider').hover(function(){
        $('.notice-slider ul').css('animation-play-state', 'paused');
    }, function(){
        $('.notice-slider ul').css('animation-play-state', 'running');
    });
});
// Zakat Modal
const zakatBox = document.getElementById('zakatBox');
const zakatModal = document.getElementById('zakatModal');
const zakatProviderBtn = document.getElementById('zakatProviderBtn');
const zakatReceiverBtn = document.getElementById('zakatReceiverBtn');
const closeZakatModal = document.getElementById('closeZakatModal');
const zakatProviderModal = document.getElementById('zakatProviderModal');
const closeZakatProviderModal = document.getElementById('closeZakatProviderModal');
const zakatReceiverModal = document.getElementById('zakatReceiverModal');
const closeZakatReceiverModal = document.getElementById('closeZakatReceiverModal');

// Show main zakat modal
zakatBox.onclick = function() {
    zakatModal.style.display = 'block';
};

// Close main zakat modal
closeZakatModal.onclick = function() {
    zakatModal.style.display = 'none';
};

// Zakat provider modal
zakatProviderBtn.onclick = function() {
    zakatModal.style.display = 'none';
    zakatProviderModal.style.display = 'block';
};

// Zakat receiver modal
zakatReceiverBtn.onclick = function() {
    zakatModal.style.display = 'none';
    zakatReceiverModal.style.display = 'block';
};

// Close zakat provider modal
closeZakatProviderModal.onclick = function() {
    zakatProviderModal.style.display = 'none';
};

// Close zakat receiver modal
closeZakatReceiverModal.onclick = function() {
    zakatReceiverModal.style.display = 'none';
};

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target === zakatModal) {
        zakatModal.style.display = 'none';
    } else if (event.target === zakatProviderModal) {
        zakatProviderModal.style.display = 'none';
    } else if (event.target === zakatReceiverModal) {
        zakatReceiverModal.style.display = 'none';
    }
};
// Function to calculate and update income-expense difference for all forms with the same class
function calculateIncomeExpenseDifference() {
    const incomeFields = document.querySelectorAll('.monthly-income');
    const expenseFields = document.querySelectorAll('.monthly-expense');
    const differenceFields = document.querySelectorAll('.income-expense-diff');

    incomeFields.forEach((incomeField, index) => {
        const expenseField = expenseFields[index];
        const differenceField = differenceFields[index];

        function updateDifference() {
            const incomeValue = parseFloat(incomeField.value) || 0;
            const expenseValue = parseFloat(expenseField.value) || 0;
            differenceField.value = incomeValue - expenseValue;
        }

        incomeField.addEventListener('input', updateDifference);
        expenseField.addEventListener('input', updateDifference);
    });
}

// Initialize the calculation for both forms
calculateIncomeExpenseDifference();
